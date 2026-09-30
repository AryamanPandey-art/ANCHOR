<template>
  <div class="anchor-app-root">
    <!-- Left Navigation Rail -->
    <Sidebar :currentTab="currentTab" @tab-change="onTabChange" />

    <!-- Main Workspace Container -->
    <div class="workspace-container">
      <!-- Top System Header -->
      <Header 
        :sessionData="session" 
        :validationStatus="validation?.overallStatus || 'PASS'"
        :isProcessing="isProcessing"
        :currentTab="currentTab"
      />

      <!-- Main Dashboard Grid -->
      <main class="dashboard-body">
        <!-- TOP THREE-COLUMN SECTION -->
        <div class="top-columns-row">
          
          <!-- LEFT COLUMN (25%) -->
          <div class="dashboard-col left-col">
            <!-- 1. OVERVIEW: Comprehensive 3-card stack -->
            <template v-if="currentTab === 'overview'">
              <UserQueryCard 
                v-model="userQuery" 
                :isLoading="isProcessing" 
                @submit-query="runDiagnosis" 
                @reset-query="onResetQuery"
              />
              <IntentCard :intentData="intent" />
              <SiisEvidenceCard :evidenceData="evidence" />
            </template>

            <!-- 2. DIAGNOSE: Troubleshooting & Problem Intake -->
            <template v-else-if="currentTab === 'diagnose'">
              <UserQueryCard 
                v-model="userQuery" 
                :isLoading="isProcessing" 
                @submit-query="runDiagnosis" 
                @reset-query="onResetQuery"
              />
              <IntentCard :intentData="intent" />
            </template>

            <!-- 3. EVIDENCE: Samsung SIIS Documentation & Grounding -->
            <template v-else-if="currentTab === 'evidence'">
              <SiisEvidenceCard :evidenceData="evidence" />
              <IntentCard :intentData="intent" />
            </template>

            <!-- 4. SOLUTION: AI Action Proposal & Deeplink Resolution -->
            <template v-else-if="currentTab === 'solution'">
              <ActionCard 
                :actionData="action" 
                :validationData="validation"
              />
              <DeeplinkCard :deeplinkData="deeplink" />
            </template>

            <!-- 5. ENGINE: Contract Guard & Decision Engine -->
            <template v-else-if="currentTab === 'engine' || currentTab === 'settings'">
              <ValidationCard :validationData="validation" />
              <IntentCard :intentData="intent" />
            </template>
          </div>

          <!-- CENTER COLUMN (47%) - EVIDENCE GRAPH -->
          <div class="dashboard-col center-col">
            <EvidenceGraph :graphData="graph" :activeTab="currentTab" />
          </div>

          <!-- RIGHT COLUMN (28%) -->
          <div class="dashboard-col right-col">
            <!-- 1. OVERVIEW: Action, Deeplink & Contract validation -->
            <template v-if="currentTab === 'overview'">
              <ActionCard 
                :actionData="action" 
                :validationData="validation"
              />
              <DeeplinkCard :deeplinkData="deeplink" />
              <ValidationCard :validationData="validation" />
            </template>

            <!-- 2. DIAGNOSE: Proposed Action & Verification Result -->
            <template v-else-if="currentTab === 'diagnose'">
              <ActionCard 
                :actionData="action" 
                :validationData="validation"
              />
              <ValidationCard :validationData="validation" />
            </template>

            <!-- 3. EVIDENCE: Contract Grounding Validation & Deeplink Catalog Check -->
            <template v-else-if="currentTab === 'evidence'">
              <ValidationCard :validationData="validation" />
              <DeeplinkCard :deeplinkData="deeplink" />
            </template>

            <!-- 4. SOLUTION: Contract Verification Verdict & Target Intent -->
            <template v-else-if="currentTab === 'solution'">
              <ValidationCard :validationData="validation" />
              <IntentCard :intentData="intent" />
            </template>

            <!-- 5. ENGINE: Action under Verification & Catalog Deeplink -->
            <template v-else-if="currentTab === 'engine' || currentTab === 'settings'">
              <ActionCard 
                :actionData="action" 
                :validationData="validation"
              />
              <DeeplinkCard :deeplinkData="deeplink" />
            </template>
          </div>

        </div>

        <!-- BOTTOM PROOF & STATUS ROW (3 PANELS) -->
        <div class="bottom-panels-row">
          <div class="bottom-panel-col">
            <PipelineStatusPanel 
              :stages="pipelineStages" 
              :isLoading="isProcessing" 
              :overallStatus="validation?.overallStatus || 'PASS'"
              :processingStepIndex="processingStepIndex"
            />
          </div>
          <div class="bottom-panel-col">
            <EvidenceProofPanel :evidenceData="evidence" />
          </div>
          <div class="bottom-panel-col">
            <ProofVerificationPanel :validationData="validation" />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Header from './components/Header.vue';
