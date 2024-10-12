import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geoplot.crs as gcrs
from matplotlib.colors import ListedColormap


'''
First, we will plot the occurrency of dengue cases for each uf (total).
Then we will analyze the main 3 symptoms (and the least 3 symptoms) and plot a geoplot to see the occurrency of them by uf (total).
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


def main_least_symptons(filepath:str, symptoms:list) -> list:
    """
    Function that will determinate the principals dengue symptoms

    Args:
        filepath (str): Add the file path
        symptoms (list): Add the symptoms list to analyze

    Returns:
        list: Output the main five in list

    >>> main_symptons(main_symptons(filepath="analise-dengue/data/sinan_dengue_sample_total.csv", symptoms=["FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA","DOR_COSTAS","CONJUNTVIT","ARTRITE","ARTRALGIA","PETEQUIA_N","LEUCOPENIA","DOR_RETRO","DIABETES","HEMATOLOG","HEPATOPAT","RENAL","HIPERTENSA","ACIDO_PEPT","AUTO_IMUNE"])
    ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO']
    """

    # Use the function to process the total dataframe 
    df = processing_total_dataframe(filepath=filepath, usecols=symptoms, chunksize=30000)

    # Define a dictionary to keep the sympton and the total cases
    means = {}

    # Iterate to all symptoms and do a sum 
    for sympton in symptoms:
        sum = np.sum((df[sympton] == 1) | (df[sympton] == 1.0))  # Handle both int and float cases
        means[sympton] = sum
    
    # Sort to find the main five symptoms
    means_order = {k: v for k, v in sorted(means.items(), key=lambda item: item[1], reverse=True)}

    # Transforms all the keys to list and keep the first five
    first_five = list(means_order.keys())[:3]
    least_five = list(means_order.keys())[-3:]

    return [first_five, least_five]


def count_dengue_cases_by_state(filepath:str, columns:list) -> pd.DataFrame:
    """
    Function that will crate a dataframe with the total amount of dengue cases by each uf

    Args:
        filepath (str): Add the file
        columns (list): Add the columns that will be analised

    Returns:
        pd.DataFrame: Output the dataframe with the amount of dengue cases by uf

    >>> count_dengue_cases_by_state("analise-dengue/data/sinan_dengue_sample_total.csv", ["SG_UF_NOT"])
        SIGLA_UF  TOTAL_CASES
    0        AC        41442
    1        AL        48514
    2        AM        26495
    3        AP         2571
    4        BA       120112
    5        CE       126495
    6        DF       140276
    7        GO       361171
    8        MA        13379
    9        MG      1492918
    10       MS        96838
    11       MT        98158
    12       PA        20343
    13       PB        58078
    14       PE        85208
    15       PI        44156
    16       PR       452999
    17       RJ       354591
    18       RN        73626
    19       RO        33894
    20       RR         1952
    21       RS       232309
    22       SC       399293
    23       SE        14515
    24       SP      1038175
    25       TO        44380
    """
    # Load the file with the uf codes and acronyms
    cities = pd.read_csv("analise-dengue/data/ufs.csv", usecols=["SG_UF_NOT","SIGLA_UF"], low_memory=False)
    
    # Inicializing a empty list to keep the chunks
    df_list = []

    # Load the total dengue dataset 
    df_chunks = pd.read_csv(filepath, usecols=columns, low_memory=False, chunksize=30000)

    # Iterate in each chunk
    for chunk in df_chunks:
        # Mergin the data on the acronyms
        merged_data = pd.merge(chunk, cities, on="SG_UF_NOT", how="left")
        df_list.append(merged_data)

    # Concatenate all the chinks
    df_total = pd.concat(df_list, ignore_index=True)
    
    # Creating a new dataframe to keep the total dengue cases grouped by uf
    cases_by_state = df_total.groupby("SIGLA_UF").size().reset_index(name='TOTAL_CASES')

    return cases_by_state


# Defining all the symptoms in the dataframe and finding the main 5 and the least 5 symptoms
symptoms = ["FEBRE","MIALGIA","CEFALEIA","EXANTEMA","VOMITO","NAUSEA","DOR_COSTAS","CONJUNTVIT","ARTRITE","ARTRALGIA","PETEQUIA_N","LEUCOPENIA","DOR_RETRO","DIABETES","HEMATOLOG","HEPATOPAT","RENAL","HIPERTENSA","ACIDO_PEPT","AUTO_IMUNE"]
main_least_symptons = main_least_symptons(filepath="analise-dengue/data/sinan_dengue_sample_total.csv", symptoms=symptoms)
main_symptons = main_least_symptons[0]
least_symptons = main_least_symptons[1]

# Calculate the total amount of dengue cases by uf 
dengue_cases = count_dengue_cases_by_state("analise-dengue/data/sinan_dengue_sample_total.csv", ["SG_UF_NOT"])

# Reading Brazil's shapefile and merging the total dengue cases
mapa_brasil = gpd.read_file("analise-dengue/data/BR_UF_2022.shp")
mapa_brasil = mapa_brasil.merge(dengue_cases, left_on='SIGLA_UF', right_on='SIGLA_UF')

# Plotting the geoplot (total cases)
colors = ["#fee0d2", "#fcbba1", "#fb6a4a", "#cb181d","#a50f15"]
cmap_red = ListedColormap(colors)

ax = gplt.polyplot(
    mapa_brasil,
    edgecolor="white",
    facecolor="lightgray",
    figsize=(12, 8),
    projection=gcrs.PlateCarree()
)

gplt.choropleth(
    mapa_brasil,
    ax=ax,
    hue="TOTAL_CASES",
    legend=True,
    legend_kwargs={
        "frameon": False,
        "loc": "lower left",
        "fontsize":8,
        "title_fontsize":10,
        "title":"Casos de dengue"
    },
    legend_labels=["0-74.000","74.001-232.000","232.001-453.000", "453.001-1.382.000", "1.382.001-1.500.00"],
    cmap=cmap_red,  
    scheme="FisherJenks",
    projection=gcrs.PlateCarree()
)
ax.set_title("Distribuição de Casos de Dengue no Brasil (2021-2024)", fontsize=18)
plt.show()

# Plotting the geoplots (total & each main/least symptoms)