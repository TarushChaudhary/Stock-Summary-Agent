import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from config import STOCK_LIST, STOCK_COLUMNS, INFO_CSV
import os
from analysis import Analysis
from get_stock_info import GetStockInfo

info_df = pd.read_csv(INFO_CSV)

def CheckDataCSV(symbol: str):
    if not os.path.exists(f"data/{symbol}_stock_data.csv"):
        stock_data = pd.DataFrame(columns=STOCK_COLUMNS)
        stock_data.to_csv(f"data/{symbol}_stock_data.csv", index=False)
        print(f"Created new empty data CSV for {symbol}")
        data = fetch_raw_historical_data(symbol, period="1y")
        analysis = Analysis(symbol, data)
        analysis.clean_df.to_csv(f"data/{symbol}_stock_data.csv", index=False)
        
        if symbol not in info_df['Symbol'].values:
            GetStockInfo(symbol)
        
        return analysis.clean_df
    else:
        print(f"Loading existing data CSV for {symbol}")
        stock_data = pd.read_csv(f"data/{symbol}_stock_data.csv")
        return stock_data

def fetch_raw_historical_data(symbol: str, period: str) -> pd.DataFrame:
    """
    Fetches historical data for a given stock symbol.
    
    Args:
        symbol (str): Stock symbol (e.g., 'RELIANCE.NS' for NSE)
        period (str): Time period to fetch data for
    
    Returns:
        pd.DataFrame: Historical data with calculated indicators
    """
    stock = yf.Ticker(symbol)
    raw_df = stock.history(period=period)

    return raw_df
    
#print(fetch_raw_historical_data("RELIANCE.NS"))