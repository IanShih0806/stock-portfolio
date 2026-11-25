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
      --tw-red: #f87171;       /* 台股紅：獲利、上漲 */
      --tw-red-bold: #ef4444;
      --tw-green: #34d399;     /* 台股綠：虧損、下跌 */
      --tw-green-bold: #10b981;
      --warning: #fbbf24;
      --c-919: #38bdf8;
      --c-56: #fb923c;
      --c-929: #a78bfa;
      --c-878: #38bdf8;
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
      background: rgba(239, 68, 68, 0.15);
      color: var(--tw-red);
      border-color: rgba(239, 68, 68, 0.3);
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      background: var(--tw-red);
      border-radius: 50%;
      display: inline-block;
      box-shadow: 0 0 8px var(--tw-red);
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
      70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }}
      100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
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

    /* KPI Cards (4 精準大卡片) */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }}
    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
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
      top: 0; left: 0; right: 0; height: 4px;
      background: var(--card-border);
    }}
    .kpi-card.c-today::before {{ background: var(--tw-red-bold); }}
    .kpi-card.c-profit::before {{ background: var(--tw-red-bold); }}
    .kpi-card.c-amber::before {{ background: var(--warning); }}
    .kpi-card.c-purple::before {{ background: #818cf8; }}
    
    .kpi-label {{ font-size: 14px; color: var(--text-muted); font-weight: 500; display: flex; justify-content: space-between; align-items: center; }}
    .kpi-value {{ font-size: 26px; font-weight: 700; color: #fff; letter-spacing: -0.5px; }}
    .kpi-sub {{ font-size: 13px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }}
    
    /* 台股色彩類別：紅獲利綠虧損 */
    .text-pos {{ color: var(--tw-red) !important; }}
    .text-neg {{ color: var(--tw-green) !important; }}
    .highlight-gain {{ color: #f87171 !important; font-size: 27px; font-weight: 800; }}

    /* 歷史排名標籤 */
    .rank-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 6px;
      line-height: 1.4;
    }}
    .rank-gain {{
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}
    .rank-loss {{
      background: rgba(34, 197, 94, 0.2);
      color: #4ade80;
      border: 1px solid rgba(34, 197, 94, 0.4);
    }}

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
    .b-878 {{ background: rgba(56, 189, 248, 0.2); color: var(--c-878); }}
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
      color: var(--tw-red);
    }}
    .pill.highlight.active {{
      background: #7f1d1d;
      color: #fca5a5;
      border: 1px solid #b91c1c;
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
      cursor: pointer;
      user-select: none;
      transition: color 0.15s, background 0.15s;
    }}
    thead th:hover {{
      color: #fff;
      background: #1e293b;
    }}
    thead th .sort-icon {{
      font-size: 11px;
      margin-left: 4px;
      color: #64748b;
    }}
    thead th.sorted {{
      color: var(--primary);
    }}
    thead th.sorted .sort-icon {{
      color: var(--primary);
    }}
    tbody tr {{ border-bottom: 1px solid rgba(51, 65, 85, 0.5); transition: background 0.15s; }}
    tbody tr:hover {{ background: rgba(51, 65, 85, 0.4); }}
    tbody td {{
      padding: 10px 14px;
      color: #e2e8f0;
      white-space: nowrap;
    }}
    .th-left, .td-left {{ text-align: left; }}

    /* List Table for Monthly Dividends */
    .monthly-table thead th {{
      cursor: default;
    }}
    .monthly-table thead th:hover {{
      color: var(--text-muted);
      background: #0f172a;
    }}

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
        <p>追蹤區間：<span id="range-label">2024-09-02 至 2026-11-25</span> · 共 541 個交易日 · 台股色彩慣例：<span style="color:var(--tw-red);font-weight:700;">紅賺</span> / <span style="color:var(--tw-green);font-weight:700;">綠賠</span></p>
      </div>
      <div class="header-actions">
        <span class="badge badge-live" id="live-badge"><span class="pulse-dot"></span> 雲端連線中 · 每5分鐘自動同步</span>
        <button class="btn" id="btn-sync" onclick="syncLiveSheet(true)">🔄 立即同步</button>
        <button class="btn btn-primary" onclick="exportCSV()">📥 匯出每日 CSV</button>
      </div>
    </div>

    <!-- KPI Summary Grid (4 大核心看板) -->
    <div class="kpi-grid">
      <!-- 1. 今日獲利 (單日損益) + 下方小字：前日獲利變化 & 歷史排名 -->
      <div class="kpi-card c-today" onclick="setMode('daily_change')">
        <div class="kpi-label">
          <span>今日獲利 (單日損益)</span>
          <span class="rank-badge rank-gain" id="today-rank-badge">🏆 獲利第 1 名</span>
        </div>
        <div class="kpi-value highlight-gain" id="kpi-today-profit">+NT$ 1,997,171</div>
        <div class="kpi-sub" id="kpi-today-sub">
          <span style="color:var(--text-muted);">前日獲利變化：</span>
          <span class="text-pos" style="font-weight:600;" id="kpi-prev-val">NT$ 7,179,469</span>
        </div>
      </div>

      <!-- 2. 持股獲利 (主要大字顯示獲利金額與%，下方小字為持股總市值) -->
      <div class="kpi-card c-profit" onclick="setMode('profit')">
        <div class="kpi-label">
          <span>持股獲利 (未實現損益)</span>
          <span>🎯 點選看走勢</span>
        </div>
        <div class="kpi-value text-pos" id="kpi-profit-main">+NT$ 7,655,223 (+54.42%)</div>
        <div class="kpi-sub" id="kpi-stock-sub">
          <span style="color:var(--text-muted);">持股總市值：</span>
          <span style="font-weight:600; color:var(--primary);" id="kpi-stock-val">NT$ 21,722,560</span>
        </div>
      </div>

      <!-- 3. 近 3 個月平均領息金額 -->
      <div class="kpi-card c-amber" onclick="scrollToMonthly()">
        <div class="kpi-label">
          <span>近 3 次平均月領息</span>
          <span>💵 穩定現金流</span>
        </div>
        <div class="kpi-value text-pos" id="kpi-3m-div">NT$ 295,253</div>
        <div class="kpi-sub" style="color:var(--text-muted);" id="kpi-3m-sub">
          <span>近 3 個月 (9、10、11月) 平均每月領息</span>
        </div>
      </div>

      <!-- 4. 淨總資產 (試算表資產總值) -->
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

    <!-- ETF Position Status (含今日漲跌金額與%數) -->
    <div class="etf-grid">
      <div class="etf-card">
        <div class="etf-header">
          <div>
            <div class="etf-code">00919 群益台灣精選高息</div>
            <div class="etf-name">佔比第一大核心持股</div>
          </div>
          <span class="etf-badge b-919" id="badge-919">41.2%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-919">320.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新股價 (今日漲跌)</span>
            <span class="etf-metric-val" id="price-box-919">
              <span id="price-919">27.95 元</span>
              <span id="chg-919" class="text-pos" style="font-size:11px; margin-left:4px;">▲ +0.08 (+0.29%)</span>
            </span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-919">NT$ 8,944,000</span>
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
          <span class="etf-badge b-56" id="badge-56">23.7%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-56">112.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新股價 (今日漲跌)</span>
            <span class="etf-metric-val" id="price-box-56">
              <span id="price-56">45.90 元</span>
              <span id="chg-56" class="text-pos" style="font-size:11px; margin-left:4px;">▲ +0.18 (+0.39%)</span>
            </span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-56">NT$ 5,140,800</span>
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
          <span class="etf-badge b-929" id="badge-929">20.3%</span>
        </div>
        <div class="etf-metrics">
          <div class="etf-metric-item">
            <span class="etf-metric-label">持股張數</span>
            <span class="etf-metric-val" id="shares-929">200.000 張</span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">最新股價 (今日漲跌)</span>
            <span class="etf-metric-val" id="price-box-929">
              <span id="price-929">22.10 元</span>
              <span id="chg-929" class="text-pos" style="font-size:11px; margin-left:4px;">▲ +0.05 (+0.23%)</span>
            </span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-929">NT$ 4,420,000</span>
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
            <span class="etf-metric-label">最新股價 (今日漲跌)</span>
            <span class="etf-metric-val" id="price-box-878">
              <span id="price-878">28.73 元</span>
              <span id="chg-878" class="text-pos" style="font-size:11px; margin-left:4px;">▲ +0.10 (+0.35%)</span>
            </span>
          </div>
          <div class="etf-metric-item">
            <span class="etf-metric-label">當前市值</span>
            <span class="etf-metric-val" id="val-878">NT$ 3,217,760</span>
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

    <!-- Daily Historical Table (支援點選表頭排序 & 歷史排名顯示) -->
    <div class="table-section">
      <div class="table-header">
        <div>
          <h2>📅 每日持股明細歷史紀錄</h2>
          <p style="color:var(--text-muted);font-size:13px;margin-top:4px;">點選任何「欄位表頭」即可自訂由大到小或由小到大排序；重新整理自動還原依最新日期排序</p>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <button class="btn" onclick="resetSort()">🔄 還原日期排序</button>
          <input type="text" id="searchInput" class="search-input" placeholder="🔍 搜尋日期 (例如: 2026-11 或 2025-05)" oninput="filterTable()">
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th class="th-left sorted" id="th-date" onclick="sortTable('date')">日期 <span class="sort-icon" id="icon-date">▼</span></th>
              <th id="th-rank_num" onclick="sortTable('rank_num')">歷史漲跌排名 <span class="sort-icon" id="icon-rank_num">↕</span></th>
              <th id="th-daily_change" onclick="sortTable('daily_change')">當日增減 (今日獲利 NT$) <span class="sort-icon" id="icon-daily_change">↕</span></th>
              <th id="th-profit" onclick="sortTable('profit')" style="color:var(--tw-red);">持股獲利 (NT$) <span class="sort-icon" id="icon-profit">↕</span></th>
              <th id="th-profit_pct" onclick="sortTable('profit_pct')" style="color:var(--tw-red);">獲利變化% <span class="sort-icon" id="icon-profit_pct">↕</span></th>
              <th id="th-stock_val" onclick="sortTable('stock_val')">持股總市值 (NT$) <span class="sort-icon" id="icon-stock_val">↕</span></th>
              <th id="th-profit_with_div" onclick="sortTable('profit_with_div')" style="color:var(--tw-red);">含息總獲利 (NT$) <span class="sort-icon" id="icon-profit_with_div">↕</span></th>
              <th id="th-cum_div" onclick="sortTable('cum_div')">累計已領息 (NT$) <span class="sort-icon" id="icon-cum_div">↕</span></th>
              <th id="th-val919" onclick="sortTable('val919')" style="color:var(--c-919);">00919 (張/價/值) <span class="sort-icon" id="icon-val919">↕</span></th>
              <th id="th-val56" onclick="sortTable('val56')" style="color:var(--c-56);">0056 (張/價/值) <span class="sort-icon" id="icon-val56">↕</span></th>
              <th id="th-val929" onclick="sortTable('val929')" style="color:var(--c-929);">00929 (張/價/值) <span class="sort-icon" id="icon-val929">↕</span></th>
              <th id="th-val878" onclick="sortTable('val878')" style="color:var(--c-878);">00878 (張/價/值) <span class="sort-icon" id="icon-val878">↕</span></th>
            </tr>
          </thead>
          <tbody id="tableBody">
            <!-- Dynamic rows -->
          </tbody>
        </table>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; color:var(--text-muted); font-size:12px;">
        <span id="tableCount">顯示 0 / 0 筆</span>
        <span>提示：點擊任一欄位表頭可自訂升降冪排序</span>
      </div>
    </div>

    <!-- Monthly Dividends List Section (最新在最上面列表呈現) -->
    <div class="table-section" id="monthly-section">
      <div class="table-header">
        <div>
          <h2>💵 歷月領息與被動現金流紀錄 (依月份最新排序)</h2>
          <p style="color:var(--text-muted);font-size:13px;margin-top:4px;">最新月份領息在最上方 · 統計各月份實際入帳股息、每檔 ETF 配發單價與領取金額</p>
        </div>
        <div style="font-size:14px; font-weight:700; color:var(--tw-red);">
          累計總入帳股息：NT$ 4,483,866 元
        </div>
      </div>
      
      <div class="table-container">
        <table class="monthly-table">
          <thead>
            <tr>
              <th class="th-left">領息月份</th>
              <th style="color:var(--tw-red);">當月總股息 (NT$)</th>
              <th style="color:var(--c-919);">00919 配息明細</th>
              <th style="color:var(--c-56);">0056 配息明細</th>
              <th style="color:var(--c-929);">00929 配息明細</th>
              <th style="color:var(--c-878);">00878 配息明細</th>
              <th>當期累計已領股息 (NT$)</th>
            </tr>
          </thead>
          <tbody id="monthlyTableBody">
            <!-- Dynamic monthly rows -->
          </tbody>
        </table>
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
    const summary = PORTFOLIO_DATA.summary || {{}};
    const COST_PRINCIPAL = summary.cost || 14066887.0;
    
    let currentMode = 'profit';
    let currentRange = 'all';
    let filteredRecords = [...allRecords];
    
    // Table sorting state
    let sortKey = 'date';
    let sortAsc = false; // default date descending

    function fmt(n) {{
      return Math.round(n || 0).toLocaleString('en-US');
    }}

    function scrollToMonthly() {{
      document.getElementById('monthly-section').scrollIntoView({{ behavior: 'smooth' }});
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

    // Canvas Chart Rendering (紅漲綠跌)
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
          ctx.fillStyle = yVal >= 0 ? '#f87171' : '#34d399';
          ctx.fillText((yVal >= 0 ? '+' : '') + pctVal, W - padRight + 10, yPos + 4);
          ctx.fillStyle = '#94a3b8';
          ctx.textAlign = 'right';
        }}
      }}

      // Zero Baseline
      if ((currentMode === 'profit' || currentMode === 'profit_with_div' || currentMode === 'daily_change') && minY <= 0 && maxY >= 0) {{
        const zeroY = padTop + plotH - (plotH * (-minY / (maxY - minY)));
        ctx.save();
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(padLeft, zeroY);
        ctx.lineTo(W - padRight, zeroY);
        ctx.stroke();
        ctx.fillStyle = '#cbd5e1';
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

      // Plot series (紅漲綠跌)
      if (currentMode === 'daily_change') {{
        const barW = Math.max(2, (plotW / filteredRecords.length) * 0.7);
        const zeroY = padTop + plotH - (plotH * (-minY / (maxY - minY)));

        filteredRecords.forEach((r, idx) => {{
          const x = padLeft + (idx / (filteredRecords.length - 1)) * plotW;
          const y = padTop + plotH - (plotH * ((r.daily_change - minY) / (maxY - minY)));
          const h = zeroY - y;

          ctx.fillStyle = r.daily_change >= 0 ? '#ef4444' : '#22c55e';
          if (h >= 0) {{
            ctx.fillRect(x - barW/2, y, barW, h);
          }} else {{
            ctx.fillRect(x - barW/2, zeroY, barW, -h);
          }}
          hitAreas.push({{ x, y, r, idx }});
        }});
      }} else if (currentMode === 'stacked') {{
        const colors = ['#38bdf8', '#a78bfa', '#fb923c', '#0284c7'];
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
        if (currentMode === 'profit') mainColor = '#f87171'; // 台股紅
        if (currentMode === 'profit_with_div') mainColor = '#ef4444';
        if (currentMode === 'stock_val_with_div') mainColor = '#38bdf8';
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

    // Mouse Move Tooltip Handler (含排名與漲跌)
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
        tooltip.style.top = Math.max(10, Math.min(rect.height - 230, closest.y - 50)) + 'px';

        const changeClass = r.daily_change >= 0 ? 'text-pos' : 'text-neg';
        const changeSign = r.daily_change >= 0 ? '+' : '';
        const profitClass = r.profit >= 0 ? 'text-pos' : 'text-neg';
        const profitSign = r.profit >= 0 ? '+' : '';

        const rankBadge = r.rank_type === 'gain' 
          ? `<span class="rank-badge rank-gain">🏆 ${{r.rank_text}}</span>`
          : (r.rank_type === 'loss' ? `<span class="rank-badge rank-loss">⚠️ ${{r.rank_text}}</span>` : '');

        tooltip.innerHTML = `
          <div class="tt-date" style="display:flex; justify-content:space-between; align-items:center;">
            <span>📅 ${{r.date}}</span>
            ${{rankBadge}}
          </div>
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
            <span class="tt-val" style="color:var(--primary)">NT$ ${{fmt(r.cum_div)}}</span>
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

    // Table Sorting Functionality
    function sortTable(key) {{
      if (sortKey === key) {{
        sortAsc = !sortAsc;
      }} else {{
        sortKey = key;
        sortAsc = (key === 'date') ? false : false; // default desc for numbers
      }}

      // Update Header Icons
      document.querySelectorAll('thead th').forEach(th => {{
        th.classList.remove('sorted');
        const icon = th.querySelector('.sort-icon');
        if (icon) icon.innerText = '↕';
      }});

      const currTh = document.getElementById('th-' + key);
      const currIcon = document.getElementById('icon-' + key);
      if (currTh) currTh.classList.add('sorted');
      if (currIcon) currIcon.innerText = sortAsc ? '▲' : '▼';

      applySortAndRender();
    }}

    function resetSort() {{
      sortKey = 'date';
      sortAsc = false;
      document.querySelectorAll('thead th').forEach(th => {{
        th.classList.remove('sorted');
        const icon = th.querySelector('.sort-icon');
        if (icon) icon.innerText = '↕';
      }});
      const thDate = document.getElementById('th-date');
      const iconDate = document.getElementById('icon-date');
      if (thDate) thDate.classList.add('sorted');
      if (iconDate) iconDate.innerText = '▼';

      document.getElementById('searchInput').value = '';
      applySortAndRender();
    }}

    function applySortAndRender() {{
      const q = document.getElementById('searchInput').value.trim().toLowerCase();
      let records = q ? allRecords.filter(r => r.date.toLowerCase().includes(q)) : [...allRecords];

      records.sort((a, b) => {{
        let vA = a[sortKey];
        let vB = b[sortKey];
        if (sortKey === 'rank_num') {{
          // Special sort for rank: gains first (1..N), then even, then losses (1..N)
          vA = a.daily_change;
          vB = b.daily_change;
        }}
        if (typeof vA === 'string') {{
          return sortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        }} else {{
          return sortAsc ? (vA - vB) : (vB - vA);
        }}
      }});

      renderTable(records);
    }}

    // Populate Daily Historical Table (含歷史漲跌排名)
    function renderTable(records) {{
      const tb = document.getElementById('tableBody');
      tb.innerHTML = '';

      records.forEach(r => {{
        const tr = document.createElement('tr');
        const changeClass = r.daily_change >= 0 ? 'text-pos' : 'text-neg';
        const changeSign = r.daily_change >= 0 ? '+' : '';
        const profitClass = r.profit >= 0 ? 'text-pos' : 'text-neg';
        const profitSign = r.profit >= 0 ? '+' : '';

        const rankBadge = r.rank_type === 'gain' 
          ? `<span class="rank-badge rank-gain">🏆 ${{r.rank_text}}</span>`
          : (r.rank_type === 'loss' ? `<span class="rank-badge rank-loss">⚠️ ${{r.rank_text}}</span>` : `<span style="color:var(--text-muted);">-</span>`);

        tr.innerHTML = `
          <td class="td-left" style="font-weight:600;">${{r.date}}</td>
          <td style="text-align:center;">${{rankBadge}}</td>
          <td class="${{changeClass}}" style="font-weight:700;">${{changeSign}}NT$ ${{fmt(r.daily_change)}}</td>
          <td class="${{profitClass}}" style="font-weight:700;">${{profitSign}}NT$ ${{fmt(r.profit)}}</td>
          <td class="${{profitClass}}">${{profitSign}}${{r.profit_pct}}%</td>
          <td style="font-weight:600; color:var(--primary);">NT$ ${{fmt(r.stock_val)}}</td>
          <td class="text-pos" style="font-weight:600;">+NT$ ${{fmt(r.profit_with_div)}}</td>
          <td style="color:var(--primary);">${{fmt(r.cum_div)}}</td>
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
      applySortAndRender();
    }}

    // Populate Monthly Dividend Table (列表方式，最新在最上方)
    function renderMonthlyTable() {{
      const tb = document.getElementById('monthlyTableBody');
      tb.innerHTML = '';

      // Sort descending by ym (最新在最上面)
      const sortedM = [...monthlyRecords].sort((a, b) => b.ym.localeCompare(a.ym));
      
      // Compute running cumulative dividends backwards
      let runningCum = summary.dividend_up_to_now || 4483866;
      
      sortedM.forEach(m => {{
        const tr = document.createElement('tr');
        
        const d919 = m['00919_div'] ? `${{m['00919_div']}}元 (${{m['00919_shares']}}張 = NT$ ${{fmt(m['00919_div']*m['00919_shares']*1000)}})` : '-';
        const d56  = m['0056_div']  ? `${{m['0056_div']}}元 (${{m['0056_shares']}}張 = NT$ ${{fmt(m['0056_div']*m['0056_shares']*1000)}})` : '-';
        const d929 = m['00929_div'] ? `${{m['00929_div']}}元 (${{m['00929_shares']}}張 = NT$ ${{fmt(m['00929_div']*m['00929_shares']*1000)}})` : '-';
        const d878 = m['00878_div'] ? `${{m['00878_div']}}元 (${{m['00878_shares']}}張 = NT$ ${{fmt(m['00878_div']*m['00878_shares']*1000)}})` : '-';

        tr.innerHTML = `
          <td class="td-left" style="font-weight:700; color:var(--primary); font-size:14px;">${{m.ym}}</td>
          <td class="text-pos" style="font-weight:800; font-size:14px;">+NT$ ${{fmt(m.total_div)}}</td>
          <td style="color:var(--c-919);">${{d919}}</td>
          <td style="color:var(--c-56);">${{d56}}</td>
          <td style="color:var(--c-929);">${{d929}}</td>
          <td style="color:var(--c-878);">${{d878}}</td>
          <td style="font-weight:600; color:var(--text);">${{fmt(runningCum)}}</td>
        `;
        tb.appendChild(tr);
        runningCum -= m.total_div;
      }});
    }}

    // Export CSV (含排名)
    function exportCSV() {{
      let csv = '日期,歷史漲跌排名,持股獲利(NT$),獲利率(%),當日市值增減(今日獲利),持股總市值,含息總獲利(NT$),累計股息,含息總價值,淨總資產,00919張數,00919價格,00919市值,0056張數,0056價格,0056市值,00929張數,00929價格,00929市值,00878張數,00878價格,00878市值\\n';
      allRecords.forEach(r => {{
        csv += `${{r.date}},"${{r.rank_text}}",${{r.profit}},${{r.profit_pct}},${{r.daily_change}},${{r.stock_val}},${{r.profit_with_div}},${{r.cum_div}},${{r.stock_val_with_div}},${{r.net_asset}},${{r.s919}},${{r.p919}},${{r.val919}},${{r.s56}},${{r.p56}},${{r.val56}},${{r.s929}},${{r.p929}},${{r.val929}},${{r.s878}},${{r.p878}},${{r.val878}}\\n`;
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
        const liveCost = rows[1]?.c[1]?.v || COST_PRINCIPAL;
        const liveStockVal = rows[1]?.c[2]?.v;
        const liveProfit = rows[1]?.c[3]?.v;
        const liveProfitPct = (rows[1]?.c[4]?.v || 0) * 100;
        const livePrevProfit = rows[1]?.c[11]?.v;
        const liveNetAsset = rows[1]?.c[12]?.v;
        const liveTodayProfit = rows[3]?.c[11]?.v;

        // ETF live prices & changes
        const p929 = rows[4]?.c[1]?.v, s929 = rows[4]?.c[3]?.v, val929 = rows[4]?.c[4]?.v, chg929 = rows[4]?.c[9]?.v;
        const p919 = rows[5]?.c[1]?.v, s919 = rows[5]?.c[3]?.v, val919 = rows[5]?.c[4]?.v, chg919 = rows[5]?.c[9]?.v;
        const p878 = rows[6]?.c[1]?.v, s878 = rows[6]?.c[3]?.v, val878 = rows[6]?.c[4]?.v, chg878 = rows[6]?.c[9]?.v;
        const p56  = rows[7]?.c[1]?.v, s56  = rows[7]?.c[3]?.v, val56  = rows[7]?.c[4]?.v, chg56  = rows[7]?.c[9]?.v;

        if (liveStockVal && liveProfit !== undefined) {{
          // 1. Update Today Profit & Prev Profit subtext
          if (liveTodayProfit !== undefined) {{
            const sign = liveTodayProfit >= 0 ? '+' : '-';
            const el = document.getElementById('kpi-today-profit');
            if (el) {{
              el.innerText = `${{sign}}NT$ ${{fmt(Math.abs(liveTodayProfit))}}`;
              el.className = 'kpi-value ' + (liveTodayProfit >= 0 ? 'text-pos highlight-gain' : 'text-neg');
            }}
          }}
          if (livePrevProfit !== undefined) {{
            const el = document.getElementById('kpi-prev-val');
            if (el) {{
              el.innerText = `NT$ ${{fmt(livePrevProfit)}}`;
              el.className = livePrevProfit >= 0 ? 'text-pos' : 'text-neg';
            }}
          }}

          // 2. Update Card 2: Main text = 持股獲利, subtext = 持股總市值
          const profitMainEl = document.getElementById('kpi-profit-main');
          if (profitMainEl) {{
            const sign = liveProfit >= 0 ? '+' : '-';
            profitMainEl.innerText = `${{sign}}NT$ ${{fmt(Math.abs(liveProfit))}} (${{sign}}${{liveProfitPct.toFixed(2)}}%)`;
            profitMainEl.className = 'kpi-value ' + (liveProfit >= 0 ? 'text-pos' : 'text-neg');
          }}

          const stockValEl = document.getElementById('kpi-stock-val');
          if (stockValEl) {{
            stockValEl.innerText = 'NT$ ' + fmt(liveStockVal);
          }}

          // 3. Update Net Assets
          if (liveNetAsset) {{
            const netEl = document.getElementById('kpi-net-asset');
            if (netEl) netEl.innerText = 'NT$ ' + fmt(liveNetAsset);
          }}

          // Helper for rendering ETF price & change badge
          function updateEtfCard(code, p, s, val, chg) {{
            if (!p || !s) return;
            const pEl = document.getElementById('price-' + code);
            const valEl = document.getElementById('val-' + code);
            const badgeEl = document.getElementById('badge-' + code);
            const chgEl = document.getElementById('chg-' + code);

            if (pEl) pEl.innerText = p + ' 元';
            if (valEl) valEl.innerText = 'NT$ ' + fmt(val);
            if (badgeEl) badgeEl.innerText = ((val / liveStockVal) * 100).toFixed(1) + '%';
            
            if (chgEl && chg !== undefined) {{
              const numChg = parseFloat(chg);
              const sign = numChg >= 0 ? '+' : '';
              const prevP = p - numChg;
              const pct = prevP > 0 ? ((numChg / prevP) * 100).toFixed(2) : '0.00';
              const arrow = numChg > 0 ? '▲ ' : (numChg < 0 ? '▼ ' : '');
              const cls = numChg >= 0 ? 'text-pos' : 'text-neg';
              chgEl.className = cls;
              chgEl.innerText = `${{arrow}}${{sign}}${{numChg}} (${{sign}}${{pct}}%)`;
            }}
          }}

          updateEtfCard('919', p919, s919, val919, chg919);
          updateEtfCard('56',  p56,  s56,  val56,  chg56);
          updateEtfCard('929', p929, s929, val929, chg929);
          updateEtfCard('878', p878, s878, val878, chg878);

          // Update latest record in array and redraw chart
          const lastR = allRecords[allRecords.length - 1];
          if (lastR) {{
            lastR.stock_val = liveStockVal;
            lastR.profit = liveProfit;
            lastR.profit_pct = parseFloat(liveProfitPct.toFixed(2));
            if (liveTodayProfit !== undefined) lastR.daily_change = liveTodayProfit;
            if (liveNetAsset) lastR.net_asset = liveNetAsset;
            drawChart();
            applySortAndRender();
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

    // Init Page
    drawChart();
    applySortAndRender();
    renderMonthlyTable();

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

print('Generated index.html with all requested enhancements successfully!')
