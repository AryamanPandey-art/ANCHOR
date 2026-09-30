import { activeDeeplinkCatalog, validateCatalogDeeplink } from '../data/index.js';
import { resolveCatalogDeeplink } from '../data/student-kit/deeplinkLoader.js';

/**
 * Authoritative Samsung Deeplink Resolver Engine
 * Resolves settings URIs strictly from the authoritative Samsung catalog.
 * Enforces direction safety (ENABLE vs DISABLE) and preserves exact original masked URIs.
 * Never invents mock or hallucinated settings URLs.
 */
export function resolveDeeplink(actionResult = {}, evidenceResult = {}, catalog = activeDeeplinkCatalog) {
  // If action wasn't resolved, deeplink cannot be resolved
  if (!actionResult || !actionResult.resolved || !actionResult.action) {
    return {
      candidate: actionResult?.action || "None",
      deeplink: null,
      direction: actionResult?.direction || "NONE",
      catalogMatch: "INVALID",
      confidence: 0,
      verified: false,
      reason: "No valid action available to map to a Samsung Deeplink."
    };
  }

  const direction = actionResult.direction || "ENABLE";
  let matchedEntry = null;

  // 1. If action provides a direct catalog deeplink path, validate it first
  if (actionResult.deeplinkPath) {
    const directCheck = validateCatalogDeeplink(actionResult.deeplinkPath, direction, catalog);
    if (directCheck.valid && directCheck.catalogEntry) {
      matchedEntry = directCheck.catalogEntry;
    }
  }

  // 2. If not found via direct path, query authoritative catalog by action name and direction
  if (!matchedEntry) {
    const hints = [
      actionResult.action,
      actionResult.deeplinkPath,
      evidenceResult?.title,
      evidenceResult?.section
    ].filter(Boolean);

    matchedEntry = resolveCatalogDeeplink(actionResult.action, direction, catalog, hints);
  }

  // 3. Reject if uncatalogued
  if (!matchedEntry) {
    return {
      candidate: actionResult.action,
      deeplink: actionResult.deeplinkPath || null,
      direction: direction,
      catalogMatch: "INVALID",
      confidence: 0,
      verified: false,
      reason: `No matching Samsung catalog deeplink found for action '${actionResult.action}' with direction '${direction}'.`
    };
  }

  // 4. Strict Direction Verification
  const directionCheck = validateCatalogDeeplink(matchedEntry.path || matchedEntry.deeplink, direction, catalog);
  if (!directionCheck.valid) {
    return {
      candidate: actionResult.action,
      deeplink: matchedEntry.path || matchedEntry.deeplink,
      direction: direction,
      catalogMatch: "INVALID",
      confidence: 25,
      verified: false,
      reason: directionCheck.reason || `Direction mismatch for catalog URI '${matchedEntry.path}'`
    };
  }

  const finalEntry = directionCheck.catalogEntry || matchedEntry;

  return {
    candidate: actionResult.action,
    deeplink: finalEntry.path || finalEntry.deeplink,
    direction: direction,
    catalogMatch: "VALID",
    confidence: 95,
    verified: true,
    catalogCategory: finalEntry.category,
    title: finalEntry.title || finalEntry.message,
    message: finalEntry.message || finalEntry.title,
    description: finalEntry.description,
    originalType: finalEntry.originalType || "onClickURL",
    validation: finalEntry.validation || null,
    provenance: finalEntry.metadata?.provenance || "Samsung Student Kit (deeplinks.json)"
  };
}

