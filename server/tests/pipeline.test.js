import { executeTroubleshootingPipeline } from '../engine/pipeline.js';
import { parseIntent } from '../engine/intentParser.js';
import { retrieveEvidence } from '../engine/evidenceRetriever.js';
import { compileAction } from '../engine/actionCompiler.js';
import { resolveDeeplink } from '../engine/deeplinkResolver.js';
import { validateContract } from '../engine/contractGuard.js';
import { activeEvidenceCatalog, activeDeeplinkCatalog, validateCatalogDeeplink } from '../data/index.js';
import { validateAgainstSchema, validateWithPythonPydantic, buildOfficialResponsePayload } from '../data/student-kit/schemaValidator.js';

let passedTests = 0;
let failedTests = 0;

function assert(condition, message) {
  if (!condition) {
    console.error(`  ❌ FAILED: ${message}`);
    failedTests++;
    throw new Error(message);
  } else {
    console.log(`  ✔ PASSED: ${message}`);
    passedTests++;
  }
}

console.log("============================================================");
console.log("ANCHOR AUTOMATED TEST SUITE: 15 STUDENT KIT TEST SCENARIOS");
console.log("============================================================\n");

// 1. Valid SIIS Retrieval
console.log("1. Valid SIIS Retrieval (Official row_20 / row_21)");
{
  const evidence = retrieveEvidence("Screen does not rotate on smartphone or tablet", { intent: "SCREEN_ROTATION", targetDirection: "ENABLE", ambiguous: false });
  assert(evidence.grounded === true, "Evidence grounded flag is true");
  assert(evidence.evidenceId === "#SIIS-ROW_20", `Retrieved official record #SIIS-ROW_20 (got ${evidence.evidenceId})`);
  assert(evidence.relevance >= 80, `Relevance is high (${evidence.relevance}%)`);
  assert(evidence.provenance.includes("Samsung Student Kit"), "Provenance confirms official Student Kit source");
}

// 2. Missing SIIS Evidence
console.log("\n2. Missing SIIS Evidence");
{
  const evidence = retrieveEvidence("Quantum teleportation time warp", { intent: "TELEPORTATION", ambiguous: false });
  assert(evidence.grounded === false, "Missing evidence returns grounded === false");
  assert(evidence.evidenceId === null, "evidenceId is null");
  assert(evidence.relevance < 50, "Relevance is below 50% threshold");
}

// 3. Irrelevant SIIS Evidence
console.log("\n3. Irrelevant SIIS Evidence");
{
  const evidence = retrieveEvidence("The weather in Honolulu is warm and tropical today", { intent: "UNSUPPORTED_INTENT", ambiguous: true });
  assert(evidence.grounded === false, "Irrelevant evidence is not grounded");
  assert(evidence.relevance < 50, "Relevance is below threshold");
}

// 4. Supported Action
console.log("\n4. Supported Action (Official SIIS Grounded)");
{
  const evidence = retrieveEvidence("Screen does not rotate on smartphone or tablet", { intent: "SCREEN_ROTATION", targetDirection: "ENABLE", ambiguous: false });
  const actionRes = compileAction(evidence, { intent: "SCREEN_ROTATION", targetDirection: "ENABLE" });
  assert(actionRes.resolved === true, "Action resolved successfully");
  assert(actionRes.action === "Enable Auto Rotate", "Action compiled is 'Enable Auto Rotate'");
  assert(actionRes.grounded === true, "Action is marked as grounded");
  assert(actionRes.explicitlySupported === true, "Action is marked explicitlySupported === true");
}

