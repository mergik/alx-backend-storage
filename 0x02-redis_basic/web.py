#!/usr/bin/env python3
""" File to implement expiring web cache and tracker """
from functools import wraps
from typing import Callable
import redis
import requests


local_redis = redis.Redis()


def cache_call(method: Callable) -> Callable:
    """
    Returns method with tracking on specified url
    Counts number of times method is called
    Adds expiration time in seconds to key
    """
    @wraps(method)
    def wrapper(*args):
        """
        Defines wrapper to count number of calls and sets expiration time
        """
        key = f"count:{args[0]}"
        local_redis.incr(key)
        local_redis.setex(key, 10, local_redis.get(key))
        return method(*args)
    return (wrapper)


@cache_call
def get_page(url: str) -> str:
    """ Return HTML content for given URL """
    content = requests.get(url)
    return content.text
