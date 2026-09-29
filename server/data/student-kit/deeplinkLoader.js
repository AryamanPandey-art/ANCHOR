import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { NormalizedDeeplink } from '../schema.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Authoritative Deeplink Loader for official Samsung Student Kit (Theme 2).
 * Loads 578 masked settings URIs from deeplinks.json, enforces exact URI preservation,
 * extracts direction semantics (onURL -> ENABLE, offURL -> DISABLE, onClickURL -> NEUTRAL),
 * and rejects uncatalogued or direction-mismatched deeplinks deterministically.
 */
export function loadDeeplinks(filePath = null) {
  const targetFile = filePath || path.join(__dirname, 'deeplinks.json');

  if (!fs.existsSync(targetFile)) {
    throw new Error(`Deeplinks file not found at: ${targetFile}`);
  }

  let rawData;
  try {
    const fileContent = fs.readFileSync(targetFile, 'utf-8');
    rawData = JSON.parse(fileContent);
  } catch (err) {
    throw new Error(`Failed to read/parse Deeplinks JSON (${targetFile}): ${err.message}`);
  }

  if (!rawData || !Array.isArray(rawData.deeplinks)) {
    throw new Error(`Invalid Deeplinks format: 'deeplinks' array missing in ${targetFile}`);
  }

  const normalizedCatalog = rawData.deeplinks.map(item => {
    if (!item.id || !item.deeplink || !item.description) {
      throw new Error(`Malformed Deeplink entry detected: ${JSON.stringify(item)}`);
    }

    // Determine direction from originalType and description
    let direction = "NEUTRAL";
    let allowedDirections = ["ENABLE", "DISABLE", "CONFIGURE", "TOGGLE", "NEUTRAL"];

    if (item.originalType === "onURL" || item.description.toLowerCase().startsWith("enables ")) {
      direction = "ENABLE";
      allowedDirections = ["ENABLE"];
    } else if (item.originalType === "offURL" || item.description.toLowerCase().startsWith("disables ")) {
      direction = "DISABLE";
      allowedDirections = ["DISABLE"];
    } else if (item.originalType === "onClickURL") {
      direction = "CONFIGURE";
      allowedDirections = ["ENABLE", "DISABLE", "CONFIGURE", "TOGGLE"];
    }

    return new NormalizedDeeplink({
      id: item.id,
      path: item.deeplink,
      deeplink: item.deeplink,
      title: item.message || item.description,
      message: item.message || "",
      description: item.description,
      qnaDescription: item.qna_description || "",
      originalType: item.originalType,
      direction: direction,
      allowedDirections: allowedDirections,
      category: deriveCategoryFromDescription(item.description),
      validation: item.validation || null,
      verified: true,
      metadata: {
        provenance: "Samsung Student Kit (deeplinks.json)",
        isOfficialStudentKit: true,
        sourceFile: "server/data/student-kit/deeplinks.json",
        originalId: item.id
      }
    });
  });

  return {
    count: normalizedCatalog.length,
    sourceFile: targetFile,
    deeplinks: normalizedCatalog
  };
}

/**
 * Derives settings category from description.
 */
function deriveCategoryFromDescription(description) {
  const lower = (description || '').toLowerCase();
  if (lower.includes('display') || lower.includes('screen') || lower.includes('dark mode') || lower.includes('rotate')) return 'Display';
  if (lower.includes('battery') || lower.includes('power')) return 'Battery';
  if (lower.includes('security') || lower.includes('fingerprint') || lower.includes('biometric') || lower.includes('lock')) return 'Security';
  if (lower.includes('wifi') || lower.includes('wi-fi') || lower.includes('network') || lower.includes('bluetooth') || lower.includes('connection')) return 'Connections';
  if (lower.includes('notification') || lower.includes('sound') || lower.includes('disturb')) return 'Notifications';
  return 'General';
}

/**
 * Searches the official catalog for a matching deeplink by action name, direction, and hints.
 * Returns exact catalog entry or null if uncatalogued.
 */
