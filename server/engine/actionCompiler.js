/**
 * Action Compiler
 * Synthesizes grounded actions from retrieved SIIS evidence.
 * Supports the AI PROPOSAL pattern where ANCHOR independently verifies directional compatibility.
 */

export function compileAction(evidenceResult = {}, intentResult = {}) {
  // If no grounded evidence is retrieved, action cannot be compiled
  if (!evidenceResult || !evidenceResult.grounded || !evidenceResult.matchedEntry) {
    return {
      action: null,
      aiProposedAction: null,
      sourceEvidence: null,
      evidenceId: null,
      grounded: false,
      confidence: 0,
      direction: null,
      condition: null,
      proof: "Action compilation rejected: No grounded SIIS evidence available.",
      resolved: false,
      relatedIssues: []
    };
  }

  const record = evidenceResult.matchedEntry;
  const requestedDirection = intentResult.targetDirection || "ENABLE";

  // Look for action supporting the requested direction
  const supportedAction = record.getActionForDirection ? record.getActionForDirection(requestedDirection) : (record.supportedActions || []).find(a => a.direction === requestedDirection);

  if (supportedAction) {
    const matchedCondition = (record.conditions || []).find(c => c.direction === requestedDirection) || record.conditions?.[0];
    const conditionStatement = typeof matchedCondition === 'string' ? matchedCondition : matchedCondition?.statement;

    return {
      action: supportedAction.action || supportedAction.actionName,
      aiProposedAction: supportedAction.action || supportedAction.actionName,
      sourceEvidence: record.id.replace("#", ""),
      evidenceId: record.id,
      grounded: true,
      confidence: Math.round(evidenceResult.relevance * 0.96),
      direction: requestedDirection,
      condition: conditionStatement || `Setting state requirement for ${requestedDirection}`,
      proof: supportedAction.proof || `Derived from ${record.id} section ${record.section}`,
      resolved: true,
      explicitlySupported: supportedAction.explicitlySupported ?? true,
      supportLevel: supportedAction.supportLevel || "EXPLICIT",
      isHardwareManualAction: Boolean(supportedAction.isHardwareManualAction),
      deeplinkPath: supportedAction.deeplink || null,
      relatedIssues: record.metadata?.relatedIssues || [
        "Orientation Lock", "Auto Rotate", "Motion Sensor"
      ]
    };
  }

  // If record does not support requested direction, AI proposes available action from evidence,
  // allowing Contract Guard to deterministically flag the direction mismatch.
  const aiProposal = record.supportedActions?.[0];
  if (aiProposal) {
    return {
      action: aiProposal.action || aiProposal.actionName,
      aiProposedAction: aiProposal.action || aiProposal.actionName,
      sourceEvidence: record.id.replace("#", ""),
      evidenceId: record.id,
      grounded: true,
      confidence: Math.round(evidenceResult.relevance * 0.75),
      direction: aiProposal.direction || "ENABLE",
      condition: `Evidence supports ${aiProposal.direction} only`,
      proof: aiProposal.proof || `Proposed from ${record.id} (direction: ${aiProposal.direction})`,
      resolved: true,
      explicitlySupported: false,
      supportLevel: "UNSUPPORTED",
      isHardwareManualAction: Boolean(aiProposal.isHardwareManualAction),
      deeplinkPath: aiProposal.deeplink || null,
      relatedIssues: record.metadata?.relatedIssues || []
    };
  }

  return {
    action: null,
    aiProposedAction: null,
    sourceEvidence: record.id,
    evidenceId: record.id,
    grounded: false,
    confidence: 0,
    direction: requestedDirection,
    condition: null,
    proof: `Action compilation rejected: Evidence ${record.id} has no actionable steps.`,
    resolved: false,
    explicitlySupported: false,
    supportLevel: "UNSUPPORTED",
    isHardwareManualAction: false,
    relatedIssues: []
  };
}


