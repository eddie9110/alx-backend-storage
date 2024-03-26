#!/usr/bin/env python3
"""
module contains insert school function
"""


def insert_school(mongo_collection, **kwargs):
    """function inserts a new document in a collection based on kwargs"""
    _id = mongo_collection.insert(kwargs)
    return _id
