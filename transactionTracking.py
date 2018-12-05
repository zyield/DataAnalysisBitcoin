#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:54:38 2018

@author: agile
"""

import pandas as pd
from collections import Counter
import blockchain

tx_in = pd.read_csv('tx_in.csv', delimiter=';', names=['txid', 'hashPrevOut', 'indexPrevOut', 'scriptSig', 'sequence'])
tx_out = pd.read_csv('tx_out.csv', delimiter=';', names=['txid', 'indexOut', 'value', 'scriptPubKey', 'address'])
txns = pd.read_csv('transactions.csv', delimiter=';', names=['txid', 'hashBlock', 'version', 'lockTime'])
#blocks = pd.read_csv('blocks.csv', names=['block_hash', 'height', 'version', 'blocksize', 'hashPrev', 'hashMerkleRoot', 'nTime', 'nBits', 'nNonce'])


def transc_backward(id):
    receive = tx_out[tx_out['txid'] == id]
    hashPrev = tx_in[tx_in['txid'] == receive['txid'].iloc[0]]
    sender = tx_out[tx_out['txid'] == hashPrev['hashPrevOut'].iloc[0]]
    
    print('TxID: ', receive['txid'].iloc[0], 'Sender: ', sender['address'].values, 'Receiver: ', receive['address'].values)
    try:
        return sender['txid'].iloc[0]
    except:
        return ''
    
idx = '7d4eeda69c0420d0b4a87c91aeefe3d4c3de7ccf816355ebe0bdc6cbd1b4c0cd'

#while(len(idx) != 0):
#    idx = transc_backward(idx)
    
def trans_forward(idx, send):
   sender = tx_out[tx_out['txid'] == idx]
   hashNext = tx_in[tx_in['hashPrevOut'] == idx]
   receive = tx_out[tx_out['txid'] == hashNext['txid'].iloc[0]]
   
   if send == '':
       print('TxID: ', sender['txid'].iloc[0], 'Sender: ', 0, 'Receiver: ', sender['address'].values)
   else:
       print('TxID: ', sender['txid'].iloc[0], 'Sender: ', send, 'Receiver: ', sender['address'].values)
   try:
        return receive['txid'].iloc[0], sender['address'].iloc[0]
   except:
        return '', 'Blank'
    
#send = ''
#while(len(idx) != 0):
#    idx, send = trans_forward(idx, send)
#wallet = '12ib7dApVFvg82TXKycWBNpN8kFyiAN1dr'    
wallet = '5a28cf42207c6817308325a05b8bfe97eed5f26a76640240f29b3b1252d1b77c'
total_txns = tx_out[tx_out['address'] == wallet]

count_address = Counter(tx_out['address'])
count_trans = Counter(tx_out['txid'])


    