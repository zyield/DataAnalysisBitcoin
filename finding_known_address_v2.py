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
import itertools
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
    list_labelled = []
    final_list = {}
    prob_list = []
    for addr in addresses:
        try:
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
        except:
               print('**************************** FAILLLLLLL')
               try:
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
               except:
                    print('**************************** LAST')
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
                    
        already_labeled = list(set(already_labeled))     
                
        for i in already_labeled:
            if i in input_addrs.keys():
                input_addrs.pop(i, None)
            if i in output_addrs.keys():
                output_addrs.pop(i, None)

        print(len(already_labeled))
        list_labelled.append(already_labeled)
        
    return prob_list, list_labelled
 
def relationships(addresses):
    match = []
    for i in range(len(address_details)):
        for j in range(i, len(address_details)):
            if(i!=j):
                #print(list(set(address_details[i]).intersection(address_details[j])))
                match.extend(list(set(address_details[i]).intersection(address_details[j])))
    return match 
    
print(datetime.now())
final_list= {}
total_addresses = []

address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    
addresses = ['1tsK4jdcUMmDCX74qZcjHyjHUwuQad4Bg'
             ]
total_addresses.extend(addresses)
final_list, address_details = address_postmortem(addresses)

#match = relationships(address_details)
    
for i in range(2):
    temp = list(itertools.chain.from_iterable(address_details))
    temp = set(temp) - set(total_addresses)
    temp = list(temp)
    total_addresses.extend(temp)
    print('------------------------------------------', len(temp))
    final_list, address_details = address_postmortem(temp)            

temp = list(itertools.chain.from_iterable(address_details))
temp = set(temp) - set(total_addresses)
temp = list(temp)
total_addresses.extend(temp)

print(datetime.now())