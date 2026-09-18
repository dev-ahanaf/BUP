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
          <span>API Online (:8000)</span>
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

    <div class="grid-2">
      <!-- Input Panel -->
      <div class="card">
        <div class="card-header">
          <div class="card-title">🧪 Scenario Test Bench</div>
          <button id="run-btn" class="btn btn-primary" onclick="runOptimization()">⚡ Run Optimization</button>
        </div>

        <div style="margin-bottom: 1rem;">
          <label for="sample-select">Load Preset Scenario:</label>
          <select id="sample-select" onchange="loadPreset()">
            <option value="sample_1">Sample 01: Standard Campus Dispatch</option>
            <option value="sample_2">Sample 02: Solar Reduction &amp; Feeder Cap</option>
            <option value="sample_3">Sample 03: Battery Reserve &amp; Window Maintenance</option>
          </select>
        </div>

        <div>
          <label for="payload-input">JSON Payload (Editable):</label>
          <textarea id="payload-input"></textarea>
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
    const presets = {
      sample_1: {
        "scenario_id": "SAMPLE-01",
        "operator_notes": [
          "Expect heavy rainfall between 12:00 and 15:00 reducing solar to 30%",
          "Keep at least 60 kWh in reserve between 18:00 and 22:00 for the evening cultural program",
          "Normal operations resume afterwards."
        ],
        "hours": [
          {"hour": 0, "demand_kwh": 60.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 1, "demand_kwh": 55.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 2, "demand_kwh": 50.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 3, "demand_kwh": 45.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 4, "demand_kwh": 50.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 5, "demand_kwh": 60.0, "solar_kwh": 5.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 6, "demand_kwh": 80.0, "solar_kwh": 25.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 7, "demand_kwh": 110.0, "solar_kwh": 50.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 8, "demand_kwh": 140.0, "solar_kwh": 80.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 9, "demand_kwh": 160.0, "solar_kwh": 110.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 10, "demand_kwh": 175.0, "solar_kwh": 130.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 11, "demand_kwh": 180.0, "solar_kwh": 140.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 12, "demand_kwh": 175.0, "solar_kwh": 145.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 13, "demand_kwh": 170.0, "solar_kwh": 135.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 14, "demand_kwh": 165.0, "solar_kwh": 120.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 15, "demand_kwh": 150.0, "solar_kwh": 90.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 16, "demand_kwh": 140.0, "solar_kwh": 60.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 17, "demand_kwh": 155.0, "solar_kwh": 20.0, "tariff_bdt_per_kwh": 12.0},
          {"hour": 18, "demand_kwh": 180.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 19, "demand_kwh": 190.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 20, "demand_kwh": 185.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 21, "demand_kwh": 170.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 12.0},
          {"hour": 22, "demand_kwh": 130.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 23, "demand_kwh": 90.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0}
        ],
        "battery": {
          "capacity_kwh": 200.0,
          "initial_energy_kwh": 40.0,
          "minimum_energy_kwh": 20.0,
          "max_charge_kwh_per_hour": 50.0,
          "max_discharge_kwh_per_hour": 50.0
        }
      },
      sample_2: {
        "scenario_id": "SAMPLE-02",
        "operator_notes": [
          "Inverter maintenance from 13:00 to 15:00: no battery discharge allowed.",
          "Cap grid import at 100 kWh from 17:00 to 20:00 to avoid transformer overload."
        ],
        "hours": [
          {"hour": 0, "demand_kwh": 50.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 1, "demand_kwh": 50.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 2, "demand_kwh": 45.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 3, "demand_kwh": 45.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 4, "demand_kwh": 50.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 5, "demand_kwh": 60.0, "solar_kwh": 10.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 6, "demand_kwh": 80.0, "solar_kwh": 30.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 7, "demand_kwh": 100.0, "solar_kwh": 60.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 8, "demand_kwh": 130.0, "solar_kwh": 90.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 9, "demand_kwh": 150.0, "solar_kwh": 120.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 10, "demand_kwh": 160.0, "solar_kwh": 140.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 11, "demand_kwh": 170.0, "solar_kwh": 150.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 12, "demand_kwh": 165.0, "solar_kwh": 150.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 13, "demand_kwh": 160.0, "solar_kwh": 140.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 14, "demand_kwh": 150.0, "solar_kwh": 120.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 15, "demand_kwh": 140.0, "solar_kwh": 80.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 16, "demand_kwh": 130.0, "solar_kwh": 50.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 17, "demand_kwh": 145.0, "solar_kwh": 20.0, "tariff_bdt_per_kwh": 12.0},
          {"hour": 18, "demand_kwh": 160.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 19, "demand_kwh": 170.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 20, "demand_kwh": 160.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 12.0},
          {"hour": 21, "demand_kwh": 140.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 22, "demand_kwh": 110.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 23, "demand_kwh": 70.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0}
        ],
        "battery": {
          "capacity_kwh": 250.0,
          "initial_energy_kwh": 50.0,
          "minimum_energy_kwh": 25.0,
          "max_charge_kwh_per_hour": 60.0,
          "max_discharge_kwh_per_hour": 60.0
        }
      },
      sample_3: {
        "scenario_id": "SAMPLE-03",
        "operator_notes": [
          "Solar panels cleaning from 10:00 to 12:00: solar output down by 50%.",
          "Prohibit battery charging between 18:00 and 22:00 peak hours."
        ],
        "hours": [
          {"hour": 0, "demand_kwh": 40.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 1, "demand_kwh": 40.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 2, "demand_kwh": 40.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 3, "demand_kwh": 40.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 4, "demand_kwh": 45.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 5, "demand_kwh": 50.0, "solar_kwh": 5.0, "tariff_bdt_per_kwh": 6.0},
          {"hour": 6, "demand_kwh": 70.0, "solar_kwh": 20.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 7, "demand_kwh": 90.0, "solar_kwh": 50.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 8, "demand_kwh": 120.0, "solar_kwh": 80.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 9, "demand_kwh": 140.0, "solar_kwh": 100.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 10, "demand_kwh": 150.0, "solar_kwh": 120.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 11, "demand_kwh": 160.0, "solar_kwh": 130.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 12, "demand_kwh": 155.0, "solar_kwh": 130.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 13, "demand_kwh": 150.0, "solar_kwh": 120.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 14, "demand_kwh": 140.0, "solar_kwh": 100.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 15, "demand_kwh": 130.0, "solar_kwh": 70.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 16, "demand_kwh": 120.0, "solar_kwh": 40.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 17, "demand_kwh": 135.0, "solar_kwh": 15.0, "tariff_bdt_per_kwh": 12.0},
          {"hour": 18, "demand_kwh": 150.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 19, "demand_kwh": 160.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 14.0},
          {"hour": 20, "demand_kwh": 150.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 12.0},
          {"hour": 21, "demand_kwh": 130.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 10.0},
          {"hour": 22, "demand_kwh": 100.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 8.0},
          {"hour": 23, "demand_kwh": 60.0, "solar_kwh": 0.0, "tariff_bdt_per_kwh": 6.0}
        ],
        "battery": {
          "capacity_kwh": 200.0,
          "initial_energy_kwh": 40.0,
          "minimum_energy_kwh": 20.0,
          "max_charge_kwh_per_hour": 50.0,
          "max_discharge_kwh_per_hour": 50.0
        }
      }
    };

    function loadPreset() {
      const select = document.getElementById('sample-select');
      const val = select.value;
      if (presets[val]) {
        document.getElementById('payload-input').value = JSON.stringify(presets[val], null, 2);
      }
    }

    async function runOptimization() {
      const runBtn = document.getElementById('run-btn');
      const loading = document.getElementById('loading-indicator');
      const respBadge = document.getElementById('response-status');
      
      let payload;
      try {
        payload = JSON.parse(document.getElementById('payload-input').value);
      } catch (err) {
        alert('Invalid JSON in payload input: ' + err.message);
        return;
      }

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
          throw new Error(data.detail ? JSON.stringify(data.detail) : 'Server error');
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

    // Initialize preset on load
    window.addEventListener('DOMContentLoaded', () => {
      loadPreset();
      // Auto run once
      runOptimization();
    });
  </script>
</body>
</html>
"""
