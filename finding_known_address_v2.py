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
import csv
import itertools
import psycopg2
#print(statistics.get().blocks_size)

#print(blockchain.statistics.get().blocks_size)
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_received)
#print(blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840'))
#print(blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt').total_sent)
#est = blockchain.blockexplorer.get_address('1FCUQUYRCjxSfkNk5XnKx1xfNYvdZScrGt')
#tt = test.transactions

#tt = blockchain.blockexplorer.get_tx('6c62072cd17410c6b17a36de9119bef59d38044647e3908d5da720d24b063840')
#try:
#    conn = psycopg2.connect(dbname='chainspark_data', user='chaispark_admin', host='db-nddw4l3bc3tfwslpm46rcbae5e.coegqtcbi3dz.us-west-2.rds.amazonaws.com', password='jYjFkgRqpGhNQoKpWF3KgDNw')
#except Exception as e:
#    print ("I am unable to connect to the database", str(e))
#    
#cur = conn.cursor()
#def read_from_db():
#    cur.execute("SELECT address FROM label_wallets")
#    #c.execute("SELECT * FROM stuffsToPlot WHERE value=3 AND keyword='Python'")
#    #c.execute("SELECT unix, datestamp FROM stuffsToPlot WHERE value=8 AND keyword='Python'")
#    #data = c.fetchall()
#    #print(data)                    #getting the data all at once
#    addr_list = []
#    for data in cur.fetchall():
#        addr_list.append(data[0])
#    
#    return addr_list
#
#def dynamic_data_entry(address):
#    wallet_name = 'allcoin'
#    #address = '1FyXSWQsesD4jM35i62wVLu92jVvuMXtND'
#    type_addr = 'bitcoin'
#    cur.execute("INSERT INTO label_wallets (wallet_name, address, type) VALUES (%s, %s, %s)",
#              (wallet_name, address, type_addr))
#    conn.commit()
    
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
    
#addresses = ['1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g',
#'1PrjPNmtfYkEmnX1DCyu2A1Smg29Ke1maP',
#'1DivaVLgz7AEsnGMD41gwuesgBRmHhUiVr',
#'3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r']
addresses = pd.read_csv('bittrex.csv')
addresses = list(addresses['address'])
#addresses = read_from_db()
total_addresses.extend(addresses)
final_list, address_details = address_postmortem(addresses)
    
for i in range(3):
    temp = list(itertools.chain.from_iterable(address_details))
    temp = set(temp) - set(total_addresses)
    temp = list(temp)
    with open('bittrex.csv', 'a') as fd:
        wr = csv.writer(fd, dialect='excel', delimiter="\n")
        wr.writerow(temp)
    fd.close()
    total_addresses.extend(temp)
    print('------------------------------------------', len(temp))
    final_list, address_details = address_postmortem(temp)            

temp = list(itertools.chain.from_iterable(address_details))
temp = set(temp) - set(total_addresses)
temp = list(temp)
total_addresses.extend(temp)

#for i in temp:
#    dynamic_data_entry(i)

print(datetime.now())