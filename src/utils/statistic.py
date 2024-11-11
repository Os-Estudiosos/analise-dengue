"""Módulo que contém funções úteis de estatística"""
import pandas as pd
import numpy as np
from math import sqrt

def chi_square_test(qualitative_variable_1: pd.Series, qualitative_variable_2: pd.Series) -> float:
    """Receive two pandas Series, and calculate the Square Chi test between them

    Args:
        qualitative_variable_1 (pd.Series): First Series
        qualitative_variable_2 (pd.Series): Second Series

    Raises:
        TypeError: Raises when the arguments are not Pandas Series

    Returns:
        float: Chi Square Result
    """
    # Checking the args types
    if not isinstance(qualitative_variable_1, pd.Series) or not isinstance(qualitative_variable_2, pd.Series):
        raise TypeError("Os argumentos passados não são Séries Pandas")

    cross_table = pd.crosstab(qualitative_variable_1, qualitative_variable_2, margins=True)

    # Creating the frequency table
    frequency_row = np.ndarray((1,len(cross_table.columns)), dtype=float)
    
    for i, element in enumerate(cross_table.loc['All']):
        frequency_row[0,i] = element/cross_table.loc['All', 'All']

    # Creating the Expected Values table
    expected_values = pd.DataFrame(index=cross_table.index, columns=cross_table.columns, dtype=pd.Float64Dtype())
    
    # Putting the expected value in each IJ entry of the expected value's table
    for row in cross_table.index:
        for i_column, column in enumerate(cross_table.columns):
            if column == 'All':
                expected_values.loc[row, column] = expected_values.loc[row].sum()
                continue
            expected_values.loc[row, column] = cross_table.loc[row, 'All']*frequency_row[0, i_column] 

    # Creating the table of the values differences
    difference_table = pd.DataFrame(index=cross_table.index, columns=cross_table.columns, dtype=pd.Float64Dtype())
    for column in difference_table.columns:
        difference_table[column] = ((cross_table[column] - expected_values[column])**2)/expected_values[column]

    # Calculating the Chi Square
    qui_quadrado = 0
    for row in difference_table.iloc:
        qui_quadrado += row.sum()

    return qui_quadrado


def crammer_V(qualitative_variable_1: pd.Series, qualitative_variable_2: pd.Series) -> float:
    """Calculates Crammer's V

    Args:
        qualitative_variable_1 (pd.Series): Series 1
        qualitative_variable_2 (pd.Series): Series 2

    Raises:
        TypeError: Raises if the args are not Pandas Series

    Returns:
        float: Crammer's V
    """
    if not isinstance(qualitative_variable_1, pd.Series) or not isinstance(qualitative_variable_2, pd.Series):
        raise TypeError
    
    qui_quadrado = chi_square_test(qualitative_variable_1, qualitative_variable_2)

    cross_table = pd.crosstab(qualitative_variable_1, qualitative_variable_2, margins=True)

    n = cross_table.loc['All', 'All']
    r = len(cross_table.index)-1
    s = len(cross_table.columns)-1

    return sqrt((qui_quadrado)/(n*min(r-1, s-1)))


def contigency_coefficient(qualitative_variable_1: pd.Series, qualitative_variable_2: pd.Series) -> float:
    """Calculates the Coeficient Contigency

    Args:
        qualitative_variable_1 (pd.Series): Serie 1
        qualitative_variable_2 (pd.Series): Serie 2

    Raises:
        TypeError: Raises when the args are not Pandas Series

    Returns:
        float: Contigency Coefficient
    """
    # Checando os tipos das variáveis
    if not isinstance(qualitative_variable_1, pd.Series) or not isinstance(qualitative_variable_2, pd.Series):
        raise TypeError("Os argumentos passados não são Séries Pandas")
    
    qui_quadrado = chi_square_test(qualitative_variable_1, qualitative_variable_2)

    cross_table = pd.crosstab(qualitative_variable_1, qualitative_variable_2, margins=True)

    n = cross_table.loc['All', 'All']
    r = len(cross_table.index)-1
    s = len(cross_table.columns)-1

    return sqrt(qui_quadrado/(qui_quadrado+n))


def n_sets_mean(sets: set[pd.Series|list|tuple|set]):
    ...

def calculate_semi_variance(df: pd.DataFrame, quantitative_variable: str, quanlitative_variable: str = None) -> dict:
    """Essa função é responsável por calcular uma 'Semi-Variância', que será posteriormente utilizada no cálculo da variância de todo um conjunto

    Args:
        df (pd.DataFrame): Dataframe contendo as variáveis
        quantitative_variable (str): Variável quantitativa que vai ter a 'Semi-Variância' calculada
        qualitative_variable (str, optional): Variável qualitativa que restringe a variável quantitativa. Defaults to None.

    Raises:
        TypeError: _description_

    Returns:
        (dict): Dicionário contendo as informações que vou utilizar para calcular a variância total
    """




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
