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
def address_postmortem(addresses):
    pool = ThreadPool(processes=8)
    address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    final_list = {}
    for addr in addresses:
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
            
        main_address = blockchain.blockexplorer.get_address(addr)
        
        balance = main_address.final_balance
        
        output_addrs={}
        input_addrs={}
        tran_id = []
        time = []
        amt_spent = []
        amt_got = []
        
        sum_in = 0
        sum_out = 0
        imp_trans = []
        
        
        already_labeled = []
        
        for i in main_address.transactions:
            temp_list = []
            tran_id.append(i.hash)
            time.append(datetime.utcfromtimestamp(int(i.time)).strftime('%Y-%m-%d %H:%M:%S'))
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
        if (len(already_labeled) > 500):
            already_labeled = already_labeled[0:500]

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
        print('*********************************Yayyyy**************************************')
    
    # 
        address_details = address_details.append(X1.get(), ignore_index=True)
        address_details = address_details.append(X2.get(), ignore_index=True)
        address_details = address_details.append(X3.get(), ignore_index=True)
        address_details = address_details.append(X4.get(), ignore_index=True)
        address_details = address_details.append(X5.get(), ignore_index=True)
        address_details = address_details.append(X6.get(), ignore_index=True)
        address_details = address_details.append(X7.get(), ignore_index=True)
        address_details = address_details.append(X8.get(), ignore_index=True)
        print('-------------------------------DONE------------------')
    #address_details = pd.concat(address_details)
    return final_list, address_details
 
print(datetime.now())
final_list= {}
total_addresses = []

address_details = pd.DataFrame(columns=['Address', 'Trans', 'Final bal', 'Received', 'Sent'])
    
addresses = ['1PXGmbXBPds2RZyrT7u7Xqors42zHu7Pzw']
        
total_addresses.extend(addresses)

final_list_temp, address_details_temp = address_postmortem(addresses)
final_list = {**final_list, **final_list_temp}

address_details = address_details.append(address_details_temp , ignore_index=True)

###########################################################################################################
address_details = address_details[~address_details['Address'].isin(total_addresses)]
address_details = address_details.drop_duplicates()
address_trans = address_details.sort_values(by=['Trans'], ascending=False)
address_amount = address_details.sort_values(by=['Received'], ascending=False)


addresses = list(address_amount.iloc[0:10]['Address'])
addresses.extend(list(address_trans.iloc[0:10]['Address']))
addresses = list(set(addresses))
total_addresses.extend(addresses)

final_list_temp, address_details_temp = address_postmortem(addresses)

final_list = {**final_list, **final_list_temp}

address_details = address_details.append(address_details_temp , ignore_index=True)  

address_details = address_details[~address_details['Address'].isin(total_addresses)]

address_details = address_details.drop_duplicates()
address_trans = address_details.sort_values(by=['Trans'], ascending=False)
address_amount = address_details.sort_values(by=['Received'], ascending=False)
#final_list = sorted(final_list.items(), key=lambda kv: kv[1], reverse=True)

total_addresses.extend(list(address_amount.iloc[0:10]['Address']))
total_addresses.extend(list(address_trans.iloc[0:10]['Address']))
total_addresses = list(set(total_addresses))
print(datetime.now())

