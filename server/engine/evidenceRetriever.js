import { activeEvidenceCatalog } from '../data/index.js';

/**
 * Authoritative Evidence Retrieval Engine for Samsung SIIS dataset.
 * Scores candidates against normalized evidence records, avoiding hallucination and explaining matches.
 */
export function retrieveEvidence(query = "", intentResult = {}, evidenceCatalog = activeEvidenceCatalog) {
  const normalizedQuery = (query || "").toLowerCase();
  const queryTokens = normalizedQuery.split(/\W+/).filter(t => t.length > 2);

  if (intentResult.ambiguous || !queryTokens.length || !evidenceCatalog.length) {
    return {
      evidenceId: null,
      source: "Samsung SIIS",
      section: "None",
      relevance: 0,
      grounded: false,
      excerpt: "No grounded evidence found in Samsung SIIS catalog for the requested query.",
      candidates: [],
      matchReason: "Query is ambiguous or has no entity matches in Samsung catalog.",
      matchedEntry: null,
      provenance: null
    };
  }

  // Score each candidate record
  const scoredCandidates = evidenceCatalog.map(record => {
    let score = 0;
    const matchReasons = [];

    // 1. Intent match (+35)
    if (record.intent && record.intent === intentResult.intent) {
      score += 35;
      matchReasons.push(`Exact intent alignment with '${record.intent}'`);
    }

    // 2. Original query similarity match (+30)
    const origQuery = (record.metadata?.originalQuery || "").toLowerCase();
    if (origQuery && normalizedQuery) {
      let commonTokens = 0;
      for (const t of queryTokens) {
        if (origQuery.includes(t)) commonTokens++;
      }
      if (commonTokens >= 2) {
        const bonus = Math.min(commonTokens * 8, 30);
        score += bonus;
        matchReasons.push(`Strong query similarity with official Student Kit query (${commonTokens} terms)`);
      }
    }

    // 3. Title match (+25)
    const titleLower = (record.title || "").toLowerCase();
    let titleMatches = 0;
    for (const t of queryTokens) {
      if (titleLower.includes(t)) titleMatches++;
    }
    if (titleMatches > 0) {
      const titleBonus = Math.min(titleMatches * 10, 25);
      score += titleBonus;
      matchReasons.push(`Title match in SIIS catalog (${titleMatches} terms)`);
    }

    // 4. Entity overlap (+10 per token match, max 20)
    let entityMatches = 0;
    const entities = record.entities || [];
    for (const entity of entities) {
      if (normalizedQuery.includes(entity.toLowerCase())) {
        entityMatches++;
      }
    }
    if (entityMatches > 0) {
      const entityBonus = Math.min(entityMatches * 5, 20);
      score += entityBonus;
      matchReasons.push(`Matched ${entityMatches} keyword entities in evidence catalog`);
    }

    // 5. Directional support (+10 if record has actions for the requested direction)
    const hasDirectionAction = (record.supportedActions || []).some(sa => sa.direction === intentResult.targetDirection);
    if (hasDirectionAction) {
      score += 10;
      matchReasons.push(`Contains verified action for direction '${intentResult.targetDirection}'`);
    }

    return {
      record,
      score: Math.min(score, 98),
      matchReasons
    };
  });

  // Filter and sort candidates
  scoredCandidates.sort((a, b) => b.score - a.score);

  const bestCandidate = scoredCandidates[0];
  const RELEVANCE_THRESHOLD = 50;

  if (!bestCandidate || bestCandidate.score < RELEVANCE_THRESHOLD) {
    return {
      evidenceId: null,
      source: "Samsung SIIS",
      section: "Unresolved",
      relevance: bestCandidate ? bestCandidate.score : 0,
      grounded: false,
      excerpt: "Evidence below minimum relevance threshold (50%). Refusing to hallucinate troubleshooting action.",
      candidates: scoredCandidates.slice(0, 3).map(c => ({ id: c.record.id, title: c.record.title, score: c.score })),
      matchReason: "No sufficiently grounded evidence meets the 50% relevance threshold.",
      matchedEntry: null,
      provenance: null
    };
  }

  const matched = bestCandidate.record;

  return {
    evidenceId: matched.id,
    source: matched.source,
    section: matched.section,
    title: matched.title,
    relevance: bestCandidate.score,
    grounded: true,
    excerpt: matched.content,
    candidates: scoredCandidates.slice(0, 3).map(c => ({
      id: c.record.id,
      title: c.record.title,
      section: c.record.section,
      score: c.score,
      reasons: c.matchReasons
    })),
    matchReason: bestCandidate.matchReasons.join("; "),
    matchedEntry: matched,
    provenance: matched.metadata?.provenance || "Samsung Student Kit (siis_responses.json)"
  };
}

