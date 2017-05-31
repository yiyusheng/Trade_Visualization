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
# Last   modified: 2017-05-22 17:48:15
#
#
#

import time
import decimal
import sqlite3
import head
import os
import btceAPI.public as bp

#%% convert before insert into sqlite
def adapt_decimal(d):
    return str(d)
    
def convert_decimal(s):
    return decimal.Decimal(s)

sqlite3.register_adapter(decimal.Decimal,adapt_decimal)
sqlite3.register_converter('decimal', convert_decimal)

#%% create sqlite database
def createSqlite(dbName,tbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    cur.execute('''create table if not exists '''+tbName+'''
             (pair text,
              type text,
              price decimal,
              tid decimal primary key,
              amount decimal,
              timestamp decimal,
              create_time text)''')
    cur.close()
    conn.close()

#%% drop sqlite database
def dropSqlite(dbName,tbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()    
    cur.execute('drop table if exists '+tbName)
    cur.close()
    conn.close()
    
#%% get sqlite infomation
def getSqliteInfo(dbName,tbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    a = cur.execute('select count(*) from '+tbName+' group by pair')
    a = a.fetchall()
    su = a[0][0] + a[1][0] + a[2][0] + a[3][0] + a[4][0]
    print('[%s][sqlite-%s]\tbu:%d\tlu:%d\tlb:%d\teu:%d\teb:%d\ttotal:%d' %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),dbName,a[0][0],a[4][0],a[3][0],a[2][0],a[1][0],su))
    cur.close()
    conn.close()

#%% getTradeHistory per hours
def getPerhour(pair, dbName, tbName, t, lmt=5000):
    try:
        history = bp.getTradeHistory(pair, lmt = lmt)
        conn = sqlite3.connect(dir_SQL+dbName+".sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
        cur = conn.cursor()
        for h in history:
            cur.execute('insert or ignore into '+tbName+' values(?,?,?,?,?,?,?)',list(h) + [t])
            conn.commit()
        cur.close()
        conn.close()
        return(1)
    except Exception,e:
        print('[%s]\tException:%s' %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e))
        return(0)
        
#%% build connection
my_pair = ['btc_usd','ltc_usd','eth_usd','ltc_btc','eth_btc']
dbName = 'btce'
tbName = 'btce'
dir_SQL = '/home/yiyusheng/Data/Trade_Visualization/'
#dir_SQL = os.path.expanduser('~')+'/Data/Trade_Visualization/'
t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

#dropSqlite(dbName,tbName)                                           
createSqlite(dbName,tbName)
[getPerhour(p,dbName,tbName,t,5000) for p in my_pair]
getSqliteInfo(dbName,tbName)
