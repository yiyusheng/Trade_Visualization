#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename: btce_collector.py
#
# Description: 
#
# Copyright (c) 2017, Yusheng Yi <yiyusheng.hust@gmail.com>
#
# Version 1.0
#
# Initial created: 2017-05-11 10:46:11
#
# Last   modified: 2017-05-18 14:49:33
#
#
#

#import btceapi
#import sys
#import pylab
#import json
#import numpy as np
#import pandas as pd
#import btceAPI.common as bc

import time
import decimal
import sqlite3
import btceAPI.public as bp

#%% convert before insert into sqlite
def adapt_decimal(d):
    return str(d)
    
def convert_decimal(s):
    return decimal.Decimal(s)

sqlite3.register_adapter(decimal.Decimal,adapt_decimal)
sqlite3.register_converter('decimal', convert_decimal)

#%% create sqlite database
def createSqlite(dbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    cur.execute('''create table if not exists '''+dbName+'''_tradeHistory
             (pair text,
              type text,
              price decimal,
              tid decimal primary key,
              amount decimal,
              timestamp decimal)''')
    cur.close()
    conn.close()

#%% drop sqlite database
def dropSqlite(dbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()    
    cur.execute('drop table if exists '+dbName+'_tradeHistory')
    cur.close()
    conn.close()
    
#%% getTradeHistory per hours
def getPerhour(pair, dbName, lmt=5000):
    try:
        history = bp.getTradeHistory(pair, lmt = lmt)
        conn = sqlite3.connect(dir_SQL+dbName+".sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
        cur = conn.cursor()
        cur.executemany('insert or ignore into btce_tradeHistory values(?,?,?,?,?,?)',history)
        conn.commit()
        cur.close()
        conn.close()
    except Exception,e:
        print('[%s]\tException:%s' %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e))
        
#%% get sqlite infomation
def getSqliteInfo(dbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    a = cur.execute('select count(*) from btce_tradeHistory')
    a = a.fetchall()
    print('[%s] %d items in sqlite-%s' %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),a[0][0],dbName))
    cur.close()
    conn.close()
    return(a[0][0])    


#%% build connection
my_pair = ['btc_usd','ltc_usd','eth_usd','ltc_btc','eth_btc']
dbName = 'btce'
dir_SQL = '/home/yiyusheng/Data/Trade_Visualization/'

#dropSqlite(dbName)                                           
createSqlite(dbName)
[getPerhour(p,dbName = dbName) for p in my_pair]
getSqliteInfo(dbName)
