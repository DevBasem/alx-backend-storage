# web.py

import requests
import redis
import time

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379)

def get_page(url: str) -> str:
    """
    Fetches the HTML content from a URL and caches the result in Redis with a short expiration time.

    :param url: The URL to fetch HTML content from.
    :return: The HTML content of the URL.
    """
    # Check if URL access count key exists
    count_key = f"count:{url}"
    access_count = redis_client.get(count_key)
    if access_count is None:
        access_count = 0
    else:
        access_count = int(access_count)
    
    # Increment access count
    access_count += 1
    redis_client.set(count_key, access_count, ex=10)  # Cache with expiration of 10 seconds

    # Fetch HTML content from URL
    response = requests.get(url)
    html_content = response.text

    return html_content

# Example usage:
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://example.com"
    html = get_page(url)
    print(html)

