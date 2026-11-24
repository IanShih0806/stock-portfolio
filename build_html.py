import json
import os

with open('/Users/10404604/.gemini/antigravity/scratch/stock-portfolio-tracker/portfolio_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data)

html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>存股每日資產與獲利變化追蹤器 | 2024/09 ~ 至今</title>
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --accent: #818cf8;
      --success: #34d399;
      --danger: #f87171;
      --warning: #fbbf24;
      --profit: #10b981;
      --today-gain: #22c55e;
      --c-919: #38bdf8;
      --c-56: #fb923c;
      --c-929: #a78bfa;
      --c-878: #34d399;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}
    body {{ background-color: var(--bg); color: var(--text); padding: 24px; min-height: 100vh; }}
    .container {{ max-width: 1400px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }}
    
    /* Header */
    .header {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}
    .header-title h1 {{ font-size: 26px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 10px; }}
    .header-title p {{ color: var(--text-muted); font-size: 14px; margin-top: 6px; }}
    .header-actions {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
    }}
    .badge-live {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--profit);
      border-color: rgba(16, 185, 129, 0.3);
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      background: var(--profit);
      border-radius: 50%;
      display: inline-block;
      box-shadow: 0 0 8px var(--profit);
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
      70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
      100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}
    .btn {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 500;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .btn:hover {{ background: #334155; border-color: var(--primary); color: #fff; }}
    .btn-primary {{ background: #0284c7; border-color: #0284c7; color: #fff; }}
    .btn-primary:hover {{ background: #0369a1; }}

    /* KPI Cards (6 Grid Layout) */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
    }}
    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: var(--primary);
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }}
    .kpi-card::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: var(--card-border);
    }}
    .kpi-card.c-today::before {{ background: #22c55e; }}
    .kpi-card.c-prev::before {{ background: #38bdf8; }}
    .kpi-card.c-profit::before {{ background: #10b981; }}
    .kpi-card.c-blue::before {{ background: #0284c7; }}
    .kpi-card.c-green::before {{ background: #059669; }}
    .kpi-card.c-purple::before {{ background: #818cf8; }}
    
    .kpi-label {{ font-size: 13px; color: var(--text-muted); font-weight: 500; display: flex; justify-content: space-between; align-items: center; }}
    .kpi-value {{ font-size: 24px; font-weight: 700; color: #fff; letter-spacing: -0.5px; }}
    .kpi-sub {{ font-size: 12px; display: flex; align-items: center; gap: 6px; }}
    .text-pos {{ color: var(--success); }}
    .text-neg {{ color: var(--danger); }}
    .highlight-gain {{ color: #4ade80 !important; font-size: 25px; }}

    /* ETF Grid */
    .etf-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .etf-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .etf-header {{ display: flex; justify-content: space-between; align-items: flex-start; }}
    .etf-code {{ font-size: 18px; font-weight: 700; color: #fff; }}
    .etf-name {{ font-size: 12px; color: var(--text-muted); }}
    .etf-badge {{
      font-size: 12px;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 600;
    }}
    .b-919 {{ background: rgba(56, 189, 248, 0.2); color: var(--c-919); }}
    .b-56 {{ background: rgba(251, 146, 60, 0.2); color: var(--c-56); }}
    .b-929 {{ background: rgba(167, 139, 250, 0.2); color: var(--c-929); }}
    .b-878 {{ background: rgba(52, 211, 153, 0.2); color: var(--c-878); }}
    .etf-metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }}
    .etf-metric-item {{ display: flex; flex-direction: column; }}
    .etf-metric-label {{ color: var(--text-muted); font-size: 11px; }}
    .etf-metric-val {{ font-weight: 600; color: #e2e8f0; }}

    /* Main Chart Section */
    .chart-section {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .chart-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .pill-group {{
      display: flex;
      background: #0f172a;
      padding: 4px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      gap: 2px;
      flex-wrap: wrap;
    }}
    .pill {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 7px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 500;
      transition: all 0.2s;
    }}
    .pill.active {{
      background: #334155;
      color: #fff;
      font-weight: 600;
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }}
    .pill.highlight {{
      color: var(--profit);
    }}
    .pill.highlight.active {{
      background: #065f46;
      color: #34d399;
      border: 1px solid #059669;
    }}
    .chart-wrapper {{
      width: 100%;
      height: 480px;
      position: relative;
    }}
    canvas {{
      width: 100% !important;
      height: 100% !important;
      display: block;
    }}

    /* Tooltip */
    #chart-tooltip {{
      position: absolute;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 16px;
      pointer-events: none;
      display: none;
      font-size: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      z-index: 10;
      backdrop-filter: blur(4px);
      min-width: 250px;
    }}
    .tt-date {{ font-weight: 700; color: #fff; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 4px; }}
    .tt-row {{ display: flex; justify-content: space-between; margin-bottom: 4px; }}
    .tt-label {{ color: var(--text-muted); }}
    .tt-val {{ font-weight: 600; }}

    /* Table Section */
    .table-section {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .table-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .search-input {{
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: #fff;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
      min-width: 220px;
    }}
    .search-input:focus {{ border-color: var(--primary); }}
    .table-container {{
      overflow-x: auto;
      max-height: 520px;
      border: 1px solid var(--card-border);
      border-radius: 10px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: right;
    }}
    thead th {{
      background: #0f172a;
      color: var(--text-muted);
      font-weight: 600;
      padding: 12px 14px;
      position: sticky;
      top: 0;
      border-bottom: 1px solid var(--card-border);
      white-space: nowrap;
    }}
    tbody tr {{ border-bottom: 1px solid rgba(51, 65, 85, 0.5); transition: background 0.15s; }}
    tbody tr:hover {{ background: rgba(51, 65, 85, 0.4); }}
    tbody td {{
      padding: 10px 14px;
      color: #e2e8f0;
      white-space: nowrap;
    }}
    .th-left, .td-left {{ text-align: left; }}

    /* Monthly Dividends Matrix */
    .matrix-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 12px;
    }}
    .matrix-card {{
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .matrix-ym {{ font-weight: 700; color: var(--primary); font-size: 14px; display: flex; justify-content: space-between; }}
    .matrix-total {{ font-size: 15px; font-weight: 700; color: #fff; }}

    .footer {{
      text-align: center;
      color: var(--text-muted);
      font-size: 12px;
      padding: 16px 0;
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <div class="header-title">
        <h1>📊 存股每日資產與獲利變化追蹤儀表板</h1>
        <p>追蹤區間：<span id="range-label">2024-09-02 至 2026-11-24</span> · 共 541 個交易日 · 資料源：Google 試算表存股紀錄</p>
      </div>
      <div class="header-actions">
        <span class="badge badge-live" id="live-badge"><span class="pulse-dot"></span> 雲端連線中 · 每5分鐘自動同步</span>
        <button class="btn" id="btn-sync" onclick="syncLiveSheet(true)">🔄 立即同步</button>
        <button class="btn btn-primary" onclick="exportCSV()">📥 匯出每日 CSV</button>
      </div>
    </div>

    <!-- KPI Summary Grid (6 Cards, including 今日獲利 & 前日獲利變化) -->
    <div class="kpi-grid">
      <!-- 1. 今日獲利 (單日獲利增減) -->
      <div class="kpi-card c-today" onclick="setMode('daily_change')">
        <div class="kpi-label">
          <span>今日獲利 (單日損益)</span>
          <span>⚡ 今日變化</span>
        </div>
        <div class="kpi-value highlight-gain" id="kpi-today-profit">+NT$ 1,997,171</div>
        <div class="kpi-sub text-pos" id="kpi-today-sub">
          <span>今日累積 - 前日變化</span>
        </div>
      </div>

      <!-- 2. 前日獲利變化 -->
      <div class="kpi-card c-prev" onclick="setMode('profit')">
        <div class="kpi-label">
          <span>前日獲利變化</span>
          <span>📅 昨日累計基準</span>
        </div>
        <div class="kpi-value text-pos" id="kpi-prev-profit">NT$ 7,179,469</div>
        <div class="kpi-sub" style="color:var(--text-muted);">
          <span>試算表前日基準累積獲利</span>
        </div>
      </div>

      <!-- 3. 目前累積持股獲利 -->
      <div class="kpi-card c-profit" onclick="setMode('profit')">
        <div class="kpi-label">
          <span>持股獲利 (未實現損益)</span>
          <span>🎯 點選看曲線</span>
        </div>
        <div class="kpi-value text-pos" id="kpi-profit">+NT$ 9,176,641</div>
        <div class="kpi-sub text-pos" id="kpi-profit-sub">
          <span>獲利變化 +65.24%</span>
          <span style="color:var(--text-muted);font-size:11px;">(成本 1,406 萬)</span>
        </div>
      </div>

      <!-- 4. 持股總市值 -->
      <div class="kpi-card c-blue" onclick="setMode('stock_val')">
        <div class="kpi-label">
          <span>持股總市值</span>
          <span>📈 點選看走勢</span>
        </div>
        <div class="kpi-value" id="kpi-stock-val">NT$ 23,244,000</div>
        <div class="kpi-sub text-pos" id="kpi-stock-sub">
          <span>▲ +NT$ 9,516,552 (+69.3%)</span>
          <span style="color:var(--text-muted);font-size:11px;">(vs 2024/09 初)</span>
        </div>
      </div>

      <!-- 5. 含息總獲利 (總報酬) -->
      <div class="kpi-card c-green" onclick="setMode('profit_with_div')">
        <div class="kpi-label">
          <span>含息總獲利 (總報酬)</span>
          <span>🎁 價差+已領股息</span>
        </div>
        <div class="kpi-value text-pos" id="kpi-with-div">+NT$ 13,660,507</div>
        <div class="kpi-sub text-pos">
          <span>含息總報酬率 +97.11%</span>
          <span style="color:var(--text-muted);font-size:11px;">(息: 448 萬)</span>
        </div>
      </div>

      <!-- 6. 淨總資產 -->
      <div class="kpi-card c-purple" onclick="setMode('net_asset')">
        <div class="kpi-label">
          <span>淨總資產</span>
          <span>🏦 試算表資產總值</span>
        </div>
        <div class="kpi-value" id="kpi-net-asset">NT$ 23,090,801</div>
        <div class="kpi-sub" style="color:var(--text-muted);">
          <span>含剩餘本金+房貸-質押借款</span>
        </div>
      </div>
    </div>

    <!-- ETF Position Status -->
    <div class="etf-grid">
      <div class="etf-card">
        <div class="etf-header">
          <div>
            <div class="etf-code">00919 群益台灣精選高息</div>
            <div class="etf-name">佔比第一大核心持股</div>
          </div>
          <span class="etf-badge b-919" id="badge-919">40.6%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-919">320.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新收盤價</span>
            <span class="etf-metric-val" id="price-919">29.50 元</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-919">NT$ 9,440,000</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">平均成本 / 獲利</span>
            <span class="etf-metric-val text-pos" id="gain-919">24.26 元 (+21.6%)</span>
          </div>
        </div>
      </div>

      <div class="etf-card">
        <div class="etf-header">
          <div>
            <div class="etf-code">0056 元大高股息</div>
            <div class="etf-name">穩健長青老牌高股息</div>
          </div>
          <span class="etf-badge b-56" id="badge-56">24.1%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-56">112.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新收盤價</span>
            <span class="etf-metric-val" id="price-56">49.94 元</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-56">NT$ 5,593,280</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">平均成本 / 獲利</span>
            <span class="etf-metric-val text-pos" id="gain-56">37.34 元 (+33.8%)</span>
          </div>
        </div>
      </div>

      <div class="etf-card">
        <div class="etf-header">
          <div>
            <div class="etf-code">00929 復華台灣科技優息</div>
            <div class="etf-name">科技月配息主力</div>
          </div>
          <span class="etf-badge b-929" id="badge-929">20.5%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-929">200.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新收盤價</span>
            <span class="etf-metric-val" id="price-929">23.80 元</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-929">NT$ 4,760,000</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">平均成本 / 獲利</span>
            <span class="etf-metric-val text-pos" id="gain-929">19.43 元 (+22.5%)</span>
          </div>
        </div>
      </div>

      <div class="etf-card">
        <div class="etf-header">
          <div>
            <div class="etf-code">00878 國泰永續高股息</div>
            <div class="etf-name">國民 ESG 高股息</div>
          </div>
          <span class="etf-badge b-878" id="badge-878">14.8%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-878">112.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新收盤價</span>
            <span class="etf-metric-val" id="price-878">30.81 元</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-878">NT$ 3,450,720</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">平均成本 / 獲利</span>
            <span class="etf-metric-val text-pos" id="gain-878">22.42 元 (+37.4%)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-section">
      <div class="chart-controls">
        <div class="pill-group" id="mode-pills">
          <button class="pill" id="btn-stock-val" onclick="setMode('stock_val')">📈 持股總市值</button>
          <button class="pill highlight active" id="btn-profit" onclick="setMode('profit')">🎯 持股獲利變化 (損益)</button>
          <button class="pill highlight" id="btn-profit-with-div" onclick="setMode('profit_with_div')">🎁 含息總獲利</button>
          <button class="pill" id="btn-stock-with-div" onclick="setMode('stock_val_with_div')">💰 含息總價值</button>
          <button class="pill" id="btn-net-asset" onclick="setMode('net_asset')">🏦 淨總資產</button>
          <button class="pill" id="btn-daily-change" onclick="setMode('daily_change')">📊 每日漲跌額</button>
          <button class="pill" id="btn-stacked" onclick="setMode('stacked')">🥧 各 ETF 堆疊</button>
        </div>
        <div class="pill-group" id="range-pills">
          <button class="pill" onclick="setRange('1m')">1個月</button>
          <button class="pill" onclick="setRange('3m')">3個月</button>
          <button class="pill" onclick="setRange('6m')">6個月</button>
          <button class="pill" onclick="setRange('1y')">1年</button>
          <button class="pill" onclick="setRange('2025')">2025年</button>
          <button class="pill" onclick="setRange('2026')">2026年</button>
          <button class="pill active" onclick="setRange('all')">全部 (All)</button>
        </div>
      </div>

      <div class="chart-wrapper">
        <canvas id="mainChart"></canvas>
        <div id="chart-tooltip"></div>
      </div>
    </div>

    <!-- Daily Historical Table -->
    <div class="table-section">
      <div class="table-header">
        <div>
          <h2>📅 每日持股明細歷史紀錄</h2>
          <p style="color:var(--text-muted);font-size:13px;margin-top:4px;">可搜尋指定日期或排序查看每日市值、持股獲利、損益率與每檔 ETF 收盤價</p>
        </div>
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 搜尋日期 (例如: 2026-11 或 2025-05)" oninput="filterTable()">
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th class="th-left">日期</th>
              <th>持股總市值 (NT$)</th>
              <th style="color:var(--profit);">持股獲利 (NT$)</th>
              <th style="color:var(--profit);">獲利變化%</th>
              <th style="color:var(--today-gain);">當日增減 (今日獲利 NT$)</th>
              <th style="color:var(--success);">含息總獲利 (NT$)</th>
              <th>累計已領息 (NT$)</th>
              <th style="color:var(--c-919);">00919 (張/價/值)</th>
              <th style="color:var(--c-56);">0056 (張/價/值)</th>
              <th style="color:var(--c-929);">00929 (張/價/值)</th>
              <th style="color:var(--c-878);">00878 (張/價/值)</th>
            </tr>
          </thead>
          <tbody id="tableBody">
            <!-- Dynamic rows -->
          </tbody>
        </table>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; color:var(--text-muted); font-size:12px;">
        <span id="tableCount">顯示 0 / 0 筆</span>
        <span>提示：點選「匯出每日 CSV」可下載完整 541 天含獲利明細試算表</span>
      </div>
    </div>

    <!-- Monthly Dividends Breakdown Section -->
    <div class="table-section">
      <div class="table-header">
        <div>
          <h2>💵 歷月領息與被動現金流紀錄</h2>
          <p style="color:var(--text-muted);font-size:13px;margin-top:4px;">統計 2024/09 ~ 2026/11 各月份實際入帳股息與各檔 ETF 配發狀況</p>
        </div>
        <div style="font-size:14px; font-weight:600; color:var(--success);">
          累計總入帳股息：NT$ 4,483,866 元
        </div>
      </div>
      <div class="matrix-grid" id="matrixGrid">
        <!-- Dynamic monthly cards -->
      </div>
    </div>

    <div class="footer">
      本儀表板根據您的 Google 試算表存股紀錄表動態計算 · 包含 00929、00919、00878、0056 之真實每日歷史交易數據與每月張數變化
    </div>
  </div>

  <script>
    const PORTFOLIO_DATA = {json_str};
    let allRecords = PORTFOLIO_DATA.daily_data;
    const monthlyRecords = PORTFOLIO_DATA.monthly_records;
    const COST_PRINCIPAL = 14066887.0;
    
    let currentMode = 'profit';
    let currentRange = 'all';
    let filteredRecords = [...allRecords];

    function fmt(n) {{
      return Math.round(n).toLocaleString('en-US');
    }}

    function setMode(mode) {{
      currentMode = mode;
      document.querySelectorAll('#mode-pills .pill').forEach(btn => btn.classList.remove('active'));
      
      const btnMap = {{
        'stock_val': 'btn-stock-val',
        'profit': 'btn-profit',
        'profit_with_div': 'btn-profit-with-div',
        'stock_val_with_div': 'btn-stock-with-div',
        'net_asset': 'btn-net-asset',
        'daily_change': 'btn-daily-change',
        'stacked': 'btn-stacked'
      }};
      const targetBtn = document.getElementById(btnMap[mode]);
      if (targetBtn) targetBtn.classList.add('active');

      drawChart();
    }}

    function setRange(range) {{
      currentRange = range;
      document.querySelectorAll('#range-pills .pill').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      
      const total = allRecords.length;
      if (range === '1m') {{
        filteredRecords = allRecords.slice(Math.max(0, total - 22));
      }} else if (range === '3m') {{
        filteredRecords = allRecords.slice(Math.max(0, total - 65));
      }} else if (range === '6m') {{
        filteredRecords = allRecords.slice(Math.max(0, total - 130));
      }} else if (range === '1y') {{
        filteredRecords = allRecords.slice(Math.max(0, total - 250));
      }} else if (range === '2025') {{
        filteredRecords = allRecords.filter(r => r.date.startsWith('2025'));
      }} else if (range === '2026') {{
        filteredRecords = allRecords.filter(r => r.date.startsWith('2026'));
      }} else {{
        filteredRecords = [...allRecords];
      }}
      drawChart();
    }}

    // Canvas Chart Rendering
    const canvas = document.getElementById('mainChart');
    const ctx = canvas.getContext('2d');
    const tooltip = document.getElementById('chart-tooltip');

    let hitAreas = [];

    function setupCanvasDPI() {{
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
    }}

    function drawChart() {{
      setupCanvasDPI();
      const rect = canvas.getBoundingClientRect();
      const W = rect.width;
      const H = rect.height;
      
      ctx.clearRect(0, 0, W, H);
      hitAreas = [];

      if (!filteredRecords.length) return;

      const padLeft = 100;
      const padRight = 70;
      const padTop = 30;
      const padBottom = 40;
      const plotW = W - padLeft - padRight;
      const plotH = H - padTop - padBottom;

      let yValues = [];
      if (currentMode === 'stock_val') {{
        yValues = filteredRecords.map(r => r.stock_val);
      }} else if (currentMode === 'profit') {{
        yValues = filteredRecords.map(r => r.profit);
      }} else if (currentMode === 'profit_with_div') {{
        yValues = filteredRecords.map(r => r.profit_with_div);
      }} else if (currentMode === 'stock_val_with_div') {{
        yValues = filteredRecords.map(r => r.stock_val_with_div);
      }} else if (currentMode === 'net_asset') {{
        yValues = filteredRecords.map(r => r.net_asset);
      }} else if (currentMode === 'daily_change') {{
        yValues = filteredRecords.map(r => r.daily_change);
      }} else if (currentMode === 'stacked') {{
        yValues = filteredRecords.map(r => r.stock_val);
      }}

      let minY = Math.min(...yValues);
      let maxY = Math.max(...yValues);

      if (currentMode === 'daily_change') {{
        const absMax = Math.max(Math.abs(minY), Math.abs(maxY)) * 1.15 || 100000;
        minY = -absMax;
        maxY = absMax;
      }} else if (currentMode === 'profit' || currentMode === 'profit_with_div') {{
        if (minY > 0) minY = 0;
        const range = maxY - minY || 1;
        minY = minY - range * 0.08;
        maxY = maxY + range * 0.08;
      }} else {{
        const range = maxY - minY || 1;
        minY = Math.max(0, minY - range * 0.1);
        maxY = maxY + range * 0.1;
      }}

      // Grid Lines & Y Axis Labels
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 1;
      ctx.fillStyle = '#94a3b8';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'right';

      const gridSteps = 5;
      for (let i = 0; i <= gridSteps; i++) {{
        const yVal = minY + (maxY - minY) * (i / gridSteps);
        const yPos = padTop + plotH - (plotH * (i / gridSteps));

        ctx.beginPath();
        ctx.moveTo(padLeft, yPos);
        ctx.lineTo(W - padRight, yPos);
        ctx.stroke();

        let label = '';
        if (Math.abs(yVal) >= 10000000) {{
          label = (yVal / 10000).toFixed(0) + ' 萬';
        }} else if (Math.abs(yVal) >= 10000) {{
          label = (yVal / 10000).toFixed(0) + ' 萬';
        }} else {{
          label = Math.round(yVal).toString();
        }}
        ctx.fillText(label, padLeft - 10, yPos + 4);

        if (currentMode === 'profit' || currentMode === 'profit_with_div') {{
          const pctVal = ((yVal / COST_PRINCIPAL) * 100).toFixed(1) + '%';
          ctx.textAlign = 'left';
          ctx.fillText((yVal >= 0 ? '+' : '') + pctVal, W - padRight + 10, yPos + 4);
          ctx.textAlign = 'right';
        }}
      }}

      // Zero Baseline
      if ((currentMode === 'profit' || currentMode === 'profit_with_div' || currentMode === 'daily_change') && minY <= 0 && maxY >= 0) {{
        const zeroY = padTop + plotH - (plotH * (-minY / (maxY - minY)));
        ctx.save();
        ctx.strokeStyle = '#f87171';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(padLeft, zeroY);
        ctx.lineTo(W - padRight, zeroY);
        ctx.stroke();
        ctx.fillStyle = '#f87171';
        ctx.textAlign = 'right';
        ctx.font = 'bold 11px sans-serif';
        ctx.fillText('0 損益兩平線', padLeft - 10, zeroY + 4);
        ctx.restore();
      }}

      // Draw X Axis dates
      ctx.textAlign = 'center';
      const xSteps = Math.min(6, filteredRecords.length);
      for (let i = 0; i < xSteps; i++) {{
        const idx = Math.floor(i * (filteredRecords.length - 1) / (xSteps - 1));
        const r = filteredRecords[idx];
        const xPos = padLeft + (idx / (filteredRecords.length - 1)) * plotW;
        ctx.fillText(r.date.substring(5), xPos, H - 12);
      }}

      // Plot series
      if (currentMode === 'daily_change') {{
        const barW = Math.max(2, (plotW / filteredRecords.length) * 0.7);
        const zeroY = padTop + plotH - (plotH * (-minY / (maxY - minY)));

        filteredRecords.forEach((r, idx) => {{
          const x = padLeft + (idx / (filteredRecords.length - 1)) * plotW;
          const y = padTop + plotH - (plotH * ((r.daily_change - minY) / (maxY - minY)));
          const h = zeroY - y;

          ctx.fillStyle = r.daily_change >= 0 ? '#34d399' : '#f87171';
          if (h >= 0) {{
            ctx.fillRect(x - barW/2, y, barW, h);
          }} else {{
            ctx.fillRect(x - barW/2, zeroY, barW, -h);
          }}
          hitAreas.push({{ x, y, r, idx }});
        }});
      }} else if (currentMode === 'stacked') {{
        const colors = ['#34d399', '#a78bfa', '#fb923c', '#38bdf8'];
        const n = filteredRecords.length;
        const stackVals = filteredRecords.map(r => [
          r.val878,
          r.val878 + r.val929,
          r.val878 + r.val929 + r.val56,
          r.val878 + r.val929 + r.val56 + r.val919
        ]);

        for (let layer = 3; layer >= 0; layer--) {{
          ctx.beginPath();
          filteredRecords.forEach((r, idx) => {{
            const x = padLeft + (idx / (n - 1)) * plotW;
            const val = stackVals[idx][layer];
            const y = padTop + plotH - (plotH * ((val - minY) / (maxY - minY)));
            if (idx === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }});
          ctx.lineTo(padLeft + plotW, padTop + plotH);
          ctx.lineTo(padLeft, padTop + plotH);
          ctx.closePath();
          ctx.fillStyle = colors[layer] + 'cc';
          ctx.fill();
        }}

        filteredRecords.forEach((r, idx) => {{
          const x = padLeft + (idx / (n - 1)) * plotW;
          const y = padTop + plotH - (plotH * ((r.stock_val - minY) / (maxY - minY)));
          hitAreas.push({{ x, y, r, idx }});
        }});
      }} else {{
        let mainColor = '#38bdf8';
        if (currentMode === 'profit') mainColor = '#10b981';
        if (currentMode === 'profit_with_div') mainColor = '#059669';
        if (currentMode === 'stock_val_with_div') mainColor = '#34d399';
        if (currentMode === 'net_asset') mainColor = '#818cf8';

        const grad = ctx.createLinearGradient(0, padTop, 0, padTop + plotH);
        grad.addColorStop(0, mainColor + '77');
        grad.addColorStop(1, mainColor + '08');

        ctx.beginPath();
        filteredRecords.forEach((r, idx) => {{
          const val = yValues[idx];
          const x = padLeft + (idx / (filteredRecords.length - 1)) * plotW;
          const y = padTop + plotH - (plotH * ((val - minY) / (maxY - minY)));
          if (idx === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
          hitAreas.push({{ x, y, r, idx }});
        }});
        ctx.strokeStyle = mainColor;
        ctx.lineWidth = 2.8;
        ctx.stroke();

        ctx.lineTo(padLeft + plotW, padTop + plotH);
        ctx.lineTo(padLeft, padTop + plotH);
        ctx.closePath();
        ctx.fillStyle = grad;
        ctx.fill();
      }}
    }}

    // Mouse Move Tooltip Handler
    canvas.addEventListener('mousemove', (e) => {{
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      if (!hitAreas.length) return;

      let closest = hitAreas[0];
      let minDx = Math.abs(mouseX - closest.x);
      for (let pt of hitAreas) {{
        const dx = Math.abs(mouseX - pt.x);
        if (dx < minDx) {{
          minDx = dx;
          closest = pt;
        }}
      }}

      if (minDx < 30) {{
        const r = closest.r;
        tooltip.style.display = 'block';
        tooltip.style.left = Math.min(rect.width - 260, Math.max(10, closest.x + 15)) + 'px';
        tooltip.style.top = Math.max(10, Math.min(rect.height - 220, closest.y - 50)) + 'px';

        const changeClass = r.daily_change >= 0 ? 'text-pos' : 'text-neg';
        const changeSign = r.daily_change >= 0 ? '+' : '';
        const profitClass = r.profit >= 0 ? 'text-pos' : 'text-neg';
        const profitSign = r.profit >= 0 ? '+' : '';

        tooltip.innerHTML = `
          <div class="tt-date">📅 ${{r.date}}</div>
          <div class="tt-row">
            <span class="tt-label">⚡ 今日獲利(增減):</span>
            <span class="tt-val ${{changeClass}}">${{changeSign}}NT$ ${{fmt(r.daily_change)}} (${{changeSign}}${{r.daily_change_pct}}%)</span>
          </div>
          <div class="tt-row">
            <span class="tt-label">🎯 持股累積獲利:</span>
            <span class="tt-val ${{profitClass}}">${{profitSign}}NT$ ${{fmt(r.profit)}} (${{profitSign}}${{r.profit_pct}}%)</span>
          </div>
          <div class="tt-row">
            <span class="tt-label">🎁 含息總獲利:</span>
            <span class="tt-val text-pos">+NT$ ${{fmt(r.profit_with_div)}} (+${{r.profit_with_div_pct}}%)</span>
          </div>
          <div class="tt-row">
            <span class="tt-label">📈 持股總市值:</span>
            <span class="tt-val" style="color:var(--primary)">NT$ ${{fmt(r.stock_val)}}</span>
          </div>
          <div class="tt-row">
            <span class="tt-label">💰 累計已領息:</span>
            <span class="tt-val" style="color:var(--success)">NT$ ${{fmt(r.cum_div)}}</span>
          </div>
          <div style="border-top:1px solid #334155; margin:6px 0; padding-top:4px;">
            <div class="tt-row" style="color:var(--c-919)"><span class="tt-label">00919:</span><span>${{r.s919}}張 @ ${{r.p919}} = NT$ ${{fmt(r.val919)}}</span></div>
            <div class="tt-row" style="color:var(--c-56)"><span class="tt-label">0056:</span><span>${{r.s56}}張 @ ${{r.p56}} = NT$ ${{fmt(r.val56)}}</span></div>
            <div class="tt-row" style="color:var(--c-929)"><span class="tt-label">00929:</span><span>${{r.s929}}張 @ ${{r.p929}} = NT$ ${{fmt(r.val929)}}</span></div>
            <div class="tt-row" style="color:var(--c-878)"><span class="tt-label">00878:</span><span>${{r.s878}}張 @ ${{r.p878}} = NT$ ${{fmt(r.val878)}}</span></div>
          </div>
        `;
      }} else {{
        tooltip.style.display = 'none';
      }}
    }});

    canvas.addEventListener('mouseleave', () => {{
      tooltip.style.display = 'none';
    }});

    window.addEventListener('resize', () => {{
      drawChart();
    }});

    // Populate Table
    function renderTable(records) {{
      const tb = document.getElementById('tableBody');
      tb.innerHTML = '';
      
      const reversed = [...records].reverse();
      reversed.forEach(r => {{
        const tr = document.createElement('tr');
        const changeClass = r.daily_change >= 0 ? 'text-pos' : 'text-neg';
        const changeSign = r.daily_change >= 0 ? '+' : '';
        const profitClass = r.profit >= 0 ? 'text-pos' : 'text-neg';
        const profitSign = r.profit >= 0 ? '+' : '';

        tr.innerHTML = `
          <td class="td-left" style="font-weight:600;">${{r.date}}</td>
          <td style="font-weight:700; color:var(--primary);">NT$ ${{fmt(r.stock_val)}}</td>
          <td class="${{profitClass}}" style="font-weight:700;">${{profitSign}}NT$ ${{fmt(r.profit)}}</td>
          <td class="${{profitClass}}">${{profitSign}}${{r.profit_pct}}%</td>
          <td class="${{changeClass}}" style="font-weight:600;">${{changeSign}}NT$ ${{fmt(r.daily_change)}}</td>
          <td style="color:var(--success); font-weight:600;">+NT$ ${{fmt(r.profit_with_div)}}</td>
          <td style="color:var(--success);">NT$ ${{fmt(r.cum_div)}}</td>
          <td style="color:var(--c-919);">${{r.s919}}張 / ${{r.p919}} / NT$ ${{fmt(r.val919)}}</td>
          <td style="color:var(--c-56);">${{r.s56}}張 / ${{r.p56}} / NT$ ${{fmt(r.val56)}}</td>
          <td style="color:var(--c-929);">${{r.s929}}張 / ${{r.p929}} / NT$ ${{fmt(r.val929)}}</td>
          <td style="color:var(--c-878);">${{r.s878}}張 / ${{r.p878}} / NT$ ${{fmt(r.val878)}}</td>
        `;
        tb.appendChild(tr);
      }});

      document.getElementById('tableCount').innerText = `顯示 ${{records.length}} / ${{allRecords.length}} 筆紀錄`;
    }}

    function filterTable() {{
      const q = document.getElementById('searchInput').value.trim().toLowerCase();
      if (!q) {{
        renderTable(allRecords);
      }} else {{
        const filtered = allRecords.filter(r => r.date.toLowerCase().includes(q));
        renderTable(filtered);
      }}
    }}

    // Populate Monthly Dividend Matrix
    function renderMonthlyGrid() {{
      const grid = document.getElementById('matrixGrid');
      grid.innerHTML = '';

      monthlyRecords.forEach(m => {{
        const card = document.createElement('div');
        card.className = 'matrix-card';
        card.innerHTML = `
          <div class="matrix-ym">
            <span>${{m.ym}}</span>
            <span style="font-size:11px; color:var(--text-muted);">領息月</span>
          </div>
          <div class="matrix-total text-pos">+NT$ ${{fmt(m.total_div)}}</div>
          <div style="font-size:11px; color:var(--text-muted); display:flex; flex-direction:column; gap:2px; margin-top:4px;">
            <span>00919: ${{m['00919_div'] ? m['00919_div'] + '元' : '-'}} (${{m['00919_shares']}}張)</span>
            <span>0056: ${{m['0056_div'] ? m['0056_div'] + '元' : '-'}} (${{m['0056_shares']}}張)</span>
            <span>00929: ${{m['00929_div'] ? m['00929_div'] + '元' : '-'}} (${{m['00929_shares']}}張)</span>
            <span>00878: ${{m['00878_div'] ? m['00878_div'] + '元' : '-'}} (${{m['00878_shares']}}張)</span>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    // Export CSV
    function exportCSV() {{
      let csv = '日期,持股總市值,持股獲利(NT$),獲利率(%),當日市值增減(今日獲利),含息總獲利(NT$),累計股息,含息總價值,淨總資產,00919張數,00919價格,00919市值,0056張數,0056價格,0056市值,00929張數,00929價格,00929市值,00878張數,00878價格,00878市值\\n';
      allRecords.forEach(r => {{
        csv += `${{r.date}},${{r.stock_val}},${{r.profit}},${{r.profit_pct}},${{r.daily_change}},${{r.profit_with_div}},${{r.cum_div}},${{r.stock_val_with_div}},${{r.net_asset}},${{r.s919}},${{r.p919}},${{r.val919}},${{r.s56}},${{r.p56}},${{r.val56}},${{r.s929}},${{r.p929}},${{r.val929}},${{r.s878}},${{r.p878}},${{r.val878}}\\n`;
      }});
      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `存股每日資產與獲利變化_${{allRecords[0].date}}_至_${{allRecords[allRecords.length-1].date}}.csv`;
      a.click();
    }}

    // Live Client-Side Sync via Google Sheets JSONP (Every 5 mins)
    const SHEET_ID = '1f60MjtB1ghxHLCYQjZgtmPGzYgm7E18fJP-K1lAViIM';

    window.handleGoogleSheetLiveResponse = function(response) {{
      try {{
        const rows = response.table.rows;
        // Parse Row 1 & Row 3
        const liveCost = rows[1]?.c[1]?.v || COST_PRINCIPAL;
        const liveStockVal = rows[1]?.c[2]?.v;
        const liveProfit = rows[1]?.c[3]?.v;
        const liveProfitPct = (rows[1]?.c[4]?.v || 0) * 100;
        const livePrevProfit = rows[1]?.c[11]?.v;
        const liveNetAsset = rows[1]?.c[12]?.v;
        const liveTodayProfit = rows[3]?.c[11]?.v;

        // Parse ETF rows (Row 4: 00929, Row 5: 00919, Row 6: 00878, Row 7: 0056)
        const p929 = rows[4]?.c[1]?.v, s929 = rows[4]?.c[3]?.v, val929 = rows[4]?.c[4]?.v;
        const p919 = rows[5]?.c[1]?.v, s919 = rows[5]?.c[3]?.v, val919 = rows[5]?.c[4]?.v;
        const p878 = rows[6]?.c[1]?.v, s878 = rows[6]?.c[3]?.v, val878 = rows[6]?.c[4]?.v;
        const p56  = rows[7]?.c[1]?.v, s56  = rows[7]?.c[3]?.v, val56  = rows[7]?.c[4]?.v;

        if (liveStockVal && liveProfit !== undefined) {{
          // Update Today Profit & Prev Profit Cards!
          if (liveTodayProfit !== undefined) {{
            const sign = liveTodayProfit >= 0 ? '+' : '-';
            document.getElementById('kpi-today-profit').innerText = `${{sign}}NT$ ${{fmt(Math.abs(liveTodayProfit))}}`;
          }}
          if (livePrevProfit !== undefined) {{
            const sign = livePrevProfit >= 0 ? '+' : '-';
            document.getElementById('kpi-prev-profit').innerText = `NT$ ${{fmt(livePrevProfit)}}`;
          }}

          // Update other KPI values
          document.getElementById('kpi-stock-val').innerText = 'NT$ ' + fmt(liveStockVal);
          document.getElementById('kpi-profit').innerText = (liveProfit >= 0 ? '+NT$ ' : '-NT$ ') + fmt(Math.abs(liveProfit));
          document.getElementById('kpi-profit-sub').innerHTML = `<span>獲利變化 ${{liveProfit >= 0 ? '+' : ''}}${{liveProfitPct.toFixed(2)}}%</span> <span style="color:var(--text-muted);font-size:11px;">(成本 ${{fmt(liveCost/10000)}} 萬)</span>`;
          if (liveNetAsset) document.getElementById('kpi-net-asset').innerText = 'NT$ ' + fmt(liveNetAsset);
          
          const lastR = allRecords[allRecords.length - 1];
          const cumDiv = lastR ? lastR.cum_div : 4483866;
          const liveProfitWithDiv = liveProfit + cumDiv;
          const liveProfitWithDivPct = ((liveProfitWithDiv / liveCost) * 100).toFixed(2);
          document.getElementById('kpi-with-div').innerText = '+NT$ ' + fmt(liveProfitWithDiv);

          // Update ETF cards
          if (p919 && s919) {{
            document.getElementById('price-919').innerText = p919 + ' 元';
            document.getElementById('val-919').innerText = 'NT$ ' + fmt(val919);
            document.getElementById('badge-919').innerText = ((val919 / liveStockVal) * 100).toFixed(1) + '%';
          }}
          if (p56 && s56) {{
            document.getElementById('price-56').innerText = p56 + ' 元';
            document.getElementById('val-56').innerText = 'NT$ ' + fmt(val56);
            document.getElementById('badge-56').innerText = ((val56 / liveStockVal) * 100).toFixed(1) + '%';
          }}
          if (p929 && s929) {{
            document.getElementById('price-929').innerText = p929 + ' 元';
            document.getElementById('val-929').innerText = 'NT$ ' + fmt(val929);
            document.getElementById('badge-929').innerText = ((val929 / liveStockVal) * 100).toFixed(1) + '%';
          }}
          if (p878 && s878) {{
            document.getElementById('price-878').innerText = p878 + ' 元';
            document.getElementById('val-878').innerText = 'NT$ ' + fmt(val878);
            document.getElementById('badge-878').innerText = ((val878 / liveStockVal) * 100).toFixed(1) + '%';
          }}

          // Update latest record in array and redraw chart
          if (lastR) {{
            lastR.stock_val = liveStockVal;
            lastR.profit = liveProfit;
            lastR.profit_pct = parseFloat(liveProfitPct.toFixed(2));
            lastR.profit_with_div = liveProfitWithDiv;
            lastR.profit_with_div_pct = parseFloat(liveProfitWithDivPct);
            if (liveTodayProfit !== undefined) lastR.daily_change = liveTodayProfit;
            if (liveNetAsset) lastR.net_asset = liveNetAsset;
            if (p919) {{ lastR.p919 = p919; lastR.val919 = val919; }}
            if (p56)  {{ lastR.p56 = p56; lastR.val56 = val56; }}
            if (p929) {{ lastR.p929 = p929; lastR.val929 = val929; }}
            if (p878) {{ lastR.p878 = p878; lastR.val878 = val878; }}
            drawChart();
            renderTable(filteredRecords.length === allRecords.length ? allRecords : filteredRecords);
          }}

          const now = new Date();
          const timeStr = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0') + ':' + String(now.getSeconds()).padStart(2, '0');
          document.getElementById('live-badge').innerHTML = `<span class="pulse-dot"></span> 雲端即時連線中 · 上次同步 ${{timeStr}} (每5分鐘自動同步)`;
        }}
      }} catch (err) {{
        console.warn('Live sheet parse error:', err);
      }}
    }};

    function syncLiveSheet(manual) {{
      const oldScript = document.getElementById('gviz-sync-script');
      if (oldScript) oldScript.remove();

      if (manual) {{
        document.getElementById('btn-sync').innerText = '⏳ 同步中...';
        setTimeout(() => {{ document.getElementById('btn-sync').innerText = '🔄 立即同步'; }}, 1200);
      }}

      const script = document.createElement('script');
      script.id = 'gviz-sync-script';
      script.src = `https://docs.google.com/spreadsheets/d/${{SHEET_ID}}/gviz/tq?tqx=responseHandler:handleGoogleSheetLiveResponse&_=${{Date.now()}}`;
      document.body.appendChild(script);
    }}

    // Init
    drawChart();
    renderTable(allRecords);
    renderMonthlyGrid();

    // Trigger initial live sync and schedule every 5 minutes (300,000 ms)
    syncLiveSheet(false);
    setInterval(() => {{
      syncLiveSheet(false);
    }}, 5 * 60 * 1000);
  </script>
</body>
</html>
'''

output_path = '/Users/10404604/.gemini/antigravity/scratch/stock-portfolio-tracker/index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Updated build_html.py and generated index.html successfully!')
