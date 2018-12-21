#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 12:45:20 2018

@author: agile
"""

import blockchain
from sklearn.cluster import KMeans
from datetime import datetime
import pandas as pd
import math
import pickle




def validation(i):
    address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    for j in i:
        try:
            temp_addr = blockchain.blockexplorer.get_address(j)
            n_tx = temp_addr.n_tx
            final_bal = temp_addr.final_balance/100000000
            recd = temp_addr.total_received/100000000
            sent = temp_addr.total_sent/100000000
            
            temp = {'Address': j, 'Trans': n_tx, 'Final bal': final_bal, 'Received': recd, 'Sent': sent}
            address_details = address_details.append(temp , ignore_index=True)   
        except Exception as e:
            print(e, j)
    return address_details 
        

clustering = pickle.load(open("cluster.sav", 'rb'))
X = validation(['37k5U5xQJkojFHkHVgrY7Dq7xtJJNSqVid', '17YyZSNFt31pzGXfZtrzs7Y5Nd56rG2uU5', 
                '39vi392JLo4ksHUQrajddPJoK1wH8rmUyS', '1CSvNmJ4kCgQr9ubPaerrdhx7yUdLgKyKo',
                '1JNW9w4kPiiBgaEW12xT5kiHxQgZxFRTQ4'])

print(datetime.now())
print('--------------------------------')

intermediate_address = X[(X['Trans'] <= 5) & (X['Final bal'] <= 10)]
intermediate_address.Sent = 'intermediate address'
X.drop(intermediate_address.index.values, axis=0, inplace=True)

still_waiting = X[X['Trans'] == 1]
still_waiting.Sent = 'still waiting'
X.drop(still_waiting.index.values, axis=0, inplace=True)
cold_store = X[abs(X['Final bal'] - X['Received']) <= 10]
cold_store.Sent = 'Cold Storage'
X.drop(cold_store.index.values, axis=0, inplace=True)
formula_address = [] 
for i in range(len(X)):
    rec = str(int(X.iloc[i]['Received']))
    rec = len(rec)
    trans = str(X.iloc[i]['Trans'])
    trans = len(trans)
    max_val = max([rec, trans])
    min_val = min([rec, trans])
    calc = min_val - (math.e/max_val)
    formula_address.append(calc)
X = X.reset_index()

X['Received'] = abs(X['Received'] - X['Trans']) / (X['Trans']+X['Received'])
X['Sent'] = pd.Series(formula_address)

addr = list(X['Address'])
predictions = clustering.predict(X[['Received', 'Sent']])

final_labels=pd.DataFrame(columns=['Address', 'Label'])

for i in range(len(addr)):
    label = ''
    if predictions[i] == 0:
        label = 'Other'
    elif predictions[i] == 1:
        label = 'Light Exchange'
    else:
        label = 'Main Exhange'
    
    final_labels = final_labels.append({'Address': addr[i], 'Label': label}, ignore_index=True)

for i in intermediate_address, cold_store, still_waiting:
    i = i[['Address', 'Sent']]
    i.columns = ['Address', 'Label']
    try:
       final_labels = pd.concat([final_labels, i], ignore_index=True)
    except:
        1

