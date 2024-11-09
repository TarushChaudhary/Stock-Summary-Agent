import pandas as pd
import yfinance as yf
from analysis import *
from historical_data import fetch_raw_historical_data, CheckDataCSV
import os
from config import MAIN_CSV, STOCK_COLUMNS, INFO_CSV, INFO_COLUMNS, STOCK_LIST
from daily import check_current_market, create_weekly_update
import datetime
from send_message import send_message

today_date = datetime.datetime.now().strftime("%Y-%m-%d")
last_week_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
no_of_days = (datetime.datetime.strptime(today_date, "%Y-%m-%d") - datetime.datetime.strptime(last_week_date, "%Y-%m-%d"))
# Create info CSV if it doesn't exist
if not os.path.exists(INFO_CSV):
    print("Creating new info CSV file")
    info_df = pd.DataFrame(columns=INFO_COLUMNS)
    info_df.to_csv(INFO_CSV, index=False)
else:
    print("Loading existing info CSV file")
    info_df = pd.read_csv(INFO_CSV)
"""
# Create main CSV if it doesn't exist
if not os.path.exists(MAIN_CSV):
    print("Creating new CSV file")
    main_df = pd.DataFrame(columns=STOCK_COLUMNS)
    main_df.to_csv(MAIN_CSV, index=False)
else:
    print("Loading existing CSV file")
    main_df = pd.read_csv(MAIN_CSV)
"""
def send_weekly_update():
    if os.path.exists(f"{today_date}.txt"):
        with open(f"{today_date}.txt", 'r') as file:
            message = file.read()
            send_message(message)
    else:
        print("No weekly update to send")

def main(current_market: bool = False):
    if current_market == True:
        for i in STOCK_LIST:
            print("Checking current market for", i)
            stock_df = CheckDataCSV(i)
            test = check_current_market(i, True, stock_df)
            print(test)

    if os.path.exists(f"{today_date}.txt"):
        print("Weekly update already exists")
    else:
        if no_of_days.days >= 7:
           create_weekly_update()

main(current_market=True)
send_weekly_update()
