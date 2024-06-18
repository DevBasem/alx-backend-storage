#!/usr/bin/env python3
"""
11-schools_by_topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Retrieve a list of schools that have a specific topic.
    """
    # Query documents where 'topics' contains the specified topic
    return mongo_collection.find({"topics": topic})
