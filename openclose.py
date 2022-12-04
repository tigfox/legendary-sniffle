#!/usr/bin/env python3
# you need to have a file in the same directory as this one, called 'config.py'
# that file needs to have a line 'apikey = "YOURAPIKEY"' with your api key.
# it's free from https://www.alphavantage.co/support/#api-key
# if you're going to commit back to the repo, add config.py to your gitignore

import config
# your api key
import time
# so we can sleep for rate limiting
import requests
# to talk to the api server
import argparse
# to get command line arguments

# you need to call this with these options. ex: python3 openclose.py -d 30 -s 100 -t tqqq -t sqqq
# will give you the open>close and close>open for 100 shares of tqqq and sqqq for the last 30 days
parser = argparse.ArgumentParser(description="Open/Close Calculator.")
parser.add_argument('-d', dest='days', help='Number of days from today to calculate.')
parser.add_argument('-s', dest='shares', help='Number of shares to hold')
parser.add_argument('-t', action='append', dest='symbols', help='The ticker symbol to calculate. Supply multiple with multiple flags.')
parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='More compact printing')
args = parser.parse_args()
symbols = args.symbols
num_days = int(args.days)
num_shares = int(args.shares)
quiet = args.quiet

def get_time_series(symbol):
    '''reach out and get the data. need to fix the error catching here,
    for rate limiting (why can't they send 429? who rate limits with a 200??)
    '''
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&apikey=" + config.apikey)
    data = r.json()
    try: 
        if "Thank you" in data["Note"]: #status codes exist for a reason
            print(f"Hit the rate limit. Waiting.")
            time.sleep(30)
            print(f"Still waiting. Premium API access only $50/mo!")
            time.sleep(30)
            return get_time_series(symbol)
    except KeyError as e:
        # no rate limiting
        pass
    dailies = data['Time Series (Daily)']
    return dailies

def compute_closeopen(dailies, num_days):
    '''compute the close to open price difference.
    for each day you need to find yesterday (forward in the list)
    and get its close, then subtract that from today's open.
    this is the change in price while the market is closed.
    '''
    running_total = 0.0
    days_counter = 0
    for date in dailies:
        while days_counter <= num_days:
            dict_list = list(dailies)
            try:
                # get yesterday's close
                yesterday = dict_list[dict_list.index(date) +1]
                y_close = dailies[yesterday]['4. close']
                # today's open
                t_open = dailies[date]['1. open']
                # some complicated math
                overnight_change = float(t_open) - float(y_close)
                running_total = running_total + float(overnight_change)
            except IndexError as e:
                # this means we got the last one (there are no more dates)
                continue
            days_counter +=1
    return running_total

def compute_openclose(dailies, num_days):
    '''compute the open to close price for the time period.
    for each day just subtract open from close.
    that's way easier than going back in time.
    this is the change in price while the market is open.
    '''
    days_counter = 0
    running_total = 0.0
    for date in dailies:
        while days_counter <= num_days:
            today_profit = float(dailies[date]['4. close']) - float(dailies[date]['1. open'])
            running_total = running_total + today_profit
            days_counter +=1
    return running_total
    
if __name__ == "__main__":
    for symbol in symbols:
        dailies = get_time_series(symbol)
        co_base_total = compute_closeopen(dailies, num_days)
        oc_base_total = compute_openclose(dailies, num_days)
        if quiet:
            print(f"{num_days} days {num_shares} {symbol} c>o: ${co_base_total * num_shares}")
            print(f"{num_days} days {num_shares} {symbol} o>c: ${oc_base_total * num_shares}")
        else:
            print(f"\n{num_shares} {symbol} close to open for {num_days} market days:\n${co_base_total * num_shares}")
            print(f"\n{num_shares} {symbol} open to close for {num_days} market days:\n${oc_base_total * num_shares}")

