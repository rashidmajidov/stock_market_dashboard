import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
from sqlalchemy import create_engine, text

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_KEY')

symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']

engine = create_engine('postgresql://postgres:rashid2007@localhost:5432/stock_market')

def get_latest_date(symbol):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT MAX(date) FROM stock_data WHERE symbol = :symbol"),
            {"symbol": symbol}
        )
        return result.scalar()

def fetch_new_data(symbol, latest_date):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if 'Weekly Time Series' not in data:
        print(f'{symbol} üçün data gəlmədi')
        return None
    
    time_series = data['Weekly Time Series']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index.name = 'date'
    df = df.reset_index()
    df['symbol'] = symbol
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df['volume'] = df['volume'].astype(int)
    df['date'] = pd.to_datetime(df['date'])
    
    # Yalnız yeni dataları götür
    if latest_date:
        df = df[df['date'] > pd.Timestamp(latest_date)]
    
    return df

# Hər səhm üçün yeni data çək
for symbol in symbols:
    print(f'{symbol} yoxlanır...')
    latest_date = get_latest_date(symbol)
    print(f'Son tarix: {latest_date}')
    
    df = fetch_new_data(symbol, latest_date)
    
    if df is not None and len(df) > 0:
        df.to_sql('stock_data', engine, if_exists='append', index=False)
        print(f'{symbol}: {len(df)} yeni sətir əlavə edildi')
    else:
        print(f'{symbol}: Yeni data yoxdur')
    
    time.sleep(15)

print('✅ Yeniləmə tamamlandı!')