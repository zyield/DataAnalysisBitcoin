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


def validation(i):
    address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    for j in i:
        temp_addr = blockchain.blockexplorer.get_address(j)
        n_tx = temp_addr.n_tx
        final_bal = temp_addr.final_balance/100000000
        recd = temp_addr.total_received/100000000
        sent = temp_addr.total_sent/100000000
        inputs = 0
        outputs = 0
        for z in temp_addr.transactions:
            inputs = inputs + len(z.inputs)
            outputs = outputs + len (outputs)
        temp = {'Address': j, 'Trans': n_tx, 'Final bal': final_bal/n_tx, 'Received': recd/n_tx, 'Sent': sent/n_tx}
        address_details = address_details.append(temp , ignore_index=True)   
    return address_details 
        

already_labeled = pd.read_csv('btc_wallets.csv')
already_labeled = list(already_labeled['address'])

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
X = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])

X = X.append(X1.get(), ignore_index=True)
X = X.append(X2.get(), ignore_index=True)
X = X.append(X3.get(), ignore_index=True)
X = X.append(X4.get(), ignore_index=True)
X = X.append(X5.get(), ignore_index=True)
X = X.append(X6.get(), ignore_index=True)
X = X.append(X7.get(), ignore_index=True)
X = X.append(X8.get(), ignore_index=True)

print(datetime.now())
print('--------------------------------')
X_ = X
X = X.drop(['Address', 'Trans'], axis=1)
clustering = KMeans(n_clusters = 2, random_state=5) # 3 for groups and 5 are random points
clustering.fit(X)    

pred_labels = clustering.labels_