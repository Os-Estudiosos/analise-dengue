import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd


'''
First, we will plot the occurrency of dengue cases for each city (total and by year).
Then we will analyze the main symptons (and the least symptons) and plot a geoplot to see the occurrency of them by city (total).
'''


def processing_total_dataframe(filepath:str, usecols:list, chunksize:int=1) -> pd.DataFrame:
    """
    Function that will process the total dataframe costing less memory

    Args:
        filepath (str): Add the file path
        usecols (list): Add a list with the columns that you will use
        chunksize (int, optional): Define the size of the chunks. Defaults to 1.

    Returns:
        pd.DataFrame: Output the final processed dataframe

    >>> processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_total.csv", usecols=colums_analyze, chunksize=30000)
    DT_SIN_PRI  FEBRE  MIALGIA  CEFALEIA  EXANTEMA  VOMITO  NAUSEA  CONJUNTVIT
    0   2021-02-20    1.0      1.0       1.0       1.0     1.0     1.0         2.0
    1   2021-02-20    1.0      2.0       1.0       1.0     2.0     2.0         1.0
    2   2021-01-12    1.0      1.0       1.0       2.0     2.0     1.0         2.0
    3   2021-01-29    1.0      2.0       1.0       2.0     2.0     1.0         2.0
    4   2021-02-26    1.0      2.0       1.0       1.0     2.0     1.0         2.0
    5   2021-02-15    1.0      1.0       1.0       1.0     1.0     2.0         1.0
    6   2021-01-27    1.0      2.0       1.0       2.0     2.0     2.0         1.0
    7   2021-02-17    1.0      2.0       1.0       2.0     2.0     1.0         2.0
    8   2021-02-05    1.0      2.0       1.0       2.0     2.0     2.0         2.0
    9   2021-03-08    1.0      2.0       1.0       2.0     2.0     1.0         2.0
    10  2021-02-15    1.0      1.0       1.0       2.0     2.0     2.0         2.0
    11  2021-03-08    1.0      1.0       1.0       1.0     2.0     2.0         2.0
    12  2021-02-15    1.0      1.0       1.0       2.0     2.0     1.0         2.0
    13  2021-01-23    1.0      1.0       1.0       2.0     2.0     1.0         1.0
    14  2021-03-25    1.0      2.0       1.0       2.0     2.0     2.0         2.0
    15  2021-03-07    1.0      1.0       1.0       2.0     2.0     1.0         2.0
    16  2021-03-05    1.0      2.0       1.0       1.0     2.0     2.0         2.0
    17  2021-01-23    1.0      1.0       1.0       2.0     2.0     2.0         1.0
    18  2021-01-15    1.0      1.0       1.0       1.0     2.0     1.0         1.0
    19  2021-01-08    2.0      2.0       1.0       2.0     2.0     1.0         2.0
    """

    # Read the dataset with chunks
    df = pd.read_csv(filepath, usecols=usecols, low_memory=False, chunksize=chunksize)

    # Set a empty list to keep the chunks
    df_list = []

    # Append each chunk in a list
    for chunk in df:
        df_list.append(chunk)

    # Concatenate the list in a dataframe
    df_total = pd.concat(df_list, ignore_index=True)

    return df_total


def main_least_symptons(filepath:str, symptons:list) -> list:
    """
    Function that will determinate the principals dengue symptons

    Args:
        filepath (str): Add the file path
        symptons (list): Add the symptons list to analyze

    Returns:
        list: Output the main five in list

    >>> main_symptons(main_symptons(filepath="analise-dengue/data/sinan_dengue_sample_total.csv", symptons=["FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA","DOR_COSTAS","CONJUNTVIT","ARTRITE","ARTRALGIA","PETEQUIA_N","LEUCOPENIA","DOR_RETRO","DIABETES","HEMATOLOG","HEPATOPAT","RENAL","HIPERTENSA","ACIDO_PEPT","AUTO_IMUNE"])
    ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO']
    """

    # Use the function to process the total dataframe 
    df = processing_total_dataframe(filepath=filepath, usecols=symptons, chunksize=30000)

    # Define a dictionary to keep the sympton and the total cases
    means = {}

    # Iterate to all symptons and do a count 
    for sympton in symptons:
        count = np.sum((df[sympton] == 1) | (df[sympton] == 1.0))  # Handle both int and float cases
        means[sympton] = count
    
    # Sort to find the main five symptons
    means_order = {k: v for k, v in sorted(means.items(), key=lambda item: item[1], reverse=True)}

    # Transforms all the keys to list and keep the first five
    first_five = list(means_order.keys())[:5]
    least_five = list(means_order.keys())[-5:]

    return [first_five, least_five]


# Define all the symptons in the dataframe
symptons = ["FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA","DOR_COSTAS","CONJUNTVIT","ARTRITE","ARTRALGIA","PETEQUIA_N","LEUCOPENIA","DOR_RETRO","DIABETES","HEMATOLOG","HEPATOPAT","RENAL","HIPERTENSA","ACIDO_PEPT","AUTO_IMUNE"]
main_symptons = main_least_symptons(filepath="analise-dengue/data/sinan_dengue_sample_total.csv", symptons=symptons)[0]
least_symptons = main_least_symptons(filepath="analise-dengue/data/sinan_dengue_sample_total.csv", symptons=symptons)[1]

# Define the columns to analyze the data
colums_analyze = ["ID_MUNICIP", "ID_AGRAVO"]
colums_analyze1 = main_least_symptons + ["ID_MUNICIP"]
colums_analyze2 = least_symptons + ["ID_MUNICIP"]

# Process the dataframes with the columns we will use to both analysis
df1 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2021.csv", usecols=colums_analyze, chunksize=20000)
df2 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2022.csv", usecols=colums_analyze, chunksize=20000)
df3 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2023.csv", usecols=colums_analyze, chunksize=20000)
df4 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2024.csv", usecols=colums_analyze, chunksize=20000)
df5 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_total.csv", usecols=colums_analyze, chunksize=30000)
df6 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_total.csv", usecols=colums_analyze1, chunksize=30000)
df7 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_total.csv", usecols=colums_analyze2, chunksize=30000)

# Plotting the geoplots
