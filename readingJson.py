#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:44:35 2018

@author: agile
"""

import json
from pprint import pprint

with open('sample_txns.json') as f:
    data = json.load(f)
    print(data)

