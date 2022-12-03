#!/usr/bin/env python3

import config
import requests

date_format = "%Y-%m-%d"

def get_time_series(symbol):
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&apikey=" + config.apikey)
    data = r.json()
    dailies = data['Time Series (Daily)']
    running_total = 0.0
#    print(dailies)
    for date in dailies:
        # get this date
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
#            print(f"There are no more dates. {e}")
            continue
    return running_total

def get_some_input():
    print("This program will check for profit\nassuming you purchased shares \nat close and sold them at open \nevery working day for the last 100.\n")
    symbol = input("What symbol do you want to check?\n")
    num_shares = input("And how many shares will you hold?\n")
    # do some input sanitizing
    return symbol, float(num_shares)
    

if __name__ == "__main__":
    symbol, num_shares = get_some_input()
    base_total = get_time_series(symbol)
    share_total = num_shares * base_total
    print(f"If you purchased {num_shares} shares of {symbol}\nevery business day at close for the last\n100 days you would have made ${share_total}")
