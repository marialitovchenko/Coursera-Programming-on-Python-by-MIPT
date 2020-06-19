"""
Write a decorator which converts everything to JSON
"""

import json # json format
import functools

def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = json.JSONEncoder().encode(func(*args, **kwargs))
        return result 
    return wrapped
