"""This module contains functions that can measure function running time"""
import time
from typing import Callable
import pandas as pd

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


def extract_month(dataframe:pd.DataFrame, column:str) -> pd.DataFrame:
    """Function that will extract by month to plot a histogram

    Args:
        dataframe (pd.DataFrame): Input the dataframe you'll be using
        column (str): Input the column that tou want to extract by month

    Returns:
        pd.DataFrame: Output a dataframe extracted by month to plot a histogram

    >>> extract_month(df1, "DT_SIN_PRI")
        0           2.0
        1           2.0
        2           1.0
        3           1.0
        4           2.0
                ...
        1010354    12.0
        1010355    12.0
        1010356    12.0
        1010357    11.0
        1010358    12.0
    """
    # Convert the column to datetime (if not already)
    dataframe[column] = pd.to_datetime(dataframe.loc[:, column], errors='coerce')
    return dataframe.loc[:, column].dt.month
