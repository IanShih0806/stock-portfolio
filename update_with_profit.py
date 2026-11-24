import urllib.request, json, datetime, os
import pandas as pd

base_dir = '/Users/10404604/.gemini/antigravity/scratch/stock-portfolio-tracker'
json_path = os.path.join(base_dir, 'portfolio_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

daily_data = data['daily_data']
cost = 14066887.0

# Calculate exact fee and profit for each day
for r in daily_data:
    p929, s929 = r['p929'], r['s929']
    p919, s919 = r['p919'], r['s919']
    p878, s878 = r['p878'], r['s878']
    p56, s56 = r['p56'], r['s56']
    
    # Unit costs from Excel
    c929 = 19.432
    c919 = 24.26
    c878 = 22.41776786
    c56 = 37.33598214
    
    # Exact fee formula from Excel cell D2
    fee929 = (p929 * 0.001 * 1000 + p929 * 0.001425 * 1000 + c929 * 0.001425 * 1000) if s929 > 0 else 0
    fee919 = (p919 * 0.001 * 1000 + p919 * 0.001425 * 1000 + c919 * 0.001425 * 1000) if s919 > 0 else 0
    fee878 = (p878 * 0.001 * 1000 + p878 * 0.001425 * 1000 + c878 * 0.001425 * 1000) if s878 > 0 else 0
    fee56  = (p56  * 0.001 * 1000 + p56  * 0.001425 * 1000 + c56  * 0.001425 * 1000) if s56 > 0 else 0
    total_fee = fee929 + fee919 + fee878 + fee56
    
    profit = round((r['stock_val'] - cost) - total_fee, 0)
    profit_pct = round((profit / cost) * 100, 2)
    
    profit_with_div = round(profit + r['cum_div'], 0)
    profit_with_div_pct = round((profit_with_div / cost) * 100, 2)
    
    r['profit'] = profit
    r['profit_pct'] = profit_pct
    r['profit_with_div'] = profit_with_div
    r['profit_with_div_pct'] = profit_with_div_pct

data['daily_data'] = daily_data
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated portfolio_data.json with profit fields.')
print('First day profit:', daily_data[0]['date'], daily_data[0]['profit'], f"{daily_data[0]['profit_pct']}%")
print('Last day profit:', daily_data[-1]['date'], daily_data[-1]['profit'], f"{daily_data[-1]['profit_pct']}%")
