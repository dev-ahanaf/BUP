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

    .btn-secondary {
      background: #374151;
      color: #f9fafb;
    }

    .btn-secondary:hover {
      background: #4b5563;
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
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
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

    .badge-true {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
    }

    .badge-false {
      background: rgba(107, 114, 128, 0.2);
      color: #9ca3af;
    }

    #loading-indicator {
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
          <div class="brand-subtitle">Smart Campus Energy Microgrid Management System</div>
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
        <div class="pill-label">Time Horizon</div>
        <div class="pill-value" style="color: #a78bfa;">24 Hours [0..23]</div>
      </div>
    </div>

    <!-- Notification Banner -->
    <div id="file-info-banner" class="notification-banner" style="display: none;">
      <span id="file-info-text"></span>
      <button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" onclick="document.getElementById('file-info-banner').style.display='none'">✕</button>
    </div>

    <div class="grid-2">
      <!-- Input Panel -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">🧪 Scenario Test Bench</div>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <!-- Hidden file input -->
            <input type="file" id="json-file-input" accept=".json" style="display: none;" onchange="handleFileSelected(event)">
            <button class="btn btn-outline" onclick="document.getElementById('json-file-input').click()">📁 Upload JSON File</button>
            <button id="run-btn" class="btn btn-primary" onclick="runOptimization()">⚡ Run Optimization</button>
          </div>
        </div>

        <div style="margin-bottom: 1rem;">
          <label for="sample-select">Select Scenario to Run:</label>
          <select id="sample-select" onchange="onScenarioSelectChanged()">
            <option value="">Loading scenarios...</option>
          </select>
        </div>

        <div>
          <label for="payload-input">Scenario JSON Payload (Auto-Unwrapped &amp; Editable):</label>
          <textarea id="payload-input" placeholder="Paste or upload scenario JSON..."></textarea>
        </div>
      </div>

      <!-- Results Panel -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">📊 Optimization Results</div>
          <span id="response-status" class="status-badge" style="display: none;"></span>
        </div>

        <div id="loading-indicator">
          <div class="spinner"></div>
          <span>Solving Mixed-Integer Linear Program...</span>
        </div>

        <div id="results-content">
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
                    <th>Battery Energy</th>
                    <th>Tariff</th>
                  </tr>
                </thead>
                <tbody id="schedule-tbody">
                  <tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No simulation run yet. Click "Run Optimization" to execute.</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    // Global store of active scenarios
    let loadedCases = [];

    // Helper: extract canonical OptimizationRequest payload from any container format
    function normalizeScenarioPayload(obj) {
      if (!obj || typeof obj !== 'object') return obj;
      // If it's a Case Pack with `cases` array
      if (Array.isArray(obj.cases) && obj.cases.length > 0) {
        const first = obj.cases[0];
        return first.input || first;
      }
      // If it has `input` key (single case object)
      if (obj.input && typeof obj.input === 'object') {
        return obj.input;
      }
      // Direct scenario object
      return obj;
    }

    // Populate the dropdown with an array of case objects
    function populateDropdown(cases) {
      const select = document.getElementById('sample-select');
      select.innerHTML = '';
      loadedCases = cases;

      cases.forEach((c, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        const sId = (c.input && c.input.scenario_id) || c.scenario_id || `Case ${idx+1}`;
        const lbl = c.label ? ` - ${c.label}` : '';
        opt.textContent = `${sId}${lbl}`;
        select.appendChild(opt);
      });

      if (cases.length > 0) {
        select.value = 0;
        selectScenario(0);
      }
    }

    function selectScenario(index) {
      if (!loadedCases || !loadedCases[index]) return;
      const c = loadedCases[index];
      const payload = normalizeScenarioPayload(c);
      document.getElementById('payload-input').value = JSON.stringify(payload, null, 2);
    }

    function onScenarioSelectChanged() {
      const idx = document.getElementById('sample-select').value;
      if (idx !== "") {
        selectScenario(parseInt(idx, 10));
      }
    }

    // Handle File Upload (Sample case pack, individual cases, or raw scenario json)
    function handleFileSelected(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const parsed = JSON.parse(e.target.result);
          const banner = document.getElementById('file-info-banner');
          const bannerText = document.getElementById('file-info-text');

          // Case 1: Case pack file (e.g. BUP_CSE_FEST_2026_Preli_Public_Sample_Cases.json)
          if (parsed && Array.isArray(parsed.cases)) {
            populateDropdown(parsed.cases);
            bannerText.innerHTML = `✨ <strong>${file.name}</strong> loaded successfully! Detected <strong>${parsed.cases.length} scenarios</strong>. Select a scenario or run optimization.`;
            banner.style.display = 'flex';
          }
          // Case 2: Array of cases or scenarios
          else if (Array.isArray(parsed)) {
            populateDropdown(parsed);
            bannerText.innerHTML = `✨ <strong>${file.name}</strong> loaded! Detected <strong>${parsed.length} scenarios</strong>.`;
            banner.style.display = 'flex';
          }
          // Case 3: Single wrapped case with 'input'
          else if (parsed.input && typeof parsed.input === 'object') {
            const single = [parsed];
            populateDropdown(single);
            bannerText.innerHTML = `✨ <strong>${file.name}</strong>: Loaded scenario <strong>${parsed.input.scenario_id || 'Unknown'}</strong>.`;
            banner.style.display = 'flex';
          }
          // Case 4: Single raw scenario object
          else if (parsed.scenario_id) {
            const single = [{ input: parsed, label: parsed.scenario_id }];
            populateDropdown(single);
            bannerText.innerHTML = `✨ <strong>${file.name}</strong>: Loaded scenario <strong>${parsed.scenario_id}</strong>.`;
            banner.style.display = 'flex';
          }
          else {
            alert('File does not match expected scenario format.');
          }
        } catch (err) {
          alert('Error parsing JSON file: ' + err.message);
        }
      };
      reader.readAsText(file);
    }

    // Run Optimization
    async function runOptimization() {
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
        alert('Invalid JSON in payload editor: ' + err.message);
        return;
      }

      // Auto-unwrap if user pasted full sample pack with 'cases' or 'input'
      payload = normalizeScenarioPayload(payload);
      // Reflect unwrapped JSON back into the textarea so user sees the clean scenario
      document.getElementById('payload-input').value = JSON.stringify(payload, null, 2);

      runBtn.disabled = true;
      loading.style.display = 'flex';
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

        // Render Metrics
        document.getElementById('metric-cost').textContent = data.total_cost_bdt.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('metric-peak').textContent = data.peak_grid_kwh.toFixed(2);
        document.getElementById('metric-grid').textContent = data.total_grid_kwh.toFixed(2);

        // Render Directives
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

        // Render Schedule Table
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

    // On Page Load: Fetch preloaded canonical sample cases
    window.addEventListener('DOMContentLoaded', async () => {
      try {
        const resp = await fetch('/api/sample-cases');
        if (resp.ok) {
          const data = await resp.json();
          if (data && data.cases && data.cases.length > 0) {
            populateDropdown(data.cases);
            // Run initial optimization on the first sample
            runOptimization();
            return;
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
