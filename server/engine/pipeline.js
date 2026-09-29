import { parseIntent } from './intentParser.js';
import { retrieveEvidence } from './evidenceRetriever.js';
import { compileAction } from './actionCompiler.js';
import { resolveDeeplink } from './deeplinkResolver.js';
import { validateContract } from './contractGuard.js';
import { buildEvidenceGraph } from './graphBuilder.js';
import { buildOfficialResponsePayload } from '../data/student-kit/schemaValidator.js';
import { activeCoverageSections, isDemoMode, activeDataSource } from '../data/index.js';

export function executeTroubleshootingPipeline(query = "My screen isn't rotating automatically.") {
  const startTime = performance.now();

  // Stage 1: Intent & State Understanding
  const tIntentStart = performance.now();
  const intent = parseIntent(query);
  const intentLatency = Number((performance.now() - tIntentStart).toFixed(2));

  // Stage 2: SIIS Evidence Retrieval
  const tEvidenceStart = performance.now();
  const evidence = retrieveEvidence(query, intent);
  const evidenceLatency = Number((performance.now() - tEvidenceStart).toFixed(2));

  // Stage 3: Grounded Action Compilation
  const tActionStart = performance.now();
  const action = compileAction(evidence, intent);
  const actionLatency = Number((performance.now() - tActionStart).toFixed(2));

  // Stage 4: Samsung Deeplink Resolution
  const tDeeplinkStart = performance.now();
  const deeplink = resolveDeeplink(action, evidence);
  const deeplinkLatency = Number((performance.now() - tDeeplinkStart).toFixed(2));

  // Stage 5: Contract Guard Validation
  const tValidationStart = performance.now();
  const validation = validateContract({ query, intent, evidence, action, deeplink });
  const validationLatency = Number((performance.now() - tValidationStart).toFixed(2));

  // Stage 6: Build Authoritative ContextDeeplinkResponse Payload (schema.py compliant)
  const officialResponsePayload = buildOfficialResponsePayload(
    query,
    intent,
    evidence,
    action,
    deeplink,
    validation
  );

  // Stage 7: Evidence Graph Construction
  const graph = buildEvidenceGraph(query, intent, evidence, action, deeplink, validation);

  const totalLatency = Number((performance.now() - startTime).toFixed(2));

  const pipelineStages = [
    { name: "Query Processed", completed: Boolean(query && query.trim().length > 0) },
    { name: "Intent Identified", completed: Boolean(!intent.ambiguous) },
    { name: "Evidence Retrieved", completed: Boolean(evidence.grounded === true) },
    { name: "Action Resolved", completed: Boolean(action.resolved === true) },
    { name: "Contract Validated", completed: Boolean(validation.overallStatus === "PASS") }
  ];

  const metrics = {
    totalExecutionTime: `${totalLatency} ms`,
    totalLatency: `${totalLatency} ms`,
    queryAnalysis: `${intentLatency} ms`,
    evidenceRetrieval: `${evidenceLatency} ms`,
    actionResolution: `${actionLatency} ms`,
    validation: `${validationLatency} ms`,
    deeplinkResolution: `${deeplinkLatency} ms`
  };

  return {
    query,
    intent,
    evidence,
    action,
    deeplink,
    validation,
    response: officialResponsePayload.response, // ContextDeeplinkResponse object matching sample_output.json
    officialResponse: officialResponsePayload,
    graph,
    pipelineStages,
    metrics,
    provenance: {
      isOfficialStudentKit: !isDemoMode,
      isDemoMode,
      activeDataSource,
      evidenceProvenance: evidence.provenance,
      deeplinkProvenance: deeplink.provenance,
      schemaSource: "schema.py (Theme 2 Official Pydantic Model)"
    }
  };
}

