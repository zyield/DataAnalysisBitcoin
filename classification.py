#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 12:45:20 2018

@author: agile
"""

import blockchain
from sklearn.cluster import KMeans
import threading
from collections import Counter
from multiprocessing.pool import ThreadPool
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2


try:
    conn = psycopg2.connect(dbname='chainspark_data', user='chaispark_admin', host='db-nddw4l3bc3tfwslpm46rcbae5e.coegqtcbi3dz.us-west-2.rds.amazonaws.com', password='jYjFkgRqpGhNQoKpWF3KgDNw')
except Exception as e:
    print ("I am unable to connect to the database", str(e))
    
cur = conn.cursor()

def read_from_db():
    cur.execute("SELECT address FROM label_wallets WHERE wallet_name='bitfinex'")
    temp = []
    for data in cur.fetchall():
        temp.append(data[0])
    return temp

def validation(i):
    address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent', 'ins', 'outs'])
    for j in i:
        temp_addr = blockchain.blockexplorer.get_address(j)
        n_tx = temp_addr.n_tx
        final_bal = temp_addr.final_balance/100000000
        recd = temp_addr.total_received/100000000
        sent = temp_addr.total_sent/100000000
        inputs = 0
        outputs = 0
        for trans in temp_addr.transactions:
            flag = 0
            for ins in trans.inputs:
                flag = flag+1
                try:
                    if j in ins.address:
                        outputs = outputs+1
                        flag=0
                        break
                except:
                    1
            if flag != 0:
                inputs = inputs+1
                
        
        temp = {'Address': j, 'Trans': n_tx, 'Final bal': final_bal, 'Received': recd, 'Sent': sent, 'ins': inputs, 'outs': outputs}
        address_details = address_details.append(temp , ignore_index=True)   
    return address_details 
        

already_labeled = pd.read_csv('bitfinex.csv')
already_labeled = list(already_labeled['address'])
already_labeled = already_labeled[-1000:]
#already_labeled = ['14yuCHnhjQudtv2CVypSbrxB7qxr3Hsote']
#already_labeled = read_from_db()
#already_labeled = already_labeled[0:10000]

pool = ThreadPool(processes=8)
total_len = int(len(already_labeled)/8)
print(len(already_labeled))        
X1 = pool.apply_async(validation, [already_labeled[0:total_len]])
X2 = pool.apply_async(validation, [already_labeled[total_len:(total_len*2)]])
X3 = pool.apply_async(validation, [already_labeled[(total_len*2):(total_len*3)]])
X4 = pool.apply_async(validation, [already_labeled[(total_len*3):(total_len*4)]])
X5 = pool.apply_async(validation, [already_labeled[(total_len*4):(total_len*5)]])
X6 = pool.apply_async(validation, [already_labeled[(total_len*5):(total_len*6)]])
X7 = pool.apply_async(validation, [already_labeled[(total_len*6):(total_len*7)]])
X8 = pool.apply_async(validation, [already_labeled[(total_len*7):]])
while(X1.ready() == False) & (X2.ready() == False) & (X3.ready() == False) & (X4.ready() == False) & (X5.ready() == False) & (X6.ready() == False) & (X7.ready() == False) & (X8.ready() == False) :
    1
print('*********************************Yayyyy**************************************', datetime.now())

# 
#address_details = address_details.append([X1.get(timeout=9999999), X2.get(timeout=9999999),
#                                          X3.get(timeout=9999999), X4.get(timeout=9999999),
#                                          X5.get(timeout=9999999), X6.get(timeout=9999999),
#                                          X7.get(timeout=9999999), X8.get(timeout=9999999)], ignore_index=True)
X = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent', 'ins', 'outs'])

X = X.append(X1.get(timeout=999999), ignore_index=True)
X = X.append(X2.get(timeout=999999), ignore_index=True)
X = X.append(X3.get(timeout=999999), ignore_index=True)
X = X.append(X4.get(timeout=999999), ignore_index=True)
X = X.append(X5.get(timeout=999999), ignore_index=True)
X = X.append(X6.get(timeout=999999), ignore_index=True)
X = X.append(X7.get(timeout=999999), ignore_index=True)
X = X.append(X8.get(timeout=999999), ignore_index=True)

print(datetime.now())
print('--------------------------------')
X_ = X

temp_address = X[X['Trans'] <= 2]
X = X[(X['Trans'] > 2) & (X['Received'] > 1000)]
X = X.reset_index()
X['Received'] = X['Received'] / X['ins']
X['Sent'] = X['Sent'] / X['outs']
X['outs'] = X['outs'] / X['ins']
addr = list(X['Address'])
X = X.drop(['Address', 'Trans', 'Final bal', 'ins', 'index'], axis=1)

clustering = KMeans(n_clusters = 3, random_state=7) # 3 for groups and 5 are random points
clustering.fit(X)    

pred_labels = clustering.labels_

if(conn):
    cur.close()
    conn.close()