export function resolveCatalogDeeplink(actionName, requestedDirection, catalog, extraHints = []) {
  if (!actionName || !Array.isArray(catalog) || !catalog.length) return null;

  const targetDir = (requestedDirection || "ENABLE").toUpperCase();
  const lowerAction = actionName.toLowerCase();
  const searchHints = [
    lowerAction,
    ...extraHints.map(h => (h || '').toLowerCase())
  ];

  // Specific high-priority exact mappings for Theme 2
  if (lowerAction.includes('rotate') || lowerAction.includes('orientation')) {
    // DL-0461: Rotate to landscape mode
    const rotationMatch = catalog.find(d => d.id === 'DL-0461' || d.path.includes('7c340914be'));
    if (rotationMatch) return rotationMatch;
  }

  if (lowerAction.includes('touch sensitivity')) {
    if (targetDir === 'ENABLE') {
      // DL-0126: Enables touch sensitivity via device Settings
      const match = catalog.find(d => d.id === 'DL-0126' || d.path.includes('14eb42b895'));
      if (match) return match;
    } else if (targetDir === 'DISABLE') {
      // DL-0125: Disables touch sensitivity via device Settings
      const match = catalog.find(d => d.id === 'DL-0125' || d.path.includes('1b0d34e9b4'));
      if (match) return match;
    }
  }

  if (lowerAction.includes('fingerprint')) {
    // DL-0551: Opens the fingerprint unlock settings page
    const match = catalog.find(d => d.id === 'DL-0551' || d.path.includes('49f61f06b4'));
    if (match) return match;
  }

  if (lowerAction.includes('back up') || lowerAction.includes('backup')) {
    if (targetDir === 'ENABLE') {
      const backupEnable = catalog.find(d => d.id === 'DL-0542' || (d.path.includes('b3ed3ed663') && d.supportsDirection('ENABLE')));
      if (backupEnable) return backupEnable;
    } else if (targetDir === 'DISABLE') {
      const backupDisable = catalog.find(d => d.id === 'DL-0541' || (d.path.includes('066ffdf83a') && d.supportsDirection('DISABLE')));
      if (backupDisable) return backupDisable;
    }
    const backupMatch = catalog.find(d => 
      ((d.message && d.message.toLowerCase().includes('back up')) || 
       (d.description && d.description.toLowerCase().includes('back up'))) &&
      d.supportsDirection(targetDir)
    );
    if (backupMatch) return backupMatch;
  }


  // General semantic match across all 578 items
  const candidates = [];
  for (const item of catalog) {
    let score = 0;
    const msg = (item.message || '').toLowerCase();
    const desc = (item.description || '').toLowerCase();
    const qna = (item.qnaDescription || '').toLowerCase();

    // Check direction compatibility
    if (targetDir === 'ENABLE' && item.direction === 'DISABLE') continue;
    if (targetDir === 'DISABLE' && item.direction === 'ENABLE') continue;

    for (const hint of searchHints) {
      if (!hint) continue;
      if (msg.includes(hint)) score += 30;
      if (desc.includes(hint)) score += 20;
      if (qna.includes(hint)) score += 10;
    }

    if (score > 0) {
      candidates.push({ item, score });
    }
  }

  if (!candidates.length) return null;
  candidates.sort((a, b) => b.score - a.score);
  return candidates[0].item;
}

/**
 * Validates whether a given URI is present in the official catalog and supports the requested direction.
 */
export function validateOfficialCatalogDeeplink(uri, direction, catalog) {
  if (!uri) {
    return { valid: false, reason: "Missing deeplink URI." };
  }
  const entry = catalog.find(d => d.deeplink === uri || d.path === uri);
  if (!entry) {
    return { valid: false, reason: `Uncatalogued deeplink URI: '${uri}' not in Samsung Student Kit catalog.` };
  }

  if (direction && !entry.supportsDirection(direction)) {
    return { 
      valid: false, 
      reason: `Direction '${direction}' not permitted for catalog URI '${uri}' (allowed: ${entry.allowedDirections.join(', ')})`,
      catalogEntry: entry 
    };
  }

  return { valid: true, catalogEntry: entry };
}
