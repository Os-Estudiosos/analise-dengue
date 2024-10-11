"""This module contains functions that can measure function running time"""
import time
from typing import Callable

def measure_function_execution(func: Callable):
    """This function measures the time the function passed takes to finish. This function needs to be used as a DECORATOR

    Args:
        func (function): Function to be executed

    Raises:
        TypeError: Raises if you doesn't pass a function

    Returns:
        Float: If used correctly as a decorator, it returns the passed function's execution time. (It's not supposed to return the passed function's return)
    """
    if not callable(func):
        raise TypeError('You need to pass a Function to this work')
    
    def wrapper(*args, **kwargs):
        initial_time = time.time()
        func(*args, **kwargs)
        final_time = time.time()

        print(f"O resultado foi {final_time - initial_time}")

        return final_time - initial_time
        
    return wrapper