// 5. Unsupported Action & Ungrounded AI Proposal (Regression Cases B & H)
console.log("\n5. Unsupported Action & Ungrounded AI Proposal (Regression Cases B & H)");
{
  const res = executeTroubleshootingPipeline("Overclock CPU to 10GHz liquid nitrogen");
  assert(res.validation.overallStatus === "FAIL", "Contract Guard refused PASS for unsupported action");
  assert(res.validation.checks.actionSupport === false || res.action.resolved === false, "Action was identified as unsupported");

  // Specific check: Correct evidence + Unsupported AI action proposal
  const mockEvidence = {
    id: "#SIIS-ROW_20",
    source: "Samsung Student Kit",
    grounded: true,
    relevance: 95,
    evidenceId: "#SIIS-ROW_20",
    provenance: "Samsung Student Kit",
    supportedActions: [{ action: "Enable Auto Rotate", direction: "ENABLE" }]
  };
  const mockAiAction = {
    action: "Factory Reset All Partition Sectors",
    resolved: true,
    grounded: true,
    direction: "ENABLE",
    explicitlySupported: false, // Ungrounded AI inference
    supportLevel: "UNSUPPORTED"
  };
  const val = validateContract({
    query: "My screen is not rotating",
    intent: { intent: "SCREEN_ROTATION", targetDirection: "ENABLE", ambiguous: false },
    evidence: mockEvidence,
    action: mockAiAction,
    deeplink: { verified: true, catalogMatch: "VALID", deeplink: "voiceassist://masked/act/7c340914be", direction: "ENABLE" }
  });
  assert(val.overallStatus === "FAIL", "Contract Guard blocked ungrounded AI action proposal");
  assert(val.checks.actionExplicitlySupported === false, "Contract Guard checked actionExplicitlySupported === false");
  assert(val.failureReasons.some(r => r.includes("not explicitly supported")), "Failure reason cites lack of explicit SIIS support");
}

// 6. ENABLE Direction Handling
console.log("\n6. ENABLE Direction Handling");
{

  const res = executeTroubleshootingPipeline("My screen isn't rotating automatically.");
  assert(res.intent.targetDirection === "ENABLE", "Intent extracted ENABLE direction");
  assert(res.action.direction === "ENABLE", "Action direction is ENABLE");
  assert(res.deeplink.direction === "ENABLE", "Deeplink direction is ENABLE");
  assert(res.validation.directionPassed === true, "Direction check passed");
  assert(res.validation.overallStatus === "PASS", "Contract awarded PASS");
}

// 7. DISABLE Direction Handling
console.log("\n7. DISABLE Direction Handling (Touch Sensitivity Turn Off)");
{
  const res = executeTroubleshootingPipeline("Touch sensitivity isn't working. Turn it off.");
  assert(res.intent.targetDirection === "DISABLE", "Intent extracted DISABLE direction");
  assert(res.action.direction === "DISABLE", "Action direction is DISABLE");
  assert(res.action.action === "Disable Touch Sensitivity", "Action compiled is 'Disable Touch Sensitivity'");
  assert(res.deeplink.direction === "DISABLE", "Deeplink direction is DISABLE");
  assert(res.validation.directionPassed === true, "Direction check passed");
  assert(res.validation.overallStatus === "PASS", "Contract awarded PASS");
}

// 8. Direction Mismatch Rejection
console.log("\n8. Direction Mismatch Rejection");
{
  const val = validateContract({
    query: "Test direction conflict",
    intent: { intent: "SCREEN_ROTATION", targetDirection: "DISABLE", ambiguous: false },
    evidence: { grounded: true, relevance: 92, evidenceId: "#SIIS-ROW_20", provenance: "Samsung Student Kit" },
    action: { resolved: true, action: "Enable Auto Rotate", grounded: true, direction: "ENABLE" },
    deeplink: { verified: true, catalogMatch: "VALID", deeplink: "voiceassist://masked/act/7c340914be", direction: "ENABLE" }
  });
  assert(val.directionPassed === false, "Contract Guard flagged direction mismatch");
  assert(val.overallStatus === "FAIL", "Contract Guard refused PASS for direction conflict");
  assert(val.failureReasons.some(r => r.includes("Direction")), "Failure reasons contain direction explanation");
}

// 9. Valid Official Catalog Deeplink
console.log("\n9. Valid Official Catalog Deeplink");
{
  const check = validateCatalogDeeplink("voiceassist://masked/act/7c340914be", "ENABLE");
  assert(check.valid === true, "Official masked URI voiceassist://masked/act/7c340914be is valid in catalog");
  assert(check.catalogEntry.metadata.isOfficialStudentKit === true, "Catalog entry verified as official Student Kit");
}

