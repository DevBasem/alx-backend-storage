#!/usr/bin/env python3
"""
9-insert_school
"""

def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a MongoDB collection based on kwargs.
    """
    # Insert one document with kwargs
    result = mongo_collection.insert_one(kwargs)
    # Return the _id of the inserted document
    return result.inserted_id

# For testing purposes, if this script is run directly
if __name__ == "__main__":
    from pymongo import MongoClient
    from pprint import pprint

    # Establish a connection to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Select the database and collection
    db = client.my_db
    collection = db.school

    # Example usage: Insert a new school document
    new_school_id = insert_school(collection, name="UCSF", address="505 Parnassus Ave")
    print("New school created: {}".format(new_school_id))

    # Print all schools in the collection
    schools = list(collection.find())
    for school in schools:
        pprint(school)
