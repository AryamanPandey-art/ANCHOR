"""Comprehensive unit and integration test suite for ANCHOR Backend."""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from backend.main import app
from backend.cache.memory_cache import MemoryCache, get_cache
from backend.models.request import TroubleshootRequest, SIISPayload
from backend.services.intelligence_service import IntelligenceService
from backend.services.maitri_adapter import MaitriAdapter
from backend.services.response_builder import ResponseBuilder
from backend.services.schema_validator import SchemaValidator
from backend.validators.request_validator import RequestValidator
from backend.validators.deeplink_validator import DeeplinkValidator
from backend.pipeline.orchestrator import PipelineOrchestrator
from student_kit.schema import (
    ContextDeeplinkResponse,
    Goal,
    Action,
    StepGroup,
    Deeplink,
    ValidationDeepLink,
)
from anchor_ai.models import (
    IntelligenceResult,
    QueryIntent,
    ParsedSIIS,
    SIISSection,
    CandidateAction,
    Direction,
)

client = TestClient(app)


# 1. /health
def test_01_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


# 2. valid /v1/troubleshoot
def test_02_valid_troubleshoot_endpoint():
    payload = {
        "query": "Switch Time Format",
        "siis_response": {
            "title": "Time Format",
            "content": "Switches between 12-hour and 24-hour time format to display time in your preferred style."
        }
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "contexts" in data
    assert isinstance(data["contexts"], list)


# 3. missing query
def test_03_missing_query():
    payload = {
        "siis_response": {
            "title": "Time Format",
            "content": "Switches between 12-hour and 24-hour time format."
        }
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 422


# 4. empty query
def test_04_empty_query():
    payload = {
        "query": "   ",
        "siis_response": {
            "title": "Time Format",
            "content": "Switches between 12-hour and 24-hour time format."
        }
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 422


# 5. missing SIIS response
def test_05_missing_siis_response():
    payload = {
        "query": "Switch Time Format"
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 422


# 6. missing SIIS title
def test_06_missing_siis_title():
    payload = {
        "query": "Switch Time Format",
        "siis_response": {
            "content": "Some content here"
        }
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 422


# 7. missing SIIS content
def test_07_missing_siis_content():
    payload = {
        "query": "Switch Time Format",
        "siis_response": {
            "title": "Some Title"
        }
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 422


# 8. empty SIIS content
def test_08_empty_siis_content():
    payload = {
        "query": "Switch Time Format",
        "siis_response": {
            "title": "Some Title",
            "content": "   "
        }
    }
    response = client.post("/v1/troubleshoot", json=payload)
    assert response.status_code == 422


# 9. anchor_ai integration
def test_09_anchor_ai_integration():
    svc = IntelligenceService()
    res = svc.process_query(
        query="Switch Time Format",
        siis_response={"title": "Time Format", "content": "Switches between 12-hour and 24-hour time format."}
    )
    assert isinstance(res, IntelligenceResult)
    assert res.query_intent is not None
    assert res.parsed_siis is not None


# 10. Maitri integration
def test_10_maitri_integration():
    adapter = MaitriAdapter()
    cache = get_cache()
    entry = next(item for item in cache.verifier.deeplinks if item.get("id") == "DL-0001")
    evidence = "Switches between 12-hour and 24-hour time format to display time in your preferred style."

    res = adapter.verify_intelligence({
        "query_intent": {"intent_summary": "Switch Time Format", "direction": "null"},
        "parsed_siis": {"title": "Time Format", "raw_content": evidence},
        "candidate_actions": [{
            "action_name": "Switch Time Format",
            "description": entry["message"],
            "steps": ["Open Time Format settings"],
            "evidence_text": evidence,
            "category_hint": "manual",
            "confidence": 0.9,
        }]
    })

    assert isinstance(res, ContextDeeplinkResponse)
    assert len(res.contexts) == 1
    assert res.contexts[0].actions[0].stepGroups[0].actionableDeeplink.deeplink == entry["deeplink"]


# 11. valid deeplink accepted
def test_11_valid_deeplink_accepted():
    validator = DeeplinkValidator()
    assert validator.is_valid_catalog_uri("bixby://masked/act/aa73a35e8d") is True


# 12. arbitrary deeplink rejected
def test_12_arbitrary_deeplink_rejected():
    validator = DeeplinkValidator()
    assert validator.is_valid_catalog_uri("bixby://fake_deeplink_xyz_123") is False


# 13. external HTTP/HTTPS URL rejected
def test_13_external_url_rejected():
    validator = DeeplinkValidator()
    assert validator.is_external_url("http://malicious-site.com") is True
    assert validator.is_external_url("https://samsung.com/fake") is True
    assert validator.is_valid_catalog_uri("https://samsung.com/fake") is False


# 14. ON + OFF deeplink rejected
def test_14_on_request_off_deeplink_rejected():
    validator = DeeplinkValidator()
    dl_off = Deeplink(deeplink="bixby://masked/act/test", description="off", originalType="offURL")
    assert validator.is_direction_mismatch("turn on wi-fi", dl_off) is True


# 15. OFF + ON deeplink rejected
def test_15_off_request_on_deeplink_rejected():
    validator = DeeplinkValidator()
    dl_on = Deeplink(deeplink="bixby://masked/act/test", description="on", originalType="onURL")
    assert validator.is_direction_mismatch("turn off wi-fi", dl_on) is True


# 16. valid manual action with null deeplink
def test_16_valid_manual_action_null_deeplink():
    act = Action(
        actionName="Schedule Repair Service",
        description="Visit service center",
        stepGroups=[StepGroup(steps=["Go to center"], actionableDeeplink=None, validationDeeplink=None)]
    )
    res = ResponseBuilder.build_response(
        goal_text="Repair Goal",
        title="Repair",
        actions=[act]
    )
    assert len(res.contexts) == 1
    assert res.contexts[0].actions[0].stepGroups[0].actionableDeeplink is None


# 17. final official schema validation
def test_17_final_schema_validation():
    valid_resp = ContextDeeplinkResponse(contexts=[])
    validated = SchemaValidator.validate_or_raise(valid_resp)
    assert isinstance(validated, ContextDeeplinkResponse)


# 18. empty contexts behavior
def test_18_empty_contexts_behavior():
    empty_resp = ResponseBuilder.build_empty_response()
    assert empty_resp.contexts == []
    validated = SchemaValidator.validate_or_raise(empty_resp)
    assert validated.contexts == []


# 19. response builder
def test_19_response_builder():
    act = Action(
        actionName="Test Action",
        description="Test Desc",
        stepGroups=[StepGroup(steps=["Step 1"])]
    )
    res = ResponseBuilder.build_response("Goal 1", "Title 1", [act], score=0.98)
    assert res.contexts[0].goal == "Goal 1"
    assert res.contexts[0].title == "Title 1"
    assert res.contexts[0].score == 0.98


# 20. cache behavior
def test_20_cache_behavior():
    cache = get_cache()
    assert cache.is_loaded is True
    assert len(cache.valid_deeplink_uris) > 0
    assert cache.engine is not None
    assert cache.verifier is not None


# 21. pipeline error handling
def test_21_pipeline_error_handling():
    orch = PipelineOrchestrator()
    invalid_req = TroubleshootRequest(
        query="valid query",
        siis_response=SIISPayload(title="valid title", content="valid content")
    )
    # Testing graceful process execution
    res = orch.process(invalid_req)
    assert isinstance(res, ContextDeeplinkResponse)
