<template>
  <header class="system-header">
    <div class="header-left">
      <h1 class="brand-title">ANCHOR</h1>
      <span class="brand-subtitle">Proof-Carrying Troubleshooting Engine</span>
      <span class="view-mode-tag">VIEW: {{ (currentTab || 'overview').toUpperCase() }}</span>
    </div>

    <div class="header-right">
      <div
        class="status-badge"
        :class="{
          'status-processing': isProcessing,
          'status-pass': !isProcessing && isPass,
          'status-fail': !isProcessing && isFail
        }"
      >
        <span class="status-dot"></span>
        <span class="status-text">{{ statusText }}</span>
      </div>

      <span class="meta-item"><span class="meta-tag">EVIDENCE:</span> <span class="meta-highlight">SIIS GROUNDED</span></span>
      <span class="meta-item"><span class="meta-tag">GUARD:</span> <span class="meta-highlight">ACTIVE</span></span>
      <span class="meta-item">
        <span class="meta-tag">CONTRACT:</span>
        <span
          class="meta-highlight"
          :class="{
            'contract-pass': !isProcessing && isPass,
            'contract-fail': !isProcessing && isFail,
            'contract-pending': isProcessing
          }"
        >
          {{ contractText }}
        </span>
      </span>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
    currentTab: {
      type: String,
      default: 'overview'
    },
    sessionData: {
      type: Object,
      default: () => ({})
    },
    validationStatus: {
      type: String,
      default: 'PASS'
    },
    isProcessing: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    isPass() {
      return this.validationStatus === 'PASS';
    },
    isFail() {
      return this.validationStatus === 'FAIL' || this.validationStatus === 'REJECTED';
    },
    statusText() {
      if (this.isProcessing) return 'PIPELINE RUNNING';
      if (this.isPass) return 'ENGINE VERIFIED';
      return 'ACTION REJECTED';
    },
    contractText() {
      if (this.isProcessing) return 'EVALUATING';
      if (this.isPass) return 'ENFORCED (PASS)';
      return 'VIOLATION (FAIL)';
    }
  }
}
</script>

<style scoped>
.system-header {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background-color: var(--bg-header);
  border-bottom: 1px solid var(--border-subtle);
  user-select: none;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 16px;
}

.brand-title {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--color-cyan);
  text-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
  margin: 0;
}

.brand-subtitle {
  font-size: 12px;
  color: #8da4be;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.view-mode-tag {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 3px 8px;
  border-radius: 4px;
  background: rgba(0, 240, 255, 0.08);
  border: 1px solid rgba(0, 240, 255, 0.35);
  color: var(--color-cyan);
  text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
  display: inline-flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 11px;
  color: var(--text-dim);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 10.5px;
  letter-spacing: 0.04em;
  transition: all 0.3s ease;
}

.status-badge.status-pass {
  background: rgba(0, 230, 118, 0.1);
  border: 1px solid rgba(0, 230, 118, 0.3);
  color: #00e676;
}

.status-badge.status-pass .status-dot {
  background-color: #00e676;
  box-shadow: 0 0 8px #00e676;
}

.status-badge.status-fail {
  background: rgba(244, 63, 94, 0.12);
  border: 1px solid rgba(244, 63, 94, 0.35);
  color: #f43f5e;
}

.status-badge.status-fail .status-dot {
  background-color: #f43f5e;
  box-shadow: 0 0 8px #f43f5e;
}

.status-badge.status-processing {
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.35);
  color: #f59e0b;
}

.status-badge.status-processing .status-dot {
  background-color: #f59e0b;
  box-shadow: 0 0 8px #f59e0b;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.9); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.5; }
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.meta-item {
  color: #5c7b9c;
  font-weight: 500;
  font-size: 11px;
}

.meta-tag {
  color: #4b6685;
  font-weight: 600;
}

.meta-highlight {
  color: #c4d7ec;
  font-weight: 600;
}

.meta-highlight.contract-pass {
  color: #00e676;
  text-shadow: 0 0 6px rgba(0, 230, 118, 0.3);
}

.meta-highlight.contract-fail {
  color: #f43f5e;
  text-shadow: 0 0 6px rgba(244, 63, 94, 0.3);
}

.meta-highlight.contract-pending {
  color: #f59e0b;
  text-shadow: 0 0 6px rgba(245, 158, 11, 0.3);
}
</style>
