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
# Last   modified: 2017-05-24 15:50:03
#
#
#

import time
import decimal
import sqlite3
import os
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
def exportDB(dbName,tbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    r = cur.execute('select * from '+tbName)
    r = r.fetchall()
    DT = pd.DataFrame(r)
    with open(dir_SQL+tbName+'.csv', "wb") as f:
        DT.to_csv(f)
    cur.close()
    conn.close()
    return(DT)    

#%% load sqlite infomation
def loadDB(dbName,tbName):
    conn = sqlite3.connect(dir_SQL+dbName+".sqlite")
    cur = conn.cursor()
    r = cur.execute('select * from '+tbName)
    r = r.fetchall()
#    DT = pd.DataFrame(r)
    DT = r
    cur.close()
    conn.close()
    return(DT)    

#%% build connection
dir_SQL = os.path.expanduser('~')+'/Data/Trade_Visualization/'
DT = loadDB('btce','btce')
#DT_old = loadDB('btce','btce_tradeHistory')
