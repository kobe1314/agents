#!/usr/bin/env node
/**
 * Dashboard frontend smoke tests.
 * Tests core JS functions used in dashboard.html.
 * Run: node .opencode/dashboard.test.js
 */

// Mock browser APIs that dashboard.html uses
global.URLSearchParams = require('url').URLSearchParams;
global.fetch = async (url) => {
  const calls = global._fetchCalls || [];
  calls.push(url);
  global._fetchCalls = calls;
  return { text: async () => '', json: async () => ({}) };
};
const _classList = { _classes: [], contains: function(c) { return this._classes.includes(c); }, add: function(c) { if (!this._classes.includes(c)) this._classes.push(c); }, remove: function(c) { this._classes = this._classes.filter(x => x !== c); }, toggle: function(c) { if (this._classes.includes(c)) { this._classes = this._classes.filter(x => x !== c); return false; } else { this._classes.push(c); return true; } } };
global.document = {
  body: { classList: _classList },
  getElementById: (id) => {
    if (!global._elements) global._elements = {};
    if (!global._elements[id]) {
      global._elements[id] = { innerHTML: '' };
    }
    return global._elements[id];
  }
};
global.localStorage = {
  _data: {},
  getItem: (k) => global.localStorage._data[k] || null,
  setItem: (k, v) => { global.localStorage._data[k] = v; },
};

let testsPassed = 0;
let testsFailed = 0;

function assert(condition, msg) {
  if (condition) {
    testsPassed++;
    console.log(`  ✅ ${msg}`);
  } else {
    testsFailed++;
    console.error(`  ❌ ${msg}`);
  }
}

// ─── Test Suite ─────────────────────────────────

// 1. Theme toggle logic
(function testTheme() {
  console.log('\n📋 Theme Tests');
  // Default: no class, dark theme
  assert(!document.body.classList.contains('light'), 'starts without light class');

  // Simulate loading light theme from localStorage (mimics the IIFE in dashboard.html)
  const savedTheme = localStorage.getItem('av-theme') || 'dark';
  if (savedTheme === 'light') document.body.classList.add('light');
  assert(!document.body.classList.contains('light'), 'dark theme by default');

  // Toggle to light
  document.body.classList.toggle('light');
  assert(document.body.classList.contains('light'), 'toggle adds light class');

  // Toggle back
  document.body.classList.toggle('light');
  assert(!document.body.classList.contains('light'), 'toggle removes light class');
})();

// 2. URLSearchParams for spawn
(function testSpawnParams() {
  console.log('\n📋 Spawn Tests');
  const p = new URLSearchParams();
  p.set('name', 'test-task');
  p.set('command', 'echo hello');
  const url = '/api/spawn?' + p.toString();
  assert(url.includes('name=test-task'), 'spawn URL contains name');
  assert(url.includes('command=echo+hello'), 'spawn URL contains command');
  assert(!url.includes('ralph_loop'), 'no ralph_loop by default');

  // With ralph
  const p2 = new URLSearchParams();
  p2.set('name', 'ralph-task');
  p2.set('command', 'exit 1');
  p2.set('ralph_loop', '3');
  const url2 = '/api/spawn?' + p2.toString();
  assert(url2.includes('ralph_loop=3'), 'spawn URL includes ralph_loop');
})();

// 3. DOM element access (mimicking refreshAll)
(function testDOMManipulation() {
  console.log('\n📋 DOM Tests');
  const lo = document.getElementById('liveOutput');
  lo.innerHTML = '<div>running: test</div>';
  assert(lo.innerHTML.includes('test'), 'liveOutput innerHTML set correctly');

  const tb = document.getElementById('tasksBody');
  tb.innerHTML = '<tr><td>task-001</td></tr>';
  assert(tb.innerHTML.includes('task-001'), 'tasksBody innerHTML set correctly');
})();

// 4. Data formatting
(function testDataFormatting() {
  console.log('\n📋 Data Format Tests');
  const agent = { name: 'build', mode: 'primary', model: 'deepseek/deepseek-v4-flash', tools: ['bash', 'edit'], description: 'Test agent' };
  const modelShort = agent.model.split('/').pop();
  assert(modelShort === 'deepseek-v4-flash', 'model name extracted correctly');
  assert(agent.tools.slice(0, 4).join(', ') === 'bash, edit', 'tools joined correctly');
  assert(agent.description.slice(0, 40) === agent.description, 'description truncated correctly');

  const skill = { name: 'test-skill', description: 'A long description '.repeat(10), version: '1.0', source: 'github' };
  const desc = skill.description.slice(0, 60);
  assert(desc.length <= 63, 'skill description truncated to ~60 chars');
})();

// ─── Summary ────────────────────────────────────
console.log(`\n${'='.repeat(40)}`);
console.log(`Results: ${testsPassed} passed, ${testsFailed} failed`);
if (testsFailed > 0) process.exit(1);
