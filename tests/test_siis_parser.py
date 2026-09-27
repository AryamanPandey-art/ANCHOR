"""Unit tests for deterministic SIIS Markdown parser."""

import json
import pytest
from anchor_ai.siis_parser import SIISParser


@pytest.fixture
def parser():
    return SIISParser()


def test_parse_empty_siis(parser):
    result = parser.parse({"title": "", "content": ""})
    assert result.title == ""
    assert len(result.sections) == 0


def test_parse_hierarchical_markdown(parser):
    siis_doc = {
        "title": "Blank or black display on a Samsung phone or tablet",
        "content": (
            "Smartphone,Others Mobile,Tablet Blank or black display: "
            "## Troubleshooting Steps for Device Not Turning On\n"
            "### Step 1: Check for Physical Damage\n"
            "Inspect phone carefully. Check the Liquid Damage Indicator (LDI).\n"
            "### Step 2: Force a Restart\n"
            "Press and hold Power button and Volume down for 20 seconds.\n"
            "### Step 3: Charge the Device\n"
            "Connect phone to charger for 1 hour."
        )
    }
    parsed = parser.parse(siis_doc)
    assert parsed.title == "Blank or black display on a Samsung phone or tablet"
    assert len(parsed.sections) >= 3
    
    # Check section titles and step order
    titles = [s.title for s in parsed.sections]
    assert any("Step 1" in t for t in titles)
    assert any("Step 2" in t for t in titles)
    assert any("Step 3" in t for t in titles)

    # Check diagnostic detection on Step 1
    step1_sec = next(s for s in parsed.sections if "Step 1" in s.title)
    assert step1_sec.is_diagnostic is True


def test_extract_exact_steps(parser):
    content = (
        "## Clear Cache\n"
        "To clear cache:\n"
        "Navigate to Settings.\n"
        "Tap Apps.\n"
        "Select your email app.\n"
        "Tap Storage.\n"
        "Tap Clear cache."
    )
    parsed = parser.parse({"title": "Test", "content": content})
    assert len(parsed.sections) == 1
    sec = parsed.sections[0]
    assert len(sec.steps) >= 4
    assert any("Navigate to Settings" in s for s in sec.steps)
    assert any("Tap Clear cache" in s for s in sec.steps)
