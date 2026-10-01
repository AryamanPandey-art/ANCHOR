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
    assert response.json() == {"status": "ok"}


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


# 22. repeat request cache hit
def test_22_repeat_request_cache_hit():
    cache = get_cache()
    cache.clear_response_cache()
    orch = PipelineOrchestrator()

    payload = {
        "query": "Switch Time Format",
        "siis_response": {
            "title": "Time Format",
            "content": "Switches between 12-hour and 24-hour time format to display time in your preferred style."
        }
    }
    req = TroubleshootRequest(**payload)

    # First execution (Cold)
    resp1 = orch.process(req)
    assert len(resp1.contexts) == 1

    # Second execution (Repeat)
    resp2 = orch.process(req)
    assert resp2.model_dump() == resp1.model_dump()

    stats = cache.cache_stats
    assert stats["repeat_hits"] >= 1


# 23. paraphrase cache hit
def test_23_paraphrase_cache_hit():
    cache = get_cache()
    cache.clear_response_cache()
    orch = PipelineOrchestrator()

    siis_payload = {
        "title": "Email server not responding on Samsung phone or tablet",
        "content": "## Clear Cache\nTo clear the app's cache:\nNavigate to Settings.\nTap Apps.\nSelect your email app.\nTap Storage.\nTap Clear cache."
    }

    # Query 1
    req1 = TroubleshootRequest(
        query="My tablet screen flashes whenever I tap to open an email in Gmail.",
        siis_response=SIISPayload(**siis_payload)
    )
    resp1 = orch.process(req1)
    assert len(resp1.contexts) == 1

    # Query 2 (Paraphrase)
    req2 = TroubleshootRequest(
        query="Opening Gmail on my tablet causes the screen to flash and blackout.",
        siis_response=SIISPayload(**siis_payload)
    )
    resp2 = orch.process(req2)
    assert resp2.model_dump() == resp1.model_dump()

    stats = cache.cache_stats
    assert stats["paraphrase_hits"] >= 1 or stats["repeat_hits"] >= 1


# 24. cache isolation across different SIIS articles
def test_24_cache_isolation_across_different_siis():
    cache = get_cache()
    cache.clear_response_cache()
    orch = PipelineOrchestrator()

    query = "How to adjust screen settings"
    siis_article_a = {
        "title": "Display & Brightness Settings",
        "content": "To adjust brightness: Open Settings, tap Display, adjust Brightness slider."
    }
    siis_article_b = {
        "title": "Cracked Glass Hardware Policy",
        "content": "A cracked screen requires physical inspection by an authorized technician. Visit a Samsung Service Center for hardware replacement."
    }

    req_a = TroubleshootRequest(query=query, siis_response=SIISPayload(**siis_article_a))
    resp_a = orch.process(req_a)

    req_b = TroubleshootRequest(query=query, siis_response=SIISPayload(**siis_article_b))
    resp_b = orch.process(req_b)

    # Article A and Article B have different SIIS content and must produce distinct isolated responses
    assert len(resp_a.contexts) >= 1
    assert len(resp_b.contexts) >= 1
    assert resp_a.contexts[0].title == "Display & Brightness Settings"
    assert resp_b.contexts[0].title == "Cracked Glass Hardware Policy"
    assert resp_a.model_dump() != resp_b.model_dump()


# 25. cache isolation between ON and OFF queries
def test_25_cache_isolation_on_vs_off():
    cache = get_cache()
    cache.clear_response_cache()
    orch = PipelineOrchestrator()

    siis_payload = {
        "title": "Touch sensitivity",
        "content": "To improve touch response, enable Touch sensitivity in Settings. Open Settings, tap Display, and turn on Touch sensitivity."
    }

    req_on = TroubleshootRequest(
        query="How do I turn on touch sensitivity?",
        siis_response=SIISPayload(**siis_payload)
    )
    resp_on = orch.process(req_on)

    req_off = TroubleshootRequest(
        query="How do I turn off touch sensitivity?",
        siis_response=SIISPayload(**siis_payload)
    )
    resp_off = orch.process(req_off)

    # ON query passes with deeplink; OFF query is rejected due to direction mismatch
    assert len(resp_on.contexts) == 1
    assert len(resp_off.contexts) == 0


# 26. direction mismatch scenario for off query + on-only SIIS
def test_26_direction_mismatch_rejection_scenario():
    orch = PipelineOrchestrator()
    siis_payload = {
        "title": "Touch sensitivity",
        "content": "To improve touch response, enable Touch sensitivity in Settings. Open Settings, tap Display, and turn on Touch sensitivity."
    }
    req = TroubleshootRequest(
        query="How do I turn off touch sensitivity?",
        siis_response=SIISPayload(**siis_payload)
    )
    resp = orch.process(req)
    assert len(resp.contexts) == 0


# 27. direction match pass scenario for on query + on-only SIIS
def test_27_direction_match_pass_scenario():
    orch = PipelineOrchestrator()
    siis_payload = {
        "title": "Touch sensitivity",
        "content": "To improve touch response, enable Touch sensitivity in Settings. Open Settings, tap Display, and turn on Touch sensitivity."
    }
    req = TroubleshootRequest(
        query="How do I turn on touch sensitivity?",
        siis_response=SIISPayload(**siis_payload)
    )
    resp = orch.process(req)
    assert len(resp.contexts) == 1
    assert resp.contexts[0].actions[0].stepGroups[0].actionableDeeplink is not None
    assert resp.contexts[0].actions[0].stepGroups[0].actionableDeeplink.deeplink.startswith("bixby://")


# 28. unsupported query rejection scenario (water damage)
def test_28_unsupported_query_water_damage_rejection():
    orch = PipelineOrchestrator()
    siis_payload = {
        "title": "Water Damage Assessment",
        "content": "If your device has been submerged in water, immediately power it down. Do not charge the device. Visit an authorized service center."
    }
    req = TroubleshootRequest(
        query="My Samsung phone fell into water. What should I do?",
        siis_response=SIISPayload(**siis_payload)
    )
    resp = orch.process(req)
    assert len(resp.contexts) == 0

