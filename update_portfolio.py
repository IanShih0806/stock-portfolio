import urllib.request
import json
import datetime
import pandas as pd
import os

print("=== 正在從 Google 試算表同步存股紀錄... ===")
sheet_id = '1f60MjtB1ghxHLCYQjZgtmPGzYgm7E18fJP-K1lAViIM'
xlsx_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx'
req = urllib.request.Request(xlsx_url, headers={'User-Agent': 'Mozilla/5.0'})

base_dir = os.path.dirname(os.path.abspath(__file__))
xlsx_path = os.path.join(base_dir, 'portfolio.xlsx')

with urllib.request.urlopen(req) as resp:
    with open(xlsx_path, 'wb') as f:
        f.write(resp.read())

print("已下載最新 Excel，正在解析月度持股張數與股息...")
df = pd.read_excel(xlsx_path, sheet_name='存股記錄表', header=None)

monthly_records = {}
for i in range(13, 40):
    row = df.iloc[i]
    dt_val = row[0]
    if pd.isna(dt_val): continue
    ym = str(dt_val)[:7]
    monthly_records[ym] = {
        'ym': ym,
        '00929_shares': float(row[2]) if pd.notna(row[2]) else 0.0,
        '00919_shares': float(row[4]) if pd.notna(row[4]) else 0.0,
        '00878_shares': float(row[6]) if pd.notna(row[6]) else 0.0,
        '0056_shares': float(row[8]) if pd.notna(row[8]) else 0.0,
        '00929_div': float(row[3]) if pd.notna(row[3]) else 0.0,
        '00919_div': float(row[5]) if pd.notna(row[5]) else 0.0,
        '00878_div': float(row[7]) if pd.notna(row[7]) else 0.0,
        '0056_div': float(row[9]) if pd.notna(row[9]) else 0.0,
        'total_div': float(row[1]) if pd.notna(row[1]) else 0.0,
    }

print("正在從 Yahoo Finance 抓取四大 ETF 歷史股價...")
start_ts = int(datetime.datetime(2024, 8, 25).timestamp())
end_ts = int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp())
tickers = {
    '00929': '00929.TW',
    '00919': '00919.TW',
    '00878': '00878.TW',
    '0056': '0056.TW'
}

raw_prices = {}
all_days = set()

for code, ticker in tickers.items():
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start_ts}&period2={end_ts}&interval=1d'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            d = json.loads(resp.read().decode('utf-8'))
            res = d['chart']['result'][0]
            ts_list = res['timestamp']
            closes = res['indicators']['quote'][0]['close']
            series = {}
            for ts, c in zip(ts_list, closes):
                if c is not None:
                    day_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    series[day_str] = round(c, 2)
                    all_days.add(day_str)
            raw_prices[code] = series
    except Exception as e:
        print(f"警告：抓取 {code} 失敗：{e}")

sorted_days = sorted([d for d in all_days if d >= '2024-09-01'])
prices = {'00929': {}, '00919': {}, '00878': {}, '0056': {}}
last_known = {'00929': 19.5, '00919': 24.5, '00878': 22.5, '0056': 37.5}

for code in tickers:
    prior_days = sorted([d for d in raw_prices.get(code, {}) if d < '2024-09-01'])
    if prior_days:
        last_known[code] = raw_prices[code][prior_days[-1]]

for d in sorted_days:
    for code in tickers:
        if d in raw_prices.get(code, {}):
            last_known[code] = raw_prices[code][d]
        prices[code][d] = last_known[code]

sorted_yms = sorted(monthly_records.keys())
ym_cum_div = {}
running_div = 0.0
for ym in sorted_yms:
    running_div += monthly_records[ym]['total_div']
    ym_cum_div[ym] = running_div

daily_data = []
prev_stock_val = None
loan_start_date = '2026-01-09'
const_remaining_capital = 1696801.0
const_paid_mortgage = 5350000.0
const_pledge_loan = 7200000.0

for d in sorted_days:
    ym = d[:7]
    m_info = monthly_records.get(ym, monthly_records[sorted_yms[-1]])
    
    p929 = prices['00929'][d]
    p919 = prices['00919'][d]
    p878 = prices['00878'][d]
    p56 = prices['0056'][d]
    
    s929 = m_info['00929_shares']
    s919 = m_info['00919_shares']
    s878 = m_info['00878_shares']
    s56 = m_info['0056_shares']
    
    val929 = round(s929 * 1000 * p929, 0)
    val919 = round(s919 * 1000 * p919, 0)
    val878 = round(s878 * 1000 * p878, 0)
    val56 = round(s56 * 1000 * p56, 0)
    
    stock_val = val929 + val919 + val878 + val56
    
    if prev_stock_val is None:
        daily_change = 0.0
        daily_change_pct = 0.0
    else:
        daily_change = stock_val - prev_stock_val
        daily_change_pct = round((daily_change / prev_stock_val) * 100, 2)
    prev_stock_val = stock_val
    
    cum_div_val = ym_cum_div.get(ym, running_div)
    stock_val_with_div = stock_val + cum_div_val
    
    loan_val = const_pledge_loan if d >= loan_start_date else 0.0
    net_asset = stock_val + const_remaining_capital + const_paid_mortgage - loan_val
    
    daily_data.append({
        'date': d,
        'stock_val': stock_val,
        'daily_change': daily_change,
        'daily_change_pct': daily_change_pct,
        'cum_div': cum_div_val,
        'stock_val_with_div': stock_val_with_div,
        'net_asset': net_asset,
        'p929': p929, 's929': s929, 'val929': val929,
        'p919': p919, 's919': s919, 'val919': val919,
        'p878': p878, 's878': s878, 'val878': val878,
        'p56': p56, 's56': s56, 'val56': val56
    })

out_json = os.path.join(base_dir, 'portfolio_data.json')
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({
        'daily_data': daily_data,
        'monthly_records': list(monthly_records.values()),
        'summary': {
            'cost': 14066887.0,
            'capital': 17300000.0,
            'remaining_capital': const_remaining_capital,
            'paid_mortgage': const_paid_mortgage,
            'pledge_loan': const_pledge_loan,
            'loan_start_date': loan_start_date,
            'dividend_up_to_now': cum_div_val,
            'latest_date': daily_data[-1]['date'],
            'latest_stock_val': daily_data[-1]['stock_val']
        }
    }, f, ensure_ascii=False, indent=2)

# Re-run build_html.py
os.system(f'python3 "{os.path.join(base_dir, "build_html.py")}"')
print("=== 更新完成！已更新 portfolio_data.json 與 index.html ===")
