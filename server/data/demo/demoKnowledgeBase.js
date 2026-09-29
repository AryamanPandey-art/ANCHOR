import { NormalizedEvidence } from '../schema.js';

export const demoEvidenceRecords = [
  new NormalizedEvidence({
    id: "#SIIS-023",
    source: "Samsung SIIS",
    section: "Display > Screen rotation",
    title: "Screen Rotation & Auto-Rotate Settings",
    content: "... To enable auto rotate, go to Settings > Display > Screen rotation and turn on Auto rotate. To lock the screen in portrait or landscape, turn off Auto rotate ...",
    intent: "SCREEN_ROTATION",
    entities: ["screen", "rotate", "rotation", "orientation", "auto rotate", "landscape", "portrait", "flip"],
    conditions: [
      { direction: "ENABLE", statement: "Auto rotate = OFF" },
      { direction: "DISABLE", statement: "Auto rotate = ON" }
    ],
    supportedActions: [
      {
        action: "Enable Auto Rotate",
        direction: "ENABLE",
        deeplink: "settings://display/screen_rotation",
        proof: "Evidence specifies turning on Auto rotate when screen does not rotate automatically"
      },
      {
        action: "Disable Auto Rotate",
        direction: "DISABLE",
        deeplink: "settings://display/screen_rotation",
        proof: "Evidence specifies turning off Auto rotate to lock orientation"
      }
    ],
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock/Demo Dataset (Phase 1 Baseline)",
      isOfficialStudentKit: false,
      sourceFile: "server/data/demo/demoKnowledgeBase.js",
      relevanceScore: 92,
      deviceContext: {
        model: "Galaxy S23",
        os: "One UI 6.x",
        type: "Smartphone (Galaxy)"
      },
      relatedIssues: ["• Orientation Lock", "• Auto Rotate", "• Motion Sensor"]
    }
  }),
  new NormalizedEvidence({
    id: "#SIIS-045",
    source: "Samsung SIIS",
    section: "Battery > Protect battery",
    title: "Battery Protection and Fast Charging",
    content: "... To extend battery lifespan, go to Settings > Battery and device care > Battery > More battery settings and turn on Protect battery ...",
    intent: "BATTERY_OPTIMIZATION",
    entities: ["battery", "drain", "charge", "fast charging", "overheating", "protect battery"],
    conditions: [
      { direction: "ENABLE", statement: "Battery protection = DISABLED" },
      { direction: "DISABLE", statement: "Battery protection = ENABLED" }
    ],
    supportedActions: [
      {
        action: "Enable Protect Battery",
        direction: "ENABLE",
        deeplink: "settings://battery/protect_battery",
        proof: "Evidence prescribes enabling Protect Battery to restrict maximum charge to 85%"
      },
      {
        action: "Disable Protect Battery",
        direction: "DISABLE",
        deeplink: "settings://battery/protect_battery",
        proof: "Evidence prescribes disabling Protect Battery to allow full 100% charging capacity"
      }
    ],
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock/Demo Dataset (Phase 1 Baseline)",
      isOfficialStudentKit: false,
      sourceFile: "server/data/demo/demoKnowledgeBase.js",
      relevanceScore: 89,
      deviceContext: {
        model: "Galaxy S24 Ultra",
        os: "One UI 6.1",
        type: "Smartphone (Galaxy)"
      },
      relatedIssues: ["• Fast Charging", "• Battery Saver", "• Thermal Throttling"]
    }
  }),
  new NormalizedEvidence({
    id: "#SIIS-012",
    source: "Samsung SIIS",
    section: "Connections > Wi-Fi Calling",
    title: "Wi-Fi Calling & Network Handover",
    content: "... When cellular reception is degraded, enable Wi-Fi Calling under Settings > Connections > Wi-Fi Calling to route voice over WLAN ...",
    intent: "NETWORK_CONNECTIVITY",
    entities: ["wifi", "wi-fi", "calling", "call drop", "network", "reception"],
    conditions: [
      { direction: "ENABLE", statement: "Wi-Fi Calling = OFF" },
      { direction: "DISABLE", statement: "Wi-Fi Calling = ON" }
    ],
    supportedActions: [
      {
        action: "Enable Wi-Fi Calling",
        direction: "ENABLE",
        deeplink: "settings://connections/wifi_calling",
        proof: "Evidence prescribes enabling Wi-Fi Calling when indoor cellular reception drops"
      },
      {
        action: "Disable Wi-Fi Calling",
        direction: "DISABLE",
        deeplink: "settings://connections/wifi_calling",
        proof: "Evidence prescribes disabling Wi-Fi Calling when network jitter causes handover issues"
      }
    ],
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock/Demo Dataset (Phase 1 Baseline)",
      isOfficialStudentKit: false,
      sourceFile: "server/data/demo/demoKnowledgeBase.js",
      relevanceScore: 88,
      deviceContext: {
        model: "Galaxy S23",
        os: "One UI 6.x",
        type: "Smartphone (Galaxy)"
      },
      relatedIssues: ["• VoLTE Handover", "• Carrier Profile", "• WLAN Signal"]
    }
  }),
  new NormalizedEvidence({
    id: "#SIIS-088",
    source: "Samsung SIIS",
    section: "Notifications > Do not disturb",
    title: "Do Not Disturb Exceptions",
    content: "... If incoming calls or alerts are silenced unexpectedly, verify Do Not Disturb schedules in Settings > Notifications > Do not disturb ...",
    intent: "NOTIFICATION_SILENCE",
    entities: ["sound", "notification", "silent", "do not disturb", "dnd", "ringtone"],
    conditions: [
      { direction: "ENABLE", statement: "Do Not Disturb = OFF" },
      { direction: "DISABLE", statement: "Do Not Disturb = ACTIVE" }
    ],
    supportedActions: [
      {
        action: "Disable Do Not Disturb",
        direction: "DISABLE",
        deeplink: "settings://notifications/do_not_disturb",
        proof: "Evidence prescribes disabling DND when essential notifications fail to ring"
      },
      {
        action: "Enable Do Not Disturb",
        direction: "ENABLE",
        deeplink: "settings://notifications/do_not_disturb",
        proof: "Evidence prescribes activating DND during quiet hours"
      }
    ],
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock/Demo Dataset (Phase 1 Baseline)",
      isOfficialStudentKit: false,
      sourceFile: "server/data/demo/demoKnowledgeBase.js",
      relevanceScore: 90,
      deviceContext: {
        model: "Galaxy Z Fold5",
        os: "One UI 6.0",
        type: "Foldable (Galaxy)"
      },
      relatedIssues: ["• Priority Alerts", "• Sleep Schedule", "• App Notification Lock"]
    }
  }),
  new NormalizedEvidence({
    id: "#SIIS-091",
    source: "Samsung SIIS",
    section: "Display > Touch sensitivity",
    title: "Touch Sensitivity & Screen Calibration",
    content: "... Increasing touch sensitivity in Settings > Display > Touch sensitivity calibrates touch response for thick screen protectors. Notice: This does not fix hardware touch digitizer unresponsiveness ...",
    intent: "TOUCH_SENSITIVITY",
    entities: ["touch", "touchscreen", "screen", "sensitivity", "touch sensitivity", "unresponsive", "responding", "protector"],
    conditions: [
      { direction: "ENABLE", statement: "Touch sensitivity = DISABLED" },
      { direction: "CALIBRATE", statement: "Screen protector applied" }
    ],
    supportedActions: [
      {
        action: "Enable Touch Sensitivity",
        direction: "ENABLE",
        deeplink: "settings://display/touch_sensitivity",
        proof: "Evidence specifies increasing touch sensitivity when screen protector is applied"
      }
    ],
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock/Demo Dataset (Phase 1 Baseline)",
      isOfficialStudentKit: false,
      sourceFile: "server/data/demo/demoKnowledgeBase.js",
      relevanceScore: 91,
      deviceContext: {
        model: "Galaxy S23",
        os: "One UI 6.x",
        type: "Smartphone (Galaxy)"
      },
      relatedIssues: ["• Touch Latency", "• Screen Protector", "• Hardware Digitizer"]
    }
  }),
  new NormalizedEvidence({
    id: "#SIIS-074",
    source: "Samsung SIIS",
    section: "Security and privacy > Biometrics > Fingerprints",
    title: "Fingerprint Sensor Registration & Recognition",
    content: "... If fingerprint recognition fails or does not unlock, re-register your fingerprint in Settings > Security and privacy > Biometrics > Fingerprints. Ensure the sensor area is clean ...",
    intent: "BIOMETRIC_FINGERPRINT",
    entities: ["fingerprint", "biometrics", "sensor", "scanner", "unlock", "finger"],
    conditions: [
      { direction: "ENABLE", statement: "Biometrics = ACTIVE" },
      { direction: "CONFIGURE", statement: "Fingerprint re-registration required" }
    ],
    supportedActions: [
      {
        action: "Re-register Fingerprint",
        direction: "ENABLE",
        deeplink: "settings://security/biometrics/fingerprints",
        proof: "Evidence prescribes re-registering fingerprints when recognition intermittently fails"
      }
    ],
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock/Demo Dataset (Phase 1 Baseline)",
      isOfficialStudentKit: false,
      sourceFile: "server/data/demo/demoKnowledgeBase.js",
      relevanceScore: 93,
      deviceContext: {
        model: "Galaxy S24 Ultra",
        os: "One UI 6.1",
        type: "Smartphone (Galaxy)"
      },
      relatedIssues: ["• In-Display Sensor", "• Biometric Security", "• Screen Protector Recalibration"]
    }
  })
];

export const demoCoverageSections = [
  { section: "Display > Screen rotation", covered: true, score: 92 },
  { section: "Display > Always On Display", covered: true, score: 88 },
  { section: "Display > Motion smoothness", covered: true, score: 79 },
  { section: "Battery > Power saving", covered: true, score: 95 },
  { section: "Battery > Background limits", covered: true, score: 84 },
  { section: "Connections > Wi-Fi Calling", covered: true, score: 91 },
  { section: "Connections > Bluetooth", covered: true, score: 86 },
  { section: "Connections > Mobile Networks", covered: true, score: 78 },
  { section: "Notifications > Do Not Disturb", covered: true, score: 96 },
  { section: "Security > Biometrics", covered: true, score: 82 },
  { section: "Device Care > Memory cleaner", covered: true, score: 75 },
  { section: "Accessibility > Touch sensitivity", covered: true, score: 90 },
  { section: "System > Software update", covered: false, score: 40 },
  { section: "Apps > Default apps", covered: false, score: 45 }
];
