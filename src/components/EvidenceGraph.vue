<template>
  <div class="anchor-card evidence-graph-container" ref="graphContainer">
    <!-- Graph Header -->
    <div class="card-header graph-header">
      <div class="card-header-left">
        <span class="card-header-icon">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="18" cy="5" r="3"/>
            <circle cx="6" cy="12" r="3"/>
            <circle cx="18" cy="19" r="3"/>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
          </svg>
        </span>
        <span class="card-title">EVIDENCE GRAPH</span>
      </div>

      <!-- Graph Legend matching reference -->
      <div class="graph-legend">
        <div class="legend-item">
          <span class="legend-dot dot-evidence"></span>
          <span class="legend-text">Evidence</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot dot-action"></span>
          <span class="legend-text">Action</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot dot-validation"></span>
          <span class="legend-text">Validation</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot dot-source"></span>
          <span class="legend-text">Source</span>
        </div>
      </div>
    </div>

    <!-- Interactive Graph Canvas Area -->
    <div 
      class="graph-canvas-area"
      @mousedown="startPan"
      @mousemove="onPan"
      @mouseup="endPan"
      @mouseleave="endPan"
      @wheel.prevent="onWheel"
    >
      <svg 
        class="graph-svg" 
        viewBox="320 30 460 590" 
        preserveAspectRatio="xMidYMid meet"
        ref="svgCanvas"
      >
        <defs>
          <!-- Background radial glow -->
          <radialGradient id="graphBgGlow" cx="50%" cy="40%" r="65%">
            <stop offset="0%" stop-color="#091b35" stop-opacity="0.7"/>
            <stop offset="60%" stop-color="#050d1a" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#030710" stop-opacity="1"/>
          </radialGradient>

          <!-- Grid dot pattern -->
          <pattern id="graphDotGrid" width="30" height="30" patternUnits="userSpaceOnUse">
            <circle cx="15" cy="15" r="0.8" fill="rgba(0, 180, 255, 0.12)"/>
          </pattern>

          <!-- Node glow filters -->
          <filter id="cyanGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>

          <filter id="greenGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>

          <filter id="purpleGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>

          <filter id="redGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>

          <!-- Arrow markers -->
          <marker id="arrow-cyan" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#00d2ff"/>
          </marker>
          <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#00e676"/>
          </marker>
          <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#8b5cf6"/>
          </marker>
          <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#f43f5e"/>
          </marker>
        </defs>

        <!-- Background grid and backdrop glow -->
        <rect width="1000" height="620" fill="url(#graphBgGlow)"/>
        <rect width="1000" height="620" fill="url(#graphDotGrid)"/>

        <!-- Transformable Scene Container (Pan & Zoom) -->
        <g :transform="`translate(${panX}, ${panY}) scale(${zoomScale})`">

          <!-- EDGES LAYER -->
          <g class="edges-group">
            <g v-for="(edge, idx) in renderedEdges" :key="idx">
              <!-- Background edge trace -->
              <path 
                :d="edge.d" 
                class="edge-background" 
              />
              
              <!-- Active illuminated glowing edge -->
              <path 
                :d="edge.d" 
                class="edge-line" 
                :class="{ 
                  'edge-active': edge.active, 
                  'edge-green': edge.isGreen,
                  'edge-purple': edge.isPurple,
                  'edge-red': edge.isRed
                }"
                :marker-end="edge.marker"
              />

              <!-- Flowing light particle pulses along the active edges -->
              <circle v-if="edge.active" r="2.8" :fill="edge.particleColor" filter="url(#cyanGlow)">
                <animateMotion 
                  :path="edge.d" 
                  :dur="edge.dur || '3.2s'" 
                  repeatCount="indefinite"
                  rotate="auto"
                />
              </circle>
            </g>
          </g>

          <!-- NODES LAYER -->
          <g class="nodes-group">
            <g 
              v-for="node in graphNodes" 
              :key="node.id"
              class="graph-node-group"
              :class="{ selected: selectedNodeId === node.id }"
              @click.stop="selectNode(node)"
            >
              <!-- Outer halo ring on hover/select -->
              <circle 
                :cx="node.x" 
                :cy="node.y" 
                :r="selectedNodeId === node.id ? 25 : 21" 
                class="node-halo"
                :class="getNodeColorClass(node.type)"
              />

              <!-- Core Node Circle -->
              <circle 
                :cx="node.x" 
                :cy="node.y" 
                r="17" 
                class="node-core"
                :class="getNodeColorClass(node.type)"
                :filter="getNodeFilter(node.type)"
              />

              <!-- Center Icon inside node -->
              <g :transform="`translate(${node.x - 9}, ${node.y - 9})`" class="node-icon" :class="getNodeIconColorClass(node.type)">
                <!-- Chat/Complaint icon -->
                <svg v-if="node.icon === 'chat'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>

                <!-- Smartphone/Device icon -->
                <svg v-else-if="node.icon === 'device'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect width="14" height="20" x="5" y="2" rx="2" ry="2"/>
                  <line x1="12" y1="18" x2="12.01" y2="18"/>
                </svg>

                <!-- Screen/Intent icon -->
                <svg v-else-if="node.icon === 'intent'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect width="18" height="14" x="3" y="5" rx="2"/>
                  <line x1="12" y1="19" x2="12" y2="19"/>
                </svg>

                <!-- Related Issues icon -->
                <svg v-else-if="node.icon === 'related'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect width="16" height="16" x="4" y="4" rx="2"/>
                  <line x1="8" y1="10" x2="16" y2="10"/>
                  <line x1="8" y1="14" x2="14" y2="14"/>
                </svg>

                <!-- SIIS Evidence / Document icon -->
                <svg v-else-if="node.icon === 'document'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>

                <!-- Condition / Gear icon -->
                <svg v-else-if="node.icon === 'gear'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>

                <!-- Action / Lightning bolt icon -->
                <svg v-else-if="node.icon === 'lightning'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>

                <!-- Link / Deeplink icon -->
                <svg v-else-if="node.icon === 'link'" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>

                <!-- Shield / Validated icon -->
                <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </g>

              <!-- Node Text Labels matching screenshot placement -->
              <g class="node-label-group">
                <text 
                  :x="getTextX(node)" 
                  :y="getTextY(node)" 
                  class="node-title-text"
                  :class="{ 
                    'text-green': node.type === 'action',
                    'text-purple': node.type === 'validation',
                    'text-red': node.type === 'rejected',
                    'text-align-center': isCenteredNode(node)
                  }"
                  :text-anchor="getTextAnchor(node)"
                >
                  {{ node.title }}
                </text>

                <!-- Multi-line subtitle lines -->
                <text 
                  v-for="(line, lIdx) in getSubtitleLines(node.subtitle)"
                  :key="lIdx"
                  :x="getTextX(node)"
                  :y="getTextY(node) + 13 + (lIdx * 11)"
                  class="node-subtitle-text"
                  :class="{ 
                    'sub-green': node.type === 'action',
                    'sub-red': node.type === 'rejected',
                    'sub-deeplink': node.icon === 'link' 
                  }"
                  :text-anchor="getTextAnchor(node)"
                >
                  {{ line }}
                </text>
              </g>
            </g>
          </g>

        </g>
      </svg>

      <!-- Floating Zoom & Reset Controls in bottom right of graph card -->
      <div class="graph-floating-controls">
        <button class="ctrl-btn" @click="resetView" title="Center View">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="22" y1="12" x2="18" y2="12"/>
            <line x1="6" y1="12" x2="2" y2="12"/>
            <line x1="12" y1="6" x2="12" y2="2"/>
            <line x1="12" y1="22" x2="12" y2="18"/>
          </svg>
        </button>
        <button class="ctrl-btn" @click="zoomIn" title="Zoom In">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
        </button>
        <button class="ctrl-btn" @click="zoomOut" title="Zoom Out">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
        </button>
        <button class="ctrl-btn" @click="toggleFullscreen" title="Fit to Screen">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 3 21 3 21 9"/>
            <polyline points="9 21 3 21 3 15"/>
            <line x1="21" y1="3" x2="14" y2="10"/>
            <line x1="3" y1="21" x2="10" y2="14"/>
          </svg>
        </button>
      </div>

      <!-- Node Details Tooltip Overlay when a node is selected -->
      <transition name="fade">
        <div v-if="selectedNode" class="node-tooltip-card">
          <div class="tooltip-header">
            <span class="tooltip-title">{{ selectedNode.title }}</span>
            <button class="tooltip-close" @click="selectedNodeId = null">✕</button>
          </div>
          <div class="tooltip-content">
            <p>{{ selectedNode.subtitle }}</p>
            <span class="tooltip-badge" :class="selectedNode.type">{{ selectedNode.type }}</span>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EvidenceGraph',
  props: {
    graphData: {
      type: Object,
      default: () => null
    },
    activeTab: {
      type: String,
      default: 'overview'
    }
  },
  watch: {
    activeTab: {
      immediate: true,
      handler(newTab) {
        if (newTab === 'diagnose') {
          this.selectedNodeId = 'node-complaint';
        } else if (newTab === 'evidence') {
          this.selectedNodeId = 'node-evidence';
        } else if (newTab === 'solution') {
          this.selectedNodeId = 'node-action';
        } else if (newTab === 'engine') {
          this.selectedNodeId = 'node-validation';
        } else {
          this.selectedNodeId = null;
        }
      }
    }
  },
  data() {
    return {
      panX: 0,
      panY: 0,
      zoomScale: 1,
      isPanning: false,
      startX: 0,
      startY: 0,
      selectedNodeId: null
    };
  },
  computed: {
    graphNodes() {
      if (this.graphData?.nodes && this.graphData.nodes.length) {
        return this.graphData.nodes.map(node => ({
          ...node,
          textSide: node.textSide || (node.id === 'node-device' ? 'bottom' : 'right')
        }));
      }
      // Default nodes arranged exactly matching the reference screenshot
      return [
        {
          id: "node-complaint",
          type: "evidence",
          title: "User Complaint",
          subtitle: '"My screen isn\'t rotating automatically."',
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
          subtitle: "Screen Rotation\n✓ Identified",
          icon: "intent",
          x: 525,
          y: 165,
          textSide: "right"
        },
        {
          id: "node-related",
          type: "evidence",
          title: "Related Issues",
          subtitle: "• Orientation Lock\n• Auto Rotate\n• Motion Sensor",
          icon: "related",
          x: 675,
          y: 215,
          textSide: "right"
        },
        {
          id: "node-evidence",
          type: "evidence",
          title: "SIIS Evidence",
          subtitle: "#SIIS-023\nDisplay > Screen rotation",
          icon: "document",
          x: 525,
          y: 275,
          textSide: "right"
        },
        {
          id: "node-condition",
          type: "evidence",
          title: "Condition",
          subtitle: "Auto rotate = OFF\n✓ State Requirement",
          icon: "gear",
          x: 415,
          y: 390,
          textSide: "right"
        },
        {
          id: "node-action",
          type: "action",
          title: "Action",
          subtitle: "Enable Auto Rotate\n✓ Grounded Action",
          icon: "lightning",
          x: 635,
          y: 385,
          textSide: "right"
        },
        {
          id: "node-deeplink",
          type: "evidence",
          title: "Samsung Deeplink",
          subtitle: "act/7c340914be\n(Screen Rotation)",
          icon: "link",
          x: 530,
          y: 480,
          textSide: "right"
        },
        {
          id: "node-validation",
          type: "validation",
          title: "Validated Response",
          subtitle: "Grounded • Verified • Ready",
          icon: "shield",
          x: 472,
          y: 565,
          textSide: "right"
        }
      ];
    },
    renderedEdges() {
      // Connect nodes matching screenshot path or dynamic backend edges
      const nodeMap = {};
      this.graphNodes.forEach(n => { nodeMap[n.id] = n; });

      const edgeDefs = (this.graphData?.edges && this.graphData.edges.length)
        ? this.graphData.edges
        : [
            { from: "node-complaint", to: "node-device", active: true, curvature: -0.22, dur: '3.4s' },
            { from: "node-complaint", to: "node-intent", active: true, curvature: 0, dur: '2.5s' },
            { from: "node-intent", to: "node-related", active: true, curvature: 0.18, dur: '3.2s' },
            { from: "node-intent", to: "node-evidence", active: true, curvature: 0, dur: '2.4s' },
            { from: "node-device", to: "node-condition", active: true, curvature: -0.18, dur: '3.6s' },
            { from: "node-evidence", to: "node-condition", active: true, curvature: -0.22, dur: '2.8s' },
            { from: "node-evidence", to: "node-action", active: true, curvature: 0.22, isGreen: true, dur: '2.8s' },
            { from: "node-condition", to: "node-action", active: false, curvature: 0.08, dur: '4s' },
            { from: "node-condition", to: "node-deeplink", active: true, curvature: -0.18, dur: '2.6s' },
            { from: "node-action", to: "node-deeplink", active: true, curvature: 0.18, isGreen: true, dur: '2.6s' },
            { from: "node-deeplink", to: "node-validation", active: true, curvature: -0.12, isPurple: true, dur: '2.5s' }
          ];

      return edgeDefs.map(ed => {
        const source = nodeMap[ed.from];
        const target = nodeMap[ed.to];
        if (!source || !target) return null;

        // Calculate smooth curved path
        const dx = target.x - source.x;
        const dy = target.y - source.y;
        const cx = (source.x + target.x) / 2 + (dy * ed.curvature);
        const cy = (source.y + target.y) / 2 - (dx * ed.curvature);

        const d = `M ${source.x} ${source.y} Q ${cx} ${cy} ${target.x} ${target.y}`;
        
        let marker = 'url(#arrow-cyan)';
        let particleColor = '#00f0ff';
        if (ed.isRed) {
          marker = 'url(#arrow-red)';
          particleColor = '#f43f5e';
        } else if (ed.isGreen) {
          marker = 'url(#arrow-green)';
          particleColor = '#00e676';
        } else if (ed.isPurple) {
          marker = 'url(#arrow-purple)';
          particleColor = '#a855f7';
        }

        return {
          d,
          active: ed.active,
          isGreen: ed.isGreen,
          isPurple: ed.isPurple,
          isRed: ed.isRed,
          marker,
          particleColor,
          dur: ed.dur
        };
      }).filter(Boolean);
    },
    selectedNode() {
      if (!this.selectedNodeId) return null;
      return this.graphNodes.find(n => n.id === this.selectedNodeId);
    }
  },
  methods: {
    getNodeColorClass(type) {
      if (type === 'action') return 'color-action';
      if (type === 'validation') return 'color-validation';
      if (type === 'rejected') return 'color-rejected';
      if (type === 'source') return 'color-source';
      return 'color-evidence';
    },
    getNodeIconColorClass(type) {
      if (type === 'action') return 'icon-action';
      if (type === 'validation') return 'icon-validation';
      if (type === 'rejected') return 'icon-rejected';
      if (type === 'source') return 'icon-source';
      return 'icon-evidence';
    },
    getNodeFilter(type) {
      if (type === 'action') return 'url(#greenGlow)';
      if (type === 'validation') return 'url(#purpleGlow)';
      if (type === 'rejected') return 'url(#redGlow)';
      return 'url(#cyanGlow)';
    },
    getTextX(node) {
      if (node.textSide === 'bottom') return node.x;
      return node.x + 28;
    },
    getTextY(node) {
      if (node.textSide === 'bottom') return node.y + 32;
      return node.y - 2;
    },
    getTextAnchor(node) {
      if (node.textSide === 'bottom') return 'middle';
      return 'start';
    },
    isCenteredNode(node) {
      return node.textSide === 'bottom';
    },
    getSubtitleLines(subtitle) {
      if (!subtitle) return [];
      return subtitle.split('\n');
    },
    selectNode(node) {
      this.selectedNodeId = node.id;
    },
    // Pan and Zoom logic
    startPan(e) {
      if (e.target.closest('.graph-floating-controls') || e.target.closest('.node-tooltip-card')) return;
      this.isPanning = true;
      this.startX = e.clientX - this.panX;
      this.startY = e.clientY - this.panY;
    },
    onPan(e) {
      if (!this.isPanning) return;
      this.panX = e.clientX - this.startX;
      this.panY = e.clientY - this.startY;
    },
    endPan() {
      this.isPanning = false;
    },
    onWheel(e) {
      const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
      const newScale = this.zoomScale * zoomFactor;
      if (newScale >= 0.6 && newScale <= 2.2) {
        this.zoomScale = newScale;
      }
    },
    zoomIn() {
      if (this.zoomScale < 2.0) this.zoomScale += 0.15;
    },
    zoomOut() {
      if (this.zoomScale > 0.6) this.zoomScale -= 0.15;
    },
    resetView() {
      this.panX = 0;
      this.panY = 0;
      this.zoomScale = 1;
      this.selectedNodeId = null;
    },
    toggleFullscreen() {
      this.resetView();
    }
  }
}
</script>

