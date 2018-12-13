#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:48:47 2018

@author: agile
"""

import psycopg2


try:
    conn = psycopg2.connect(dbname='chainspark_data', user='chaispark_admin', host='db-nddw4l3bc3tfwslpm46rcbae5e.coegqtcbi3dz.us-west-2.rds.amazonaws.com', password='jYjFkgRqpGhNQoKpWF3KgDNw')
except Exception as e:
    print ("I am unable to connect to the database", str(e))
    
cur = conn.cursor()

def create_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS label_wallets(wallet_name TEXT NOT NULL, address TEXT PRIMARY KEY NOT NULL,
                                                          type TEXT NOT NULL)''')
    conn.commit()

def read_from_db():
    cur.execute("SELECT address FROM label_wallets WHERE wallet_name='allcoin'")
    #c.execute("SELECT * FROM stuffsToPlot WHERE value=3 AND keyword='Python'")
    #c.execute("SELECT unix, datestamp FROM stuffsToPlot WHERE value=8 AND keyword='Python'")
    #data = c.fetchall()
    #print(data)                    #getting the data all at once
    
    for data in cur.fetchall():
        print(data[0])

def dynamic_data_entry(address):
    wallet_name = 'bitfinex'
    #address = '1FyXSWQsesD4jM35i62wVLu92jVvuMXtND'
    type_addr = 'bitcoin'
    cur.execute("INSERT INTO label_wallets (wallet_name, address, type) VALUES (%s, %s, %s)",
              (wallet_name, address, type_addr))
    conn.commit()

def delete(address):
    cur.execute("DELETE FROM label_wallets WHERE address = address")
    conn.commit()
    
    #c.execute("SELECT * FROM stuffsToPlot WHERE value=3")
    #for data in c.fetchall():
        #print(data)
#read_from_db()
#create_table()
for i in total_addresses:
    dynamic_data_entry(i)
#for i in total_addresses:
#    delete(i)
#print(len(read_from_db()))
if(conn):
    cur.close()
    conn.close()