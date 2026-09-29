
from student_kit.verification import ActionVerifier
from student_kit.schema import ContextDeeplinkResponse


def test_missing_evidence_is_rejected():
    verifier = ActionVerifier()

    result = verifier.verify({
        "action_name": "Enable Mouse Keys",
        "description": "Enable mouse keys",
        "evidence_text": "",
    })

    assert result.verified is False
    assert "evidence" in result.reason.lower()


def test_unknown_action_is_rejected():
    verifier = ActionVerifier()

    result = verifier.verify({
        "action_name": "Enable imaginary feature",
        "description": "Enable imaginary feature",
        "evidence_text": "Enable imaginary feature",
    })

    assert result.verified is False


def test_verify_intelligence_returns_schema_response():
    verifier = ActionVerifier()

    result = verifier.verify_intelligence({
        "query_intent": {
            "intent_summary": "Switch Time Format",
            "direction": "null",
        },
        "parsed_siis": {
            "title": "Time Format",
            "raw_content": "Switch Time Format",
        },
        "candidate_actions": [],
    })

    assert isinstance(result, ContextDeeplinkResponse)
    assert result.contexts == []


def test_unmatched_candidate_is_excluded():
    verifier = ActionVerifier()

    result = verifier.verify_intelligence({
        "query_intent": {
            "intent_summary": "Enable imaginary feature",
            "direction": "null",
        },
        "parsed_siis": {
            "title": "Test",
            "raw_content": "Enable imaginary feature",
        },
        "candidate_actions": [{
            "action_name": "Enable imaginary feature",
            "description": "Enable imaginary feature",
            "steps": ["Enable imaginary feature"],
            "evidence_text": "Enable imaginary feature",
            "category_hint": "manual",
            "confidence": 1.0,
        }],
    })

    assert result.contexts == []


def test_verified_action_is_converted_to_schema():
    verifier = ActionVerifier()

    # Use the catalog's actual wording to test a real match.
    entry = next(
        item for item in verifier.deeplinks
        if item.get("id") == "DL-0001"
    )

    evidence = (
        "Switches between 12-hour and 24-hour time format "
        "to display time in your preferred style."
    )

    result = verifier.verify_intelligence({
        "query_intent": {
            "intent_summary": "Switch Time Format",
            "direction": "null",
        },
        "parsed_siis": {
            "title": "Time Format",
            "raw_content": evidence,
        },
        "candidate_actions": [{
            "action_name": "Switch Time Format",
            "description": entry["message"],
            "steps": ["Open Time Format settings"],
            "evidence_text": evidence,
            "category_hint": "manual",
            "confidence": 0.9,
        }],
    })

    assert len(result.contexts) == 1
    goal = result.contexts[0]
    assert len(goal.actions) == 1

    action = goal.actions[0]
    assert action.actionName == "Switch Time Format"
    assert len(action.stepGroups) == 1

    step_group = action.stepGroups[0]
    assert step_group.actionableDeeplink.deeplink == entry["deeplink"]
    assert step_group.validationDeeplink.deeplink == entry["validation"]["deeplink"]
    assert step_group.validationDeeplink.key == entry["validation"]["key"]