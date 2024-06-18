#!/usr/bin/env python3
"""
12-log_stats
"""

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.
    """
    total_logs = mongo_collection.count_documents({})

    # Count documents for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: mongo_collection.count_documents({"method": method}) for method in methods}

    # Count documents where method=GET and path=/status
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})

    # Print the stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Select the database and collection
    db = client.logs
    collection = db.nginx

    # Call the log_stats function to print statistics
    log_stats(collection)
