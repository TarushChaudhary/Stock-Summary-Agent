import pandas as pd
import numpy as np
from config import MAIN_CSV, STOCK_COLUMNS
import os
import yfinance as yf

class Analysis:
    def __init__(self, symbol: str, raw_df: pd.DataFrame):
        self.raw_df = raw_df
        self.symbol = symbol
        self.clean_df = pd.DataFrame()
        
        # Initialize and run all calculations
        self.process_data()
        
    def process_data(self):
        """Run all data processing steps in sequence"""
        self.get_general_info()
        self.extract_data()
        self.calculate_indicators()
        self.calculate_atr()
        self.calculate_volume_averages()
        
        # Ensure columns are in the correct order as per STOCK_COLUMNS
        self.clean_df = self.clean_df[STOCK_COLUMNS]
        
    def get_general_info(self):
        """Get general stock info and store temporarily"""
        stock = yf.Ticker(self.symbol)
        info = stock.info
        # Store info for later use when we know how many rows we'll need
        self.stock_info = {
            'Name': info.get('shortName', 'Unknown'),
            'Industry': info.get('industry', 'Unknown'),
            'Sector': info.get('sector', 'Unknown')
        }
        
        print("General info extracted")
        
    def extract_data(self):
        """Extract price data and combine with general info"""
        # Create a copy of raw data and reset index to make Date a column
        data = self.raw_df.copy()
        data.reset_index(inplace=True)
        data.rename(columns={'index': 'Date'}, inplace=True)
        
        # Ensure column names are properly capitalized
        column_mapping = {
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }
        data.rename(columns=column_mapping, inplace=True)
        
        # Create DataFrame with stock info first
        self.clean_df = pd.DataFrame({
            'Name': [self.stock_info['Name']] * len(data),
            'Date': data['Date'],
            'Symbol': [self.symbol] * len(data),
            'Open': data['Open'],
            'High': data['High'],
            'Low': data['Low'],
            'Close': data['Close'],
            'Volume': data['Volume']
        })
        
        print("Data extracted")
    def calculate_indicators(self):
        """Calculate all technical indicators"""
        # Calculate SMAs
        self.clean_df['3_SMA'] = self.clean_df['Close'].rolling(window=3).mean()
        self.clean_df['5_SMA'] = self.clean_df['Close'].rolling(window=5).mean()
        self.clean_df['200_SMA'] = self.clean_df['Close'].rolling(window=200).mean()
        
        # Calculate trends
        self.clean_df['Trend_Short'] = np.where(self.clean_df['Close'] > self.clean_df['5_SMA'], 'Up', 'Down')
        self.clean_df['Trend_Long'] = np.where(self.clean_df['Close'] > self.clean_df['200_SMA'], 'Up', 'Down')

        print("Indicators calculated")
    
    def calculate_atr(self):
        """Calculate True Range and Average True Range"""
        # Calculate True Range
        high_low = self.clean_df['High'] - self.clean_df['Low']
        high_close = abs(self.clean_df['High'] - self.clean_df['Close'].shift(1))
        low_close = abs(self.clean_df['Low'] - self.clean_df['Close'].shift(1))
        
        # True Range is the greatest of the three
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        self.clean_df['TR'] = ranges.max(axis=1)
        
        # Calculate 14-period ATR
        self.clean_df['ATR'] = self.clean_df['TR'].rolling(window=14).mean()

        print("ATR calculated")

    
    def calculate_volume_averages(self):
        """Calculate volume moving averages"""
        self.clean_df['3_Volume_Avg'] = self.clean_df['Volume'].rolling(window=3).mean()
        self.clean_df['5_Volume_Avg'] = self.clean_df['Volume'].rolling(window=5).mean()

        print("Volume averages calculated")
    