import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { loadSiisResponses } from './siisLoader.js';
import { loadDeeplinks, resolveCatalogDeeplink, validateOfficialCatalogDeeplink } from './deeplinkLoader.js';
import { buildOfficialResponsePayload, validateAgainstSchema, validateWithPythonPydantic } from './schemaValidator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Master loader and coordinator for official Samsung Student Kit data.
 * Verifies official files presence, exposes normalized catalogs with full provenance disclosure.
 */
export function loadOfficialStudentKit() {
  const siisFile = path.join(__dirname, 'siis_responses.json');
  const deeplinkFile = path.join(__dirname, 'deeplinks.json');

  const hasSiisFile = fs.existsSync(siisFile);
  const hasDeeplinkFile = fs.existsSync(deeplinkFile);

  let officialEvidence = [];
  let officialDeeplinks = [];
  let foundEvidencePath = null;
  let foundDeeplinkPath = null;

  if (hasSiisFile) {
    try {
      const siisResult = loadSiisResponses(siisFile);
      officialEvidence = siisResult.records;
      foundEvidencePath = siisFile;
    } catch (e) {
      console.error(`Failed to load official SIIS responses from ${siisFile}:`, e);
    }
  }

  if (hasDeeplinkFile) {
    try {
      const deeplinkResult = loadDeeplinks(deeplinkFile);
      officialDeeplinks = deeplinkResult.deeplinks;
      foundDeeplinkPath = deeplinkFile;
    } catch (e) {
      console.error(`Failed to load official deeplinks from ${deeplinkFile}:`, e);
    }
  }

  const isOfficialPresent = officialEvidence.length > 0 && officialDeeplinks.length > 0;

  return {
    isOfficialPresent,
    evidencePath: foundEvidencePath,
    deeplinkPath: foundDeeplinkPath,
    evidence: officialEvidence,
    deeplinks: officialDeeplinks
  };
}

export {
  resolveCatalogDeeplink,
  validateOfficialCatalogDeeplink,
  buildOfficialResponsePayload,
  validateAgainstSchema,
  validateWithPythonPydantic
};
