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
import warnings
from multiprocessing.pool import ThreadPool
import json

warnings.filterwarnings('ignore')

def label_address(X):
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
    print(datetime.now())
    print('--------------------------------')
    pool = ThreadPool(processes=8)
    total_len = int(len(X)/8)
    print(len(X))        
    X1 = pool.apply_async(validation, [X[0:total_len]])
    X2 = pool.apply_async(validation, [X[total_len:(total_len*2)]])
    X3 = pool.apply_async(validation, [X[(total_len*2):(total_len*3)]])
    X4 = pool.apply_async(validation, [X[(total_len*3):(total_len*4)]])
    X5 = pool.apply_async(validation, [X[(total_len*4):(total_len*5)]])
    X6 = pool.apply_async(validation, [X[(total_len*5):(total_len*6)]])
    X7 = pool.apply_async(validation, [X[(total_len*6):(total_len*7)]])
    X8 = pool.apply_async(validation, [X[(total_len*7):]])
    while(X1.ready() == False) & (X2.ready() == False) & (X3.ready() == False) & (X4.ready() == False) & (X5.ready() == False) & (X6.ready() == False) & (X7.ready() == False) & (X8.ready() == False) :
        1
    print('*********************************Yayyyy**************************************', datetime.now())
    X = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    
    X = pd.concat([X, X1.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X2.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X3.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X4.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X5.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X6.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X7.get(timeout=999999)], ignore_index=True)
    X = pd.concat([X, X8.get(timeout=999999)], ignore_index=True)
    print(datetime.now())
    print('--------------------------------')
    #X = validation(X)
    try:
        intermediate_address = X[(X['Trans'] <= 5) & (X['Final bal'] <= 10)]
        intermediate_address.Sent = 'intermediate address'
        X.drop(intermediate_address.index.values, axis=0, inplace=True)
        
        still_waiting = X[X['Trans'] == 1]
        still_waiting.Sent = 'still waiting'
        X.drop(still_waiting.index.values, axis=0, inplace=True)
        cold_store = X[(abs(X['Final bal'] - X['Received']) <= 10) & (X['Received']>100)]
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
    except:
        1
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
        try:
           i = i[['Address', 'Sent']]
           i.columns = ['Address', 'Label']
           final_labels = pd.concat([final_labels, i], ignore_index=True)
        except:
            1
    return final_labels


address = ['3MRaLSzdFtMMsqvF95a8fBmqx252rNqCQA', '392LK4ZQD3gixWg5xJRTv1a24N3YDgCbwP']
final_labels = label_address(address)
print(final_labels)