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

pool = ThreadPool(processes=4)
addr = '3KR3WFLeW2bdWu1BGFM6uwM3uTkeJG3xvm'
#tt = blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840')
X = []
def kmeans(i):
    global X
    temp_addr = blockchain.blockexplorer.get_address(i)
    n_tx = temp_addr.n_tx
    final_bal = temp_addr.final_balance/100000000
    recd = temp_addr.total_received/100000000
    sent = temp_addr.total_sent/100000000
    X.append([(final_bal/n_tx), (recd/n_tx), (sent/n_tx), (n_tx)])

def kmeans2(i):
    global test
    temp_addr = blockchain.blockexplorer.get_address(i)
    n_tx = temp_addr.n_tx
    final_bal = temp_addr.final_balance/100000000
    recd = temp_addr.total_received/100000000
    sent = temp_addr.total_sent/100000000
    test.append([(final_bal/n_tx), (recd/n_tx), (sent/n_tx), (n_tx)])

        
    #clustering = KMeans(n_clusters = 2, random_state=5) # 3 for groups and 5 are random points
    #clustering.fit(X)    
    #print(clustering.labels_)
        
def get_addresses(addr):
    main_address = blockchain.blockexplorer.get_address(addr)    
    output_addrs={}
    input_addrs={}
    tran_id = []
    
    
    already_labeled = []
    
    for i in main_address.transactions:
        temp_list = []
        tran_id.append(i.hash)
        for j in i.inputs:
            temp_list.append(j.address)
        if (len(temp_list) > 1) & (addr in temp_list):
            temp_list.remove(addr)
            already_labeled.extend(temp_list)
        elif addr in temp_list:
            for x in i.outputs:
                if x.address not in output_addrs.keys():
                    output_addrs[x.address] = []
                output_addrs[x.address].append(x.value)
        else:
            for j in i.inputs:
                if j.address not in input_addrs.keys():
                    input_addrs[j.address] = []
                input_addrs[j.address].append(j.value)
                
    already_labeled = list(set(already_labeled))     
            
    for i in already_labeled:
        if i in input_addrs.keys():
            input_addrs.pop(i, None)
        if i in output_addrs.keys():
            output_addrs.pop(i, None)
    
        
    freq_addrs_in = sorted(input_addrs, key=lambda k: len(input_addrs[k]), reverse=True)
    freq_addrs_out = sorted(output_addrs, key=lambda k: len(output_addrs[k]), reverse=True)
    
    amt_addrs_in = {key: sum(input_addrs[key]) for key in input_addrs}
    amt_addrs_in = sorted(amt_addrs_in, key=lambda x: amt_addrs_in[x], reverse=True)
    amt_addrs_out = {key: sum(output_addrs[key]) for key in output_addrs}
    amt_addrs_out = sorted(amt_addrs_out, key=lambda x: amt_addrs_out[x], reverse=True)
    
    try:
        freq_addrs_in.remove(addr)
        amt_addrs_in.remove(addr)
        freq_addrs_out.remove(addr)
        amt_addrs_out.remove(addr)
    except:
        1
    final_list = {}
    for i in freq_addrs_out, amt_addrs_out, freq_addrs_in, amt_addrs_in:
    #    try:
    #        for j in i[0:10]:
    #            final_list.append(j)
    #    except:
    #        for j in i:
    #            final_list.append(j)
        for j in i:
            if j not in final_list.keys():
                final_list[j]=0
            final_list[j]= final_list[j]+1

    final_list = sorted(final_list.items(), key=lambda kv: kv[1], reverse=True)
    
    return final_list, already_labeled
#final_list = (Counter(final_list)).most_common
#print(final_list)

#for i in len(final_list):
#    print(i, blockchain.blockexplorer.get_address(i).total_received, blockchain.blockexplorer.get_address(i).n_tx, blockchain.blockexplorer.get_address(i).final_balance)
#label(already_labeled)

final_list, already_labeled = get_addresses(addr)
test = []
print(datetime.now())
for i in already_labeled:
    kmeans2(i)
print('***********************************DONE******************************************')
print(datetime.now())
for i in range(0, len(already_labeled)-3, 4):
    X1 = pool.apply_async(kmeans, [already_labeled[i]])
    X2 = pool.apply_async(kmeans, [already_labeled[i+1]])
    X3 = pool.apply_async(kmeans, [already_labeled[i+2]])
    X4 = pool.apply_async(kmeans, [already_labeled[i+3]])

while(X4.ready() == False):
    1

print(datetime.now())
print('--------------------------------')
clustering = KMeans(n_clusters = 3, random_state=10) # 3 for groups and 5 are random points
clustering.fit(X)    
print(clustering.labels_)