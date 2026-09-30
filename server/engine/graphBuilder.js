/**
 * Dynamic Evidence Graph Compiler
 * Compiles graph nodes and active reasoning paths directly from verified pipeline outcomes.
 */

export function buildEvidenceGraph(query, intent, evidence, action, deeplink, validation) {
  const isActionResolved = Boolean(action && action.resolved && action.action);
  const isDeeplinkResolved = Boolean(deeplink && deeplink.verified);
  const isValidationPass = Boolean(validation && validation.overallStatus === "PASS");

  const isDirectionPass = Boolean(validation?.directionPassed);
  const isRejected = !isValidationPass;

  const nodes = [
    {
      id: "node-complaint",
      type: "evidence",
      title: "User Complaint",
      subtitle: `"${query}"`,
      icon: "chat",
      x: 520,
      y: 75,
      status: "active"
    },
    {
      id: "node-device",
      type: "evidence",
      title: "Device Context",
      subtitle: `${intent?.deviceType || 'Galaxy S23'}\n${intent?.osVersion || 'One UI 6.x'}`,
      icon: "device",
      x: 385,
      y: 195,
      status: "active"
    },
    {
      id: "node-intent",
      type: "evidence",
      title: "Intent",
      subtitle: `${intent?.intent || 'SCREEN_ROTATION'}\n${intent?.ambiguous ? '✕ Ambiguous' : '✓ Identified'}`,
      icon: "intent",
      x: 525,
      y: 170,
      status: intent?.ambiguous ? "warning" : "active"
    },
    {
      id: "node-related",
      type: "evidence",
      title: "Related Issues",
      subtitle: (action?.relatedIssues && action.relatedIssues.length > 0)
        ? action.relatedIssues.join("\n")
        : "• Orientation Lock\n• Auto Rotate\n• Motion Sensor",
      icon: "related",
      x: 675,
      y: 210,
      status: "active"
    },
    {
      id: "node-evidence",
      type: "evidence",
      title: "SIIS Evidence",
      subtitle: evidence?.evidenceId
        ? `${evidence.evidenceId}\n${evidence.section}`
        : "No Grounded Evidence\n(Unresolved)",
      icon: "document",
      x: 525,
      y: 280,
      status: evidence?.grounded ? "active" : "failed"
    },
    {
      id: "node-action",
      type: "action",
      title: "AI Proposed Action",
      subtitle: (action?.aiProposedAction || action?.action)
        ? `${action.aiProposedAction || action.action}\n${isValidationPass ? '✓ Verified Proposal' : '○ AI Proposal'}`
        : "Action Unsupported\n(Unresolved)",
      icon: "lightning",
      x: 635,
      y: 385,
      status: isActionResolved ? "active" : "failed"
    },
    {
      id: "node-condition",
      type: isValidationPass ? "action" : (isRejected ? "rejected" : "evidence"),
      title: "ANCHOR Verification",
      subtitle: isValidationPass
        ? "Direction • Grounding\n✓ Verified"
        : (isRejected
            ? (validation?.failureReasons?.[0] ? `Direction Mismatch\n✕ ${validation.failureReasons[0]}` : "Verification Failed\n✕ Rejected")
            : (action?.condition || "State Undetermined\n(Unresolved)")),
      icon: "gear",
      x: 415,
      y: 390,
      status: isValidationPass ? "active" : "failed"
    },
    {
      id: "node-deeplink",
      type: "evidence",
      title: "Samsung Deeplink",
      subtitle: isDeeplinkResolved ? deeplink.deeplink : "No Valid Settings URI",
      icon: "link",
      x: 530,
      y: 485,
      status: isDeeplinkResolved ? "active" : "failed"
    },
    {
      id: "node-validation",
      type: isValidationPass ? "validation" : "rejected",
      title: isValidationPass ? "Validated Response" : "Rejection Terminal",
      subtitle: isValidationPass ? "Grounded • Verified • Ready" : (validation?.failureReasons?.[0] || "Action Blocked (✕ REJECTED)"),
      icon: "shield",
      x: 472,
      y: 570,
      status: isValidationPass ? "active" : "failed"
    }
  ];

  // Dynamic edges highlighting the verified path vs rejected termination
  const edges = [
    { from: "node-complaint", to: "node-device", active: true, curvature: -0.22, dur: '3.4s' },
    { from: "node-complaint", to: "node-intent", active: !intent?.ambiguous, curvature: 0, dur: '2.5s' },
    { from: "node-intent", to: "node-related", active: true, curvature: 0.18, dur: '3.2s' },
    { from: "node-intent", to: "node-evidence", active: evidence?.grounded === true, curvature: 0, dur: '2.4s' },
    { from: "node-device", to: "node-condition", active: false, curvature: -0.18, dur: '3.6s' },
    { from: "node-evidence", to: "node-action", active: isActionResolved, curvature: 0.22, dur: '2.8s' },
    { from: "node-action", to: "node-condition", active: isActionResolved, curvature: 0.08, isGreen: isValidationPass, isRed: isRejected, dur: '3.2s' },
    { from: "node-evidence", to: "node-condition", active: evidence?.grounded === true, curvature: -0.22, dur: '2.8s' },
    { from: "node-condition", to: "node-deeplink", active: isValidationPass, curvature: -0.18, dur: '2.6s' },
    { from: "node-action", to: "node-deeplink", active: isValidationPass, curvature: 0.18, isGreen: true, dur: '2.6s' },
    { from: "node-deeplink", to: "node-validation", active: isValidationPass, curvature: -0.12, isPurple: true, dur: '2.5s' }
  ];

  return { nodes, edges };
}
