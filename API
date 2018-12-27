#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 13:38:04 2018

@author: agile
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
from classification_v2 import label_address
import json

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, address):
        address = str(address).split(',')
        final_labels = ''
        final_labels = label_address(address)
        if len(final_labels) != 0:
            return (final_labels.to_json(), 200)
        return ("Not found", 404)

api.add_resource(User, "/<string:address>")
app.run(debug=True)

