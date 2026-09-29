// Samsung SIIS (Samsung Interactive Intelligence & Settings) Knowledge Base
export const siisKnowledgeBase = [
  {
    id: "#SIIS-023",
    category: "Display & Rotation",
    title: "Screen Rotation & Auto-Rotate Settings",
    section: "Display > Screen rotation",
    excerpt: "... To enable auto rotate, go to Settings > Display > Screen rotation and turn on Auto rotate ...",
    keywords: ["screen", "rotate", "rotation", "orientation", "auto rotate", "landscape", "portrait", "flip"],
    action: "Enable Auto Rotate",
    direction: "ENABLE",
    deeplink: "settings://display/screen_rotation",
    deviceContext: {
      model: "Galaxy S23",
      os: "One UI 6.x",
      type: "Smartphone (Galaxy)"
    },
    condition: "Auto rotate = OFF",
    relatedIssues: ["• Orientation Lock", "• Auto Rotate", "• Motion Sensor"]
  },
  {
    id: "#SIIS-045",
    category: "Battery & Device Care",
    title: "Battery Protection and Fast Charging",
    section: "Battery > Protect battery",
    excerpt: "... To extend battery lifespan, go to Settings > Battery and device care > Battery > More battery settings and turn on Protect battery ...",
    keywords: ["battery", "drain", "charge", "fast charging", "overheating", "protect battery"],
    action: "Enable Protect Battery",
    direction: "ENABLE",
    deeplink: "settings://battery/protect_battery",
    deviceContext: {
      model: "Galaxy S24 Ultra",
      os: "One UI 6.1",
      type: "Smartphone (Galaxy)"
    },
    condition: "Battery protection = DISABLED",
    relatedIssues: ["• Fast Charging", "• Battery Saver", "• Thermal Throttling"]
  },
  {
    id: "#SIIS-012",
    category: "Connections & Network",
    title: "Wi-Fi Calling & Network Handover",
    section: "Connections > Wi-Fi Calling",
    excerpt: "... When cellular reception is degraded, enable Wi-Fi Calling under Settings > Connections > Wi-Fi Calling to route voice over WLAN ...",
    keywords: ["wifi", "wi-fi", "calling", "call drop", "network", "reception"],
    action: "Enable Wi-Fi Calling",
    direction: "ENABLE",
    deeplink: "settings://connections/wifi_calling",
    deviceContext: {
      model: "Galaxy S23",
      os: "One UI 6.x",
      type: "Smartphone (Galaxy)"
    },
    condition: "Wi-Fi Calling = OFF",
    relatedIssues: ["• VoLTE Handover", "• Carrier Profile", "• WLAN Signal"]
  },
  {
    id: "#SIIS-088",
    category: "Sound & Notifications",
    title: "Do Not Disturb Exceptions",
    section: "Notifications > Do not disturb",
    excerpt: "... If incoming calls or alerts are silenced unexpectedly, verify Do Not Disturb schedules in Settings > Notifications > Do not disturb ...",
    keywords: ["sound", "notification", "silent", "do not disturb", "dnd", "ringtone"],
    action: "Disable Do Not Disturb",
    direction: "DISABLE",
    deeplink: "settings://notifications/do_not_disturb",
    deviceContext: {
      model: "Galaxy Z Fold5",
      os: "One UI 6.0",
      type: "Foldable (Galaxy)"
    },
    condition: "Do Not Disturb = ACTIVE",
    relatedIssues: ["• Priority Alerts", "• Sleep Schedule", "• App Notification Lock"]
  }
];

export const siisCoverageSections = [
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
