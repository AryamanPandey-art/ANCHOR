<template>
  <aside class="sidebar-rail">
    <!-- Top Logo -->
    <div class="logo-box">
      <div class="logo-glyph">
        <svg viewBox="0 0 32 32" class="logo-svg">
          <path d="M16 4 L28 28 L23 28 L16 14 L9 28 L4 28 Z" fill="#00f0ff" />
          <path d="M8 20 L24 20" stroke="#00f0ff" stroke-width="2.5" stroke-linecap="round" />
        </svg>
      </div>
    </div>

    <!-- Nav Items -->
    <nav class="nav-list">
      <button 
        class="nav-item" 
        :class="{ active: currentTab === 'overview' }"
        @click="selectTab('overview')"
        title="Overview"
      >
        <div class="nav-icon-wrapper">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        </div>
        <span class="nav-label">Overview</span>
      </button>

      <button 
        class="nav-item" 
        :class="{ active: currentTab === 'diagnose' }"
        @click="selectTab('diagnose')"
        title="Diagnose"
      >
        <div class="nav-icon-wrapper">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.3-4.3"/>
            <path d="M11 8v6M8 11h6"/>
          </svg>
        </div>
        <span class="nav-label">Diagnose</span>
      </button>

      <button 
        class="nav-item" 
        :class="{ active: currentTab === 'evidence' }"
        @click="selectTab('evidence')"
        title="Evidence"
      >
        <div class="nav-icon-wrapper">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="18" height="18" x="3" y="3" rx="2"/>
            <path d="M3 9h18M9 21V9"/>
          </svg>
        </div>
        <span class="nav-label">Evidence</span>
      </button>

      <button 
        class="nav-item" 
        :class="{ active: currentTab === 'solution' }"
        @click="selectTab('solution')"
        title="Solution"
      >
        <div class="nav-icon-wrapper">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/>
            <path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.2 2.2M16.9 16.9l2.2 2.2M4.9 19.1l2.2-2.2M16.9 7.1l2.2-2.2"/>
          </svg>
        </div>
        <span class="nav-label">Solution</span>
      </button>

      <button 
        class="nav-item" 
        :class="{ active: currentTab === 'engine' }"
        @click="selectTab('engine')"
        title="Engine"
      >
        <div class="nav-icon-wrapper">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="14" height="14" x="5" y="5" rx="2"/>
            <path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>
          </svg>
        </div>
        <span class="nav-label">Engine</span>
      </button>
    </nav>

    <!-- Bottom Settings -->
    <div class="bottom-box">
      <button 
        class="nav-item" 
        :class="{ active: currentTab === 'settings' }"
        @click="selectTab('settings')"
        title="Settings"
      >
        <div class="nav-icon-wrapper">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
        </div>
        <span class="nav-label">Settings</span>
      </button>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    currentTab: {
      type: String,
      default: 'overview'
    }
  },
  emits: ['tab-change'],
  methods: {
    selectTab(tab) {
      this.$emit('tab-change', tab);
    }
  }
}
</script>

<style scoped>
.sidebar-rail {
  width: 68px;
  background-color: var(--bg-sidebar);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 14px 0 16px 0;
  user-select: none;
  flex-shrink: 0;
  height: 100vh;
}

.logo-box {
  margin-bottom: 24px;
}

.logo-glyph {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  filter: drop-shadow(0 0 8px rgba(0, 240, 255, 0.6));
  transition: transform 0.2s ease;
}

.logo-glyph:hover {
  transform: scale(1.06);
}

.logo-svg {
  width: 30px;
  height: 30px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
  align-items: center;
}

.nav-item {
  background: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 52px;
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.2s ease;
  padding: 0;
}

.nav-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 28px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-label {
  font-size: 10.5px;
  font-weight: 500;
  margin-top: 3px;
  letter-spacing: 0.01em;
}

.nav-item:hover {
  color: #c5d8ea;
}

.nav-item.active {
  color: var(--color-cyan);
}

.nav-item.active .nav-icon-wrapper {
  background: rgba(0, 240, 255, 0.12);
  border: 1px solid rgba(0, 240, 255, 0.5);
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.28);
  color: var(--color-cyan);
}

.bottom-box {
  margin-top: auto;
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
