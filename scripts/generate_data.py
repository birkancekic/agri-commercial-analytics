import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# Yıllık tam üretim miktarları ve anonimleştirilmiş gerçekçi piyasa fiyatları
# Toplam Hacim: 1.200 kg Bal, 900 kg Fıstık, 500 kg Pekmez, 500 kg Kuru Üzüm, 50 Hayvan
products_cfg = [
    {'name': 'Bal', 'cost': 320, 'b2b': 440, 'd2c': 720, 'n_d2c': 60, 'n_b2b': 12, 'd2c_qty': 12.0, 'b2b_qty': 40.0, 'shrink': 0.012},
    {'name': 'Cig Antep Fistigi', 'cost': 380, 'b2b': 520, 'd2c': 850, 'n_d2c': 35, 'n_b2b': 11, 'd2c_qty': 10.0, 'b2b_qty': 50.0, 'shrink': 0.022},
    {'name': 'Pekmez', 'cost': 160, 'b2b': 230, 'd2c': 400, 'n_d2c': 40, 'n_b2b': 8, 'd2c_qty': 7.5, 'b2b_qty': 25.0, 'shrink': 0.010},
    {'name': 'Kuru Uzum', 'cost': 110, 'b2b': 160, 'd2c': 280, 'n_d2c': 45, 'n_b2b': 8, 'd2c_qty': 6.0, 'b2b_qty': 28.7, 'shrink': 0.015},
    {'name': 'Kucukbas Besi (Canli)', 'cost': 7500, 'b2b': 12000, 'd2c': 14500, 'n_d2c': 10, 'n_b2b': 8, 'd2c_qty': 1.0, 'b2b_qty': 5.0, 'shrink': 0.0}
]

rows = []
trx_id = 1
start_date = datetime(2025, 1, 1)

for cfg in products_cfg:
    # D2C (Perakende)
    for _ in range(cfg['n_d2c']):
        qty = cfg['d2c_qty']
        shrinkage = round(qty * cfg['shrink'], 2)
        received = round(qty - shrinkage, 2)
        price = cfg['d2c']
        lead = int(np.random.randint(1, 4))
        delay = int(np.random.choice([0, 1], p=[0.85, 0.15]))
        
        o_date = start_date + timedelta(days=int(np.random.uniform(0, 350)))
        d_date = o_date + timedelta(days=lead + delay)
        
        cogs = round(qty * cfg['cost'], 2)
        rev = round(received * price, 2)
        margin = round(rev - cogs, 2)
        margin_pct = round((margin / rev) * 100, 2) if rev > 0 else 0.0
        
        rows.append([
            f"TRX-{trx_id:04d}", o_date.strftime('%Y-%m-%d'), d_date.strftime('%Y-%m-%d'),
            cfg['name'], 'D2C - Perakende', cfg['cost'], price, qty, received, shrinkage,
            lead, delay, rev, cogs, margin, margin_pct
        ])
        trx_id += 1

    # B2B (Toptan)
    for _ in range(cfg['n_b2b']):
        qty = cfg['b2b_qty']
        shrinkage = round(qty * cfg['shrink'], 2)
        received = round(qty - shrinkage, 2)
        price = cfg['b2b']
        lead = int(np.random.randint(2, 5))
        delay = int(np.random.choice([0, 1, 2], p=[0.75, 0.20, 0.05]))
        
        o_date = start_date + timedelta(days=int(np.random.uniform(0, 350)))
        d_date = o_date + timedelta(days=lead + delay)
        
        cogs = round(qty * cfg['cost'], 2)
        rev = round(received * price, 2)
        margin = round(rev - cogs, 2)
        margin_pct = round((margin / rev) * 100, 2) if rev > 0 else 0.0
        
        rows.append([
            f"TRX-{trx_id:04d}", o_date.strftime('%Y-%m-%d'), d_date.strftime('%Y-%m-%d'),
            cfg['name'], 'B2B - Toptan', cfg['cost'], price, qty, received, shrinkage,
            lead, delay, rev, cogs, margin, margin_pct
        ])
        trx_id += 1

cols = [
    'transaction_id', 'order_date', 'delivery_date', 'product_name', 'sales_channel',
    'unit_cost_try', 'unit_price_try', 'dispatched_qty_kg', 'received_qty_kg', 'shrinkage_qty_kg',
    'actual_lead_time_days', 'delay_days', 'gross_revenue_try', 'cogs_try', 'gross_margin_try', 'gross_margin_pct'
]

df = pd.DataFrame(rows, columns=cols).sort_values(by='order_date').reset_index(drop=True)
df.to_csv('data/commercial_transactions.csv', index=False)
df.to_csv('data/fact_commercial_sales.csv', index=False)

print(f"ISLEM BASARILI: {len(df)} islem kaydedildi.")
print(f"Toplam Hasılat: {df['gross_revenue_try'].sum():,.2f} TL")