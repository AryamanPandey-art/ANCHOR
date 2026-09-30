import { loadOfficialStudentKit } from './student-kit/loader.js';
import { validateOfficialCatalogDeeplink } from './student-kit/deeplinkLoader.js';
import { demoEvidenceRecords, demoCoverageSections } from './demo/demoKnowledgeBase.js';
import { demoDeeplinks, validateCatalogDeeplink as validateDemoCatalogDeeplink } from './demo/demoDeeplinkCatalog.js';

// Load official Student Kit if present
const officialKit = loadOfficialStudentKit();

export const isDemoMode = !officialKit.isOfficialPresent;
export const activeDataSource = officialKit.isOfficialPresent
  ? `Official Samsung Student Kit (${officialKit.evidencePath})`
  : "Samsung PRISM Mock/Demo Data (Isolated Phase 1 Baseline)";

export const activeEvidenceCatalog = officialKit.isOfficialPresent
  ? officialKit.evidence
  : demoEvidenceRecords;

export const activeDeeplinkCatalog = officialKit.isOfficialPresent && officialKit.deeplinks.length > 0
  ? officialKit.deeplinks
  : demoDeeplinks;

export const activeCoverageSections = demoCoverageSections;

export function validateCatalogDeeplink(pathOrUri, direction, catalog = activeDeeplinkCatalog) {
  if (officialKit.isOfficialPresent) {
    return validateOfficialCatalogDeeplink(pathOrUri, direction, catalog);
  }
  return validateDemoCatalogDeeplink(pathOrUri, direction, catalog);
}

export function getDataSourceReport() {
  return {
    mode: officialKit.isOfficialPresent ? "student-kit" : "demo",
    isOfficialStudentKit: officialKit.isOfficialPresent,
    siisRecords: officialKit.isOfficialPresent ? officialKit.evidence.length : 0,
    deeplinkRecords: officialKit.isOfficialPresent ? officialKit.deeplinks.length : 0,
    totalEvidenceRecords: activeEvidenceCatalog.length,
    totalDeeplinkRecords: activeDeeplinkCatalog.length,
    sources: officialKit.isOfficialPresent ? [
      { file: officialKit.evidencePath, type: "SIIS Knowledge Base", records: officialKit.evidence.length },
      { file: officialKit.deeplinkPath, type: "Deeplink Catalog", records: officialKit.deeplinks.length }
    ] : [
      { file: "server/data/demo/demoKnowledgeBase.js", type: "Demo Knowledge Base", records: demoEvidenceRecords.length },
      { file: "server/data/demo/demoDeeplinkCatalog.js", type: "Demo Deeplink Catalog", records: demoDeeplinks.length }
    ],
    activeDataSource,
    records: activeEvidenceCatalog.map(e => ({
      id: e.id,
      title: e.title,
      section: e.section,
      supportedActions: (e.supportedActions || []).map(a => `${a.action || a.actionName} [${a.direction}]`),
      provenance: e.metadata?.provenance
    }))
  };
}

