import { validateAgainstSchema, buildOfficialResponsePayload } from '../data/student-kit/schemaValidator.js';

/**
 * ANCHOR Contract Guard Engine
 * Enforces contract rules, schema consistency, grounding proofs, and direction safety.
 * Refuses PASS state if any precondition or validation fails.
 * Deterministic gatekeeper: AI proposes, ANCHOR verifies.
 */
export function validateContract(pipelineResults = {}) {
  const { query, intent, evidence, action, deeplink } = pipelineResults;

  const failureReasons = [];

  // 1. Query & Intent Validation
  const hasQuery = typeof query === 'string' && query.trim().length > 0;
  const hasIntent = Boolean(intent && typeof intent.intent === 'string' && !intent.ambiguous && intent.intent !== 'UNSUPPORTED_INTENT' && intent.intent !== 'EMPTY_QUERY');

  if (!hasQuery) failureReasons.push("Query validation failed: Empty or invalid input query string.");
  if (!hasIntent) failureReasons.push("Intent validation failed: Query is ambiguous or unsupported by Samsung catalog.");

  // 2. Grounding Validation
  const groundingValid = Boolean(
    evidence &&
    evidence.grounded === true &&
    typeof evidence.relevance === 'number' &&
    evidence.relevance >= 50 &&
    evidence.evidenceId &&
    evidence.provenance
  );
  if (!groundingValid) failureReasons.push("Grounding validation failed: Insufficient or ungrounded SIIS evidence (<50% relevance).");

  // 3. Action Support & Explicit Grounding Validation
  const actionValid = Boolean(
    action &&
    action.resolved === true &&
    typeof action.action === 'string' &&
    action.action.length > 0 &&
    action.grounded === true
  );

  const actionExplicitlySupported = Boolean(
    actionValid &&
    action.explicitlySupported === true &&
    action.supportLevel === "EXPLICIT"
  );

  if (!actionValid) {
    failureReasons.push("Action validation failed: Action is unsupported or unresolved from SIIS evidence.");
  } else if (!actionExplicitlySupported) {
    failureReasons.push(`Proposed action '${action.action}' is not explicitly supported by the retrieved Samsung SIIS evidence.`);
  }

  // 3B. Hardware Manual Actions Check
  if (action?.isHardwareManualAction) {
    failureReasons.push("Physical hardware/power troubleshooting required; no actionable software settings deeplink in official Samsung catalog.");
  }

  // 4. Deeplink Validation (Authoritative Samsung Catalog)
  const deeplinkValid = Boolean(
    deeplink &&
    deeplink.verified === true &&
    deeplink.catalogMatch === "VALID" &&
    !action?.isHardwareManualAction &&
    typeof deeplink.deeplink === 'string' &&
    (deeplink.deeplink.startsWith("voiceassist://") || deeplink.deeplink.startsWith("settings://"))
  );
  if (!deeplinkValid && !action?.isHardwareManualAction) {
    failureReasons.push(deeplink?.reason || "Deeplink validation failed: Uncatalogued or unverified Samsung settings path.");
  }

  // 5. Direction Safety Validation (ENABLE vs DISABLE)
  const intentDirectionMatch = Boolean(
    intent &&
    action &&
    intent.targetDirection &&
    intent.targetDirection !== "NONE" &&
    intent.targetDirection !== "INVALID" &&
    intent.targetDirection === action.direction
  );


  const actionDeeplinkDirectionMatch = Boolean(
    action &&
    deeplink &&
    action.direction === deeplink.direction
  );

  const directionValid = Boolean(
    actionValid &&
    deeplinkValid &&
    action.direction &&
    (action.direction === "ENABLE" || action.direction === "DISABLE" || action.direction === "CONFIGURE") &&
    intentDirectionMatch &&
    actionDeeplinkDirectionMatch
  );

  if (!directionValid) {
    if (!intentDirectionMatch) {
      failureReasons.push("Direction does not match the user's request.");
    } else if (!actionDeeplinkDirectionMatch) {
      failureReasons.push(`Direction conflict: Action direction '${action?.direction}' does not match deeplink direction '${deeplink?.direction}'.`);
    } else {
      failureReasons.push("Direction validation failed: Unable to verify directional safety.");
    }
  }

  // 6. Schema Compliance (Official ContextDeeplinkResponse schema.py)
  let schemaValid = false;
  if (hasQuery && hasIntent && groundingValid && actionValid && deeplinkValid && directionValid) {
    const candidatePayload = buildOfficialResponsePayload(
      query,
      intent,
      evidence,
      action,
      deeplink,
      { overallStatus: "PASS" }
    );
    const schemaCheck = validateAgainstSchema(candidatePayload);
    schemaValid = schemaCheck.valid;
    if (!schemaValid) {
      failureReasons.push(`Official schema validation failed: ${schemaCheck.errors.join('; ')}`);
    }
  } else {
    schemaValid = false;
    failureReasons.push("Schema validation failed: Prerequisites not met to build official ContextDeeplinkResponse.");
  }

  const allPass = hasQuery && hasIntent && groundingValid && actionValid && actionExplicitlySupported && deeplinkValid && directionValid && schemaValid;

  return {
    verified: allPass,
    checks: {
      evidence: Boolean(evidence?.grounded),
      relevance: Boolean(evidence?.relevance >= 50),
      actionSupport: actionValid && actionExplicitlySupported,
      actionExplicitlySupported: actionExplicitlySupported,
      direction: directionValid,
      deeplink: deeplinkValid,
      schema: schemaValid
    },
    grounding: groundingValid ? "Validated ✔" : "Failed ✘",
    groundingPassed: groundingValid,
    actionPassed: actionValid && actionExplicitlySupported,
    deeplink: deeplinkValid ? "Validated ✔" : "Failed ✘",
    deeplinkPassed: deeplinkValid,
    direction: directionValid ? "Validated ✔" : "Failed ✘",
    directionPassed: directionValid,
    schema: schemaValid ? "Validated ✔" : "Failed ✘",
    schemaPassed: schemaValid,
    overallStatus: allPass ? "PASS" : "FAIL",
    failureReasons,
    validatedTimestamp: new Date().toISOString()
  };
}


