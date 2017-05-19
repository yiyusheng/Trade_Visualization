#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Filename: btce_export.py
#
# Description: 
#
# Copyright (c) 2017, Yusheng Yi <yiyusheng.hust@gmail.com>
#
# Version 1.0
#
# Initial created: 2017-05-11 10:46:11
#
# Last   modified: 2017-05-19 12:44:44
#
#
#

import time
import decimal
import sqlite3
import head
import os
import btceAPI.public as bp
import btceAPI.common as bc
import numpy as np
import pandas as pd

#%% convert before insert into sqlite
def adapt_decimal(d):
    return str(d)
    
def convert_decimal(s):
    return decimal.Decimal(s)

sqlite3.register_adapter(decimal.Decimal,adapt_decimal)
sqlite3.register_converter('decimal', convert_decimal)

#%% export sqlite infomation
def exportDB(dbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    r = cur.execute('select * from btce_tradeHistory')
    r = r.fetchall()
    DT = pd.DataFrame(r)
    with open(dir_SQL+dbName+'.csv', "a") as f:
        DT.to_csv(f)
    cur.close()
    conn.close()
    return(DT)    


#%% build connection
my_pair = ['btc_usd','ltc_usd','eth_usd','ltc_btc','eth_btc']
dbName = 'btce'
dir_SQL = os.path.expanduser('~')+'/Data/Trade_Visualization/'
DT = exportDB('btce')
