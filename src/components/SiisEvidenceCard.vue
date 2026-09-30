<template>
  <div class="anchor-card siis-evidence-card">
    <div class="card-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <ellipse cx="12" cy="5" rx="9" ry="3"/>
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
          </svg>
        </span>
        <span class="card-title">SIIS EVIDENCE</span>
      </div>
      <div class="evidence-proof-tag">
        <span>GROUNDED PROOF</span>
      </div>
    </div>

    <!-- Prominent Evidence Banner -->
    <div class="prominent-evidence-banner">
      <div class="evidence-main-line">
        <span class="evidence-badge-id">{{ evidenceData?.evidenceId || '#SIIS-023' }}</span>
        <div class="evidence-grounded-pill" :class="evidenceData?.grounded ? 'pill-grounded' : 'pill-unresolved'">
          <svg v-if="evidenceData?.grounded" viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span v-else>✕</span>
          <span>{{ evidenceData?.grounded ? 'GROUNDED' : 'UNRESOLVED' }}</span>
        </div>
      </div>
      <div class="evidence-section-line">
        <span class="section-icon">›</span>
        <span class="section-path">{{ evidenceData?.section || 'Display > Screen rotation' }}</span>
      </div>
    </div>

    <!-- Prominent Evidence Quote Excerpt Box -->
    <div class="evidence-excerpt-box">
      <div class="excerpt-header">
        <span class="quote-mark">“</span>
        <span class="excerpt-source-label">{{ evidenceData?.source || 'Samsung SIIS' }} Documentation Excerpt</span>
      </div>
      <p class="excerpt-text">
        {{ evidenceData?.excerpt || '... To enable auto rotate, go to Settings > Display > Screen rotation and turn on Auto rotate ...' }}
      </p>
    </div>

    <!-- Provenance metadata bar -->
    <div class="evidence-footer-provenance">
      <span class="prov-label">PROVENANCE:</span>
      <span class="prov-value">{{ evidenceData?.provenance || 'Samsung PRISM Student Kit Dataset' }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SiisEvidenceCard',
  props: {
    evidenceData: {
      type: Object,
      default: () => ({
        evidenceId: '#SIIS-023',
        source: 'Samsung SIIS',
        section: 'Display > Screen rotation',
        grounded: true,
        excerpt: '... To enable auto rotate, go to Settings > Display > Screen rotation and turn on Auto rotate ...',
        provenance: 'Samsung Student Kit (siis_responses.json)'
      })
    }
  }
}
</script>

<style scoped>
.siis-evidence-card {
  padding: 10px 12px;
}

.evidence-proof-tag {
  font-size: 8.5px;
  font-weight: 700;
  color: var(--color-cyan);
  background: rgba(0, 240, 255, 0.08);
  border: 1px solid rgba(0, 240, 255, 0.22);
  border-radius: 4px;
  padding: 2px 6px;
  letter-spacing: 0.5px;
}

.prominent-evidence-banner {
  background: rgba(0, 24, 48, 0.45);
  border: 1px solid rgba(0, 180, 255, 0.22);
  border-radius: 6px;
  padding: 7px 9px;
  margin-bottom: 7px;
}

.evidence-main-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.evidence-badge-id {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: #00f0ff;
  letter-spacing: 0.5px;
  text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
}

.evidence-grounded-pill {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.4px;
}

.pill-grounded {
  background: rgba(0, 230, 118, 0.12);
  color: #00e676;
  border: 1px solid rgba(0, 230, 118, 0.3);
}

.pill-unresolved {
  background: rgba(244, 63, 94, 0.12);
  color: #f43f5e;
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.evidence-section-line {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
}

.section-icon {
  color: #00d2ff;
  font-weight: 700;
  font-size: 11px;
}

.section-path {
  font-size: 11px;
  color: #c4d7ec;
  font-weight: 600;
}

/* Excerpt Box */
.evidence-excerpt-box {
  background: rgba(3, 10, 22, 0.6);
  border-left: 2.5px solid #00f0ff;
  border-radius: 0 6px 6px 0;
  padding: 6px 8px;
  margin-bottom: 6px;
}

.excerpt-header {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 2px;
}

.quote-mark {
  color: #00f0ff;
  font-size: 14px;
  font-family: serif;
  line-height: 1;
}

.excerpt-source-label {
  font-size: 9.5px;
  color: #7997b6;
  font-weight: 600;
}

.excerpt-text {
  margin: 0;
  font-size: 10px;
  color: #a8c4de;
  line-height: 1.4;
  font-style: italic;
}

/* Provenance Footer */
.evidence-footer-provenance {
  display: flex;
  gap: 4px;
  font-size: 8.5px;
  color: #5c7b9c;
  align-items: center;
}

.prov-label {
  font-weight: 700;
  color: #4b6685;
}

.prov-value {
  color: #7998b8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
