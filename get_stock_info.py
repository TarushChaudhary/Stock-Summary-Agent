import yfinance as yf
from config import INFO_CSV, INFO_COLUMNS
import pandas as pd
import os

def CheckInfoCSV():
    if not os.path.exists(INFO_CSV):
        print("Creating new info CSV file")
        info_df = pd.DataFrame(columns=INFO_COLUMNS)
        info_df.to_csv(INFO_CSV, index=False)
        return info_df
    else:
        print("Loading existing info CSV file")
        return pd.read_csv(INFO_CSV)

def GetStockInfo(symbol: str):

    info_df = pd.read_csv(INFO_CSV)
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Create new row
        new_data = pd.DataFrame([{
            'Name': info.get('longName', 'Unknown'),
            'Industry': info.get('industry', 'Unknown'),
            'Sector': info.get('sector', 'Unknown'),
            'Symbol': symbol,
            'Summary': info.get('longBusinessSummary', 'Unknown')
        }])
        
        # Append using concat
        info_df = pd.concat([info_df, new_data], ignore_index=True)
        info_df.to_csv(INFO_CSV, index=False)
        print(f"Added new symbol {symbol} to the info CSV")
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
