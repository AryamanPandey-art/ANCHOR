<template>
  <div class="anchor-card pipeline-panel">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="6" cy="6" r="3"/>
            <circle cx="6" cy="18" r="3"/>
            <path d="M20 4L8.12 15.88M14.47 14.48L20 20M8.12 8.12L12 12"/>
          </svg>
        </span>
        <span class="card-title">PIPELINE STATUS</span>
      </div>
      <div 
        class="pipeline-status-badge"
        :class="{
          'badge-pass': !isLoading && isPass,
          'badge-fail': !isLoading && isFail,
          'badge-pending': isLoading
        }"
      >
        <span v-if="isLoading" class="pulse-indicator"></span>
        <span>{{ statusBadgeText }}</span>
      </div>
    </div>

    <!-- Active Processing Step Indicator -->
    <div v-if="isLoading" class="processing-strip">
      <div class="processing-spinner-sm"></div>
      <span class="processing-text">{{ currentProcessingStepText }}</span>
    </div>

    <!-- 5 Stepper items -->
    <div class="stepper-container" :class="{ 'stepper-processing': isLoading }">
      <div 
        v-for="(stage, index) in computedStages" 
        :key="stage.name" 
        class="step-item"
      >
        <div class="step-circle-wrapper">
          <div 
            class="step-circle" 
            :class="{ 
              completed: stage.completed && !stage.failed, 
              current: isCurrent(index),
              failed: stage.failed
            }"
          >
            <!-- Checkmark for completed -->
            <svg v-if="stage.completed && !stage.failed" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <!-- Red X for failed -->
            <svg v-else-if="stage.failed" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            <!-- Processing or pending dot -->
            <span v-else class="pending-dot"></span>
          </div>

          <!-- Connector line -->
          <div 
            v-if="index < computedStages.length - 1" 
            class="step-line" 
            :class="{ 
              active: stage.completed && !stage.failed && computedStages[index + 1]?.completed && !computedStages[index + 1]?.failed,
              'line-fail': stage.completed && computedStages[index + 1]?.failed
            }"
          ></div>
        </div>

        <span class="step-label" :class="{ 'label-failed': stage.failed }">{{ stage.displayName || stage.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PipelineStatusPanel',
  props: {
    stages: {
      type: Array,
      default: () => [
        { name: 'Query Processed', completed: true },
        { name: 'Intent Identified', completed: true },
        { name: 'Evidence Retrieved', completed: true },
        { name: 'Action Resolved', completed: true },
        { name: 'Contract Validated', completed: true }
      ]
    },
    isLoading: {
      type: Boolean,
      default: false
    },
    overallStatus: {
      type: String,
      default: 'PASS'
    },
    processingStepIndex: {
      type: Number,
      default: 3
    }
  },
  data() {
    return {
      processingSteps: [
        "✓ Query received",
        "✓ Intent identified",
        "✓ Evidence retrieved",
        "→ Verifying action...",
        "○ Resolving deeplink...",
        "○ Final validation..."
      ]
    };
  },
  computed: {
    isPass() {
      return this.overallStatus === 'PASS';
    },
    isFail() {
      return this.overallStatus === 'FAIL' || this.overallStatus === 'REJECTED';
    },
    statusBadgeText() {
      if (this.isLoading) return 'PROCESSING...';
      if (this.isPass) return 'VERIFIED • PASS';
      return 'REJECTED • FAIL';
    },
    currentProcessingStepText() {
      const idx = Math.min(this.processingStepIndex, this.processingSteps.length - 1);
      return this.processingSteps[idx] || "→ Verifying action...";
    },
    computedStages() {
      return this.stages.map((stage, idx) => {
        if (this.isFail && idx === 4) {
          return {
            ...stage,
            displayName: 'Contract Rejected',
            completed: false,
            failed: true
          };
        }
        return {
          ...stage,
          displayName: stage.name,
          failed: false
        };
      });
    }
  },
  methods: {
    isCurrent(index) {
      if (!this.isLoading) return false;
      return index === this.processingStepIndex;
    }
  }
}
</script>

<style scoped>
.pipeline-panel {
  padding: 10px 12px;
  height: 100%;
}

.pipeline-status-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 9.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}

.badge-pass {
  background: rgba(0, 230, 118, 0.12);
  color: #00e676;
  border: 1px solid rgba(0, 230, 118, 0.35);
}

.badge-fail {
  background: rgba(244, 63, 94, 0.12);
  color: #f43f5e;
  border: 1px solid rgba(244, 63, 94, 0.35);
}

.badge-pending {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.35);
}

.pulse-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #f59e0b;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 0.4; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.15); }
  100% { opacity: 0.4; transform: scale(0.9); }
}

.processing-strip {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.25);
  border-radius: 4px;
  padding: 3px 8px;
  margin-top: 6px;
  font-size: 10px;
  color: #fbbf24;
  font-family: var(--font-mono);
}

.processing-spinner-sm {
  width: 10px;
  height: 10px;
  border: 2px solid rgba(251, 191, 36, 0.25);
  border-top-color: #fbbf24;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.stepper-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 8px;
  position: relative;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  text-align: center;
  position: relative;
}

.step-circle-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
  justify-content: center;
}

.step-circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #061122;
  border: 1px solid rgba(0, 180, 255, 0.28);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-cyan);
  z-index: 2;
  transition: all 0.3s ease;
}

.step-circle.completed {
  background: rgba(0, 240, 255, 0.12);
  border-color: #00f0ff;
  color: #00f0ff;
  box-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
}

.step-circle.current {
  border-color: #f59e0b;
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.15);
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.45);
}

.step-circle.failed {
  border-color: #f43f5e;
  color: #f43f5e;
  background: rgba(244, 63, 94, 0.15);
  box-shadow: 0 0 8px rgba(244, 63, 94, 0.45);
}

.pending-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(0, 180, 255, 0.3);
}

.step-line {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 2px;
  background: rgba(0, 180, 255, 0.12);
  z-index: 1;
  transform: translateY(-50%);
  transition: background 0.3s ease;
}

.step-line.active {
  background: #00d2ff;
  box-shadow: 0 0 6px rgba(0, 210, 255, 0.4);
}

.step-line.line-fail {
  background: #f43f5e;
  box-shadow: 0 0 6px rgba(244, 63, 94, 0.4);
}

.step-label {
  font-size: 9.5px;
  color: #7997b6;
  margin-top: 5px;
  max-width: 65px;
  line-height: 1.2;
}

.step-label.label-failed {
  color: #f43f5e;
  font-weight: 600;
}
</style>
