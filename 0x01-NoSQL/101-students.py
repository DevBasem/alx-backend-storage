#!/usr/bin/env python3
""" 101-students """
from pymongo import MongoClient

def top_students(mongo_collection):
    students = list(mongo_collection.find())
    
    for student in students:
        total_score = 0
        num_topics = len(student['topics'])
        for topic in student['topics']:
            total_score += topic['score']
        student['averageScore'] = total_score / num_topics if num_topics > 0 else 0
    
    sorted_students = sorted(students, key=lambda x: x['averageScore'], reverse=True)
    
    return sorted_students
