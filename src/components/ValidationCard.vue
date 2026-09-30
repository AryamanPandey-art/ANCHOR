<template>
  <div class="anchor-card validation-card">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </span>
        <span class="card-title">CONTRACT VALIDATION</span>
      </div>
      <span class="card-menu">•••</span>
    </div>

    <!-- Validation Checklist -->
    <div class="validation-checklist">
      <div class="validation-item">
        <span class="item-label">Grounding</span>
        <div class="item-status" :class="validationData?.groundingPassed ? 'status-pass' : 'status-fail'">
          <span>{{ validationData?.groundingPassed ? 'Validated' : 'Failed' }}</span>
          <svg v-if="validationData?.groundingPassed" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>
      </div>

      <div class="validation-item">
        <span class="item-label">Deeplink</span>
        <div class="item-status" :class="validationData?.deeplinkPassed ? 'status-pass' : 'status-fail'">
          <span>{{ validationData?.deeplinkPassed ? 'Validated' : 'Failed' }}</span>
          <svg v-if="validationData?.deeplinkPassed" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>
      </div>

      <div class="validation-item">
        <span class="item-label">Direction</span>
        <div class="item-status" :class="validationData?.directionPassed ? 'status-pass' : 'status-fail'">
          <span>{{ validationData?.directionPassed ? 'Validated' : 'Failed' }}</span>
          <svg v-if="validationData?.directionPassed" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>
      </div>

      <div class="validation-item">
        <span class="item-label">Schema</span>
        <div class="item-status" :class="validationData?.schemaPassed ? 'status-pass' : 'status-fail'">
          <span>{{ validationData?.schemaPassed ? 'Validated' : 'Failed' }}</span>
          <svg v-if="validationData?.schemaPassed" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>
      </div>
    </div>

    <!-- Divider -->
    <div class="validation-divider"></div>

    <!-- Overall Status -->
    <div class="overall-row">
      <span class="overall-label">Overall Status</span>
      <div
        class="overall-badge"
        :class="validationData?.overallStatus === 'PASS' ? 'overall-pass' : 'overall-fail'"
      >
        <div class="badge-dot-icon">
          <svg v-if="validationData?.overallStatus === 'PASS'" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>
        <span class="badge-text">{{ validationData?.overallStatus === 'PASS' ? 'PASS' : 'FAILED' }}</span>
      </div>
    </div>

    <!-- Failure reason disclosure if validation fails -->
    <div v-if="validationData?.overallStatus !== 'PASS' && validationData?.failureReasons && validationData.failureReasons.length" class="failure-reasons-box">
      <span class="failure-title">Constraint:</span>
      <p class="failure-desc">{{ validationData.failureReasons[0] }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ValidationCard',
  props: {
    validationData: {
      type: Object,
      default: () => ({
        groundingPassed: true,
        deeplinkPassed: true,
        directionPassed: true,
        schemaPassed: true,
        overallStatus: 'PASS'
      })
    }
  }
}
</script>

<style scoped>
.validation-card {
  padding: 12px 14px;
}

.validation-checklist {
  display: flex;
  flex-direction: column;
  gap: 7px;
  font-size: 11px;
}

.validation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-label {
  color: #6a88a7;
}

.item-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  font-size: 11.5px;
}

.status-pass {
  color: #00e676;
}

.status-fail {
  color: #f43f5e;
}

.validation-divider {
  height: 1px;
  background: rgba(0, 180, 255, 0.12);
  margin: 10px 0;
}

.overall-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overall-label {
  font-size: 11px;
  color: #7997b6;
  font-weight: 500;
}

.overall-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.05em;
}

.overall-pass {
  background: rgba(0, 230, 118, 0.14);
  color: #00e676;
  border: 1px solid rgba(0, 230, 118, 0.45);
  box-shadow: 0 0 10px rgba(0, 230, 118, 0.25);
}

.overall-fail {
  background: rgba(244, 63, 94, 0.14);
  color: #f43f5e;
  border: 1px solid rgba(244, 63, 94, 0.45);
  box-shadow: 0 0 10px rgba(244, 63, 94, 0.25);
}

.failure-reasons-box {
  margin-top: 8px;
  background: rgba(244, 63, 94, 0.08);
  border: 1px solid rgba(244, 63, 94, 0.25);
  border-radius: 4px;
  padding: 5px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.failure-title {
  color: #f43f5e;
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.failure-desc {
  color: #fca5a5;
  font-size: 10px;
  line-height: 1.3;
  margin: 0;
}

.badge-dot-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: currentColor;
  color: #040913;
}
</style>
