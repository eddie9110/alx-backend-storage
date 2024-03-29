#!/usr/bin/env python3
''' Redis-Python Cache module '''
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """count_calls decorator"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        key_ = method.__qualname__
        self._redis.incr(key_)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs and
    outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        key_ = method.__qualname__
        in_put = key_ + ":inputs"
        out_put = key_ + ":outputs"
        data_ = str(args)
        self._redis.rpush(in_put, data_)
        final_data = method(self, *args, **kwargs)
        self._redis.rpush(out_put, str(final_data))
        return final_data
    return wrapper


class Cache:
    """ Cache Class """
    def __init__(self):
        """Initialising a Cache instance using Redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Method creates a key and stores it with data'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) ->\
            Union[str, bytes, int, float]:
        """method converts data back to the desired format"""
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key) -> int:
        """method automatically parametrizes Cache.get
        with the correct conversion function."""
        return int(self._redis.get(key))

    def get_str(self, key) -> str:
        """method automatically parametrizes Cache.get
        with the correct conversion function."""
        return str(self._redis.get(key))
