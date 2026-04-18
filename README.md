# Stock Market Dashboard 📈

## Contact
- LinkedIn: [Rashid Majidov](linkedin.com/in/rashid-majidov)
- GitHub: [rashidmajidov](https://github.com/rashidmajidov)

## Overview
An automated stock market analysis dashboard tracking 5 major tech stocks (AAPL, GOOGL, MSFT, AMZN, TSLA) with real-time data updates and interactive visualizations.

## Tools Used
- **Python** — Data fetching (Alpha Vantage API), cleaning & automation
- **PostgreSQL** — Data storage & SQL analysis
- **Power BI** — Interactive dashboard

## Features
- 📊 Price trend with Moving Averages (SMA-7, SMA-30)
- 📉 RSI Indicator (overbought/oversold signals)
- 🔗 Stock correlation analysis
- ⚡ 30-day volatility tracking
- 🔄 Automated weekly data updates

## Dataset
- Source: Alpha Vantage API
- 5 stocks: AAPL, GOOGL, MSFT, AMZN, TSLA
- Weekly data from 1999 to present
- ~6,000 rows

## Dashboard
🔗 [View Live Dashboard on Power BI](https://app.powerbi.com/groups/me/reports/f610fb1c-b715-49e9-b501-4e1f2a3cb905/38c4dcf0408674b02a09?experience=power-bi)

## SQL Analysis

### Views Created

**`v_stock_trends`** — Moving Averages
- SMA-7 (7-week) and SMA-30 (30-week) moving averages
- Identifies price trends and momentum

**`v_daily_performance`** — Weekly Performance
- Calculates week-over-week percentage change
- Identifies best and worst performing weeks

**`v_latest_stats`** — Latest KPIs
- Most recent price and volume for each stock
- Used for KPI cards in dashboard

**`v_rsi_indicator`** — Relative Strength Index
- RSI calculated over 14-period window
- Values above 70 = overbought, below 30 = oversold

**`v_stock_correlation`** — Correlation Matrix
- Measures relationship between stock pairs
- Values range from -1 (inverse) to 1 (perfect correlation)

**`v_risk_analysis`** — Volatility Analysis
- 30-week rolling standard deviation
- Higher values indicate higher risk/volatility

**`calendar_table`** — Date Dimension Table
- Full date table from 1999 to 2030
- Enables time-based filtering in Power BI

## Contact
- LinkedIn: [Rashid Majidov](linkedin.com/in/rashid-majidov)
- GitHub: [rashidmajidov](https://github.com/rashidmajidov)