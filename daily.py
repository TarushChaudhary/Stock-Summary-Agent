import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from config import STOCK_LIST
from historical_data import CheckDataCSV
import os
today_date = datetime.now().strftime("%Y-%m-%d")

weekly_update_format = """ *{symbol}*
Current Price: {current_price}
Price Change from Last Week: {price_change:.2%}
Price {three_day_status} {price_deviation_3:.2%} from 3-day Moving Average and {long_term_status} {price_deviation_200:.2%} from 200 Day Moving Average
Volume is {volume_change:.2%} higher than 5-day average volume
Short Term Trend: {short_term_trend}, Long Term Trend: {long_term_trend}
\n
"""
weekly_message_list = []
current_message_list = []
def check_current_market(symbol: str, values: bool, main_df: pd.DataFrame) -> dict:
    """
    Checks current market data against historical data for anomalies.
    
    Args:
        symbol (str): Stock symbol
        main_df (pd.DataFrame): Historical data DataFrame
    
    Returns:
        dict: Dictionary containing alert flags and messages
    """

    stock = yf.Ticker(symbol)
    current_data = stock.history(period='1d').iloc[-1]
    yesterdays_record = main_df[main_df['Symbol'] == symbol].iloc[-1]
    last_week_record = main_df[main_df['Symbol'] == symbol].iloc[-5]

    
    current_message_list.append(f"Checking current market for {symbol}")
    current_message_list.append(f"Current Price: {current_data['Close']}, Last Week Price: {last_week_record['Close']}")
    current_message_list.append(f"Short Term Trend: {yesterdays_record['Trend_Short']}, Long Term Trend: {yesterdays_record['Trend_Long']}")

    # Check price deviation from moving averages
    price_deviation_3 = abs(current_data['Close'] - yesterdays_record['3_SMA']) / yesterdays_record['3_SMA']
    price_deviation_5 = abs(current_data['Close'] - yesterdays_record['5_SMA']) / yesterdays_record['5_SMA']
    is_increased_3d = True if current_data['Close'] > yesterdays_record['3_SMA'] else False
    is_increased_5d = True if current_data['Close'] > yesterdays_record['5_SMA'] else False
    if values == True:
        if is_increased_3d and is_increased_5d:
            message = f"Price increased by {price_deviation_3:.2%} from 3-day Moving Average and increased by {price_deviation_5:.2%} from 5-day Moving Average"
        elif not is_increased_3d and not is_increased_5d:
            message = f"Price decreased by {price_deviation_3:.2%} from 3-day Moving Average and decreased by {price_deviation_5:.2%} from 5-day Moving Average"
        elif is_increased_3d and not is_increased_5d:
            message = f"Price increased by {price_deviation_3:.2%} from 3-day Moving Average and decreased by {price_deviation_5:.2%} from 5-day Moving Average"
        elif not is_increased_3d and is_increased_5d:
            message = f"Price decreased by {price_deviation_3:.2%} from 3-day Moving Average and increased by {price_deviation_5:.2%} from 5-day Moving Average"
        current_message_list.append(message)
        return current_message_list
    
#print(check_current_market("RELIANCE.NS", pd.read_csv("data/RELIANCE.NS_stock_data.csv")))
def weekly_update():
    print("Creating weekly update")
    for symbol in STOCK_LIST:
        last_week_record = CheckDataCSV(symbol).iloc[-5]
        current_record = CheckDataCSV(symbol).iloc[-1]
        price_change = (current_record['Close'] - last_week_record['Close']) / last_week_record['Close']
        price_deviation_3 = abs(current_record['Close'] - last_week_record['3_SMA']) / last_week_record['3_SMA']
        price_deviation_200 = abs(current_record['Close'] - last_week_record['200_SMA']) / last_week_record['200_SMA']
        volume_change = current_record['Volume'] / last_week_record['5_Volume_Avg']
        short_term_trend = current_record['Trend_Short']
        long_term_trend = current_record['Trend_Long']
        current_price = current_record['Close']
        three_day_status = "increased" if current_record['Close'] > last_week_record['3_SMA'] else "decreased"
        long_term_status = "increased" if current_record['Close'] > last_week_record['200_SMA'] else "decreased"
        message = weekly_update_format.format(symbol=symbol, current_price=current_price, price_change=price_change, price_deviation_3=price_deviation_3, price_deviation_200=price_deviation_200, volume_change=volume_change, short_term_trend=short_term_trend, long_term_trend=long_term_trend, three_day_status=three_day_status, long_term_status=long_term_status)
        weekly_message_list.append(message)
    return weekly_message_list
    
def create_weekly_update():
    weekly_update()
    
    if not os.path.exists(f"{today_date}.txt"):
        with open(f"{today_date}.txt", 'w') as file:
            file.write(f"Weekly Update for {today_date}\n")
            for i in weekly_message_list:
                file.write(i)
    else:
        with open(f"{today_date}.txt", 'a') as file:
            for i in weekly_message_list:
                file.write(i)