// 10. Missing Deeplink
console.log("\n10. Missing Deeplink Rejection");
{
  const dlRes = resolveDeeplink({ action: "Unmapped Hardware Step", resolved: true, direction: "ENABLE" }, {});
  assert(dlRes.verified === false, "Unmapped action returns unverified deeplink");
  assert(dlRes.catalogMatch === "INVALID", "Catalog match is INVALID");
}

// 11. Wrong / Uncatalogued Deeplink Rejection
console.log("\n11. Wrong / Uncatalogued Deeplink Rejection");
{
  const check = validateCatalogDeeplink("settings://hallucinated/deep/link", "ENABLE");
  assert(check.valid === false, "Hallucinated URI correctly rejected as uncatalogued");
  assert(check.reason.includes("not in Samsung Student Kit") || check.reason.includes("not found"), "Rejection reason clearly explained");
}

// 12. Schema Validation (Official Pydantic schema.py)
console.log("\n12. Schema Validation (Pydantic schema.py)");
{
  const res = executeTroubleshootingPipeline("My screen isn't rotating automatically.");
  assert(res.officialResponse !== null, "Official response payload constructed");
  
  // Validate with JS schema validator
  const schemaCheck = validateAgainstSchema(res.officialResponse);
  assert(schemaCheck.valid === true, "Response satisfies ContextDeeplinkResponse schema rules");

  // Validate directly with Python Pydantic ContextDeeplinkResponse model
  const pythonValid = validateWithPythonPydantic(res.officialResponse);
  assert(pythonValid === true, "Payload validated by Python Pydantic ContextDeeplinkResponse.model_validate!");
}

// 13. Ambiguous Query Handling
console.log("\n13. Ambiguous Query Handling");
{
  const res = executeTroubleshootingPipeline("hello phone");
  assert(res.intent.ambiguous === true, "Query correctly flagged as ambiguous");
  assert(res.validation.overallStatus === "FAIL", "Ambiguous query is not granted PASS");
  assert(res.validation.failureReasons.some(r => r.includes("ambiguous")), "Failure reason specifies ambiguity");
}

// 14. Complete Successful Pipeline (Official Theme 2 Round-trip)
console.log("\n14. Complete Successful Pipeline (Official Theme 2 Round-trip)");
{
  const res = executeTroubleshootingPipeline("My screen isn't rotating automatically.");
  assert(Boolean(res.query), "Query present");
  assert(Boolean(res.intent && res.intent.intent), "Intent identified");
  assert(res.evidence.grounded === true, "Evidence grounded");
  assert(res.action.resolved === true, "Action resolved");
  assert(res.deeplink.verified === true, "Deeplink verified in official catalog");
  assert(res.deeplink.deeplink.startsWith("voiceassist://"), "Deeplink uses official masked URI");
  assert(res.validation.overallStatus === "PASS", "Contract Guard status is PASS");
  assert(res.response.contexts.length > 0, "Response contexts array contains Goal");
  assert(res.provenance.isOfficialStudentKit === true, "Provenance confirms official Student Kit");
}

// 15. Complete Rejected Pipeline
console.log("\n15. Complete Rejected Pipeline (Safe Rejection)");
{
  const res = executeTroubleshootingPipeline("Make my screen project a 3D hologram in midair");
  assert(res.validation.overallStatus === "FAIL", "Overall status is FAIL");
  assert(res.validation.verified === false, "Contract Guard verified is false");
  assert(res.response.contexts.length === 0, "Response contexts array is empty (no hallucinations)");
  assert(res.validation.failureReasons.length > 0, "Failure reasons populated");
}

console.log("\n============================================================");
console.log(`TEST SUMMARY: ${passedTests} passed, ${failedTests} failed.`);
console.log("============================================================\n");

if (failedTests > 0) {
  process.exit(1);
} else {
  console.log("ALL 15 SAMSUNG STUDENT KIT TEST SCENARIOS PASSED!");
}

