#!/usr/bin/env python3
"""
8-all
"""

def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection.
    """
    documents = list(mongo_collection.find({}))
    return documents

# For testing purposes, if this script is run directly
if __name__ == "__main__":
    from pymongo import MongoClient

    # Establish a connection to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Select the database and collection
    db = client.my_db
    collection = db.school

    # Call the list_all function
    schools = list_all(collection)

    # Print each school's _id and name
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
