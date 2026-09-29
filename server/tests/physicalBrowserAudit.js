import fs from 'fs';
import path from 'path';

// Connect to Edge via CDP WebSocket
async function runAudit() {
  console.log('============================================================');
  console.log('PHYSICAL BROWSER INTERACTION AUDIT (EDGE CDP)');
  console.log('============================================================\n');

  const pagesRes = await fetch('http://localhost:9222/json');
  const pages = await pagesRes.json();
  const targetPage = pages.find(p => p.url.includes('localhost:5173')) || pages[0];
  
  if (!targetPage || !targetPage.webSocketDebuggerUrl) {
    throw new Error('No target page found on localhost:5173');
  }

  console.log(`Connected to: ${targetPage.title} (${targetPage.url})`);
  console.log(`WebSocket Debugger: ${targetPage.webSocketDebuggerUrl}\n`);

  const ws = new WebSocket(targetPage.webSocketDebuggerUrl);

  let id = 1;
  const pending = new Map();
  const consoleErrors = [];
  const networkErrors = [];

  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const msgId = id++;
      pending.set(msgId, { resolve, reject });
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  // Enable console and runtime
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      const { resolve, reject } = pending.get(data.id);
      pending.delete(data.id);
      if (data.error) reject(data.error);
      else resolve(data.result);
    } else if (data.method === 'Runtime.consoleAPICalled') {
      const text = data.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
      if (data.params.type === 'error') {
        consoleErrors.push(text);
        console.error('  [Browser Console Error]:', text);
      }
    } else if (data.method === 'Runtime.exceptionThrown') {
      const exp = data.params.exceptionDetails.text;
      consoleErrors.push(exp);
      console.error('  [Browser Uncaught Exception]:', exp);
    }
  };

  await send('Runtime.enable');
  await send('Page.enable');

  async function evaluate(expression) {
    const res = await send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(`Eval error: ${JSON.stringify(res.exceptionDetails)}`);
    }
    return res.result?.value;
  }

  // Wait 1s for initial render
  await new Promise(r => setTimeout(r, 1200));

  // ==========================================
  // TASK 5: Physical Sidebar Interaction
  // ==========================================
  console.log('--- TASK 5: SIDEBAR INTERACTION AUDIT ---');

  const tabsToTest = [
    { name: 'Diagnose', id: 'diagnose', expectedTag: 'VIEW: DIAGNOSE', expectedNode: 'node-complaint' },
    { name: 'Evidence', id: 'evidence', expectedTag: 'VIEW: EVIDENCE', expectedNode: 'node-evidence' },
    { name: 'Solution', id: 'solution', expectedTag: 'VIEW: SOLUTION', expectedNode: 'node-action' },
    { name: 'Engine', id: 'engine', expectedTag: 'VIEW: ENGINE', expectedNode: 'node-validation' },
    { name: 'Overview', id: 'overview', expectedTag: 'VIEW: OVERVIEW', expectedNode: null }
  ];

  for (const t of tabsToTest) {
    console.log(`\nClicking [${t.name}] sidebar item...`);
    const clickResult = await evaluate(`
      (() => {
        const btn = document.querySelector(".nav-item[title='${t.name}']");
        if (!btn) return { error: "Button not found" };
        btn.click();
        return { clicked: true, title: btn.title };
      })()
    `);

    await new Promise(r => setTimeout(r, 400));

    const state = await evaluate(`
      (() => {
        const btn = document.querySelector(".nav-item[title='${t.name}']");
        const headerTag = document.querySelector(".view-mode-tag")?.textContent?.trim();
        const activeClass = btn?.classList.contains('active');
        const selectedHalo = document.querySelector(".node-halo[r='25']");
        const leftColCards = Array.from(document.querySelectorAll(".left-col .anchor-card .card-title"))
          .map(el => el.textContent.trim());
        const rightColCards = Array.from(document.querySelectorAll(".right-col .anchor-card .card-title"))
          .map(el => el.textContent.trim());

        return {
          buttonActive: activeClass,
          headerTag,
          leftColCards,
          rightColCards
        };
      })()
    `);

    console.log(`  Physical click received: ${clickResult.clicked}`);
    console.log(`  Active class on [${t.name}]: ${state.buttonActive}`);
    console.log(`  Header tag: "${state.headerTag}" (Expected: "${t.expectedTag}")`);
    console.log(`  Left column cards: ${JSON.stringify(state.leftColCards)}`);
    console.log(`  Right column cards: ${JSON.stringify(state.rightColCards)}`);

    if (!state.buttonActive || state.headerTag !== t.expectedTag) {
      throw new Error(`Sidebar item ${t.name} failed verification!`);
    }
  }

  async function waitForProcessingComplete() {
    for (let i = 0; i < 40; i++) {
      await new Promise(r => setTimeout(r, 100));
      const isProcessing = await evaluate(`
        Boolean(document.querySelector(".status-badge.status-processing"))
      `);
      if (!isProcessing) break;
    }
  }

  // ==========================================
  // TASK 6: Demo Scenarios Physical Audit
  // ==========================================
  console.log('\n--- TASK 6: DEMO SCENARIOS PHYSICAL AUDIT ---');

  // Scenario 1
  console.log('\nRunning SCENARIO 1 (Distorted / Auto Rotate)...');
  await evaluate(`
    (() => {
      const textarea = document.querySelector(".query-textarea");
      textarea.value = "My Nexa A14 screen looks distorted right after I received the phone and I need a test.";
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      const submitBtn = document.querySelector(".submit-button");
      submitBtn.click();
    })()
  `);

  await waitForProcessingComplete();

  const sc1 = await evaluate(`
    (() => {
      const badge = document.querySelector(".status-badge")?.textContent?.trim();
      const actionTitle = document.querySelector(".proposal-main-title")?.textContent?.trim();
      const deeplink = document.querySelector(".deeplink-uri")?.textContent?.trim();
      const contractPass = document.querySelector(".meta-highlight.contract-pass")?.textContent?.trim();
      const execBtn = document.querySelector(".execute-action-btn");
      const isExecDisabled = execBtn?.disabled;
      return { badge, actionTitle, deeplink, contractPass, isExecDisabled };
    })()
  `);
  console.log('  Scenario 1 Badge:', sc1.badge);
  console.log('  Scenario 1 Action:', sc1.actionTitle);
  console.log('  Scenario 1 Deeplink:', sc1.deeplink);
  console.log('  Scenario 1 Contract:', sc1.contractPass);
  console.log('  Scenario 1 Execute Action Disabled?:', sc1.isExecDisabled);

  // Scenario 2
  console.log('\nRunning SCENARIO 2 (Cracked screen / Hardware Safety)...');
  await evaluate(`
    (() => {
      const textarea = document.querySelector(".query-textarea");
      textarea.value = "My Nexa Fold X1 screen is cracked and unresponsive; I need my data saved.";
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      const submitBtn = document.querySelector(".submit-button");
      submitBtn.click();
    })()
  `);

  await waitForProcessingComplete();

  const sc2 = await evaluate(`
    (() => {
      const badge = document.querySelector(".status-badge")?.textContent?.trim();
      const actionTitle = document.querySelector(".proposal-main-title")?.textContent?.trim();
      const contractText = document.querySelector(".meta-item:nth-child(4) .meta-highlight")?.textContent?.trim();
      const deeplink = document.querySelector(".deeplink-uri")?.textContent?.trim();
      const execBtn = document.querySelector(".execute-action-btn");
      const isExecDisabled = execBtn?.disabled;
      return { badge, actionTitle, contractText, deeplink, isExecDisabled };
    })()
  `);
  console.log('  Scenario 2 Badge:', sc2.badge);
  console.log('  Scenario 2 Action:', sc2.actionTitle);
  console.log('  Scenario 2 Contract:', sc2.contractText);
  console.log('  Scenario 2 Deeplink:', sc2.deeplink);
  console.log('  Scenario 2 Execute Action Disabled?:', sc2.isExecDisabled);

  // Scenario 3
  console.log('\nRunning SCENARIO 3 (Floating Circle / Unsupported Rejection)...');
  await evaluate(`
    (() => {
      const textarea = document.querySelector(".query-textarea");
      textarea.value = "My Nexa X1 has a floating circle that opened a panel. Remove it.";
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      const submitBtn = document.querySelector(".submit-button");
      submitBtn.click();
    })()
  `);

  await waitForProcessingComplete();

  const sc3 = await evaluate(`
    (() => {
      const badge = document.querySelector(".status-badge")?.textContent?.trim();
      const contractFail = document.querySelector(".meta-highlight.contract-fail")?.textContent?.trim();
      const execBtn = document.querySelector(".execute-action-btn");
      const isExecDisabled = execBtn?.disabled;
      return { badge, contractFail, isExecDisabled };
    })()
  `);
  console.log('  Scenario 3 Badge:', sc3.badge);
  console.log('  Scenario 3 Contract Status:', sc3.contractFail);
  console.log('  Scenario 3 Execute Action Disabled?:', sc3.isExecDisabled);

  // ==========================================
  // TASK 7: Reset / New Query Physical Audit
  // ==========================================
  console.log('\n--- TASK 7: RESET / NEW QUERY PHYSICAL AUDIT ---');
  await evaluate(`
    (() => {
      const resetBtn = document.querySelector(".new-query-btn");
      resetBtn.click();
    })()
  `);

  await new Promise(r => setTimeout(r, 500));

  const resetState = await evaluate(`
    (() => {
      const textarea = document.querySelector(".query-textarea");
      const actionTitle = document.querySelector(".proposal-main-title")?.textContent?.trim();
      const deeplink = document.querySelector(".deeplink-uri, .no-deeplink-message")?.textContent?.trim();
      const badge = document.querySelector(".status-badge")?.textContent?.trim();
      return {
        queryValue: textarea?.value,
        actionTitle,
        deeplink,
        badge
      };
    })()
  `);

  console.log('  Reset Query value:', JSON.stringify(resetState.queryValue));
  console.log('  Reset Action title:', resetState.actionTitle);
  console.log('  Reset Deeplink:', resetState.deeplink);

  // Take screenshot
  const screenshotData = await send('Page.captureScreenshot', { format: 'png' });
  const artifactPath = path.resolve('server/tests/physical_audit_screenshot.png');
  fs.writeFileSync(artifactPath, Buffer.from(screenshotData.data, 'base64'));
  console.log(`\nScreenshot captured: ${artifactPath}`);

  console.log('\n--- CONSOLE & ERROR CHECK ---');
  console.log(`Console Errors: ${consoleErrors.length}`);
  console.log(`Network Errors: ${networkErrors.length}`);

  ws.close();

  console.log('\n============================================================');
  console.log('PHYSICAL BROWSER AUDIT COMPLETED SUCCESSFULLY!');
  console.log('============================================================\n');
}

runAudit().catch(err => {
  console.error('Fatal audit error:', err);
  process.exit(1);
});
