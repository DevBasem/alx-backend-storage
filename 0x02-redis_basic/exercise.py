#!/usr/bin/env python3
"""
exercise.py

This module contains the Cache class for interacting with a Redis database,
as well as decorators to count method calls and store call histories.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.

    :param method: The method to be decorated.
    :return: The decorated method with call count functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment the call count in Redis and
        call the original method.

        :param args: Positional arguments for the original method.
        :param kwargs: Keyword arguments for the original method.
        :return: The return value of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    :param method: The method to be decorated.
    :return: The decorated method with call history functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store inputs and outputs in Redis
        and call the original method.

        :param args: Positional arguments for the original method.
        :param kwargs: Keyword arguments for the original method.
        :return: The return value of the original method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string
        self._redis.rpush(input_key, str(args))

        # Execute the original method and store the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    :param method: The method whose call history is to be displayed.
    """
    r = redis.Redis(host='127.0.0.1', port=6379)
    method_name = method.__qualname__
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for input_val, output_val in zip(inputs, outputs):
        input_str = input_val.decode('utf-8')
        output_str = output_val.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache:
    """
    Cache class

    This class provides methods to interact with a Redis database,
    including storing data with randomly generated keys and
    retrieving data with type conversion.
    """

    def __init__(self):
        """
        Initialize the Cache class.

        Creates an instance of the Redis client and flushes the database.
        """
        self._redis = redis.Redis(host='127.0.0.1', port=6379)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        :param data: The data to be stored, which can be
        of type str, bytes, int, or float.
        :return: The randomly generated key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        :param key: The key string to look up in Redis.
        :param fn: The optional callable to convert the retrieved data.
        :return: The retrieved data, optionally converted by fn,
        or None if key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        :param key: The key string to look up in Redis.
        :return: The retrieved string data or None if key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        :param key: The key string to look up in Redis.
        :return: The retrieved integer data or None if key does not exist.
        """
        return self.get(key, lambda d: int(d))
