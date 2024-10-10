import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Fazer o histograma separado por mês no fundo (ax) e depois os kdeplots de cada ano por cima com hue ativado
'''
We will plot the total amount of dengue cases (when the symptons appeared) divided by month to give an idea which part of the year has the most cases (each year).
Then, we will plot a histplot with kde to observe the distribution type (each year).
Now to relate the symptons, we will plot a PairGrid
'''


'''BY TIME'''

def processing_total_dataset(filepath:str, usecols:list, chunksize:int):
    return pd.read_csv(filepath, usecols=usecols, low_memory=False, chunksize=chunksize)

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
colums_analyze = ["DT_SIN_PRI","FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA","DOR_COSTAS","CONJUNTVIT"]

# Loading the datasets and choosing the right columns
# df1 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2021.csv", low_memory=False, usecols=colums_analyze)
# df2 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2022.csv", low_memory=False, usecols=colums_analyze)
# df3 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2023.csv", low_memory=False, usecols=colums_analyze)
# df4 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2024.csv", low_memory=False, usecols=colums_analyze)
df_total = processing_total_dataset("analise-dengue/data/sinan_dengue_sample_total.csv", colums_analyze, 30000)


# Extracting the month from 'DT_SIN_PRI' (begin of the symptons) and adding it as a new column 'MESES' in each dataframe
# df1["MESES"] = extract_month(df1, "DT_SIN_PRI")
# df2["MESES"] = extract_month(df2, "DT_SIN_PRI")
# df3["MESES"] = extract_month(df3, "DT_SIN_PRI")
# df4["MESES"] = extract_month(df4, "DT_SIN_PRI")


# Ploting the histograms by months (each year)
# sns.set_style("white")
# sns.histplot(df1["MESES"], bins=12, color='red')
# plt.title("CASOS DE DENGUE 2021 (dividido por mês)")
# plt.xlabel("Mês")
# plt.ylabel("Número de ocorrências")
# plt.xticks(range(1, 13))
# plt.show()

# sns.set_style("white")
# sns.histplot(df2["MESES"], bins=12, color='red')
# plt.title("CASOS DE DENGUE 2022 (dividido por mês)")
# plt.xlabel("Mês")
# plt.ylabel("Número de ocorrências")
# plt.xticks(range(1, 13))
# plt.show()

# sns.set_style("white")
# sns.histplot(df3["MESES"], bins=12, color='red')
# plt.title("CASOS DE DENGUE 2023 (dividido por mês)")
# plt.xlabel("Mês")
# plt.ylabel("Número de ocorrências")
# plt.xticks(range(1, 13))
# plt.show()

# sns.set_style("white")
# sns.histplot(df4["MESES"], bins=12, color='red')
# plt.title("CASOS DE DENGUE 2024 (dividido por mês)")
# plt.xlabel("Mês")
# plt.ylabel("Número de ocorrências")
# plt.xticks(range(1, 13))
# plt.show()


# # Ploting the histograms by periods (each year)
# sns.set_style("white")
# sns.histplot(df1["DT_SIN_PRI"], kde=True, stat='count')
# plt.title("CASOS DE DENGUE 2021 (detalhado)")
# plt.xlabel("Período")
# plt.ylabel("Número de ocorrências")
# plt.show()

# sns.set_style("white")
# sns.histplot(df2["DT_SIN_PRI"], kde=True, stat='count')
# plt.title("CASOS DE DENGUE 2022 (detalhado)")
# plt.xlabel("Período")
# plt.ylabel("Número de ocorrências")
# plt.show()

# sns.set_style("white")
# sns.histplot(df3["DT_SIN_PRI"], kde=True, stat='count')
# plt.title("CASOS DE DENGUE 2023 (detalhado)")
# plt.xlabel("Período")
# plt.ylabel("Número de ocorrências")
# plt.show()

# sns.set_style("white")
# sns.histplot(df4["DT_SIN_PRI"], kde=True, stat='count')
# plt.title("CASOS DE DENGUE 2024 (detalhado)")
# plt.xlabel("Período")
# plt.ylabel("Número de ocorrências")
# plt.show()

'''BY SYMPTOM'''
sns.set_style("darkgrid")
g = sns.PairGrid(df_total)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)  
plt.show()
