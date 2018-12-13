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
    output_addrs={}
    count = 0
    try:
        for addr in addresses:
            main_address = blockchain.blockexplorer.get_address(addr)
            for i in main_address.transactions:
                for j in i.outputs: 
                    if j.address != addr:
                        if j.address not in output_addrs.keys():
                            output_addrs[j.address] = 1
                            #final_list[j.address] = blockchain.blockexplorer.(j.address).total_received
                        output_addrs[j.address] = output_addrs[j.address]+1
                                
            print(count)
            count = count+1
    except Exception as e:
        print(e)

    return output_addrs

def address_varification(addresses, know_list):
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
        except Exception as e:
               print('**************************** FAILLLLLLL', e)
               already_labeled = []
                    
        already_labeled = list(set(already_labeled))     

        print(len(already_labeled))
        
        if (len(list(set(already_labeled).intersection(know_list))) != 0):
            prob_list.append(1)
        else:
            prob_list.append(0)
        
    return prob_list
 
    
print(datetime.now())
final_list= {}
total_addresses = []

#address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
addresses = pd.read_csv('list.csv')
addresses = list(addresses['address'])
addresses1 = addresses[0:10000]
#addresses = ['1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g',
#'1PrjPNmtfYkEmnX1DCyu2A1Smg29Ke1maP',
#'1DivaVLgz7AEsnGMD41gwuesgBRmHhUiVr',
#'3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r']
        
total_addresses.extend(addresses1)

#address_details = address_postmortem(addresses1)
#test = []
#for i in range(len(address_details)):
#    for j in range(i, len(address_details)):
#        if(i!=j):
#            print(list(set(address_details[i]).intersection(address_details[j])))
#            test.extend(list(set(address_details[i]).intersection(address_details[j])))
#
#
#matched = Counter(test)

#prob_list = [k for k,v in address_details.items() if v >= 50]
test = pd.read_csv('btc_transactions.csv')
#test = test.iloc[0:200, :]
test2=[]
test2.extend(list(test['from_address']))
test2.extend(list(test['to_address']))
test2 = list(set(test2))
proof = address_varification(test2, addresses)

print(datetime.now())

