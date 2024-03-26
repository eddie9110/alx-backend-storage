#!/usr/bin/env python3
"""
Script contains a Python function that
lists all documents in a collection
"""

def list_all(mongo_collection):
    """
    function that lists all documents in a collection
    """
    docs_ = []
    for x in mongo_collection.find():
        docs_.append(x)
    return docs_
