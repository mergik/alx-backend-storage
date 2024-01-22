#!/usr/bin/env python3
"""Provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def loggedStats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient()
    db = client.logs
    logs = db.nginx
    print("{} logs".format(logs.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(f"\tmethod {method}: " +
              f"{logs.count_documents({'method': method})}")
    print(f"{logs.count_documents({'method': 'GET', 'path': '/status'})} \
status check")


if __name__ == "__main__":
    loggedStats()
