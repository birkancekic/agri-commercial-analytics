import sqlite3
import pandas as pd

# 1. CSV verisini oku
csv_path = 'data/commercial_transactions.csv'
df = pd.read_csv(csv_path)

# 2. SQLite veritabanı bağlantısı aç ve tabloyu bas
conn = sqlite3.connect('data/commercial_database.db')
df.to_sql('commercial_transactions', conn, if_exists='replace', index=False)
print("-> Veriler SQLite veritabanina ('data/commercial_database.db') aktarildi.")

# 3. SQL dosyasındaki sorguları oku ve çalıştır
with open('sql/commercial_analytics_engine.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(';') if q.strip()]

print("\n--- ANALİZ 1: KANAL MARJ ARBİTRAJI (B2B vs D2C) ---")
res1 = pd.read_sql_query(queries[0], conn)
print(res1.to_string(index=False))

print("\n--- ANALİZ 2: LOJİSTİK DARBOĞAZ VE FİRE RİSKİ (WINDOW FUNCTION) ---")
res2 = pd.read_sql_query(queries[1], conn)
print(res2.head(6).to_string(index=False))

conn.close()
print("\nISLEM BASARILI: Analitik SQL motoru calisti ve sonuclari cikardi.")