import numpy as np
import pandas as pd


def generate_random_dataframe(rows=10, cols=5) -> pd.DataFrame:
    """Function to generate random datasets

    Args:
        rows (int, optional): How many rows. Defaults to 10.
        cols (int, optional): How many columns. Defaults to 5.
        random_seed (float, optional): Seed for random function. Defaults to 42.

    Returns:
        pd.Dataframe: Random Dataframe
    """
    data = {}
    for i in range(cols):
        col_type = np.random.choice(['numeric', 'string', 'mixed'])
        if col_type == 'numeric':
            data[f'col_{i+1}'] = np.random.choice([np.nan, *np.random.randn(rows)], size=rows)
        elif col_type == 'string':
            data[f'col_{i+1}'] = np.random.choice([np.nan, *['a', 'b', 'c', 'd']], size=rows)
        else:
            mixed_data = np.random.choice([np.nan, *np.random.randn(rows), *['a', 'b', 'c', 'd']], size=rows)
            data[f'col_{i+1}'] = mixed_data
    
    return pd.DataFrame(data)
