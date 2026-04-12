import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

# .env faylından API key-i yüklə
load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_KEY')

# Səhm siyahısı
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def parse_stock_data(data, symbol):
    if 'Weekly Time Series' not in data:
        print(f'{symbol} üçün data gəlmədi: {data}')
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
    return df

# Bütün səhmlər üçün data çək
all_data = []

for symbol in symbols:
    print(f'{symbol} çəkilir...')
    data = fetch_stock_data(symbol)
    df = parse_stock_data(data, symbol)
    if df is not None:
        all_data.append(df)
    time.sleep(15)

# Birləşdir
final_df = pd.concat(all_data, ignore_index=True)
print(final_df.shape)
print(final_df.head())

# Saxla
final_df.to_csv('data/raw/stock_data.csv', index=False)
print('✅ Data saxlanıldı!')