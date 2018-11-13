#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 21:54:38 2018

@author: agile
"""

import pandas as pd

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
    
#def trans_forward(id):

sender = tx_out[tx_out['txid'] == idx]
receiver = tx_in[tx_in['hashPrevOut'] == idx]
test = tx_out[tx_out['txid'] == receiver['txid'].iloc[0]]

print(sender['address'], test['address'])
    
    