from historical_data import CheckDataCSV, fetch_raw_historical_data
from analysis import Analysis
from config import STOCK_LIST
from get_stock_info import CheckInfoCSV, GetStockInfo

symbol = "RELIANCE.NS"

if symbol not in STOCK_LIST:
    print(f"Symbol {symbol} not in stock list")
    STOCK_LIST.append(symbol)


if CheckDataCSV(symbol) == False:
    raw_data = fetch_raw_historical_data(symbol, period="1y")
    analysis = Analysis(symbol, raw_data)
    analysis.clean_df.to_csv(f"data/{symbol}_stock_data.csv", mode='a', header=False, index=False)
    print(f"CSV created for {symbol}")
else:
    print(f"CSV already exists for {symbol}")


