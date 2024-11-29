"""Módulo que contém funções úteis de estatística"""
import pandas as pd
import numpy as np

# Create this function to filter the most taken exam
def top_3_counts_numpy(df: pd.DataFrame, columns: list|str) -> list[tuple]:
    """Analyzes the DataFrame to identify the top 3 most taken exams based on non-null values.
    Args:
        df (pd.DataFrame): The DataFrame containing the exam data.
        columns (list | str): A list of column names to compare for counting non-null values.

    Raises:
        TypeError: Raises if there is a missing column in the Dataframe

    Returns:
        list[tuple]: A list of tuples, each containing the column name and its respective count of non-null values, representing the top 3 most taken exams
    """
    # Check if the provided columns are valid
    for col in columns:
        if col not in df.columns:
            raise TypeError(f"Missing column in DataFrame: {col}")

    counts = {}
    # Loop over each column and count non-null values using NumPy
    for col in columns:
        # Convert the column to a NumPy array and count non-nan values
        column_data = df[col].to_numpy()
        counts[col] = np.count_nonzero(~pd.isna(column_data))
    
    # Sort the counts dictionary by values (counts) in descending order and return the top 3
    top_3 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return top_3
