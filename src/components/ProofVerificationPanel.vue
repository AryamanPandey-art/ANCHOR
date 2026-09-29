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
          {{ validationData?.groundingPassed ? '✓ Validated' : '✕ Unverified' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Deeplink Catalog</span>
        <span class="v-val" :class="validationData?.deeplinkPassed ? 'status-pass' : 'status-fail'">
          {{ validationData?.deeplinkPassed ? '✓ Verified in Catalog' : '✕ Uncatalogued' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Direction Match</span>
        <span class="v-val" :class="validationData?.directionPassed ? 'status-pass' : 'status-fail'">
          {{ validationData?.directionPassed ? '✓ Validated Direction' : '✕ Direction Mismatch' }}
        </span>
      </div>

      <div class="verification-row">
        <span class="v-label">Decision Outcome</span>
        <span class="v-val" :class="validationData?.overallStatus === 'PASS' ? 'status-pass' : 'status-fail'">
          {{ validationData?.overallStatus === 'PASS' ? '✓ PASS — Proof Carried' : '✕ REJECTED — Blocked' }}
        </span>
      </div>

      <div v-if="validationData?.overallStatus !== 'PASS' && validationData?.failureReasons && validationData.failureReasons.length" class="failure-reason-micro">
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

.status-fail {
  color: #f43f5e;
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
