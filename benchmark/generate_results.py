"""Generate results.jsonl from official SIIS dataset through the ANCHOR pipeline."""

import json
import sys
import time
from pathlib import Path

# Ensure project root is in sys.path for standalone direct execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.cache.memory_cache import get_cache
from backend.models.request import TroubleshootRequest, SIISPayload
from backend.pipeline.orchestrator import PipelineOrchestrator



QUERY_VARIATIONS_MAP = {
    "row_1": [
        "Opening Gmail on my Samsung A115G tablet causes the screen to flash and turn completely dark after briefly working.",
        "Whenever I open an email in the Gmail app on my A115G tablet, the display flickers and shuts off.",
        "My Samsung A115G tab screen keeps going blank shortly after tapping any email inside Gmail.",
        "Gmail causes my Samsung A115G tablet display to flash intermittently and blackout while trying to view messages.",
        "My A115G tablet display turns off and goes black right after launching an email in Gmail.",
        "Every time I select an email message on my Samsung A115G, the screen blinks rapidly before going completely black.",
        "The display on my Samsung A115G tablet flashes and turns off whenever I access Gmail.",
        "My Samsung tablet A115G screen goes dark after a brief flicker upon opening emails in Gmail.",
    ],
    "row_2": [
        "Searching for stocks or using Smart Tutor on my Galaxy S22 makes the screen turn solid white or blank with no text.",
        "My Samsung Galaxy S22 display goes blank or all-white across multiple applications including Smart Tutor.",
        "Text vanishes and the display becomes blank or white when I run apps like Smart Tutor on my S22.",
        "My Galaxy S22 phone screen turns blank or totally white whenever I attempt to look up stock prices.",
        "Opening Smart Tutor or performing stock searches on my Galaxy S22 results in a blank white screen.",
        "My S22 display shows a completely blank white screen without any readable text in various apps.",
        "When launching Smart Tutor or checking stock quotes on my S22, the display goes entirely white.",
        "Multiple apps on my Galaxy S22 trigger a blank or plain white screen with missing content.",
    ],
    "row_3": [
        "The screen on my Galaxy Z Flip 7 turned completely black, blocking all touch interaction and data transfer via Smart Switch.",
        "My Z Flip 7 display is totally dark, preventing me from viewing content or transferring data to another device.",
        "I cannot use Smart Switch or see anything on my Galaxy Z Flip 7 because the display is completely black.",
        "My Galaxy Z Flip 7 has a blackout display, so I can't interact with the UI or back up my files.",
        "The main display of my Z Flip 7 went dark and unresponsive, leaving me unable to transfer device data.",
        "Because my Galaxy Z Flip 7 display remains completely black, touch inputs and Smart Switch transfers are impossible.",
        "My Z Flip 7 screen is dark and blank, making data migration and regular phone operation inaccessible.",
        "I am unable to run Smart Switch or interact with my Galaxy Z Flip 7 due to a total screen blackout.",
    ],
    "row_4": [
        "After a month of normal use, my Samsung Galaxy A15 screen suddenly went pitch black and won't turn back on.",
        "My Galaxy A16 display went blank spontaneously after a few weeks, showing no picture when powering up.",
        "The display on my Samsung A15/A16 stopped working out of nowhere and stays dark when pressing power.",
        "My Samsung Galaxy A15 screen abruptly turned black after one month and fails to show any image.",
        "Powering on my Galaxy A16 yields no display output after the screen unexpectedly went black today.",
        "My Galaxy A15/A16 display turned completely black after about four weeks of use and remains unresponsive.",
        "Without any physical damage, my Samsung A15 screen went totally black and refuses to power on display output.",
        "My Galaxy A16 screen suddenly became black and unreadable after a month, failing to turn on.",
    ],
    "row_5": [
        "Scanning the Smart Switch QR code from my Galaxy S25 causes my tablet screen to stay blank, halting data transfer.",
        "My Samsung tablet display goes completely dark during Smart Switch QR scanning from a Galaxy S25.",
        "I cannot proceed with Smart Switch transfer because my tablet screen turns blank while attempting to scan the S25 QR code.",
        "When pairing my Galaxy S25 with my tablet via Smart Switch QR code, the tablet display stays blank.",
        "The tablet screen remains dark when scanning the QR code in Smart Switch to transfer files from my Galaxy S25.",
        "Data transfer is stuck because the QR code scanning screen on my Galaxy tablet stays entirely blank.",
        "My Galaxy tablet display remains pitch black during the Smart Switch connection process with my S25.",
        "Smart Switch cannot finish data migration because my tablet display goes blank while reading the QR code.",
    ],
    "row_7": [
        "Only three application icons illuminate on my tablet's dark screen while all other apps fail to open.",
        "My Samsung tablet display remains mostly black, with just three lit app icons that don't load properly.",
        "The screen on my tablet stays dark and unexecutable except for three illuminated icons that won't launch.",
        "I can't use my tablet because the display is pitch dark aside from three lit app shortcuts.",
        "My tablet screen is frozen in a dark state where only three app icons are visible and nothing opens.",
        "Except for three glowing app icons, my tablet display stays dim and unresponsive to user commands.",
        "Three app icons stay lit on my dark tablet screen, but tapping them opens nothing and the device is stuck.",
        "My tablet's display fails to render anything beyond three lit application icons on a dark background.",
    ],
    "row_8": [
        "The display area on my new Samsung phone is shrunk down and won't expand to fill the entire screen.",
        "My new Galaxy phone screen output stays minimized in a small box rather than stretching full screen.",
        "I am unable to expand the display to full size on my new Samsung device, leaving dark margins around the screen.",
        "The picture on my new Samsung smartphone stays scaled down and will not switch to full screen mode.",
        "My new Samsung phone display appears restricted to a small window and refuses to expand across the panel.",
        "Instead of filling the whole glass panel, my new Samsung phone screen stays small and centered.",
        "I cannot get my new Galaxy device display to enlarge to full screen dimensions.",
        "The screen content on my new Samsung handset remains shrunk down with unused space surrounding it.",
    ],
    "row_9": [
        "The main internal screen of my Galaxy Flip 7 has no display or touch response, though the cover screen works fine.",
        "My Galaxy Flip 7 inner foldable display went black and unresponsive, even though the external screen functions.",
        "While the outer cover screen operates normally, the interior display on my Z Flip 7 shows no image.",
        "The inner main display of my Flip 7 failed completely, showing nothing while the outer screen still works.",
        "My Z Flip 7 inner screen is blank and non-responsive to touch, but the cover display turns on.",
        "Only the external cover screen works on my Galaxy Z Flip 7; the primary inner display is dead.",
        "My Galaxy Flip 7 inside screen shows a black display without touch feedback, despite the cover screen working.",
        "The folding internal screen on my Z Flip 7 stopped rendering images, whereas the cover display functions.",
    ],
    "row_10": [
        "Unfolding my Samsung Galaxy Z Flip 6 causes the screen to flicker and go black, blocking access to settings.",
        "Every time I open my Z Flip 6, the display flickers rapidly before turning completely blank.",
        "My Galaxy Z Flip 6 display goes dark whenever the hinge is opened, preventing phone usage.",
        "Opening the Galaxy Z Flip 6 triggers severe screen flickering followed by a blackout.",
        "I cannot view settings or use my Z Flip 6 because the screen flashes and goes blank when opened.",
        "The main screen of my Samsung Z Flip 6 blinks and shuts off upon unfolding the device.",
        "Whenever I flip open my Z Flip 6, the display flickers and turns black, making the phone unusable.",
        "Opening my Galaxy Z Flip 6 results in screen flickering and a blank display, preventing device access.",
    ],
    "row_11": [
        "Half of my Galaxy Flip 6 screen is completely black, while the other side displays normally.",
        "One side of my Z Flip 6 display went dark while the remaining half functions properly.",
        "My Samsung Galaxy Flip 6 screen has a split black section covering one half of the panel.",
        "A vertical half of my Z Flip 6 screen is pitch dark, making normal interaction impossible.",
        "Only one side of my Galaxy Flip 6 display works; the other half stays entirely black.",
        "The display on my Galaxy Z Flip 6 is partially blacked out on one side.",
        "Half of the foldable screen on my Z Flip 6 turned dark, rendering the device partially unusable.",
        "My Galaxy Flip 6 screen displays content on only one half while the opposite half is black.",
    ],
    "row_12": [
        "How do I turn off the floating shortcut circle overlay on my Galaxy S25 screen?",
        "A floating circle widget with home and back shortcuts keeps hovering on my S25 display and I want it gone.",
        "My Galaxy S25 shows an annoying floating action circle for volume and navigation that I want to disable.",
        "I need to remove the floating shortcut menu circle that stays on top of my Galaxy S25 screen.",
        "How can I disable the persistent floating circle button on my Samsung S25 display?",
        "There is a floating circle overlay providing quick settings on my S25 screen that I wish to hide.",
        "My S25 screen features a floating shortcut circle for app switching and screen off that I want removed.",
        "I want to get rid of the floating assistant circle widget hovering over my Galaxy S25 display.",
    ],
    "row_13": [
        "After carrier deactivation of my previous device, my Galaxy S22 screen remains completely blank on boot.",
        "My Samsung S22 display won't show activation prompt or screen content after switching phones with my carrier.",
        "Turning on my Galaxy S22 shows a blank dark screen with no activation messaging following carrier switch.",
        "My Galaxy S22 screen stays dark and shows nothing when powered on post-carrier deactivation.",
        "Following carrier transfer, my Galaxy S22 display stays blank without displaying any activation setup.",
        "No activation message or display output appears on my Galaxy S22 screen when powering up.",
        "My S22 display remains black and unilluminated after my mobile service was transferred.",
        "My Galaxy S22 screen shows zero content or setup messages upon startup after carrier phone swap.",
    ],
    "row_14": [
        "The front glass on my Samsung Galaxy phone is severely shattered and I cannot use the screen.",
        "My Galaxy phone screen has a total crack across the panel, rendering the phone unusable.",
        "Because my Galaxy phone display is completely cracked, touch and viewing are impossible.",
        "My Samsung phone screen is totally broken with severe cracks all over the glass.",
        "I cannot operate my Galaxy device due to a completely shattered and cracked display.",
        "The display glass on my Galaxy smartphone has total crack damage preventing normal use.",
        "My Samsung Galaxy display is fully cracked across the front glass panel.",
        "A major crack across my Galaxy phone screen prevents me from interacting with the device.",
    ],
    "row_15": [
        "Powering on my Galaxy S26 Ultra results in a blue or black screen with small text that won't boot.",
        "My S26 Ultra gets stuck on a dark screen with tiny text when holding the power button.",
        "Holding the power key on my Galaxy S26 Ultra only displays a blue/black screen with micro text.",
        "My Samsung S26 Ultra won't boot into Android and only displays a dark screen with tiny lettering.",
        "When I start my Galaxy S26 Ultra, it shows a blank blue screen with tiny lines of text.",
        "My Galaxy S26 Ultra displays a crash-like blue/black screen with tiny text instead of booting.",
        "Pressing power on my S26 Ultra yields only a dark screen showing small text without starting up.",
        "My S26 Ultra is stuck on a blue or black boot screen with tiny text despite long-pressing power.",
    ],
    "row_16": [
        "Connecting a charger to my Samsung Ultra phone causes rapid millisecond screen flashing.",
        "My Samsung Ultra display flickers rapidly for a few moments whenever I plug in the charging cable.",
        "Plugging in the charger triggers fast high-frequency flashing on my Samsung Ultra screen.",
        "My Samsung Ultra device screen flashes intensely when connected to a battery charger.",
        "Whenever charging begins, my Samsung Ultra display blinks continuously for a short duration.",
        "My Samsung Ultra display flashes rapidly upon inserting the charging cord, temporarily disrupting use.",
        "Plugging in power to my Samsung Ultra phone causes brief, rapid display flickering.",
        "My Samsung Ultra display flickers in quick bursts whenever a charger is connected.",
    ],
    "row_17": [
        "My Galaxy S24 display is completely dark with occasional scrolling glitches, blocking Smart Switch transfers.",
        "I can't view content or migrate data via Smart Switch because my S24 screen goes totally blank.",
        "My Samsung S24 screen stays dark with faint scrolling artifacts and no visible app interface.",
        "Smart Switch data transfer fails because my Galaxy S24 screen goes blank without rendering UI.",
        "The display on my Galaxy S24 turns black with sporadic scrolling, leaving me unable to see anything.",
        "My S24 display output goes dark and unreadable, preventing Smart Switch connection and data backup.",
        "I cannot see any icons or transfer data on my S24 due to a dark, blank screen with scrolling lines.",
        "My Galaxy S24 screen goes black during operation, hindering both visibility and Smart Switch usage.",
    ],
    "row_19": [
        "The folding crease on my Galaxy Z Flip 7 is cracked, causing unresponsive touch areas and poor visibility.",
        "My Z Flip 7 screen has a crack at the hinge line, dead touch zones, and very faint display output.",
        "I can barely see my Z Flip 7 display due to a cracked fold area and non-working touch regions.",
        "Cracking along the fold of my Galaxy Z Flip 7 has resulted in partial touch failure and low screen visibility.",
        "My Z Flip 7 display is cracked at the fold, touch response is missing in spots, and content is barely visible.",
        "Because of a crack across the Z Flip 7 folding point, touch is unresponsive and the display is obscured.",
        "My Galaxy Z Flip 7 fold line is cracked, causing dead touch spots and severe display distortion.",
        "Touch inputs fail and visibility is degraded on my Z Flip 7 after the screen cracked along the hinge.",
    ],
    "row_20": [
        "My brand new Galaxy A17 has a distorted screen display and I want to run a diagnostic check.",
        "The screen on my newly unboxed Galaxy A17 looks distorted, so I need to test display hardware.",
        "I need a diagnostic tool to evaluate the distorted display on my new Samsung Galaxy A17.",
        "My Galaxy A17 display output appears corrupted right out of the box; how do I test it?",
        "Right after receiving my Galaxy A17, the screen rendering looks distorted and needs diagnosis.",
        "How can I run a hardware test on my Galaxy A17 because the screen visuals look distorted?",
        "My new A17 display suffers from visual distortion and requires diagnostic testing.",
        "I noticed screen distortion on my new Galaxy A17 immediately upon delivery and need a diagnostic test.",
    ],
    "row_21": [
        "Touch inputs on my Galaxy S22 are laggy and delayed, creating noticeable response latency.",
        "My Galaxy S22 screen has severe touch lag and delayed responsiveness during daily use.",
        "Interacting with my Samsung S22 is frustrating because touch response is noticeably delayed.",
        "The touch sensitivity on my Galaxy S22 display feels slow and laggy when tapping icons.",
        "My S22 screen suffers from input lag and delayed touch registration across all apps.",
        "Taps and swipes on my Galaxy S22 display experience a heavy lag before responding.",
        "My Samsung Galaxy S22 screen reacts with a noticeable delay whenever I attempt touch input.",
        "Touch response is sluggish on my S22, resulting in delayed reactions to screen taps.",
    ],
    "row_22": [
        "My Galaxy S24 Ultra rings and powers on normally, but the undamaged screen stays completely black.",
        "Although my S24 Ultra functions and receives calls, the screen shows no display and has no physical damage.",
        "The display on my Galaxy S24 Ultra is pitch black despite the phone ringing and being powered on.",
        "My undamaged Galaxy S24 Ultra turns on and plays notification sounds, but the screen won't illuminate.",
        "Even though my S24 Ultra works internally and rings, the display remains dark without any physical cracks.",
        "My S24 Ultra screen is black and unlit, yet the phone vibrates and rings when called.",
        "Without any physical damage, my S24 Ultra display turned black while the device stays powered on.",
        "My Galaxy S24 Ultra stays on a black screen even though incoming calls ring and the hardware is intact.",
    ],
}


def generate_results(output_path: Path) -> None:
    """Run all 20 official SIIS queries and write results.jsonl strictly matching Theme 2 FAQ schema."""
    cache = get_cache()
    cache.load()

    dataset_path = Path(__file__).parent.parent / "student_kit" / "siis_responses.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    responses = data.get("responses", [])
    orchestrator = PipelineOrchestrator()

    with open(output_path, "w", encoding="utf-8") as out:
        for row in responses:
            row_id = row.get("id", "")
            query = row.get("original_query", "")
            siis_raw = row.get("siis_response", {})
            siis_title = siis_raw.get("title", "")
            siis_content = siis_raw.get("content", "")

            req = TroubleshootRequest(
                query=query,
                siis_response=SIISPayload(title=siis_title, content=siis_content),
                row_id=row_id,
            )
            resp = orchestrator.process(req)

            variations = QUERY_VARIATIONS_MAP.get(row_id, [])

            entry = {
                "query": query,
                "query_variations": variations,
                "response": resp.model_dump(),
            }

            out.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Generated {len(responses)} entries -> {output_path}")


if __name__ == "__main__":
    out = Path(__file__).parent.parent / "results.jsonl"
    generate_results(out)

