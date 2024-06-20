#!/usr/bin/env python3
"""
exercise.py

This module contains the Cache class for interacting with a Redis database.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class

    This class provides methods to interact with a Redis database, including storing
    data with randomly generated keys.
    """

    def __init__(self):
        """
        Initialize the Cache class.

        Creates an instance of the Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        :param data: The data to be stored, which can be of type str, bytes, int, or float.
        :return: The randomly generated key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
