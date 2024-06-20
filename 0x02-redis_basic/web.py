# web.py

import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """
    Decorator for get_page function.
    Tracks how many times the function is called for each URL
    and caches the results in Redis with a 10-second expiration.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        # Initialize Redis connection
        client = redis.Redis(host='localhost', port=6379)

        # Increment count for the URL
        client.incr(f'count:{url}')

        # Check if the URL's response is cached
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')

        # If not cached, fetch from the web
        response = fn(url)

        # Cache the response with a 10-second expiration
        client.set(f'{url}', response, ex=10)

        return response

    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """
    Makes an HTTP GET request to a given URL and returns the response text.
    """
    response = requests.get(url)
    return response.text


# Example usage:
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"
    html = get_page(url)
    print(html)
