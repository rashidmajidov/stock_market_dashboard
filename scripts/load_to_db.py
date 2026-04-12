import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:rashid2007@localhost:5432/stock_market')

df = pd.read_csv(r"C:\Users\rashid\Desktop\stock_market_dashboard\data\processed\cleaned_stock_data.csv")

df.to_sql('stock_data', engine, if_exists='replace', index=False)

print("Data loaded successfully to PostgreSQL!")
print(len(df))