#!/usr/bin/env python3
""" Functions to perform basic redis operations """
from functools import wraps
from typing import Callable, Union
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a method is called
    Returns method with count newly attached
    """

    @wraps(method)
    def wrapper(self, *args) -> Union[int, str]:
        """
        Defines wrapper to increment counter on each call
        Returns value of wrapped method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args)
    return (wrapper)


def call_history(method: Callable) -> Callable:
    """
    Appends input parameters to :inputs list in redis
    Appends output to :outputs list in redis
    Returns method with history attached
    """
    @wraps(method)
    def wrapper(self, *args) -> Union[int, str]:
        """
        Defines wrapper to append inputs and outputs to redis
        Returns output of wrapped method (aka output from :outputs)
        """
        key = method.__qualname__
        self._redis.rpush(f"{key}:inputs", str(args))
        output = method(self, *args)
        self._redis.rpush(f"{key}:outputs", output)
        return (output)
    return (wrapper)


def replay(method: Callable) -> None:
    """
    Displays history of method calls
    Prints how many times method was called and key/value pairs
        of inputs/outputs in specific format
    """
    local_redis = redis.Redis()
    qn = method.__qualname__
    inputs = local_redis.lrange(f"{qn}:inputs", 0, -1)
    outputs = local_redis.lrange(f"{qn}:outputs", 0, -1)
    print(f"{qn} was called {len(inputs)} times:")
    for i, o in zip(inputs, outputs):
        print(f"{qn}(*{(i).decode('utf-8')}) -> {(o).decode('utf-8')}")


class Cache():
    """ Class to cache info in a Redis database """

    def __init__(self):
        """ Initializes Redis database """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in key:value pair in Redis database
        Return randomly-generated key associated with given data
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return (key)

    def get(self, key: str, fn: Callable = None) -> Union[str, int]:
        """
        Convert data to desired format and return it
        Conserve original Redis.get behavior if fn not passed
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """ Returns data in string format """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """ Returns data in int format """
        return self.get(key, int)
