import { execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Validates and formats pipeline responses against the official Samsung Theme 2 schema.py.
 * Ensures ContextDeeplinkResponse model compliance without creating competing schemas.
 */
export function buildOfficialResponsePayload(query, intent, evidence, action, deeplink, validation) {
  // If pipeline validation failed or no action resolved, return empty/rejected contexts
  if (!action || !action.resolved || validation?.overallStatus !== 'PASS') {
    return {
      query: query || "",
      response: {
        contexts: []
      }
    };
  }

  // Construct StepGroup
  const steps = [
    `Navigate to Settings on your device.`,
    evidence?.title ? `Review ${evidence.title} guidance.` : `Locate the relevant feature settings.`,
    `Apply ${action.action} to resolve the issue.`
  ];

  let actionableDeeplink = null;
  if (deeplink && deeplink.verified && deeplink.deeplink) {
    actionableDeeplink = {
      deeplink: deeplink.deeplink,
      description: deeplink.description || `${action.action} via device Settings`,
      message: deeplink.message || action.action,
      originalType: deeplink.originalType || "onClickURL"
    };
  }

  let validationDeeplink = null;
  if (deeplink?.validation && deeplink.validation.deeplink) {
    validationDeeplink = {
      deeplink: deeplink.validation.deeplink,
      key: deeplink.validation.key || action.action,
      resultType: deeplink.validation.resultType || "boolean",
      condition: deeplink.validation.condition || "equal",
      value: deeplink.validation.value || "True"
    };
  }

  const stepGroup = {
    steps: steps,
    actionableDeeplink: actionableDeeplink,
    validationDeeplink: validationDeeplink
  };

  const actionPayload = {
    actionName: action.action,
    description: action.proof || `Troubleshooting action supported by SIIS evidence`,
    stepGroups: [stepGroup],
    category: actionableDeeplink ? "auto" : "manual"
  };

  const goalPayload = {
    goal: `Follow these steps to perform ${action.action}`,
    title: evidence?.title || "Device Troubleshooting",
    actions: [actionPayload],
    score: Number(((evidence?.relevance || 92) / 100).toFixed(2))
  };

  return {
    query: query,
    response: {
      contexts: [goalPayload]
    }
  };
}

/**
 * Validates a response object against schema.py rules.
 * Returns { valid: boolean, errors: string[] }.
 */
export function validateAgainstSchema(payload) {
  const errors = [];

  if (!payload || typeof payload !== 'object') {
    return { valid: false, errors: ["Payload must be a non-null object."] };
  }

  if (typeof payload.query !== 'string') {
    errors.push("Missing or invalid 'query' (must be string).");
  }

  if (!payload.response || typeof payload.response !== 'object') {
    errors.push("Missing or invalid 'response' object.");
    return { valid: false, errors };
  }

  if (!Array.isArray(payload.response.contexts)) {
    errors.push("Missing or invalid 'response.contexts' (must be an array).");
    return { valid: false, errors };
  }

  // Validate each Goal in contexts
  payload.response.contexts.forEach((goal, gIdx) => {
    if (typeof goal.goal !== 'string' || !goal.goal.trim()) {
      errors.push(`Context[${gIdx}]: 'goal' must be a non-empty string.`);
    }
    if (typeof goal.title !== 'string' || !goal.title.trim()) {
      errors.push(`Context[${gIdx}]: 'title' must be a non-empty string.`);
    }
    if (typeof goal.score !== 'number' || isNaN(goal.score)) {
      errors.push(`Context[${gIdx}]: 'score' must be a valid float number.`);
    }
    if (!Array.isArray(goal.actions)) {
      errors.push(`Context[${gIdx}]: 'actions' must be an array.`);
      return;
    }

    // Validate each Action
    goal.actions.forEach((act, aIdx) => {
      if (typeof act.actionName !== 'string' || !act.actionName.trim()) {
        errors.push(`Context[${gIdx}].Action[${aIdx}]: 'actionName' must be a non-empty string.`);
      }
      if (typeof act.description !== 'string') {
        errors.push(`Context[${gIdx}].Action[${aIdx}]: 'description' must be a string.`);
      }
      if (act.category && !["auto", "manual", "critical"].includes(act.category)) {
        errors.push(`Context[${gIdx}].Action[${aIdx}]: 'category' must be auto, manual, or critical.`);
      }
      if (!Array.isArray(act.stepGroups)) {
        errors.push(`Context[${gIdx}].Action[${aIdx}]: 'stepGroups' must be an array.`);
        return;
      }

      // Validate each StepGroup
      act.stepGroups.forEach((sg, sIdx) => {
        if (!Array.isArray(sg.steps) || !sg.steps.every(s => typeof s === 'string')) {
          errors.push(`Context[${gIdx}].Action[${aIdx}].StepGroup[${sIdx}]: 'steps' must be array of strings.`);
        }

        if (sg.actionableDeeplink) {
          if (typeof sg.actionableDeeplink.deeplink !== 'string') {
            errors.push(`StepGroup[${sIdx}].actionableDeeplink: 'deeplink' must be a string.`);
          }
          if (typeof sg.actionableDeeplink.description !== 'string') {
            errors.push(`StepGroup[${sIdx}].actionableDeeplink: 'description' must be a string.`);
          }
        }

        if (sg.validationDeeplink) {
          if (typeof sg.validationDeeplink.deeplink !== 'string') {
            errors.push(`StepGroup[${sIdx}].validationDeeplink: 'deeplink' must be a string.`);
          }
          if (typeof sg.validationDeeplink.key !== 'string') {
            errors.push(`StepGroup[${sIdx}].validationDeeplink: 'key' must be a string.`);
          }
          if (sg.validationDeeplink.condition && !["greater", "equal", "less"].includes(sg.validationDeeplink.condition)) {
            errors.push(`StepGroup[${sIdx}].validationDeeplink: 'condition' must be greater, equal, or less.`);
          }
          if (sg.validationDeeplink.resultType && !["boolean", "integer", "str", "float"].includes(sg.validationDeeplink.resultType)) {
            errors.push(`StepGroup[${sIdx}].validationDeeplink: 'resultType' must be boolean, integer, str, or float.`);
          }
        }
      });
    });
  });

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Validates payload directly using Python Pydantic schema.py if python is available.
 */
export function validateWithPythonPydantic(payload) {
  try {
    if (!payload || !payload.response) return false;
    const jsonBase64 = Buffer.from(JSON.stringify(payload.response), 'utf-8').toString('base64');
    const cmd = `python -c "import json, sys, base64; sys.path.append('${__dirname.replace(/\\/g, '/')}'); from schema import ContextDeeplinkResponse; data = json.loads(base64.b64decode('${jsonBase64}').decode('utf-8')); ContextDeeplinkResponse.model_validate(data); print('OK')"`;
    const output = execSync(cmd, { timeout: 4000 }).toString();
    return output.trim() === 'OK';
  } catch (err) {
    return false;
  }
}

