/**
 * ANCHOR Normalized Data Schema
 * Formats evidence and catalog records to guarantee contract safety and traceability.
 */

export class NormalizedEvidence {
  constructor({
    id,
    source,
    section,
    title,
    content,
    intent,
    entities = [],
    conditions = [],
    supportedActions = [],
    metadata = {}
  }) {
    if (!id || !section || !title) {
      throw new Error(`Invalid Evidence record: missing id, section, or title (${id})`);
    }
    this.id = id;
    this.source = source || "Samsung SIIS";
    this.section = section;
    this.title = title;
    this.content = content || "";
    this.intent = intent || "UNKNOWN_INTENT";
    this.entities = Array.isArray(entities) ? entities : [entities];
    this.conditions = Array.isArray(conditions) ? conditions : [conditions];
    this.supportedActions = Array.isArray(supportedActions) ? supportedActions : [];
    this.metadata = {
      provenance: metadata.provenance || "UNSPECIFIED",
      isOfficialStudentKit: Boolean(metadata.isOfficialStudentKit),
      sourceFile: metadata.sourceFile || "unknown",
      version: metadata.version || "1.0.0",
      ...metadata
    };
  }

  supportsAction(actionName, direction) {
    return this.supportedActions.some(sa => {
      const nameMatch = sa.action.toLowerCase() === (actionName || '').toLowerCase();
      const dirMatch = !direction || sa.direction === direction;
      return nameMatch && dirMatch;
    });
  }

  getActionForDirection(direction) {
    return this.supportedActions.find(sa => sa.direction === direction) || null;
  }
}

export class NormalizedDeeplink {
  constructor({
    id,
    path,
    deeplink,
    title,
    message,
    description,
    qnaDescription,
    originalType,
    direction,
    validation,
    allowedDirections = ["ENABLE", "DISABLE"],
    category = "General",
    verified = true,
    metadata = {}
  }) {
    const actualUri = deeplink || path;
    const actualTitle = title || message || description;
    if (!actualUri || !actualTitle) {
      throw new Error(`Invalid Deeplink record: missing uri/path or title/message (${actualUri})`);
    }
    this.id = id || "DL-AUTO";
    this.path = actualUri;
    this.deeplink = actualUri;
    this.title = actualTitle;
    this.message = message || actualTitle;
    this.description = description || actualTitle;
    this.qnaDescription = qnaDescription || "";
    this.originalType = originalType || null;
    this.direction = direction || "NEUTRAL";
    this.validation = validation || null;
    this.allowedDirections = Array.isArray(allowedDirections) ? allowedDirections : [allowedDirections];
    this.category = category;
    this.verified = Boolean(verified);
    this.metadata = {
      provenance: metadata.provenance || "UNSPECIFIED",
      isOfficialStudentKit: Boolean(metadata.isOfficialStudentKit),
      ...metadata
    };
  }

  supportsDirection(dir) {
    if (!dir) return false;
    const upper = dir.toUpperCase();
    return this.allowedDirections.includes(upper) || this.direction === upper;
  }
}
