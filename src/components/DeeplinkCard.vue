<template>
  <div class="anchor-card deeplink-card">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
          </svg>
        </span>
        <span class="card-title">DEEPLINK RESOLUTION</span>
      </div>
      <span class="card-menu">•••</span>
    </div>

    <div class="deeplink-rows">
      <div class="deeplink-row">
        <span class="field-label">Candidate</span>
        <span class="field-value">{{ displayCandidate }}</span>
      </div>

      <div class="deeplink-row deeplink-path-row">
        <span class="field-label">Deeplink</span>
        <span class="field-value deeplink-uri" :class="{ 'uri-none': !deeplinkData?.deeplink }">
          {{ displayDeeplinkURI }}
        </span>
      </div>

      <div class="deeplink-row">
        <span class="field-label">Direction</span>
        <span 
          class="direction-badge" 
          :class="directionClass"
        >
          {{ deeplinkData?.direction || 'NONE' }}
        </span>
      </div>

      <div class="deeplink-row">
        <span class="field-label">Catalog Match</span>
        <div class="match-status" :class="catalogMatchClass">
          <svg v-if="deeplinkData?.catalogMatch === 'VALID'" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span v-else-if="deeplinkData?.catalogMatch === 'IDLE'" class="idle-dot">○</span>
          <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
          <span class="match-text">{{ deeplinkData?.catalogMatch || 'IDLE' }}</span>
        </div>
      </div>

      <div class="deeplink-row">
        <span class="field-label">Settings Link</span>
        <div class="match-status" :class="settingsLinkClass">
          <svg v-if="deeplinkData?.verified" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span v-else-if="deeplinkData?.catalogMatch === 'IDLE'" class="idle-dot">○</span>
          <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
          <span class="match-text">{{ settingsLinkText }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeeplinkCard',
  props: {
    deeplinkData: {
      type: Object,
      default: () => ({
        candidate: 'None',
        deeplink: null,
        direction: 'NONE',
        catalogMatch: 'IDLE',
        verified: false
      })
    }
  },
  computed: {
    displayCandidate() {
      return this.deeplinkData?.candidate || 'None';
    },
    displayDeeplinkURI() {
      if (this.deeplinkData?.deeplink) return this.deeplinkData.deeplink;
      if (this.deeplinkData?.catalogMatch === 'INVALID') return 'None (Uncatalogued)';
      return 'None';
    },
    directionClass() {
      if (this.deeplinkData?.direction === 'ENABLE') return 'dir-enable';
      if (this.deeplinkData?.direction === 'DISABLE') return 'dir-disable';
      return 'dir-none';
    },
    catalogMatchClass() {
      if (this.deeplinkData?.catalogMatch === 'VALID') return 'status-pass';
      if (this.deeplinkData?.catalogMatch === 'IDLE') return 'status-idle';
      return 'status-fail';
    },
    settingsLinkClass() {
      if (this.deeplinkData?.verified) return 'status-pass';
      if (this.deeplinkData?.catalogMatch === 'IDLE') return 'status-idle';
      return 'status-fail';
    },
    settingsLinkText() {
      if (this.deeplinkData?.verified) return '✓ VERIFIED';
      if (this.deeplinkData?.catalogMatch === 'IDLE') return 'IDLE';
      return 'UNVERIFIED';
    }
  }
}
</script>

<style scoped>
.deeplink-card {
  padding: 12px 14px;
}

.deeplink-rows {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 11px;
}

.deeplink-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field-label {
  color: #6a88a7;
}

.field-value {
  color: #d8e5f2;
  font-weight: 500;
}

.deeplink-path-row {
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.deeplink-uri {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: #00d2ff;
  word-break: break-all;
}

.direction-badge {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 2px 7px;
  border-radius: 4px;
}

.dir-enable {
  color: #00e676;
  background: rgba(0, 230, 118, 0.12);
  border: 1px solid rgba(0, 230, 118, 0.35);
  box-shadow: 0 0 8px rgba(0, 230, 118, 0.2);
}

.dir-disable {
  color: #f43f5e;
  background: rgba(244, 63, 94, 0.12);
  border: 1px solid rgba(244, 63, 94, 0.35);
}

.match-status {
  display: flex;
  align-items: center;
  gap: 4px;
}

.match-status.status-pass {
  color: var(--color-green);
}

.match-status.status-fail {
  color: #f43f5e;
}

.match-text {
  font-weight: 700;
  font-size: 11.5px;
}

.confidence-row {
  flex-direction: column;
  align-items: stretch;
  gap: 4px;
  margin-top: 2px;
}

.confidence-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.confidence-percent {
  font-size: 11px;
  color: #00f0ff;
  font-weight: 600;
}

.confidence-track {
  width: 100%;
  height: 5px;
  background: rgba(0, 180, 255, 0.15);
  border-radius: 3px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #0099ff, #00f0ff);
  box-shadow: 0 0 6px rgba(0, 240, 255, 0.6);
  border-radius: 3px;
  transition: width 0.6s ease;
}
</style>
