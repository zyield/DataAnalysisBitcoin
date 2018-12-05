#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:56:04 2018
@author: agile
"""

#from blockchain import statistics
import blockchain
from collections import Counter, OrderedDict
from datetime import datetime
from multiprocessing.pool import ThreadPool
import pandas as pd
import threading
#print(statistics.get().blocks_size)

#print(blockchain.statistics.get().blocks_size)
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_received)
#print(blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840'))
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_sent)
#est = blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt')
#tt = test.transactions

#tt = blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840')
def validation(i):
    address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    for j in i:
        temp_addr = blockchain.blockexplorer.get_address(j)
        n_tx = temp_addr.n_tx
        final_bal = temp_addr.final_balance/100000000
        recd = temp_addr.total_received/100000000
        sent = temp_addr.total_sent/100000000
        temp = {'Address': j, 'Trans': n_tx, 'Final bal': final_bal, 'Received': recd, 'Sent': sent}
        address_details = address_details.append(temp , ignore_index=True)   
    return address_details 
def address_postmortem(addresses):
    pool = ThreadPool(processes=8)
    address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    list_labelled = []
    final_list = {}
    prob_list = []
    for addr in addresses:
        main_address = blockchain.blockexplorer.get_address(addr)
        output_addrs={}
        input_addrs={}
        
        already_labeled = []
        for i in main_address.transactions:
            temp_list = []
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
        temp_prob_list = []    
        for i in freq_addrs_out, amt_addrs_out, freq_addrs_in, amt_addrs_in:
            for j in i:
                temp_prob_list.append(j)
                if j not in final_list.keys():
                    final_list[j]=0
                final_list[j]= final_list[j]+1

        total_len = int(len(already_labeled)/8)
        print(len(already_labeled))
        prob_list.append(temp_prob_list)
    #address_details = pd.concat(address_details)
        list_labelled.append(already_labeled)
    return prob_list, list_labelled
 
def relationships(addresses):
    match = []
    for i in range(len(address_details)):
        for j in range(i, len(address_details)):
            if(i!=j):
                #print(list(set(address_details[i]).intersection(address_details[j])))
                match.append(list(set(address_details[i]).intersection(address_details[j])))
    return match 
    
print(datetime.now())
final_list= {}
total_addresses = []

address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    
addresses = ['1Q4mE3nUqwu8iyySHLZ7svgwdahnAw5b25'
             ]
final_list, address_details = address_postmortem(addresses)
    
match_inputs = relationships(address_details)
match_outputs = relationships(final_list)        

addresses = []
temp_addr = []
temp_final = []

for i in range(1):
    for j in address_details:
        temp_final, temp_addr = address_postmortem(j)
        for z in temp_addr:
            addresses.extend(z)
        

print(datetime.now())