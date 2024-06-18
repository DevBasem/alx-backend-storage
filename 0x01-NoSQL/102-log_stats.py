#!/usr/bin/env python3
"""
Advanced script to provide stats about Nginx logs stored in MongoDB,
including methods counts, status checks, and top 10 IPs.
"""

from pymongo import MongoClient

def get_logs_stats(mongo_collection):
    # Count total number of logs
    total_logs = mongo_collection.count_documents({})

    # Count methods
    methods_counts = {
        "GET": mongo_collection.count_documents({"method": "GET"}),
        "POST": mongo_collection.count_documents({"method": "POST"}),
        "PUT": mongo_collection.count_documents({"method": "PUT"}),
        "PATCH": mongo_collection.count_documents({"method": "PATCH"}),
        "DELETE": mongo_collection.count_documents({"method": "DELETE"})
    }

    # Count status check
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})

    # Top 10 IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)

    return total_logs, methods_counts, status_check_count, top_ips

def print_logs_stats(total_logs, methods_counts, status_check_count, top_ips):
    print(f"{total_logs} logs")

    print("Methods:")
    for method, count in methods_counts.items():
        print(f"\tmethod {method}: {count}")

    print(f"{status_check_count} status check")

    print("IPs:")
    for idx, ip_data in enumerate(top_ips, start=1):
        ip = ip_data["_id"]
        count = ip_data["count"]
        print(f"\t{ip}: {count}")

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Retrieve and print stats
    total_logs, methods_counts, status_check_count, top_ips = get_logs_stats(nginx_collection)
    print_logs_stats(total_logs, methods_counts, status_check_count, top_ips)
