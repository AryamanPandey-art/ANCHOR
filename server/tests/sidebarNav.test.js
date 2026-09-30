import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '../..');

console.log('============================================================');
console.log('ANCHOR SIDEBAR NAVIGATION VERIFICATION TEST');
console.log('============================================================');

let passedTests = 0;
let failedTests = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✔ PASSED: ${message}`);
    passedTests++;
  } else {
    console.error(`  ✕ FAILED: ${message}`);
    failedTests++;
  }
}

// 1. Inspect Sidebar.vue
console.log('\n1. Verifying Sidebar.vue Navigation Items & Event Emission:');
const sidebarCode = fs.readFileSync(path.join(rootDir, 'src/components/Sidebar.vue'), 'utf-8');

const tabs = ['overview', 'diagnose', 'evidence', 'solution', 'engine'];
for (const tab of tabs) {
  const hasActiveBinding = sidebarCode.includes(`currentTab === '${tab}'`);
  const hasClickHandler = sidebarCode.includes(`selectTab('${tab}')`);
  assert(hasActiveBinding, `Sidebar.vue binds active class for tab '${tab}'`);
  assert(hasClickHandler, `Sidebar.vue has @click="selectTab('${tab}')" for tab '${tab}'`);
}

assert(sidebarCode.includes("this.$emit('tab-change', tab)"), "Sidebar.vue emits 'tab-change' event on click");
assert(sidebarCode.includes("props: {\n    currentTab:"), "Sidebar.vue accepts currentTab prop");

// 2. Inspect App.vue Navigation Wiring & View Templates
console.log('\n2. Verifying App.vue Tab State & View Switching:');
const appCode = fs.readFileSync(path.join(rootDir, 'src/App.vue'), 'utf-8');

assert(appCode.includes('@tab-change="onTabChange"'), "App.vue listens to @tab-change");
assert(appCode.includes("this.currentTab = tab;"), "App.vue onTabChange updates this.currentTab");
assert(appCode.includes(":currentTab=\"currentTab\""), "App.vue passes currentTab to Sidebar and Header");
assert(appCode.includes(":activeTab=\"currentTab\""), "App.vue passes activeTab to EvidenceGraph");

for (const tab of tabs) {
  assert(appCode.includes(`currentTab === '${tab}'`), `App.vue has conditional view template for tab '${tab}'`);
}

// 3. Inspect Header.vue View Tag
console.log('\n3. Verifying Header.vue Active View Indicator:');
const headerCode = fs.readFileSync(path.join(rootDir, 'src/components/Header.vue'), 'utf-8');

assert(headerCode.includes("currentTab:"), "Header.vue accepts currentTab prop");
assert(headerCode.includes("VIEW: {{ (currentTab || 'overview').toUpperCase() }}"), "Header.vue renders dynamic active view indicator");

// 4. Inspect EvidenceGraph.vue Node Focus Behavior
console.log('\n4. Verifying EvidenceGraph.vue Node Focus & Watcher:');
const graphCode = fs.readFileSync(path.join(rootDir, 'src/components/EvidenceGraph.vue'), 'utf-8');

assert(graphCode.includes("activeTab:"), "EvidenceGraph.vue accepts activeTab prop");
assert(graphCode.includes("newTab === 'diagnose'"), "EvidenceGraph.vue handles 'diagnose' tab focus");
assert(graphCode.includes("this.selectedNodeId = 'node-complaint'"), "EvidenceGraph.vue focuses 'node-complaint' in diagnose view");
assert(graphCode.includes("newTab === 'evidence'"), "EvidenceGraph.vue handles 'evidence' tab focus");
assert(graphCode.includes("this.selectedNodeId = 'node-evidence'"), "EvidenceGraph.vue focuses 'node-evidence' in evidence view");
assert(graphCode.includes("newTab === 'solution'"), "EvidenceGraph.vue handles 'solution' tab focus");
assert(graphCode.includes("this.selectedNodeId = 'node-action'"), "EvidenceGraph.vue focuses 'node-action' in solution view");
assert(graphCode.includes("newTab === 'engine'"), "EvidenceGraph.vue handles 'engine' tab focus");
assert(graphCode.includes("this.selectedNodeId = 'node-validation'"), "EvidenceGraph.vue focuses 'node-validation' in engine view");
assert(graphCode.includes("this.selectedNodeId = null"), "EvidenceGraph.vue clears node focus in overview tab");

// 5. Test Live Frontend & Backend Servers
console.log('\n5. Verifying Live Servers & Pipeline Execution:');
try {
  const frontRes = await fetch('http://localhost:5173');
  assert(frontRes.status === 200, "Frontend server running on http://localhost:5173 returns 200 OK");
} catch (e) {
  assert(false, `Frontend server check failed: ${e.message}`);
}

try {
  const backRes = await fetch('http://localhost:3001/api/diagnose', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: "My screen isn't rotating automatically." })
  });
  const data = await backRes.json();
  assert(backRes.status === 200, "Backend API /api/diagnose returns 200 OK");
  assert(data.validation?.overallStatus === 'PASS', "Diagnostic pipeline produces verified PASS for official Auto Rotate query");
  assert(data.deeplink?.verified === true, "Deeplink is verified in official Samsung catalog");
} catch (e) {
  assert(false, `Backend API check failed: ${e.message}`);
}

console.log('\n============================================================');
console.log(`TOTAL: ${passedTests} passed, ${failedTests} failed.`);
console.log('============================================================');

if (failedTests > 0) {
  process.exit(1);
} else {
  console.log('ALL SIDEBAR NAVIGATION INTEGRATION CHECKS PASSED!\n');
}
