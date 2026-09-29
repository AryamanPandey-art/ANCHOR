
from student_kit.verification import ActionVerifier


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