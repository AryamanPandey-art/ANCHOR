import { NormalizedDeeplink } from '../schema.js';

export const demoDeeplinks = [
  new NormalizedDeeplink({
    path: "settings://display/screen_rotation",
    title: "Screen Rotation Settings",
    allowedDirections: ["ENABLE", "DISABLE", "TOGGLE"],
    category: "Display",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  }),
  new NormalizedDeeplink({
    path: "settings://battery/protect_battery",
    title: "Protect Battery Settings",
    allowedDirections: ["ENABLE", "DISABLE"],
    category: "Battery",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  }),
  new NormalizedDeeplink({
    path: "settings://connections/wifi_calling",
    title: "Wi-Fi Calling Settings",
    allowedDirections: ["ENABLE", "DISABLE"],
    category: "Connections",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  }),
  new NormalizedDeeplink({
    path: "settings://notifications/do_not_disturb",
    title: "Do Not Disturb Settings",
    allowedDirections: ["ENABLE", "DISABLE", "CONFIGURE"],
    category: "Notifications",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  }),
  new NormalizedDeeplink({
    path: "settings://display/motion_smoothness",
    title: "Motion Smoothness (120Hz)",
    allowedDirections: ["ENABLE", "DISABLE", "STANDARD", "ADAPTIVE"],
    category: "Display",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  }),
  new NormalizedDeeplink({
    path: "settings://display/touch_sensitivity",
    title: "Touch Sensitivity Calibration",
    allowedDirections: ["ENABLE", "CALIBRATE"],
    category: "Display",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  }),
  new NormalizedDeeplink({
    path: "settings://security/biometrics/fingerprints",
    title: "Biometrics & Fingerprints",
    allowedDirections: ["ENABLE", "CONFIGURE"],
    category: "Security",
    verified: true,
    metadata: {
      provenance: "Samsung PRISM Student Kit Mock Catalog (Phase 1 Baseline)",
      isOfficialStudentKit: false
    }
  })
];

export function validateCatalogDeeplink(path, direction, catalog = demoDeeplinks) {
  const entry = catalog.find(d => d.path === path);
  if (!entry) {
    return { valid: false, reason: `Deeplink '${path}' not found in Samsung catalog` };
  }
  if (!entry.supportsDirection(direction)) {
    return { 
      valid: false, 
      reason: `Direction '${direction}' not permitted for '${path}'. Allowed: [${entry.allowedDirections.join(', ')}]` 
    };
  }
  return { valid: true, catalogEntry: entry };
}
