<template>
  <div class="anchor-card action-analysis-card">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon action-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#00e676" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
        </span>
        <span class="card-title">ACTION ANALYSIS</span>
      </div>
      <span class="ai-anchor-badge">AI → ANCHOR</span>
    </div>

    <div class="action-body">
      <!-- 1. AI PROPOSED ACTION -->
      <div class="ai-proposal-box">
        <div class="box-micro-header">
          <span class="micro-label ai-label">AI PROPOSED ACTION</span>
          <span class="micro-status ai-status-tag">AI SUGGESTION</span>
        </div>
        
        <div class="proposal-main-title">
          {{ displayAction }}
        </div>

        <div class="proposal-meta-grid">
          <div class="meta-row">
            <span class="meta-label">WHY?</span>
            <span class="meta-value">{{ displayWhy }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">EVIDENCE</span>
            <span class="meta-value mono evidence-id-tag">{{ displayEvidence }}</span>
          </div>
        </div>
      </div>

      <!-- Flow Connector: AI suggests ↓ ANCHOR verifies -->
      <div class="flow-divider">
        <div class="flow-line"></div>
        <div class="flow-badge">
          <span class="flow-text">ANCHOR VERIFICATION</span>
          <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </div>
        <div class="flow-line"></div>
      </div>

      <!-- 2. ANCHOR VERIFICATION -->
      <div class="anchor-verification-box" :class="isPass ? 'box-pass' : (isIdle ? 'box-idle' : 'box-fail')">
        <div class="verification-checks-grid">
          <!-- Evidence Check -->
          <div class="check-pill" :class="isIdle ? 'pill-idle' : (isEvidenceValid ? 'pill-pass' : 'pill-fail')">
            <span class="check-label">Evidence</span>
            <span class="check-icon">{{ isIdle ? '○' : (isEvidenceValid ? '✓' : '✕') }}</span>
          </div>

          <!-- Relevance Check -->
          <div class="check-pill" :class="isIdle ? 'pill-idle' : (isRelevanceValid ? 'pill-pass' : 'pill-fail')">
            <span class="check-label">Relevance</span>
            <span class="check-icon">{{ isIdle ? '○' : (isRelevanceValid ? '✓' : '✕') }}</span>
          </div>

          <!-- Direction Check -->
          <div class="check-pill" :class="isIdle ? 'pill-idle' : (isDirectionValid ? 'pill-pass' : 'pill-fail')">
            <span class="check-label">Direction</span>
            <span class="check-icon">{{ isIdle ? '○' : (isDirectionValid ? '✓' : '✕') }}</span>
          </div>

          <!-- Deeplink Check -->
          <div class="check-pill" :class="isIdle ? 'pill-idle' : (isDeeplinkValid ? 'pill-pass' : 'pill-fail')">
            <span class="check-label">Deeplink</span>
            <span class="check-icon">{{ isIdle ? '○' : (isDeeplinkValid ? '✓' : '✕') }}</span>
          </div>

          <!-- Schema Check -->
          <div class="check-pill" :class="isIdle ? 'pill-idle' : (isSchemaValid ? 'pill-pass' : 'pill-fail')">
            <span class="check-label">Schema</span>
            <span class="check-icon">{{ isIdle ? '○' : (isSchemaValid ? '✓' : '✕') }}</span>
          </div>
        </div>

        <!-- Outcome Banner: VERIFIED ACTION or REJECTED ACTION -->
        <div class="verdict-bar" :class="isPass ? 'verdict-pass' : (isIdle ? 'verdict-idle' : 'verdict-fail')">
          <div class="verdict-icon-wrap">
            <svg v-if="isPass" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span v-else-if="isIdle" class="idle-dot-icon">○</span>
            <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </div>
          <span class="verdict-title">{{ verdictTitle }}</span>
        </div>

        <!-- Rejection Reason if Rejected -->
        <div v-if="!isPass && !isIdle" class="rejection-reason-row">
          <span class="reason-prefix">REASON:</span>
          <span class="reason-text">{{ displayRejectionReason }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActionCard',
  props: {
    actionData: {
      type: Object,
      default: () => ({
        action: 'Enable Auto Rotate',
        aiProposedAction: 'Enable Auto Rotate',
        sourceEvidence: 'SIIS-023',
        grounded: true,
        resolved: true
      })
    },
    validationData: {
      type: Object,
      default: () => ({
        groundingPassed: true,
        deeplinkPassed: true,
        directionPassed: true,
        schemaPassed: true,
        overallStatus: 'PASS',
        failureReasons: []
      })
    }
  },
  computed: {
    displayAction() {
      return this.actionData?.aiProposedAction || this.actionData?.action || (this.actionData?.resolved === false ? 'Unresolved Action' : 'Enable Auto Rotate');
    },
    isPass() {
      return this.validationData?.overallStatus === 'PASS';
    },
    isIdle() {
      return this.validationData?.overallStatus === 'READY' || !this.validationData?.overallStatus;
    },
    verdictTitle() {
      if (this.isPass) return '✓ VERIFIED ACTION';
      if (this.isIdle) return '○ AWAITING QUERY';
      return '✕ REJECTED ACTION';
    },
    displayWhy() {
      if (this.isPass) {
        return 'Supported by SIIS evidence';
      }
      if (this.isIdle) {
        return 'Awaiting diagnostic query';
      }
      return 'Proposed by AI policy (Unverified)';
    },
    displayEvidence() {
      return this.actionData?.sourceEvidence || this.actionData?.evidenceId || 'None';
    },
    isEvidenceValid() {
      return Boolean(this.validationData?.checks ? this.validationData.checks.evidence : this.validationData?.groundingPassed);
    },
    isRelevanceValid() {
      return Boolean(this.validationData?.checks ? this.validationData.checks.relevance : this.validationData?.groundingPassed);
    },
    isDirectionValid() {
      return Boolean(this.validationData?.checks ? this.validationData.checks.direction : this.validationData?.directionPassed);
    },
    isDeeplinkValid() {
      return Boolean(this.validationData?.checks ? this.validationData.checks.deeplink : this.validationData?.deeplinkPassed);
    },
    isSchemaValid() {
      return Boolean(this.validationData?.checks ? this.validationData.checks.schema : this.validationData?.schemaPassed);
    },
    displayRejectionReason() {
      return this.validationData?.failureReasons?.[0] || "Proposed action failed Contract Guard verification.";
    }
  }
}
</script>

<style scoped>
.action-analysis-card {
  padding: 10px 12px;
}

.ai-anchor-badge {
  font-size: 9px;
  font-weight: 700;
  color: #00d2ff;
  background: rgba(0, 210, 255, 0.08);
  border: 1px solid rgba(0, 210, 255, 0.28);
  border-radius: 4px;
  padding: 2px 6px;
  letter-spacing: 0.6px;
}

.action-body {
  display: flex;
  flex-direction: column;
}

/* 1. AI Proposal Box */
.ai-proposal-box {
  background: rgba(0, 30, 60, 0.35);
  border: 1px solid rgba(0, 210, 255, 0.2);
  border-radius: 6px;
  padding: 7px 9px;
}

.box-micro-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2px;
}

