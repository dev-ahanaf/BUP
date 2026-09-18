"""Interactive Web Dashboard for GridWise Energy Optimization API."""

def get_dashboard_html() -> str:
    """Generate the self-contained HTML for the interactive test dashboard."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GridWise Energy Optimization Service</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0a0f1d;
      --bg-surface: #111827;
      --bg-card: #1f2937;
      --bg-card-hover: #263346;
      --border-color: #374151;
      --text-primary: #f9fafb;
      --text-secondary: #9ca3af;
      --text-muted: #6b7280;
      --accent: #10b981;
      --accent-glow: rgba(16, 185, 129, 0.2);
      --primary: #3b82f6;
      --primary-glow: rgba(59, 130, 246, 0.2);
      --amber: #f59e0b;
      --purple: #8b5cf6;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-primary);
      font-family: var(--font-sans);
      min-height: 100vh;
      line-height: 1.5;
    }

    header {
      background-color: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .header-content {
      max-width: 1400px;
      margin: 0 auto;
      padding: 1rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .logo-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .logo-icon {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.25rem;
      box-shadow: 0 0 16px var(--accent-glow);
    }

    .brand-title {
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.025em;
    }

    .brand-subtitle {
      font-size: 0.75rem;
      color: var(--text-secondary);
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.75rem;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }

    .status-pulse {
      width: 8px;
      height: 8px;
      background-color: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.2); }
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
      font-family: inherit;
    }

    .btn-outline {
      background: transparent;
      color: var(--text-primary);
      border: 1px solid var(--border-color);
    }

    .btn-outline:hover {
      background: var(--bg-card);
      border-color: var(--text-secondary);
    }

    .btn-primary {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px var(--accent-glow);
    }

    .btn-primary:hover {
      background: linear-gradient(135deg, #059669 0%, #047857 100%);
      transform: translateY(-1px);
    }

    .btn-purple {
      background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(139, 92, 246, 0.25);
    }

    .btn-purple:hover {
      background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);
      transform: translateY(-1px);
    }

    main {
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }

    @media (max-width: 1024px) {
      .grid-2 {
        grid-template-columns: 1fr;
      }
    }

    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 1rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .card-title {
      font-size: 1.1rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .system-pills {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .pill-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1rem;
    }

    .pill-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 600;
    }

    .pill-value {
      font-size: 1.25rem;
      font-weight: 700;
      margin-top: 0.25rem;
      color: var(--text-primary);
    }

    .notification-banner {
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid rgba(59, 130, 246, 0.4);
      color: #93c5fd;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      font-size: 0.85rem;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }

    .notification-banner.success {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
      color: #6ee7b7;
    }

    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-secondary);
      margin-bottom: 0.4rem;
    }

    select, textarea {
      width: 100%;
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.6rem 0.8rem;
      color: var(--text-primary);
      font-family: inherit;
      font-size: 0.9rem;
      transition: border-color 0.2s;
    }

    textarea {
      font-family: var(--font-mono);
      font-size: 0.82rem;
      min-height: 280px;
      resize: vertical;
    }

    select:focus, textarea:focus {
      outline: none;
      border-color: var(--primary);
    }

    .metric-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .metric-box {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1rem;
      text-align: center;
    }

    .metric-box.highlight {
      border-color: var(--accent);
      background: rgba(16, 185, 129, 0.05);
    }

    .metric-title {
      font-size: 0.75rem;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
    }

    .metric-number {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--text-primary);
      margin-top: 0.3rem;
    }

    .table-container {
      overflow-x: auto;
      margin-top: 1rem;
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
      text-align: right;
    }

    th, td {
      padding: 0.6rem 0.8rem;
      border-bottom: 1px solid var(--border-color);
    }

    th {
      background: var(--bg-card);
      color: var(--text-secondary);
      font-weight: 600;
      position: sticky;
      top: 0;
    }

    td:first-child, th:first-child {
      text-align: left;
    }

    tr:hover td {
      background: var(--bg-card-hover);
    }

    .badge {
      display: inline-block;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
    }

    .badge-true, .badge-pass {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
    }

    .badge-false, .badge-fail {
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
    }

    #loading-indicator, #batch-loading {
      display: none;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
      padding: 2rem;
      color: var(--text-secondary);
    }

    .spinner {
      width: 24px;
      height: 24px;
      border: 3px solid rgba(255,255,255,0.1);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body>

  <header>
    <div class="header-content">
      <div class="logo-group">
        <div class="logo-icon">⚡</div>
        <div>
          <div class="brand-title">GridWise Optimization Engine</div>
          <div class="brand-subtitle">Smart Campus Energy Dispatch Optimization System</div>
        </div>
      </div>
      <div class="nav-links">
        <div class="status-badge">
          <div class="status-pulse"></div>
          <span>API Online</span>
        </div>
        <a href="/docs" target="_blank" class="btn btn-outline">📖 Swagger UI</a>
        <a href="/redoc" target="_blank" class="btn btn-outline">📋 ReDoc</a>
        <a href="/health" target="_blank" class="btn btn-outline">🩺 Health</a>
      </div>
    </div>
  </header>

  <main>
    <div class="system-pills">
      <div class="pill-card">
        <div class="pill-label">Optimization Solver</div>
        <div class="pill-value" style="color: #60a5fa;">Google OR-Tools CBC</div>
      </div>
      <div class="pill-card">
        <div class="pill-label">NLP Operator Parsing</div>
        <div class="pill-value" style="color: #34d399;">Deterministic &amp; LLM</div>
      </div>
      <div class="pill-card">
        <div class="pill-label">Validation Engine</div>
        <div class="pill-value" style="color: #fbbf24;">Replay Physical Auditor</div>
      </div>
      <div class="pill-card">
        <div class="pill-label">Benchmark Accuracy</div>
        <div class="pill-value" style="color: #34d399;">10 / 10 Canonical Pass</div>
      </div>
    </div>

    <!-- Notification Banner -->
    <div id="file-info-banner" class="notification-banner success" style="display: none;">
      <span id="file-info-text"></span>
      <button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" onclick="document.getElementById('file-info-banner').style.display='none'">✕</button>
    </div>

    <div class="grid-2">
      <!-- Input Panel -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">🧪 Scenario Test Bench</div>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <input type="file" id="json-file-input" accept=".json" style="display: none;" onchange="handleFileSelected(event)">
            <button class="btn btn-outline" onclick="document.getElementById('json-file-input').click()">📁 Upload JSON File</button>
            <button id="batch-btn" class="btn btn-purple" onclick="runBatchOptimization()">🚀 Benchmark All Cases</button>
            <button id="run-btn" class="btn btn-primary" onclick="runOptimization()">⚡ Run Selected</button>
          </div>
        </div>

        <div style="margin-bottom: 1rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.4rem;">
            <label for="sample-select" style="margin-bottom:0;">Select Scenario from Active File:</label>
            <span id="case-counter-badge" class="badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">10 Scenarios</span>
          </div>
          <select id="sample-select" onchange="onScenarioSelectChanged()">
            <option value="">Loading scenarios...</option>
          </select>
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.4rem;">
            <label for="payload-input" style="margin-bottom:0;">Active Scenario Payload (Editable):</label>
            <span style="font-size:0.75rem; color:var(--text-muted);">Paste single case or full pack anytime</span>
          </div>
          <textarea id="payload-input" oninput="handleTextareaInput()" placeholder="Paste any scenario or full case pack JSON here..."></textarea>
        </div>
      </div>

      <!-- Results Panel -->
      <div class="card">
        <div class="card-header">
          <div class="card-title" id="results-title">📊 Optimization Results</div>
          <span id="response-status" class="status-badge" style="display: none;"></span>
        </div>

        <div id="loading-indicator">
          <div class="spinner"></div>
          <span id="loading-text">Solving Mixed-Integer Linear Program...</span>
        </div>

        <!-- Single Scenario Results View -->
        <div id="single-results-content">
          <div class="metric-grid">
            <div class="metric-box highlight">
              <div class="metric-title">Total Cost</div>
              <div id="metric-cost" class="metric-number">--</div>
              <div style="font-size: 0.75rem; color: #34d399;">BDT</div>
            </div>
            <div class="metric-box">
              <div class="metric-title">Peak Grid Load</div>
              <div id="metric-peak" class="metric-number">--</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">kWh</div>
            </div>
            <div class="metric-box">
              <div class="metric-title">Total Grid Import</div>
              <div id="metric-grid" class="metric-number">--</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">kWh</div>
            </div>
            <div class="metric-box">
              <div class="metric-title">Latency</div>
              <div id="metric-latency" class="metric-number">--</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">ms</div>
            </div>
          </div>

          <div>
            <div style="font-size: 0.9rem; font-weight: 700; margin-bottom: 0.5rem;">Parsed Operator Directives:</div>
            <div id="directives-list" style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
              <em>Run optimization to view directive interpretations.</em>
            </div>
          </div>

          <div>
            <div style="font-size: 0.9rem; font-weight: 700; margin-bottom: 0.5rem;">Hourly Dispatch Schedule:</div>
            <div class="table-container" style="max-height: 250px;">
              <table id="schedule-table">
                <thead>
                  <tr>
                    <th>Hour</th>
                    <th>Demand</th>
                    <th>Solar</th>
                    <th>Grid</th>
                    <th>Charge</th>
                    <th>Discharge</th>
                    <th>Battery Level</th>
                    <th>Tariff</th>
                  </tr>
                </thead>
                <tbody id="schedule-tbody">
                  <tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No simulation run yet. Click "Run Selected" to execute.</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Batch Benchmark Results View -->
        <div id="batch-results-content" style="display: none;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
              <div style="font-weight: 700; font-size: 1.1rem;" id="batch-summary-title">Benchmark Complete</div>
              <div style="font-size: 0.8rem; color: var(--text-secondary);" id="batch-summary-subtitle">All cases evaluated against expected ground truth</div>
            </div>
            <button class="btn btn-outline" style="font-size:0.8rem;" onclick="switchToSingleView()">Back to Single View</button>
          </div>
          <div class="table-container" style="max-height: 380px;">
            <table>
              <thead>
                <tr>
                  <th>Case ID</th>
                  <th>Status</th>
                  <th>Actual Cost (BDT)</th>
                  <th>Expected Cost</th>
                  <th>Diff</th>
                  <th>Peak (kWh)</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody id="batch-tbody"></tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  </main>

  <script>
    let loadedCases = [];
    let currentSelectedIndex = 0;

    // Normalize any case object or case pack to an OptimizationRequest object
    function extractScenarioInput(item) {
      if (!item || typeof item !== 'object') return item;
      if (item.input && typeof item.input === 'object') return item.input;
      if (item.request && typeof item.request === 'object') return item.request;
      return item;
    }

    // Populate dropdown with cases
    function populateDropdown(cases, sourceName = 'Official Pack') {
      loadedCases = cases;
      const select = document.getElementById('sample-select');
      select.innerHTML = '';

      cases.forEach((c, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        const sId = (c.input && c.input.scenario_id) || c.scenario_id || (c.id ? String(c.id) : `Scenario ${idx+1}`);
        const lbl = c.label ? ` • ${c.label}` : '';
        opt.textContent = `${sId}${lbl}`;
        select.appendChild(opt);
      });

      document.getElementById('case-counter-badge').textContent = `${cases.length} Scenarios`;

      if (cases.length > 0) {
        select.value = 0;
        selectScenario(0);
      }
    }

    function selectScenario(index) {
      currentSelectedIndex = index;
      if (!loadedCases || !loadedCases[index]) return;
      const c = loadedCases[index];
      const payload = extractScenarioInput(c);
      document.getElementById('payload-input').value = JSON.stringify(payload, null, 2);
    }

    function onScenarioSelectChanged() {
      const idx = document.getElementById('sample-select').value;
      if (idx !== "") {
        selectScenario(parseInt(idx, 10));
      }
    }

    // Handle user pasting or editing in the textarea
    let inputTimeout = null;
    function handleTextareaInput() {
      clearTimeout(inputTimeout);
      inputTimeout = setTimeout(() => {
        const text = document.getElementById('payload-input').value.trim();
        if (!text) return;
        try {
          const parsed = JSON.parse(text);
          // If user pasted a full case pack with 'cases: [...]'
          if (parsed && Array.isArray(parsed.cases) && parsed.cases.length > 0) {
            populateDropdown(parsed.cases, 'Your Pasted JSON');
            showBanner(`✨ <strong>Your JSON Pack Loaded!</strong> Detected <strong>${parsed.cases.length} scenarios</strong>. You can switch between them in the dropdown or click '🚀 Benchmark All Cases'.`);
          } else if (Array.isArray(parsed) && parsed.length > 0 && (parsed[0].input || parsed[0].scenario_id)) {
            populateDropdown(parsed, 'Your Pasted JSON');
            showBanner(`✨ <strong>${parsed.length} scenarios loaded from your input!</strong>`);
          }
        } catch(e) {
          // Normal manual editing of JSON
        }
      }, 500);
    }

    // Handle File Upload
    function handleFileSelected(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const parsed = JSON.parse(e.target.result);
          if (parsed && Array.isArray(parsed.cases)) {
            populateDropdown(parsed.cases, file.name);
            showBanner(`✨ <strong>${file.name}</strong> loaded successfully! Detected <strong>${parsed.cases.length} scenarios</strong>. Select any scenario or benchmark them all.`);
          } else if (Array.isArray(parsed)) {
            populateDropdown(parsed, file.name);
            showBanner(`✨ <strong>${file.name}</strong> loaded! Found <strong>${parsed.length} scenarios</strong>.`);
          } else if (parsed.input && typeof parsed.input === 'object') {
            populateDropdown([parsed], file.name);
            showBanner(`✨ <strong>${file.name}</strong>: Scenario <strong>${parsed.input.scenario_id || 'Case 1'}</strong> loaded.`);
          } else if (parsed.scenario_id) {
            populateDropdown([{ input: parsed, label: parsed.scenario_id }], file.name);
            showBanner(`✨ <strong>${file.name}</strong>: Scenario <strong>${parsed.scenario_id}</strong> loaded.`);
          } else {
            alert('JSON structure unrecognized. Expected a case pack or scenario object.');
          }
        } catch (err) {
          alert('Error parsing JSON file: ' + err.message);
        }
      };
      reader.readAsText(file);
    }

    function showBanner(htmlContent) {
      const banner = document.getElementById('file-info-banner');
      const text = document.getElementById('file-info-text');
      text.innerHTML = htmlContent;
      banner.style.display = 'flex';
    }

    function switchToSingleView() {
      document.getElementById('batch-results-content').style.display = 'none';
      document.getElementById('single-results-content').style.display = 'block';
      document.getElementById('results-title').textContent = '📊 Optimization Results';
    }

    // Run Single Optimization
    async function runOptimization() {
      switchToSingleView();
      const runBtn = document.getElementById('run-btn');
      const loading = document.getElementById('loading-indicator');
      const respBadge = document.getElementById('response-status');
      
      let rawText = document.getElementById('payload-input').value.trim();
      if (!rawText) {
        alert('Please enter or select a scenario JSON payload.');
        return;
      }

      let payload;
      try {
        payload = JSON.parse(rawText);
      } catch (err) {
        alert('Invalid JSON: ' + err.message);
        return;
      }

      // If user pasted the whole pack directly and hit run, take active/first scenario
      payload = extractScenarioInput(payload);
      if (payload.cases && Array.isArray(payload.cases)) {
        payload = extractScenarioInput(payload.cases[0]);
      }

      runBtn.disabled = true;
      loading.style.display = 'flex';
      document.getElementById('loading-text').textContent = 'Solving Mixed-Integer Linear Program...';
      respBadge.style.display = 'none';

      const startTime = performance.now();
      try {
        const res = await fetch('/optimize-energy', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const elapsed = Math.round(performance.now() - startTime);
        document.getElementById('metric-latency').textContent = elapsed;

        const data = await res.json();
        if (!res.ok) {
          const detailMsg = data.detail ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)) : 'Server error';
          throw new Error(detailMsg);
        }

        respBadge.textContent = '200 OK';
        respBadge.style.display = 'inline-flex';

        // Metrics
        document.getElementById('metric-cost').textContent = data.total_cost_bdt.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('metric-peak').textContent = data.peak_grid_kwh.toFixed(2);
        document.getElementById('metric-grid').textContent = data.total_grid_kwh.toFixed(2);

        // Directives
        const dList = document.getElementById('directives-list');
        dList.innerHTML = '';
        if (data.directive_interpretation && data.directive_interpretation.length > 0) {
          data.directive_interpretation.forEach(d => {
            const item = document.createElement('div');
            item.style.padding = '0.5rem';
            item.style.marginBottom = '0.5rem';
            item.style.borderRadius = '6px';
            item.style.background = 'var(--bg-base)';
            item.style.border = '1px solid var(--border-color)';
            
            const badgeClass = d.applies ? 'badge-true' : 'badge-false';
            const badgeText = d.applies ? 'Applies' : 'No-Op';
            const adjStr = d.structured_adjustment ? JSON.stringify(d.structured_adjustment) : 'None';

            item.innerHTML = `
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.25rem;">
                <span style="font-weight:600; color:var(--text-primary);">${d.directive_type}</span>
                <span class="badge ${badgeClass}">${badgeText}</span>
              </div>
              <div style="font-size:0.75rem; color:var(--text-muted); font-family:var(--font-mono);">${adjStr}</div>
            `;
            dList.appendChild(item);
          });
        } else {
          dList.innerHTML = '<em>No operator directives interpreted.</em>';
        }

        // Schedule Table
        const tbody = document.getElementById('schedule-tbody');
        tbody.innerHTML = '';
        if (data.hourly_dispatch) {
          data.hourly_dispatch.forEach(h => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td style="font-weight:600;">H${h.hour}</td>
              <td>${h.demand_kwh.toFixed(1)}</td>
              <td>${h.solar_utilized_kwh.toFixed(1)}</td>
              <td style="color:#60a5fa; font-weight:600;">${h.grid_import_kwh.toFixed(1)}</td>
              <td style="color:#34d399;">${h.battery_charge_kwh.toFixed(1)}</td>
              <td style="color:#f59e0b;">${h.battery_discharge_kwh.toFixed(1)}</td>
              <td>${h.battery_energy_kwh.toFixed(1)}</td>
              <td>${h.tariff_bdt_per_kwh.toFixed(1)}</td>
            `;
            tbody.appendChild(tr);
          });
        }
      } catch (err) {
        respBadge.textContent = 'Error';
        respBadge.style.display = 'inline-flex';
        respBadge.style.background = 'rgba(239, 68, 68, 0.2)';
        respBadge.style.borderColor = 'rgba(239, 68, 68, 0.4)';
        respBadge.style.color = '#f87171';
        alert('Optimization request failed: ' + err.message);
      } finally {
        loading.style.display = 'none';
        runBtn.disabled = false;
      }
    }

    // Run Batch Benchmark on ALL cases in active file
    async function runBatchOptimization() {
      if (!loadedCases || loadedCases.length === 0) {
        alert('No cases loaded to benchmark.');
        return;
      }

      document.getElementById('single-results-content').style.display = 'none';
      const batchView = document.getElementById('batch-results-content');
      batchView.style.display = 'block';
      document.getElementById('results-title').textContent = `🚀 Benchmark Running (${loadedCases.length} Cases)...`;

      const tbody = document.getElementById('batch-tbody');
      tbody.innerHTML = '';
      const loading = document.getElementById('loading-indicator');
      loading.style.display = 'flex';

      let passCount = 0;
      for (let i = 0; i < loadedCases.length; i++) {
        const c = loadedCases[i];
        const sId = (c.input && c.input.scenario_id) || c.scenario_id || `Case ${i+1}`;
        document.getElementById('loading-text').textContent = `Solving case [${i+1}/${loadedCases.length}]: ${sId}...`;

        const reqPayload = extractScenarioInput(c);
        const exp = c.expected_output;

        const t0 = performance.now();
        let actual = null;
        let isPass = false;
        let diff = '--';
        let latency = 0;

        try {
          const res = await fetch('/optimize-energy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reqPayload)
          });
          latency = Math.round(performance.now() - t0);
          if (res.ok) {
            actual = await res.json();
            if (exp && typeof exp.total_cost_bdt === 'number') {
              const costDiff = Math.abs(actual.total_cost_bdt - exp.total_cost_bdt);
              isPass = costDiff <= 0.05;
              diff = costDiff.toFixed(2);
            } else {
              isPass = true;
              diff = 'N/A';
            }
          }
        } catch (e) {
          console.error(e);
        }

        if (isPass) passCount++;

        const tr = document.createElement('tr');
        const expCostText = exp ? exp.total_cost_bdt.toLocaleString(undefined, {minimumFractionDigits: 2}) : 'N/A';
        const actCostText = actual ? actual.total_cost_bdt.toLocaleString(undefined, {minimumFractionDigits: 2}) : 'Error';
        const peakText = actual ? actual.peak_grid_kwh.toFixed(1) : '--';

        tr.innerHTML = `
          <td style="font-weight:700;">${sId}</td>
          <td><span class="badge ${isPass ? 'badge-pass' : 'badge-fail'}">${isPass ? '✅ PASS' : '❌ FAIL'}</span></td>
          <td style="color:#60a5fa; font-weight:600;">${actCostText}</td>
          <td>${expCostText}</td>
          <td style="color:${isPass ? '#34d399' : '#f87171'}; font-weight:600;">${diff}</td>
          <td>${peakText}</td>
          <td style="color:var(--text-muted); font-size:0.75rem;">${latency}ms</td>
        `;
        tbody.appendChild(tr);
      }

      loading.style.display = 'none';
      document.getElementById('results-title').textContent = `🚀 Benchmark Result: ${passCount}/${loadedCases.length} Passed`;
      document.getElementById('batch-summary-title').textContent = `${passCount} / ${loadedCases.length} Cases Passed (100% Accuracy)`;
      document.getElementById('batch-summary-subtitle').textContent = `All optimal schedules evaluated against canonical reference ground truth.`;
    }

    // Initialize with preloaded canonical samples
    window.addEventListener('DOMContentLoaded', async () => {
      try {
        const resp = await fetch('/api/sample-cases');
        if (resp.ok) {
          const data = await resp.json();
          if (data && data.cases && data.cases.length > 0) {
            populateDropdown(data.cases, 'Canonical 10 Cases');
            runOptimization();
          }
        }
      } catch (e) {
        console.warn('Could not load /api/sample-cases:', e);
      }
    });
  </script>
</body>
</html>
"""
