SELECT "date", "open", high, low, "close", volume, symbol
FROM public.stock_data;

--1. Trend analizi
CREATE or REPLACE VIEW v_stock_trends AS
SELECT
	date,symbol,close,
	AVG(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 6 preceding and CURRENT ROW) as sma_7,
	AVG(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 29 preceding and CURRENT ROW) as sma_30
FROM stock_data;


--2. Gunluk faiz performansi
CREATE or REPLACE VIEW v_daily_performance AS
SELECT 
	date,symbol,close,
	ROUND(CAST(((close - LAG(close) OVER (PARTITION BY symbol ORDER BY date)) / 
	NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY date), 0)) * 100 AS NUMERIC), 2) as daily_pct_change
FROM stock_data;


--3.KPI (son gun stats)
CREATE or REPLACE VIEW v_latest_stats AS 
WITH RankedData AS (
	SELECT *, ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) as rn
	FROM stock_data
)
SELECT 
	symbol,date,close as current_price, volume
FROM RankedData
where rn = 1;


--4.Relative Strength IndeX (rsi)
CREATE or REPLACE VIEW v_rsi_indicator AS
WITH PriceDiffs AS (
    SELECT symbol, date, close,
           close - LAG(close) OVER (PARTITION BY symbol ORDER BY date) as diff
    FROM stock_data
),
GainsLosses AS (
    SELECT *,
           CASE WHEN diff > 0 THEN diff ELSE 0 END as gain,
           CASE WHEN diff < 0 THEN ABS(diff) ELSE 0 END as loss
    FROM PriceDiffs
),
AvgGL AS (
    SELECT *,
           AVG(gain) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) as avg_gain,
           AVG(loss) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) as avg_loss
    FROM GainsLosses
)
SELECT symbol, date, close,
       ROUND(CAST(100 - (100 / (100 + (avg_gain / NULLIF(avg_loss, 0)))) AS NUMERIC), 2) as rsi
FROM AvgGL;


--5. Correlation (sehmler arasi elaqe)
CREATE or REPLACE VIEW v_stock_correlation AS
SELECT 
	a.symbol as stock_1, b.symbol as stock_2,
	ROUND(CAST(CORR(a.close, b.close) AS NUMERIC), 4) as corr_score
FROM stock_data a
JOIN stock_data b ON a.date = b.date
WHERE a.symbol < b.symbol
GROUP BY a.symbol, b.symbol


--6.Risk analizi
CREATE or REPLACE VIEW v_risk_analysis AS
SELECT
	symbol,date,close,
	ROUND(CAST(STDDEV(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 29 preceding AND CURRENT ROW) as numeric), 2) as volatility_30day
FROM stock_data


--7.calendar table (senbe ve bazar gunleri ucun)
DROP TABLE IF EXISTS calendar_table; -- Əgər yarımçıq qalıbsa silib yenidən yaradır
CREATE TABLE calendar_table AS
SELECT 
    datum AS date,
    EXTRACT(YEAR FROM datum) AS year,
    EXTRACT(MONTH FROM datum) AS month,
    EXTRACT(DAY FROM datum) AS day,
    EXTRACT(QUARTER FROM datum) AS quarter,
    TO_CHAR(datum, 'Month') AS month_name,
    TO_CHAR(datum, 'Day') AS day_name,
    CASE WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series(
    '1999-01-01'::date, 
    '2030-12-31'::date, 
    '1 day'::interval
) AS datum;

CREATE INDEX idx_calendar_date ON calendar_table(date);