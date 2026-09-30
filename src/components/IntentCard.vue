<template>
  <div class="anchor-card intent-card">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <circle cx="12" cy="12" r="6"/>
            <circle cx="12" cy="12" r="2"/>
          </svg>
        </span>
        <span class="card-title">INTENT ANALYSIS</span>
      </div>
      <span class="card-menu">•••</span>
    </div>

    <div class="intent-content">
      <!-- Left info details -->
      <div class="intent-details">
        <div class="intent-row main-intent">
          <span class="field-label">Intent</span>
          <span class="field-value intent-highlight">{{ intentData?.intent || 'SCREEN_ROTATION' }}</span>
        </div>

        <div class="intent-meta-grid">
          <div class="intent-row">
            <span class="field-label">Category</span>
            <span class="field-value">{{ intentData?.category || 'Display & Rotation' }}</span>
          </div>

          <div class="intent-row">
            <span class="field-label">Device Type</span>
            <span class="field-value">{{ intentData?.deviceType || 'Smartphone (Galaxy)' }}</span>
          </div>

          <div class="intent-row">
            <span class="field-label">OS Version</span>
            <span class="field-value">{{ intentData?.osVersion || 'One UI 6.x' }}</span>
          </div>
        </div>
      </div>

      <!-- Right Proof State Ring -->
      <div class="confidence-ring-container">
        <div class="ring-wrapper">
          <svg class="progress-ring" width="68" height="68">
            <circle
              class="ring-bg"
              stroke="rgba(0, 180, 255, 0.15)"
              stroke-width="4.5"
              fill="transparent"
              r="28"
              cx="34"
              cy="34"
            />
            <circle
              class="ring-progress"
              :stroke="isIntentVerified ? '#00f0ff' : '#f43f5e'"
              stroke-width="4.5"
              stroke-linecap="round"
              fill="transparent"
              r="28"
              cx="34"
              cy="34"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="isIntentVerified ? 0 : circumference * 0.75"
            />
          </svg>
          <div class="ring-text">
            <svg v-if="isIntentVerified" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#00e676" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span v-else class="ring-unresolved">✕</span>
          </div>
        </div>
        <span class="confidence-label">{{ isIntentVerified ? 'Intent Matched ✓' : 'Unresolved' }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IntentCard',
  props: {
    intentData: {
      type: Object,
      default: () => ({
        intent: 'SCREEN_ROTATION',
        confidence: 94,
        category: 'Display & Rotation',
        deviceType: 'Smartphone (Galaxy)',
        osVersion: 'One UI 6.x'
      })
    }
  },
  computed: {
    circumference() {
      return 2 * Math.PI * 28;
    },
    isIntentVerified() {
      return Boolean(
        this.intentData && 
        !this.intentData.ambiguous && 
        this.intentData.intent && 
        this.intentData.intent !== 'UNSUPPORTED_INTENT' &&
        this.intentData.intent !== 'EMPTY_QUERY'
      );
    }
  }
}
</script>

<style scoped>
.intent-card {
  padding: 12px 14px;
}

.intent-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.intent-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.intent-row {
  display: flex;
  flex-direction: column;
}

.main-intent {
  margin-bottom: 3px;
}

.main-intent .field-label {
  font-size: 10px;
  color: #7997b6;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 2px;
}

.intent-highlight {
  font-size: 13.5px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.03em;
}

.intent-meta-grid {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.intent-meta-grid .intent-row {
  flex-direction: row;
  justify-content: space-between;
  font-size: 11px;
}

.field-label {
  color: #6a88a7;
}

.field-value {
  color: #d8e5f2;
  font-weight: 500;
}

/* Confidence Ring */
.confidence-ring-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-left: 8px;
}

.ring-wrapper {
  position: relative;
  width: 68px;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-ring {
  transform: rotate(-90deg);
  filter: drop-shadow(0 0 6px rgba(0, 240, 255, 0.4));
}

.ring-progress {
  transition: stroke-dashoffset 0.8s ease;
}

.ring-text {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ring-percent {
  font-size: 14.5px;
  font-weight: 700;
  color: #ffffff;
}

.ring-unresolved {
  font-size: 18px;
  font-weight: 700;
  color: #f43f5e;
}

.confidence-label {
  font-size: 9.5px;
  color: #7997b6;
  margin-top: 3px;
  letter-spacing: 0.02em;
}
</style>
