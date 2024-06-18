#!/usr/bin/env python3
"""
10-update_topics
"""

def update_topics(mongo_collection, name, topics):
    """
    Update topics of a school document based on name.
    """
    # Update documents where 'name' matches
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
