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
            
        for i in freq_addrs_out, amt_addrs_out, freq_addrs_in, amt_addrs_in:
            for j in i:
                if j not in final_list.keys():
                    final_list[j]=0
                final_list[j]= final_list[j]+1

        total_len = int(len(already_labeled)/8)
        print(len(already_labeled))
    #address_details = pd.concat(address_details)
        list_labelled.append(already_labeled)
    return final_list, list_labelled
 
print(datetime.now())
final_list= {}
total_addresses = []

address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    
addresses = ['1D27vWhZgLETSAitA4VGhphzjvcVwa6ygJ',
'14qPaAAw8vNwRtVk82ddXVeVSQ1hpcVhu5',
'12ceuQRXpyM2BzY9vXKPpnkQuu5W7j7sCe',
'18hcVGPUyn1tqNoa7xMtgHXdj7FwNRC5K3',
'1Q2TWz2xnHSFfAT2TBKYYwor85ztf4STjz',
'1BUT4VtvsxfNkfmsZ2FNrEx12AyKhrwUyJ',
'1JZQ1zhnYitgMNTRqjRVLntscy1cFnPNsz',
'1PnfBQLpQhTymXoZVf4kGMDYACwoPVNxKX',
'1At9sjtWqbYiu8qGwfu21wkQBSVhdrHov',
'1NEoNMs43XmJ3XvEvwxQEzNFjQsmnt94NG',
'1MomM9WaaEvMkGQQz4Gq5xYWEnaxyk9pHs',
'1Cr9L3fupF8xKPCsxj2D4xhYqDumy8nEuE',
'1GXavRMNX9rKgRt43pTJtVYKEbM9AJ4rCA',
'19gAQv8YizsqruRPkBfoVpdL8jccnGauq8',
'18zSbvhjLHXuHFzuWGqHdGRCAUBehRqckB',
'1HqrMM4qnGbtsTqmjKZoWwzBCQbEyseVbo',
'1PGRw6ozoXydPb2wf1AgG8mzg6H4xJcT9E',
'17BymcHaGRbXGnEzR2m9woUYNf9FBPPJ2P',
'1EGuNh3nBiFz4JQdob4brN292K3kzCbXvn']
        
total_addresses.extend(addresses)

final_list, address_details = address_postmortem(addresses)
test = []
for i in range(len(address_details)):
    for j in range(i, len(address_details)):
        if(i!=j):
            print(list(set(address_details[i]).intersection(address_details[j])))
            test.extend(list(set(address_details[i]).intersection(address_details[j])))



#addresses = list(address_amount.iloc[0:10]['Address'])
#addresses.extend(list(address_trans.iloc[0:10]['Address']))
#addresses = list(set(addresses))
#total_addresses.extend(addresses)
#
#final_list_temp, address_details_temp = address_postmortem(addresses)
#
#final_list = {**final_list, **final_list_temp}
#
#address_details = address_details.append(address_details_temp , ignore_index=True)  
#
#address_details = address_details[~address_details['Address'].isin(total_addresses)]
#
#address_details = address_details.drop_duplicates()
#address_trans = address_details.sort_values(by=['Trans'], ascending=False)
#address_amount = address_details.sort_values(by=['Received'], ascending=False)
##final_list = sorted(final_list.items(), key=lambda kv: kv[1], reverse=True)
#
#total_addresses.extend(list(address_amount.iloc[0:10]['Address']))
#total_addresses.extend(list(address_trans.iloc[0:10]['Address']))
#total_addresses = list(set(total_addresses))
print(datetime.now())