.micro-label {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.ai-label {
  color: #00d2ff;
}

.ai-status-tag {
  font-size: 8.5px;
  font-weight: 600;
  color: #79a3c8;
  letter-spacing: 0.4px;
}

.proposal-main-title {
  font-size: 12.5px;
  font-weight: 700;
  color: #ffffff;
  margin: 3px 0 6px 0;
  text-shadow: 0 0 8px rgba(0, 210, 255, 0.25);
}

.proposal-meta-grid {
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 10.5px;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-label {
  color: #6a88a7;
  font-weight: 600;
  font-size: 10px;
}

.meta-value {
  color: #d8e5f2;
  font-weight: 500;
}

.evidence-id-tag {
  color: #00f0ff;
  font-family: var(--font-mono);
  font-weight: 600;
}

/* Flow Connector Divider */
.flow-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin: 5px 0;
}

.flow-line {
  flex: 1;
  height: 1px;
  background: rgba(0, 180, 255, 0.15);
}

.flow-badge {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 9px;
  font-weight: 700;
  color: #789bbb;
  letter-spacing: 0.6px;
}

/* 2. ANCHOR Verification Box */
.anchor-verification-box {
  border-radius: 6px;
  padding: 6px 9px;
  transition: all 0.3s ease;
}

.box-pass {
  background: rgba(0, 230, 118, 0.04);
  border: 1px solid rgba(0, 230, 118, 0.28);
}

.box-fail {
  background: rgba(244, 63, 94, 0.06);
  border: 1px solid rgba(244, 63, 94, 0.35);
}

.box-idle {
  background: rgba(5, 18, 38, 0.45);
  border: 1px solid rgba(0, 180, 255, 0.15);
}

.verification-checks-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
}

.check-pill {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 600;
}

.pill-pass {
  background: rgba(0, 230, 118, 0.08);
  color: #00e676;
  border: 1px solid rgba(0, 230, 118, 0.22);
}

.pill-fail {
  background: rgba(244, 63, 94, 0.1);
  color: #f43f5e;
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.pill-idle {
  background: rgba(0, 180, 255, 0.04);
  color: #6484a4;
  border: 1px solid rgba(0, 180, 255, 0.12);
}

.check-icon {
  font-weight: 700;
  font-size: 11px;
}

.verdict-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border-radius: 4px;
  padding: 4px 8px;
  margin-top: 6px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.verdict-pass {
  background: rgba(0, 230, 118, 0.14);
  color: #00e676;
  border: 1px solid rgba(0, 230, 118, 0.35);
  box-shadow: 0 0 10px rgba(0, 230, 118, 0.2);
}

.verdict-fail {
  background: rgba(244, 63, 94, 0.14);
  color: #f43f5e;
  border: 1px solid rgba(244, 63, 94, 0.4);
  box-shadow: 0 0 10px rgba(244, 63, 94, 0.25);
}

.verdict-idle {
  background: rgba(0, 180, 255, 0.08);
  color: #7c9cb8;
  border: 1px solid rgba(0, 180, 255, 0.2);
}

.idle-dot-icon {
  font-size: 12px;
  color: #7c9cb8;
}

.rejection-reason-row {
  margin-top: 5px;
  font-size: 9.5px;
  color: #ff8095;
  display: flex;
  gap: 4px;
  align-items: flex-start;
  line-height: 1.3;
}

.reason-prefix {
  font-weight: 700;
  color: #f43f5e;
  flex-shrink: 0;
}

.reason-text {
  font-weight: 500;
}
</style>
