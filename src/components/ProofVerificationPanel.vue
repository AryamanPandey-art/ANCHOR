<template>
  <div class="anchor-card proof-verification-panel">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </span>
        <span class="card-title">VALIDATION & INTEGRITY STATUS</span>
      </div>
      <span class="card-menu">•••</span>
    </div>

    <!-- Truthful Verification Rows -->
    <div class="verification-rows">
      <div class="verification-row">
        <span class="v-label">Grounding Proof</span>
        <span class="v-val" :class="validationData?.groundingPassed ? 'status-pass' : 'status-fail'">
          {{ validationData?.groundingPassed ? '✓ Validated SIIS' : '✕ Unverified' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Deeplink Catalog</span>
        <span class="v-val" :class="validationData?.deeplinkPassed ? 'status-pass' : 'status-fail'">
          {{ validationData?.deeplinkPassed ? `✓ ${validationData?.proofTrace?.catalogMatchId || 'Catalog Verified'}` : '✕ Uncatalogued' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Direction Match</span>
        <span class="v-val" :class="validationData?.directionPassed ? 'status-pass' : 'status-fail'">
          {{ validationData?.groundingPassed ? `✓ ${validationData?.proofTrace?.queryDirection || 'ON'} Matched` : '✕ Direction Mismatch' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Execution Mode</span>
        <span class="v-val" :class="validationData?.proofTrace?.llmUsed ? 'status-ai' : 'status-pass'">
          {{ validationData?.proofTrace?.llmUsed ? '✓ AI Proposed → Verified' : '✓ Symbolic Fallback → Verified' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Decision Outcome</span>
        <span class="v-val" :class="validationData?.overallStatus === 'PASS' ? 'status-pass' : 'status-fail'">
          {{ validationData?.overallStatus === 'PASS' ? '✓ PASS — Proof Carried' : '✕ REJECTED — Blocked' }}
        </span>
      </div>

      <!-- Verbatim Evidence Quote Snippet -->
      <div v-if="validationData?.proofTrace?.verbatimEvidence" class="evidence-quote-box">
        <span class="quote-title">EVIDENCE:</span>
        <p class="quote-text">"{{ validationData.proofTrace.verbatimEvidence }}"</p>
        <span v-if="validationData?.proofTrace?.sourceSectionTitle" class="quote-source">
          Source: {{ validationData.proofTrace.sourceSectionTitle }}
        </span>
      </div>

      <div v-else-if="validationData?.overallStatus !== 'PASS' && validationData?.failureReasons && validationData.failureReasons.length" class="failure-reason-micro">
        <span class="reason-micro-label">REASON:</span>
        <span class="reason-micro-val">{{ validationData.failureReasons[0] }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProofVerificationPanel',
  props: {
    validationData: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>

<style scoped>
.proof-verification-panel {
  padding: 10px 14px;
  height: 100%;
}

.verification-rows {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 3px;
}

.verification-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10.5px;
}

.v-label {
  color: #6a88a7;
}

.v-val {
  font-weight: 700;
  font-size: 11px;
}

.status-pass {
  color: var(--color-green);
}

.status-ai {
  color: #38bdf8;
}

.status-fail {
  color: #f43f5e;
}

.evidence-quote-box {
  margin-top: 4px;
  background: rgba(0, 180, 255, 0.06);
  border: 1px solid rgba(0, 180, 255, 0.2);
  border-radius: 4px;
  padding: 4px 7px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.quote-title {
  font-size: 8.5px;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 0.04em;
}

.quote-text {
  color: #93c5fd;
  font-size: 9.5px;
  line-height: 1.35;
  margin: 0;
  font-style: italic;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.quote-source {
  font-size: 8.5px;
  color: #64748b;
  font-weight: 500;
}

.failure-reason-micro {
  margin-top: 3px;
  background: rgba(244, 63, 94, 0.08);
  border: 1px solid rgba(244, 63, 94, 0.25);
  border-radius: 4px;
  padding: 3px 6px;
  font-size: 9.5px;
  display: flex;
  gap: 4px;
  align-items: center;
}

.reason-micro-label {
  font-weight: 700;
  color: #f43f5e;
  font-size: 9px;
  flex-shrink: 0;
}

.reason-micro-val {
  color: #ff94a5;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
