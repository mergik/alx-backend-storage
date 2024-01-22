#!/usr/bin/env python3
"""fn that returns all students sorted by average score"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """Returns all students in a collection"""
    if mongo_collection is None:
        return []
    else:
        unwind = [
            {"$unwind": "$topics"},
            {
                "$group":
                {
                    "_id": "$_id",
                    "name": {"$first": "$name"},
                    "averageScore":
                        {"$avg": "$topics.score"}
                }
            },
            {
                "$sort": {"averageScore": -1}
            },
        ]
        return mongo_collection.aggregate(unwind)
