import pandas as pd

# 1. Ana veriyi oku
df = pd.read_csv('data/commercial_transactions.csv')

# 2. Fact Tablosu: Power BI'ın aradığı tüm sütunları eksiksiz bırakıyoruz
fact_sales = df.copy()
fact_sales.to_csv('data/fact_commercial_sales.csv', index=False)

# 3. Dim_Product: 'product_id' sütununu ekliyoruz
categories = {
    'Bal': 'Aricilik & Katma Deger',
    'Cig Antep Fistigi': 'Sert Kabuklu Tarim',
    'Pekmez': 'Geleneksel Islenmis Gida',
    'Kuru Uzum': 'Kuru Meyve',
    'Kucukbas Besi (Canli)': 'Canli Hayvan & Besi'
}
dim_product = pd.DataFrame({
    'product_name': list(categories.keys()),
    'category': list(categories.values()),
    'product_id': [f'PRD-0{i+1}' for i in range(len(categories))]
})
dim_product.to_csv('data/dim_product.csv', index=False)

# 4. Dim_Channel: 'channel_model' sütununu ekliyoruz
dim_channel = pd.DataFrame({
    'channel_name': ['B2B - Toptan', 'D2C - Perakende'],
    'channel_model': ['Tuccar / Canli Hayvan Pazari / Toptanci', 'Dogrudan Tuketici (Kargo / Yerel Teslim)'],
    'logistics_focus': ['Toplu Sevk', 'Hizli Kargo']
})
dim_channel.to_csv('data/dim_channel.csv', index=False)

print("Star-Schema tablolari Power BI ile tam uyumlu hale getirildi.")