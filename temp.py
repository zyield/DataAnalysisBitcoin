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

gg = blockchain.blockexplorer.get_address('34GRz5DtCBXZTF9xCGYYMvix88DFUVVc1K')
inputs=0
outputs = 0
for i in gg.transactions:
    if gg.address in i.inputs:
        print('sdfsdfsdf')