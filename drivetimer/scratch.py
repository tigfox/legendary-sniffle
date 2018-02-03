# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests

stockSymbol = 'NASDAQ:ETSY' #string as MARKET:STOCK see alphavantage API guide for details
alphaVantageAPI = '3R81P8I8EK4HV3ES' #alphavantage API key

#==============================================================================
#r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=Brooklyn,NY&destination=Oyster+Bay,NY&key=AIzaSyCriePfKNU2Rkb-bCwcT9ESHLiAA-vVpDc')
#for routes in r.json()['routes']:
#     for legs in routes['legs']:
#         duration = legs['duration']
#         if duration['value'] <= 3600:
#             print("Go Home Right Meow. It'll take you " + str(duration['value']/60) + " minutes.")
# 
#==============================================================================

#==============================================================================
# r = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=ETSY&apikey=3R81P8I8EK4HV3ES')
# symbol = r.json()['Realtime Global Securities Quote']['01. Symbol']
# price  = r.json()['Realtime Global Securities Quote']['03. Latest Price']
# openPrice = r.json()['Realtime Global Securities Quote']['04. Open (Current Trading Day)']
# direction = price >= openPrice
#==============================================================================

def get_stockprice():
    stockURL = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + stockSymbol + '&apikey=' + alphaVantageAPI 
    r = requests.get(stockURL)
    symbol = r.json()['Realtime Global Securities Quote']['01. Symbol']
    price  = r.json()['Realtime Global Securities Quote']['03. Latest Price']
    openPrice = r.json()['Realtime Global Securities Quote']['04. Open (Current Trading Day)']
    direction = price >= openPrice
    print(price)#, direction)
    
get_stockprice()