<style scoped>
.evidence-graph-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 12px 14px 10px 14px;
  overflow: hidden;
  position: relative;
}

.graph-header {
  margin-bottom: 6px;
  flex-shrink: 0;
}

.graph-legend {
  display: flex;
  align-items: center;
  gap: 14px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-dot {
  width: 6.5px;
  height: 6.5px;
  border-radius: 50%;
}

.dot-evidence {
  background-color: var(--color-cyan);
  box-shadow: 0 0 6px var(--color-cyan);
}

.dot-action {
  background-color: var(--color-green);
  box-shadow: 0 0 6px var(--color-green);
}

.dot-validation {
  background-color: var(--color-purple);
  box-shadow: 0 0 6px var(--color-purple);
}

.dot-source {
  background-color: var(--color-orange);
  box-shadow: 0 0 6px var(--color-orange);
}

.legend-text {
  font-size: 10.5px;
  color: #7997b6;
  font-weight: 500;
}

/* Canvas Area */
.graph-canvas-area {
  flex: 1;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  cursor: grab;
  border: 1px solid rgba(0, 180, 255, 0.12);
  background-color: #030710;
}

.graph-canvas-area:active {
  cursor: grabbing;
}

.graph-svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* Edges */
.edge-background {
  fill: none;
  stroke: rgba(0, 180, 255, 0.12);
  stroke-width: 2.2px;
}

.edge-line {
  fill: none;
  stroke: rgba(0, 180, 255, 0.35);
  stroke-width: 1.8px;
  transition: stroke 0.3s ease;
}

.edge-line.edge-active {
  stroke: #00d2ff;
  stroke-width: 2px;
  filter: drop-shadow(0 0 4px rgba(0, 240, 255, 0.6));
}

.edge-line.edge-green {
  stroke: #00e676;
  filter: drop-shadow(0 0 4px rgba(0, 230, 118, 0.6));
}

.edge-line.edge-purple {
  stroke: #8b5cf6;
  filter: drop-shadow(0 0 4px rgba(139, 92, 246, 0.6));
}

.edge-line.edge-red {
  stroke: #f43f5e;
  filter: drop-shadow(0 0 5px rgba(244, 63, 94, 0.7));
}

/* Nodes */
.graph-node-group {
  cursor: pointer;
  transition: transform 0.15s ease;
}

.graph-node-group:hover .node-halo {
  opacity: 0.8;
  transform: scale(1.1);
}

.node-halo {
  fill: transparent;
  stroke-width: 1.5px;
  opacity: 0.4;
  transition: all 0.2s ease;
}

.node-halo.color-evidence {
  stroke: #00f0ff;
}

.node-halo.color-action {
  stroke: #00e676;
}

.node-halo.color-validation {
  stroke: #8b5cf6;
}

.node-halo.color-rejected {
  stroke: #f43f5e;
}

.node-core {
  stroke-width: 2px;
  transition: all 0.2s ease;
}

.node-core.color-evidence {
  fill: #06152a;
  stroke: #00f0ff;
}

.node-core.color-action {
  fill: #042416;
  stroke: #00e676;
}

.node-core.color-validation {
  fill: #190c33;
  stroke: #8b5cf6;
}

.node-core.color-rejected {
  fill: #290811;
  stroke: #f43f5e;
}

.node-icon {
  pointer-events: none;
}

.icon-evidence {
  color: #00f0ff;
}

.icon-action {
  color: #00e676;
}

.icon-validation {
  color: #c084fc;
}

.icon-rejected {
  color: #f43f5e;
}

/* Node Text */
.node-title-text {
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 700;
  fill: #ffffff;
  letter-spacing: 0.02em;
}

.node-title-text.text-green {
  fill: #00e676;
}

.node-title-text.text-purple {
  fill: #c084fc;
}

.node-title-text.text-red {
  fill: #f43f5e;
}

.node-subtitle-text {
  font-family: var(--font-sans);
  font-size: 9.5px;
  fill: #8ba5bf;
  letter-spacing: 0.01em;
}

.node-subtitle-text.sub-green {
  fill: #00e676;
  font-weight: 500;
}

.node-subtitle-text.sub-red {
  fill: #ff8095;
  font-weight: 500;
}

.node-subtitle-text.sub-deeplink {
  font-family: var(--font-mono);
  font-size: 9px;
  fill: #38bdf8;
}

/* Floating Controls */
.graph-floating-controls {
  position: absolute;
  right: 14px;
  bottom: 14px;
  display: flex;
  flex-direction: column;
  background: rgba(4, 10, 20, 0.85);
  border: 1px solid rgba(0, 180, 255, 0.25);
  border-radius: 6px;
  backdrop-filter: blur(8px);
  padding: 2px;
  gap: 2px;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.ctrl-btn {
  width: 26px;
  height: 26px;
  background: transparent;
  border: none;
  color: #7997b6;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.ctrl-btn:hover {
  background: rgba(0, 240, 255, 0.15);
  color: var(--color-cyan);
}

/* Tooltip overlay on node selection */
.node-tooltip-card {
  position: absolute;
  left: 14px;
  bottom: 14px;
  background: rgba(6, 14, 28, 0.95);
  border: 1px solid rgba(0, 240, 255, 0.35);
  border-radius: 6px;
  padding: 8px 12px;
  max-width: 220px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
  z-index: 12;
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.tooltip-title {
  font-size: 11px;
  font-weight: 700;
  color: #00f0ff;
}

.tooltip-close {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-size: 10px;
}

.tooltip-close:hover {
  color: #fff;
}

.tooltip-content p {
  font-size: 10px;
  color: #cbd5e1;
  white-space: pre-line;
  margin-bottom: 6px;
}

.tooltip-badge {
  font-size: 9px;
  text-transform: uppercase;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 3px;
}

.tooltip-badge.evidence {
  background: rgba(0, 240, 255, 0.15);
  color: #00f0ff;
}

.tooltip-badge.action {
  background: rgba(0, 230, 118, 0.15);
  color: #00e676;
}

.tooltip-badge.validation {
  background: rgba(139, 92, 246, 0.15);
  color: #a855f7;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