import UserQueryCard from './components/UserQueryCard.vue';
import IntentCard from './components/IntentCard.vue';
import SiisEvidenceCard from './components/SiisEvidenceCard.vue';
import EvidenceGraph from './components/EvidenceGraph.vue';
import ActionCard from './components/ActionCard.vue';
import DeeplinkCard from './components/DeeplinkCard.vue';
import ValidationCard from './components/ValidationCard.vue';
import PipelineStatusPanel from './components/PipelineStatusPanel.vue';
import EvidenceProofPanel from './components/EvidenceProofPanel.vue';
import ProofVerificationPanel from './components/ProofVerificationPanel.vue';

export default {
  name: 'App',
  components: {
    Sidebar,
    Header,
    UserQueryCard,
    IntentCard,
    SiisEvidenceCard,
    EvidenceGraph,
    ActionCard,
    DeeplinkCard,
    ValidationCard,
    PipelineStatusPanel,
    EvidenceProofPanel,
    ProofVerificationPanel
  },
  data() {
    return {
      currentTab: 'overview',
      isProcessing: false,
      processingStepIndex: 0,
      processingTimer: null,
      userQuery: "My Nexa A14 screen looks distorted right after I received the phone and I need a test.",
      
      // Verified runtime pipeline state
      session: {
        systemStatus: "SYSTEM ONLINE"
      },
      intent: {
        intent: "SCREEN_ROTATION",
        category: "Display & Rotation",
        deviceType: "Smartphone (Galaxy)",
        osVersion: "One UI 6.x",
        ambiguous: false
      },
      evidence: {
        evidenceId: "#SIIS-023",
        source: "Samsung SIIS",
        section: "Display > Screen rotation",
        grounded: true,
        excerpt: "... To enable auto rotate, go to Settings > Display > Screen rotation and turn on Auto rotate ...",
        provenance: "Samsung PRISM Student Kit Dataset"
      },
      action: {
        action: "Enable Auto Rotate",
        aiProposedAction: "Enable Auto Rotate",
        sourceEvidence: "SIIS-023",
        grounded: true,
        resolved: true,
        condition: "Auto rotate = OFF"
      },
      deeplink: {
        candidate: "Enable Auto Rotate",
        deeplink: "voiceassist://masked/act/7c340914be",
        direction: "ENABLE",
        catalogMatch: "VALID",
        verified: true
      },
      validation: {
        groundingPassed: true,
        deeplinkPassed: true,
        directionPassed: true,
        schemaPassed: true,
        overallStatus: "PASS",
        failureReasons: []
      },
      pipelineStages: [
        { name: "Query Processed", completed: true },
        { name: "Intent Identified", completed: true },
        { name: "Evidence Retrieved", completed: true },
        { name: "Action Resolved", completed: true },
        { name: "Contract Validated", completed: true }
      ],
      graph: null
    };
  },
  mounted() {
    this.runDiagnosis(this.userQuery);
  },
  beforeUnmount() {
    if (this.processingTimer) clearInterval(this.processingTimer);
  },
  methods: {
    onTabChange(tab) {
      this.currentTab = tab;
    },
    onResetQuery() {
      if (this.processingTimer) clearInterval(this.processingTimer);
      this.isProcessing = false;
      this.userQuery = "";
      this.intent = {
        intent: "READY",
        category: "Awaiting Query",
        deviceType: "Smartphone (Galaxy)",
        osVersion: "One UI 6.x",
        ambiguous: false
      };
      this.evidence = {
        evidenceId: "None",
        source: "Samsung SIIS",
        section: "None",
        grounded: false,
        excerpt: "Enter or select a troubleshooting query to initiate evidence retrieval and proof synthesis.",
        provenance: "Awaiting Input"
      };
      this.action = {
        action: "No Action Proposed",
        aiProposedAction: "Awaiting Input",
        sourceEvidence: "None",
        grounded: false,
        resolved: false,
        condition: "Idle"
      };
      this.deeplink = {
        candidate: "None",
        deeplink: null,
        direction: "NONE",
        catalogMatch: "IDLE",
        verified: false
      };
      this.validation = {
        groundingPassed: false,
        deeplinkPassed: false,
        directionPassed: false,
        schemaPassed: false,
        overallStatus: "READY",
        failureReasons: []
      };
      this.graph = {
        nodes: [
          {
            id: "node-complaint",
            type: "evidence",
            title: "User Complaint",
            subtitle: "Awaiting input...",
            icon: "chat",
            x: 525,
            y: 75,
            textSide: "right"
          },
          {
            id: "node-device",
            type: "evidence",
            title: "Device Context",
            subtitle: "Galaxy S23\nOne UI 6.x",
            icon: "device",
            x: 385,
            y: 200,
            textSide: "bottom"
          },
          {
            id: "node-intent",
            type: "evidence",
            title: "Intent",
            subtitle: "Ready\n○ Idle",
            icon: "intent",
            x: 525,
            y: 165,
            textSide: "right"
          },
          {
            id: "node-related",
            type: "evidence",
            title: "Related Issues",
            subtitle: "Awaiting Query",
            icon: "related",
            x: 675,
            y: 215,
            textSide: "right"
          },
          {
            id: "node-evidence",
            type: "evidence",
            title: "SIIS Evidence",
            subtitle: "Awaiting Query\n(Unresolved)",
            icon: "document",
            x: 525,
            y: 275,
            textSide: "right"
          },
          {
            id: "node-condition",
            type: "evidence",
            title: "ANCHOR Check",
            subtitle: "State Undetermined\n○ Idle",
            icon: "gear",
            x: 415,
            y: 390,
            textSide: "right"
          },
          {
            id: "node-action",
            type: "evidence",
            title: "AI Proposal",
            subtitle: "No Action Proposed\n○ Idle",
            icon: "lightning",
            x: 635,
            y: 385,
            textSide: "right"
          },
          {
            id: "node-deeplink",
            type: "evidence",
            title: "Samsung Deeplink",
            subtitle: "None",
            icon: "link",
            x: 530,
            y: 480,
            textSide: "right"
          },
          {
            id: "node-validation",
            type: "evidence",
            title: "Decision Engine",
            subtitle: "Engine Ready • Awaiting Input",
            icon: "shield",
            x: 472,
            y: 565,
            textSide: "right"
          }
        ],
        edges: []
      };
      this.pipelineStages = [
        { name: "Query Processed", completed: false },
        { name: "Intent Identified", completed: false },
        { name: "Evidence Retrieved", completed: false },
        { name: "Action Resolved", completed: false },
        { name: "Contract Validated", completed: false }
      ];
    },
    async runDiagnosis(queryText) {
      const targetQuery = (queryText !== undefined && queryText !== null && queryText !== "") 
        ? queryText 
        : this.userQuery;

      if (!targetQuery || !targetQuery.trim()) return;

      this.isProcessing = true;
      this.processingStepIndex = 0;

      // Start sequential processing steps animation
      if (this.processingTimer) clearInterval(this.processingTimer);
      this.processingTimer = setInterval(() => {
        if (this.processingStepIndex < 5) {
          this.processingStepIndex++;
        }
      }, 120);

      const minProcessingTime = new Promise(resolve => setTimeout(resolve, 750));

      try {
        const fetchPromise = fetch('/api/diagnose', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: targetQuery })
        });

        const [response] = await Promise.all([fetchPromise, minProcessingTime]);

        if (response.ok) {
          const data = await response.json();
          this.session = data.session || this.session;
          this.intent = data.intent;
          this.evidence = data.evidence;
          this.action = data.action;
          this.deeplink = data.deeplink;
          this.validation = data.validation;
          this.graph = data.graph;
          this.pipelineStages = data.pipelineStages;
        } else {
          this.handlePipelineError(targetQuery, `Server returned HTTP ${response.status}`);
        }
      } catch (err) {
        console.warn('Backend API connection error:', err);
        await minProcessingTime;
        this.handlePipelineError(targetQuery, 'Connection error: Unable to reach ANCHOR backend engine.');
      } finally {
        if (this.processingTimer) clearInterval(this.processingTimer);
        this.isProcessing = false;
      }
    },
    handlePipelineError(targetQuery, errMessage) {
      this.intent = {
        intent: "PIPELINE_ERROR",
        category: "System Error",
        deviceType: "Unknown",
        osVersion: "Unknown",
        ambiguous: true
      };
      this.evidence = {
        evidenceId: "None",
        source: "Samsung SIIS",
        section: "None",
        grounded: false,
        excerpt: "Pipeline execution encountered an unexpected connection error. No evidence could be verified.",
        provenance: "System Fallback"
      };
      this.action = {
        action: "No Action Authorized",
        aiProposedAction: "None",
        sourceEvidence: "None",
        grounded: false,
        resolved: false,
        condition: "Error"
      };
      this.deeplink = {
        candidate: "None",
        deeplink: null,
        direction: "NONE",
        catalogMatch: "INVALID",
        verified: false
      };
      this.validation = {
        groundingPassed: false,
        deeplinkPassed: false,
        directionPassed: false,
        schemaPassed: false,
        overallStatus: "FAIL",
        failureReasons: [
          errMessage || "PIPELINE ERROR: Unable to complete verification. No action was authorized."
        ]
      };
      this.graph = {
        nodes: [
          {
            id: "node-complaint",
            type: "evidence",
            title: "User Complaint",
            subtitle: `"${targetQuery}"`,
            icon: "chat",
            x: 525,
            y: 75,
            textSide: "right"
          },
          {
            id: "node-validation",
            type: "rejected",
            title: "Pipeline Error",
            subtitle: "No action was authorized (FAIL)",
            icon: "shield",
            x: 472,
            y: 565,
            textSide: "right"
          }
        ],
        edges: []
      };
      this.pipelineStages = [
        { name: "Query Processed", completed: true, failed: false },
        { name: "Intent Identified", completed: false, failed: true },
        { name: "Evidence Retrieved", completed: false, failed: true },
        { name: "Action Resolved", completed: false, failed: true },
        { name: "Contract Validated", completed: false, failed: true }
      ];
    }
  }
}
</script>

<style scoped>
.anchor-app-root {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: var(--bg-main);
}

.workspace-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.dashboard-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 10px;
  gap: 10px;
  overflow: hidden;
  background-color: var(--bg-main);
}

/* TOP ROW: 3 COLUMNS */
.top-columns-row {
  display: flex;
  flex: 1;
  gap: 10px;
  min-height: 0;
}

/* COLUMN PROPORTIONS */
.dashboard-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
}

.left-col {
  flex: 0 0 25%;
  max-width: 25%;
}

.center-col {
  flex: 0 0 47%;
  max-width: 47%;
}

.right-col {
  flex: 0 0 28%;
  max-width: 28%;
}

/* BOTTOM PANELS ROW (3 EQUAL COLUMNS) */
.bottom-panels-row {
  display: flex;
  height: 116px;
  min-height: 116px;
  max-height: 116px;
  gap: 10px;
  flex-shrink: 0;
}

.bottom-panel-col {
  flex: 1;
  min-width: 0;
  height: 100%;
}
</style>
