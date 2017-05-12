#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename: btc-e.py
#
# Description: 
#
# Copyright (c) 2017, Yusheng Yi <yiyusheng.hust@gmail.com>
#
# Version 1.0
#
# Initial created: 2017-05-11 10:46:11
#
# Last   modified: 2017-05-11 10:46:13
#
#
#

import btceapi
#import sys
import pylab
import numpy as np
import btceAPI.common as bc
import btceAPI.public as bp
import pandas as pd


#%% build connection
connection = bc.BTCEConnection()
my_pair = ['btc_usd','ltc_usd','eth_usd','ltc_btc','eth_usd']
pair = 'btc_usd'
#%% tickers
attrs = ('high', 'low', 'avg', 'vol', 'vol_cur', 'last','buy', 'sell', 'updated')

print("Tickers:")
info = bp.APIInfo(connection)
my_pair = ['btc_usd','ltc_usd','ltc_btc']
for pair in my_pair:
    ticker = bp.getTicker(pair)
    print(pair)
    for a in attrs:
        print("\t%s %s" % (a, getattr(ticker, a)))
        
#%% history
#if len(sys.argv) >= 2:
#    pair = sys.argv[1]
#    print("Showing history for %s" % pair)
#else:
#    print("No currency pair provided, defaulting to btc_usd")
#    pair = "btc_usd"

for pair in my_pair:
    history = bp.getTradeHistory(pair, lmt=100)
    
    print(len(history))
    
    pylab.plot([t.timestamp for t in history if t.type == u'ask'],
               [t.price for t in history if t.type == u'ask'], 'ro')
    
    pylab.plot([t.timestamp for t in history if t.type == u'bid'],
               [t.price for t in history if t.type == u'bid'], 'go')
    
    pylab.grid()          
    pylab.show()

his_ts = [int(h.timestamp) for h in history]
min_ts = pd.to_datetime(min(his_ts)*1e9)
max_ts = pd.to_datetime(max(his_ts)*1e9)

#%% depth
#if len(sys.argv) >= 2:
#    pair = sys.argv[1]
#    print("Showing depth for %s" % pair)
#else:
#    print("No currency pair provided, defaulting to btc_usd")
#    pair = "btc_usd"

for pair in my_pair:
    asks, bids = bp.getDepth(pair,lmt=5000)

    print(len(asks), len(bids))
    
    ask_prices, ask_volumes = zip(*asks)
    bid_prices, bid_volumes = zip(*bids)
    
    pylab.plot(ask_prices, np.cumsum(ask_volumes), 'r-')
    pylab.plot(bid_prices, np.cumsum(bid_volumes), 'g-')
    pylab.grid()
    pylab.title("%s depth" % pair)
    pylab.show()

#%% depth
a = [bp.getDepth(pair,lmt=5000) for pair in my_pair]
asks1,bids1 = a[0]
asks2,bids2 = a[1]
a = pd.DataFrame(asks2,columns=['price','value'])
b = pd.DataFrame(bids2,columns=['price','value'])
asks3,bids3 = a[2]
asks4,bids4 = a[3]
asks5,bids5 = a[4]

