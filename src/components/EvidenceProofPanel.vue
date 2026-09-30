<template>
  <div class="anchor-card evidence-proof-panel">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </span>
        <span class="card-title">EVIDENCE & PROOF STATUS</span>
      </div>
      <span class="card-menu">•••</span>
    </div>

    <!-- Truthful Evidence Proof Rows -->
    <div class="proof-rows">
      <div class="proof-row">
        <span class="proof-label">Relevant Evidence</span>
        <div class="proof-status-badge" :class="evidenceData?.grounded ? 'status-pass' : 'status-fail'">
          <svg v-if="evidenceData?.grounded" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span v-else>✕</span>
          <span>{{ evidenceData?.grounded ? 'Found' : 'Not Found' }}</span>
        </div>
      </div>

      <div class="proof-row">
        <span class="proof-label">Source Document</span>
        <span class="proof-val">{{ evidenceData?.source || 'Samsung SIIS' }} ({{ evidenceData?.evidenceId || 'None' }})</span>
      </div>

      <div class="proof-row">
        <span class="proof-label">Grounding</span>
        <div class="proof-status-badge" :class="evidenceData?.grounded ? 'status-pass' : 'status-fail'">
          <svg v-if="evidenceData?.grounded" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span v-else>✕</span>
          <span>{{ evidenceData?.grounded ? 'Verified' : 'Unverified' }}</span>
        </div>
      </div>

      <div class="proof-row">
        <span class="proof-label">Target Section</span>
        <span class="proof-val section-val">{{ evidenceData?.section || 'Unresolved' }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EvidenceProofPanel',
  props: {
    evidenceData: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>

<style scoped>
.evidence-proof-panel {
  padding: 10px 14px;
  height: 100%;
}

.proof-rows {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 3px;
}

.proof-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10.5px;
}

.proof-label {
  color: #6a88a7;
}

.proof-val {
  color: #d8e5f2;
  font-weight: 500;
}

.section-val {
  color: #00d2ff;
  font-family: var(--font-mono);
  font-size: 10px;
}

.proof-status-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 700;
  font-size: 11px;
}

.status-pass {
  color: var(--color-green);
}

.status-fail {
  color: #f43f5e;
}
</style>
