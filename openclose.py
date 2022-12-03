#!/usr/bin/env python3

import config
import requests

date_format = "%Y-%m-%d"

def get_time_series(symbol):
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&apikey=" + config.apikey)
    data = r.json()
    dailies = data['Time Series (Daily)']
    running_total = 0.0
    return dailies

def compute_closeopen(dailies, num_days):
    running_total = 0.0
    days_counter = 0
    for date in dailies:
        while days_counter <= num_days:
            dict_list = list(dailies)
            # get yesterday's close
            try:
                yesterday = dict_list[dict_list.index(date) +1]
    #            print(date + ": " + yesterday)
                y_close = dailies[yesterday]['4. close']
    #            print(y_close)
                t_open = dailies[date]['1. open']
                overnight_change = float(t_open) - float(y_close)
    #            print(overnight_change)
                running_total = running_total + float(overnight_change)
            except (KeyError, ValueError) as e:
                print(e)
            except IndexError as e:
                # this means we got the last one (there are no more dates)
                continue
            days_counter +=1
    return running_total

def compute_openclose(dailies, num_days):
    days_counter = 0
    running_total = 0.0
    for date in dailies:
        while days_counter <= num_days:
            today_profit = float(dailies[date]['4. close']) - float(dailies[date]['1. open'])
            running_total = running_total + today_profit
            days_counter +=1
    return running_total

def get_some_input():
    print("This program will check for profit\nassuming you purchased shares \nat close and sold them at open \nevery working day for the last 100.\n")
    symbol = input("What symbol do you want to check?\n")
    num_shares = input("And how many shares will you hold?\n")
    num_days = int(input("For many days back?\n"))
    # do some input sanitizing
    return symbol, float(num_shares), num_days
    

if __name__ == "__main__":
    symbol, num_shares, num_days = get_some_input()
    dailies = get_time_series(symbol)
    co_base_total = compute_closeopen(dailies, num_days)
    oc_base_total = compute_openclose(dailies, num_days)
    print(f"\n{num_shares} shares of {symbol} close to open\nfor the last {num_days} market days:\n${co_base_total * num_shares}")
    print(f"\n{num_shares} shares of {symbol} open to close\nfor the last {num_days} market days:\n${oc_base_total * num_shares}")
