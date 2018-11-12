#!/usr/bin/env python3

import config
import requests
try:
    from papirus import PapirusTextPos
    display = True
except ImportError:
    display = False

thing1 = {'name': 'ETSY', 'type': 'security', 'price': 0, 'last_daily_price': 0, 'daily_trend': 'U'}
#thing2 = {'name': 'BTC', 'type': 'currency', 'price': 0, 'last_daily_price': 0, 'daily_trend': 'U'}
thing2 = {'name': 'BBVA', 'type': 'security', 'price': 0, 'last_daily_price': 0, 'daily_trend': 'U'}
thing3 = {'name': 'AAPL', 'type': 'security', 'price': 0, 'last_daily_price': 0, 'daily_trend': 'U'}
things = [thing1, thing2, thing3]


def get_cur_price(currency):
    r = requests.get("https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_INTRADAY&symbol=" + currency + "&market=USD&apikey=" + config.av_key)
    full_data = r.json()
    last_refresh = full_data["Meta Data"]["7. Last Refreshed"]
    cur_price = full_data['Time Series (Digital Currency Intraday)'][last_refresh]['1a. price (USD)']
    return "{:.2f}".format(float(cur_price))


def get_cur_last_daily_close(currency):
    r = requests.get("https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=" + currency + "&market=USD&apikey=" + config.av_key)
    full_data = r.json()
    last_refresh = str(full_data["Meta Data"]["7. Last Refreshed"].split(" ")[0])
    last_close = full_data['Time Series (Digital Currency Daily)'][last_refresh]['4a. close (USD)']
    return "{:.2f}".format(float(last_close))


def get_sec_price(symbol):
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol + "&interval=1min&apikey=" + config.av_key)
    full_data = r.json()
    last_refresh = full_data["Meta Data"]["3. Last Refreshed"]
    cur_price = full_data['Time Series (1min)'][last_refresh]['4. close']
    return "{:.2f}".format(float(cur_price))


def get_sec_last_daily_close(symbol):
    r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + config.av_key)
    full_data = r.json()
    last_refresh = str(full_data["Meta Data"]["3. Last Refreshed"].split(" ")[0])
    last_close = full_data['Time Series (Daily)'][last_refresh]['4. close']
    return "{:.2f}".format(float(last_close))


def eval_trends(thing):
    if thing['last_daily_price'] > thing['price']:
        thing['daily_trend'] = "V"
    elif thing['last_daily_price'] < thing['price']:
        thing['daily_trend'] = "^"
    else:
        thing['daily_trend'] = "-"
    return thing


def write_display(things):
    text = PapirusTextPos(False)
    pos = 10
    for i in things:
        text.AddText(i['name'] + ": " + str(i['price']), 10, pos)
#        text.AddText(i['name'] + ": " + str(i['price']) + " " + i['daily_trend'], 10, pos)
        pos = pos + 25
    text.WriteAll()


def write_console(things):
    for i in things:
        print(i['name'] + ": " + str(i['price']))
#        print(i['name'] + ": " + str(i['price']) + " " + i['daily_trend'])

if __name__ == "__main__":
    for i in things:
        if i['type'] == 'security':
            i['price'] = get_sec_price(i['name'])
#            i['last_daily_price'] = get_sec_last_daily_close(i['name'])
#            i = eval_trends(i)

        if i['type'] == 'currency':
            i['price'] = get_cur_price(i['name'])
#            i['last_daily_price'] = i['price'] # get_cur_last_daily_close(i['name'])
#            i = eval_trends(i)
    if display:
        write_display(things)
    else:
        write_console(things)
