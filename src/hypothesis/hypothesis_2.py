import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geoplot.crs as gcrs
from matplotlib.colors import ListedColormap
import seaborn as sns


'''
Part 1:
We will plot the total amount of dengue cases (when the symptoms appeared) divided by month to give an idea which part of the year has the most cases (each year and total).
Then, we will plot a histplot with kde to observe the distribution type (each year and total).

Part 2:
First, we will plot the occurrency of dengue cases for each uf (total).
Then we will analyze the proportion of death in each uf (total).
'''


'''PART 1'''
def hypothesis2_part1(df:pd.DataFrame):

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


'''PART 2'''
def hypothesis2_part2(df:pd.DataFrame):
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


    def count_dengue_cases_by_state(filepath:str, columns:list) -> pd.DataFrame:
        """
        Function that will crate a dataframe with the total amount of dengue cases by each uf

        Args:
            filepath (str): Add the file
            columns (list): Add the columns that will be analised

        Returns:
            pd.DataFrame: Output the dataframe with the uf acronym and total cases, total deaths and proportion (total deaths/total cases) by uf

        >>> count_dengue_cases_by_state("analise-dengue/data/sinan_dengue_sample_total.csv", ["SG_UF_NOT","EVOLUCAO"])
            SIGLA_UF  TOTAL_CASES  TOTAL_DEATHS  PROPORCION
        0        AC        41442           9.0    0.021717
        1        AL        48514          21.0    0.043286
        2        AM        26495          32.0    0.120778
        3        AP         2571           0.0    0.000000
        4        BA       120112          73.0    0.060777
        5        CE       126495          50.0    0.039527
        6        DF       140276          48.0    0.034218
        7        GO       361171         256.0    0.070881
        8        MA        13379          23.0    0.171911
        9        MG      1492918         825.0    0.055261
        10       MS        96838          80.0    0.082612
        11       MT        98158          53.0    0.053995
        12       PA        20343           8.0    0.039326
        13       PB        58078          19.0    0.032715
        14       PE        85208          15.0    0.017604
        15       PI        44156          19.0    0.043029
        16       PR       452999         275.0    0.060707
        17       RJ       354591         271.0    0.076426
        18       RN        73626          27.0    0.036672
        19       RO        33894          30.0    0.088511
        20       RR         1952           2.0    0.102459
        21       RS       232309         290.0    0.124834
        22       SC       399293         301.0    0.075383
        23       SE        14515          27.0    0.186014
        24       SP      1038175         660.0    0.063573
        25       TO        44380          22.0    0.049572
        """
        # Load the file with the uf codes and acronyms
        cities = pd.read_csv("analise-dengue/files/ufs.csv", usecols=["SG_UF_NOT","SIGLA_UF"], low_memory=False)
        
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

        # Creating a new dataframe to keep the total dengue deaths grouped by uf
        deaths_by_state = df_total[df_total["EVOLUCAO"].isin([2, 2.0])]
        deaths_by_state = deaths_by_state.groupby("SIGLA_UF").size().reset_index(name='TOTAL_DEATHS')

        # Mergin both dataframes
        df = pd.merge(cases_by_state, deaths_by_state, on="SIGLA_UF", how="left")

        # replacing de NaN values to 0
        df['TOTAL_DEATHS'] = df['TOTAL_DEATHS'].fillna(0)
        df['TOTAL_CASES'] = df['TOTAL_CASES'].fillna(0)

        # MAking the proportion
        df["PROPORTION"] = df["TOTAL_DEATHS"]/df["TOTAL_CASES"]*100

        return df


    # Calculate the total amount of dengue cases by uf 
    dengue = count_dengue_cases_by_state("analise-dengue/data/sinan_dengue_sample_total.csv", ["SG_UF_NOT", "EVOLUCAO"])

    # Reading Brazil's shapefile and merging the total dengue cases
    mapa_brasil = gpd.read_file("analise-dengue/files/BR_UF_2022.shp")
    mapa_brasil = mapa_brasil.merge(dengue, left_on='SIGLA_UF', right_on='SIGLA_UF')

    # Making a new colormap
    colors = ["#fee0d2", "#fcbba1", "#fb6a4a", "#cb181d","#a50f15"]
    cmap_red = ListedColormap(colors)

    # Plotting the geoplot (total cases by uf)
    ax1 = gplt.polyplot(
        mapa_brasil,
        edgecolor="black",
        facecolor="lightgray",
        figsize=(12, 8),
        projection=gcrs.PlateCarree()
    )

    gplt.choropleth(
        mapa_brasil,
        ax=ax1,
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
    ax1.set_title("Distribuição de Casos de Dengue no Brasil (2021-2024)", fontsize=18)
    plt.show()

    # Plotting the geoplot (proportion of deaths by uf)
    ax2 = gplt.polyplot(
        mapa_brasil,
        edgecolor="black",
        facecolor="lightgray",
        figsize=(12, 8),
        projection=gcrs.PlateCarree()
    )

    gplt.choropleth(
        mapa_brasil,
        ax=ax2,
        hue="PROPORTION",
        legend=True,
        legend_kwargs={
            "frameon": False,
            "loc": "lower left",
            "fontsize":8,
            "title_fontsize":10,
            "title":"Proporção"
        },
        legend_labels=["0% - 0,022%","0,0221% - 0,056%","0,0561% - 0,0886%", "0,08861% - 0,125%", "0,1251% - 0,187%"],
        cmap=cmap_red,  
        scheme="FisherJenks",
        projection=gcrs.PlateCarree()
    )
    ax2.set_title("Distribuição das proporções de mortes no Brasil (2021-2024)", fontsize=18)
    plt.show()