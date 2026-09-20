-- 1. KANAL MARJ ARBİTRAJI (B2B Toptan vs D2C Perakende Katkı Analitiği)
WITH ChannelPerformance AS (
    SELECT 
        product_name,
        category,
        sales_channel,
        SUM(gross_revenue_try) AS total_revenue,
        SUM(cogs_try) AS total_cogs,
        SUM(gross_margin_try) AS total_margin,
        ROUND((SUM(gross_margin_try) / SUM(gross_revenue_try)) * 100, 2) AS blended_margin_pct,
        ROUND(SUM(shrinkage_qty_kg), 2) AS total_loss_kg
    FROM commercial_transactions
    GROUP BY product_name, category, sales_channel
)
SELECT 
    product_name,
    category,
    MAX(CASE WHEN sales_channel = 'B2B - Toptan' THEN blended_margin_pct END) AS b2b_margin_pct,
    MAX(CASE WHEN sales_channel = 'D2C - Perakende' THEN blended_margin_pct END) AS d2c_margin_pct,
    ROUND(
        MAX(CASE WHEN sales_channel = 'D2C - Perakende' THEN blended_margin_pct END) - 
        MAX(CASE WHEN sales_channel = 'B2B - Toptan' THEN blended_margin_pct END), 2
    ) AS direct_channel_premium_pct,
    ROUND(SUM(total_revenue), 2) AS total_product_revenue
FROM ChannelPerformance
GROUP BY product_name, category
ORDER BY direct_channel_premium_pct DESC;


-- 2. LOJİSTİK DARBOĞAZ VE FİRE MALİYETİ SIRALAMASI (Window Function ile Risk Derecelendirmesi)
WITH LogisticsRisk AS (
    SELECT 
        product_name,
        sales_channel,
        COUNT(transaction_id) AS total_shipments,
        ROUND(AVG(delay_days), 2) AS avg_delay_days,
        ROUND(SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(transaction_id), 2) AS delay_rate_pct,
        ROUND(SUM(shrinkage_qty_kg * unit_cost_try), 2) AS total_shrinkage_cost_try
    FROM commercial_transactions
    GROUP BY product_name, sales_channel
)
SELECT 
    product_name,
    sales_channel,
    total_shipments,
    avg_delay_days,
    delay_rate_pct,
    total_shrinkage_cost_try,
    DENSE_RANK() OVER (ORDER BY total_shrinkage_cost_try DESC) AS shrinkage_risk_rank
FROM LogisticsRisk
ORDER BY shrinkage_risk_rank ASC;