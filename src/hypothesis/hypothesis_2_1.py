import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


'''
We will plot the total amount of dengue cases (when the symptoms appeared) divided by month to give an idea which part of the year has the most cases (each year and total).
Then, we will plot a histplot with kde to observe the distribution type (each year and total).
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


def extract_month(dataframe:pd.DataFrame, column:str) -> pd.DataFrame:
    """
    Function that will extract by month to plot a histogram

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


# Choosing the columns to analyze and creating dataframes with these columns
colums_analyze = ["DT_SIN_PRI"]

# Loading the datasets and choosing the right columns
df1 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2021.csv", usecols=colums_analyze, chunksize=20000)
df2 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2022.csv", usecols=colums_analyze, chunksize=20000)
df3 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2023.csv", usecols=colums_analyze, chunksize=20000)
df4 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_2024.csv", usecols=colums_analyze, chunksize=20000)
df5 = processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_total.csv", usecols=colums_analyze, chunksize=30000)

# Extracting the month from 'DT_SIN_PRI' (begin of the symptoms) and adding it as a new column 'MESES' in each dataframe
df1["MESES"] = extract_month(df1, "DT_SIN_PRI")
df2["MESES"] = extract_month(df2, "DT_SIN_PRI")
df3["MESES"] = extract_month(df3, "DT_SIN_PRI")
df4["MESES"] = extract_month(df4, "DT_SIN_PRI")
df5["MESES"] = extract_month(df5, "DT_SIN_PRI")

# Ploting the histograms by months (each year and total)
dfs1 = [df1["MESES"], df2["MESES"], df3["MESES"], df4["MESES"]]
ano1 = 2021
for df in dfs1:
    sns.set_style("white")
    sns.histplot(df, bins=12, color='red')
    plt.title(f"CASOS DE DENGUE {ano1} (dividido por mês)")
    plt.xlabel("Mês")
    plt.ylabel("Número de ocorrências")
    plt.xticks(range(1, 13))
    plt.show()
    ano1 += 1

sns.set_style("white")
sns.histplot(df5["MESES"], bins=12, color='red')
plt.title("CASOS DE DENGUE TOTAL (dividido por mês)")
plt.xlabel("Mês")
plt.ylabel("Número de ocorrências")
plt.xticks(range(1, 13))
plt.show()

# Ploting the histograms by periods (each year and total)
dfs2 = [df1["DT_SIN_PRI"], df2["DT_SIN_PRI"], df3["DT_SIN_PRI"], df4["DT_SIN_PRI"]]
ano2 = 2021
for df in dfs2:
    sns.set_style("white")
    sns.histplot(df, kde=True, stat='count')
    plt.title(f"CASOS DE DENGUE {ano2} (detalhado)")
    plt.xlabel("Período")
    plt.ylabel("Número de ocorrências")
    plt.show()
    ano2 += 1

sns.set_style("white")
sns.histplot(df5["DT_SIN_PRI"], kde=True, stat='count')
plt.title("CASOS DE DENGUE TOTAL (detalhado)")
plt.xlabel("Período")
plt.ylabel("Número de ocorrências")
plt.show()
