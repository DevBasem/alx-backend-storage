#!/usr/bin/env python3
"""
Main file
"""

from exercise import Cache

cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))  # should print b'1'

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))  # should print b'3'
