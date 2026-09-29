<template>
  <div class="anchor-card user-query-card">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </span>
        <span class="card-title">USER QUERY</span>
      </div>
      <div class="card-header-actions">
        <button 
          class="new-query-btn" 
          @click="resetQuery" 
          title="Reset to New Clean Query"
        >
          <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="1 4 1 10 7 10"></polyline>
            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
          </svg>
          <span>New Query</span>
        </button>
        <span class="card-menu">•••</span>
      </div>
    </div>

    <!-- Query Input Area -->
    <div class="query-input-container">
      <textarea 
        v-model="localQuery" 
        class="query-textarea"
        placeholder="Describe the Samsung troubleshooting issue..."
        rows="2"
        @keydown.enter.prevent="submitQuery"
      ></textarea>
      
      <button 
        class="submit-button" 
        :class="{ loading: isLoading }"
        @click="submitQuery"
        title="Execute Diagnostic Pipeline"
      >
        <svg v-if="!isLoading" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
        </svg>
        <span v-else class="loader-spinner"></span>
      </button>
    </div>

    <!-- Demo Mode Scenarios -->
    <div class="demo-mode-section">
      <div class="demo-mode-header">
        <span class="demo-mode-tag">DEMO SCENARIOS</span>
        <span class="demo-mode-hint">Live AI Proposal → ANCHOR Verification</span>
      </div>
      <div class="quick-chips">
        <button 
          v-for="chip in quickChips" 
          :key="chip.scenario" 
          class="chip-button"
          :class="{ 'chip-fail': chip.status === 'fail' }"
          @click="selectChip(chip)"
          :title="chip.query"
        >
          <span class="chip-status-dot" :class="chip.status === 'fail' ? 'dot-red' : 'dot-green'"></span>
          <span class="chip-scenario-id">{{ chip.scenario }}:</span>
          <span class="chip-label-text">{{ chip.label }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserQueryCard',
  props: {
    modelValue: {
      type: String,
      default: "My Nexa A14 screen looks distorted right after I received the phone and I need a test."
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'submit-query', 'reset-query'],
  data() {
    return {
      localQuery: this.modelValue,
      quickChips: [
        { 
          scenario: 'S1', 
          label: 'Auto Rotate [PASS]', 
          query: "My Nexa A14 screen looks distorted right after I received the phone and I need a test.", 
          status: 'pass' 
        },
        { 
          scenario: 'S2', 
          label: 'Data Backup [PASS]', 
          query: "My Nexa Fold X1 screen is cracked and unresponsive; I need my data saved.", 
          status: 'pass' 
        },
        { 
          scenario: 'S3', 
          label: 'Floating Circle [REJECTED]', 
          query: "My Nexa X1 has a floating circle that opened a panel. Remove it.", 
          status: 'fail' 
        }
      ]
    };
  },
  watch: {
    modelValue(newVal) {
      this.localQuery = newVal;
    }
  },
  methods: {
    submitQuery() {
      this.$emit('update:modelValue', this.localQuery);
      this.$emit('submit-query', this.localQuery);
    },
    selectChip(chip) {
      this.localQuery = chip.query;
      this.$emit('update:modelValue', this.localQuery);
      this.$emit('submit-query', this.localQuery);
    },
    resetQuery() {
      this.localQuery = "";
      this.$emit('update:modelValue', "");
      this.$emit('reset-query');
    }
  }
}
</script>

<style scoped>
.user-query-card {
  padding: 10px 12px;
}

.card-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.new-query-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(0, 180, 255, 0.08);
  border: 1px solid rgba(0, 180, 255, 0.25);
  color: #79a3c8;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 9.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.new-query-btn:hover {
  background: rgba(0, 240, 255, 0.15);
  color: #00f0ff;
  border-color: rgba(0, 240, 255, 0.45);
}

.query-input-container {
  display: flex;
  background-color: var(--bg-input);
  border: 1px solid rgba(0, 180, 255, 0.22);
  border-radius: 8px;
  padding: 6px 6px 6px 10px;
  align-items: center;
  gap: 8px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.query-input-container:focus-within {
  border-color: rgba(0, 240, 255, 0.55);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.15);
}

.query-textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 11.5px;
  line-height: 1.4;
  resize: none;
  font-family: inherit;
  outline: none;
}

.query-textarea::placeholder {
  color: #4b6685;
}

.submit-button {
  background: linear-gradient(135deg, #00d2ff 0%, #0077ff 100%);
  color: #020712;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0, 210, 255, 0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  flex-shrink: 0;
}

.submit-button:hover:not(.loading) {
  transform: scale(1.04);
  box-shadow: 0 0 14px rgba(0, 210, 255, 0.55);
}

.submit-button.loading {
  opacity: 0.8;
  cursor: not-allowed;
}

.loader-spinner {
  width: 13px;
  height: 13px;
  border: 2px solid rgba(2, 7, 18, 0.3);
  border-top-color: #020712;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.demo-mode-section {
  margin-top: 8px;
}

.demo-mode-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 5px;
}

.demo-mode-tag {
  font-size: 8.5px;
  font-weight: 800;
  color: #00f0ff;
  letter-spacing: 0.6px;
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid rgba(0, 240, 255, 0.25);
  padding: 1px 4px;
  border-radius: 3px;
}

.demo-mode-hint {
  font-size: 9px;
  color: #5c799a;
  letter-spacing: 0.2px;
}

.quick-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.chip-scenario-id {
  font-weight: 700;
  color: #00f0ff;
  font-size: 9.5px;
}

.chip-button.chip-fail .chip-scenario-id {
  color: #ff8095;
}

.chip-button {
  background: rgba(4, 18, 38, 0.8);
  border: 1px solid rgba(0, 180, 255, 0.22);
  color: #8da4be;
  border-radius: 4px;
  padding: 3px 7px;
  font-size: 10px;
  cursor: pointer;
  transition: all 0.18s ease;
  display: flex;
  align-items: center;
  gap: 4px;
}

.chip-button:hover {
  background: rgba(0, 210, 255, 0.12);
  border-color: rgba(0, 240, 255, 0.45);
  color: #00f0ff;
}

.chip-button.chip-fail:hover {
  background: rgba(244, 63, 94, 0.12);
  border-color: rgba(244, 63, 94, 0.45);
  color: #ff8095;
}

.chip-status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.dot-green {
  background: #00e676;
  box-shadow: 0 0 4px #00e676;
}

.dot-red {
  background: #f43f5e;
  box-shadow: 0 0 4px #f43f5e;
}
</style>
