/**
 * ANCHOR Intent & State Understanding Engine
 * Extracts device domain, user goal, requested action direction (ENABLE vs DISABLE),
 * entities, and identifies ambiguous queries deterministically.
 */

export function parseIntent(query = "") {
  const normalized = query.trim().toLowerCase();

  if (!normalized || normalized.length < 5) {
    return {
      intent: "EMPTY_QUERY",
      confidence: 0,
      targetDirection: "NONE",
      goal: "Unspecified",
      category: "Unspecified",
      deviceType: "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: [],
      ambiguous: true
    };
  }

  // 1. Detect requested direction
  let targetDirection = null;

  const disablePhrases = [
    "turn off", "turn it off", "turn auto rotate off", "disable", "stop", "deactivate",
    "lock screen orientation", "lock screen rotation", "lock rotation",
    "keeps rotating", "don't want it to rotate", "prevent rotation",
    "turn protect battery off", "disable protect battery",
    "turn off do not disturb", "disable do not disturb", "turn off dnd",
    "turn off touch sensitivity", "disable touch sensitivity", "turn touch sensitivity off"
  ];

  const enablePhrases = [
    "turn on", "turn it on", "turn auto rotate on", "enable", "activate", "start",
    "isn't rotating", "is not rotating", "not rotating", "won't rotate", "wont rotate",
    "doesn't rotate", "does not rotate", "allow rotate",
    "turn on protect battery", "enable protect battery",
    "turn on do not disturb", "enable do not disturb", "turn on dnd",
    "turn on touch sensitivity", "enable touch sensitivity", "turn touch sensitivity on",
    "laggy", "delayed", "not responding", "unresponsive", "touchscreen issues", "inputs are delayed"
  ];

  const hasDisableMatch = disablePhrases.some(phrase => normalized.includes(phrase));
  const hasEnableMatch = enablePhrases.some(phrase => normalized.includes(phrase));

  if (hasDisableMatch && !hasEnableMatch) {
    targetDirection = "DISABLE";
  } else if (hasEnableMatch && !hasDisableMatch) {
    targetDirection = "ENABLE";
  } else if (hasDisableMatch && hasEnableMatch) {
    // If both present, prioritize explicit "turn it off" or "turn off" command over symptoms
    if (normalized.includes("turn it off") || normalized.includes("turn off") || normalized.includes("disable")) {
      targetDirection = "DISABLE";
    } else {
      targetDirection = "ENABLE";
    }
  }

  // 2. Identify Intent & Category with specific mobile troubleshooting context
  // Screen Rotation & Distorted Orientation
  const hasRotateContext = normalized.includes("rotat") || 
    normalized.includes("distorted") ||
    normalized.includes("diagnostic test") ||
    (normalized.includes("screen") && (normalized.includes("orient") || normalized.includes("tilt") || normalized.includes("portrait") || normalized.includes("landscape")));

  if (hasRotateContext) {
    return {
      intent: "SCREEN_ROTATION",
      confidence: 94,
      targetDirection: targetDirection || "ENABLE",
      goal: targetDirection === "DISABLE" ? "Disable Auto Screen Rotation" : "Enable Auto Screen Rotation",
      category: "Display & Rotation",
      deviceType: normalized.includes("tablet") ? "Tablet (Galaxy Tab)" : "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: ["screen", "rotation", "auto rotate", "orientation"],
      ambiguous: false
    };
  }

  // Touch sensitivity & responsiveness
  if (normalized.includes("touch") || normalized.includes("touchscreen") || normalized.includes("digitizer") || normalized.includes("laggy") || normalized.includes("delayed")) {
    const finalDir = targetDirection || "ENABLE";
    return {
      intent: "TOUCH_SENSITIVITY",
      confidence: 93,
      targetDirection: finalDir,
      goal: finalDir === "DISABLE" ? "Disable Touch Sensitivity" : "Enable Touch Sensitivity / Improve Responsiveness",
      category: "Display & Touch",
      deviceType: normalized.includes("tablet") ? "Tablet (Galaxy Tab)" : "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: ["touchscreen", "display", "touch response", "sensitivity"],
      ambiguous: false
    };
  }

  // Biometrics & Fingerprint
  if (normalized.includes("fingerprint") || normalized.includes("biometric")) {
    return {
      intent: "BIOMETRIC_FINGERPRINT",
      confidence: 93,
      targetDirection: "ENABLE",
      goal: "Configure Fingerprint Recognition",
      category: "Security & Biometrics",
      deviceType: "Smartphone (Galaxy)",
      osVersion: "One UI 6.1",
      detectedEntities: ["fingerprint", "biometrics", "sensor"],
      ambiguous: false
    };
  }

  // Cracked Screen / Hardware Damage
  if (normalized.includes("crack") || normalized.includes("bleeding") || normalized.includes("broken screen") || normalized.includes("physical damage")) {
    return {
      intent: "CRACKED_SCREEN",
      confidence: 95,
      targetDirection: "ENABLE",
      goal: "Screen Damage Troubleshooting & Data Backup",
      category: "Hardware & Service",
      deviceType: normalized.includes("fold") ? "Foldable (Galaxy Fold)" : "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: ["screen", "cracked", "damage", "repair", "backup"],
      ambiguous: false
    };
  }

  // Blank / Black Display (including blue screen, won't turn on, won't start up)
  const isBlankOrBlack = normalized.includes("blank") || 
    normalized.includes("black screen") || 
    normalized.includes("blue screen") || 
    normalized.includes("flicker") || 
    normalized.includes("flashes") || 
    (normalized.includes("screen") && (
      normalized.includes("black") || 
      normalized.includes("dark") || 
      normalized.includes("stays dark") || 
      normalized.includes("display anything") || 
      normalized.includes("won't start") || 
      normalized.includes("wont start") || 
      normalized.includes("won't turn on") || 
      normalized.includes("wont turn on") || 
      normalized.includes("blue")
    ));

  if (isBlankOrBlack) {
    return {
      intent: "BLANK_DISPLAY",
      confidence: 92,
      targetDirection: "ENABLE",
      goal: "Blank Screen Recovery & Diagnostic",
      category: "Display & Power",
      deviceType: normalized.includes("tablet") ? "Tablet (Galaxy Tab)" : (normalized.includes("fold") ? "Foldable (Galaxy Fold)" : "Smartphone (Galaxy)"),
      osVersion: "One UI 6.x",
      detectedEntities: ["blank screen", "display", "flicker", "power"],
      ambiguous: false
    };
  }

  // Display Aspect Ratio / Screen Mirroring
  if (normalized.includes("stays small") || normalized.includes("expand to full") || normalized.includes("doesn't fill the whole display") || normalized.includes("aspect ratio")) {
    return {
      intent: "DISPLAY_ASPECT_RATIO",
      confidence: 88,
      targetDirection: "ENABLE",
      goal: "Adjust Display Aspect Ratio / Full Screen",
      category: "Display & Screen Mirroring",
      deviceType: "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: ["screen", "display", "aspect ratio", "full size"],
      ambiguous: false
    };
  }

  // Data Transfer
  if (normalized.includes("transfer") || (normalized.includes("data") && normalized.includes("switch"))) {
    return {
      intent: "DATA_TRANSFER",
      confidence: 90,
      targetDirection: "ENABLE",
      goal: "Data Transfer and Backup Setup",
      category: "Accounts & Transfer",
      deviceType: normalized.includes("tablet") ? "Tablet (Galaxy Tab)" : "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: ["data transfer", "backup", "switch"],
      ambiguous: false
    };
  }


  // Battery & Power
  if (normalized.includes("battery") && (normalized.includes("drain") || normalized.includes("charg") || normalized.includes("protect") || normalized.includes("save") || normalized.includes("power"))) {
    return {
      intent: "BATTERY_OPTIMIZATION",
      confidence: 91,
      targetDirection: targetDirection || "ENABLE",
      goal: "Battery Health and Optimization",
      category: "Battery & Device Care",
      deviceType: "Smartphone (Galaxy)",
      osVersion: "One UI 6.1",
      detectedEntities: ["battery", "protect battery", "charge"],
      ambiguous: false
    };
  }

  // Multi-window / Floating circle / Assist
  if (normalized.includes("floating circle") || normalized.includes("assistant menu") || normalized.includes("shortcuts")) {
    return {
      intent: "MULTI_WINDOW",
      confidence: 89,
      targetDirection: targetDirection || "DISABLE",
      goal: "Configure Assistant Menu / Floating Shortcuts",
      category: "Accessibility & Navigation",
      deviceType: "Smartphone (Galaxy)",
      osVersion: "One UI 6.x",
      detectedEntities: ["floating circle", "shortcuts", "assistant menu"],
      ambiguous: false
    };
  }

  // Ambiguous or unsupported query
  return {
    intent: "UNSUPPORTED_INTENT",
    confidence: 20,
    targetDirection: "NONE",
    goal: "Unknown",
    category: "Unknown",
    deviceType: "Smartphone (Galaxy)",
    osVersion: "One UI 6.x",
    detectedEntities: [],
    ambiguous: true
  };
}

