// Samsung Settings Deeplink Catalog and Supported Actions
export const deeplinkCatalog = [
  {
    path: "settings://display/screen_rotation",
    title: "Screen Rotation Settings",
    allowedDirections: ["ENABLE", "DISABLE", "TOGGLE"],
    verified: true,
    category: "Display"
  },
  {
    path: "settings://battery/protect_battery",
    title: "Protect Battery Settings",
    allowedDirections: ["ENABLE", "DISABLE"],
    verified: true,
    category: "Battery"
  },
  {
    path: "settings://connections/wifi_calling",
    title: "Wi-Fi Calling Settings",
    allowedDirections: ["ENABLE", "DISABLE"],
    verified: true,
    category: "Connections"
  },
  {
    path: "settings://notifications/do_not_disturb",
    title: "Do Not Disturb Settings",
    allowedDirections: ["ENABLE", "DISABLE", "CONFIGURE"],
    verified: true,
    category: "Notifications"
  },
  {
    path: "settings://display/motion_smoothness",
    title: "Motion Smoothness (120Hz)",
    allowedDirections: ["ENABLE", "DISABLE", "STANDARD", "ADAPTIVE"],
    verified: true,
    category: "Display"
  },
  {
    path: "settings://display/touch_sensitivity",
    title: "Touch Sensitivity Calibration",
    allowedDirections: ["ENABLE", "CALIBRATE"],
    verified: true,
    category: "Display"
  },
  {
    path: "settings://security/biometrics/fingerprints",
    title: "Biometrics & Fingerprints",
    allowedDirections: ["ENABLE", "CONFIGURE"],
    verified: true,
    category: "Security"
  }
];

export function validateDeeplink(path, direction) {
  const entry = deeplinkCatalog.find(d => d.path === path);
  if (!entry) {
    return { valid: false, reason: "Deeplink not found in Samsung catalog" };
  }
  if (!entry.allowedDirections.includes(direction)) {
    return { valid: false, reason: `Direction '${direction}' not permitted for ${path}` };
  }
  return { valid: true, catalogEntry: entry };
}
