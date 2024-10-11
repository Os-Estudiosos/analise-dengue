import pandas as pd
import os
import sys
sys.path.append(os.getcwd())
from src.config import REQUIRED_COLUMNS

def filter_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Function responsible for filtering the complete dataframe and get only the required columns mentioned in the CONFIG file
    
    Args:
        df (pd.DataFrame): Dataframe that will be filtered

    Raises:
        ValueError: Raised if the dataframe doesn't have any column required in the config file

    Returns:
        pd.DataFrame: The filtered dataframe
    """
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            raise ValueError('The passed dataframe doesn\'t have all the required columns mentioned in the config')
    
    return df[REQUIRED_COLUMNS]