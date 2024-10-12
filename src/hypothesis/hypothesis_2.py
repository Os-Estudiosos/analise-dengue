import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geoplot.crs as gcrs
from matplotlib.colors import ListedColormap
import seaborn as sns
import os
import sys
sys.path.append(os.getcwd())
from src.config import FILES_FOLDER, OUTPUT_FOLDER, DATASET_LOCAL
from src.utils.reading import processing_partial_dataset
from src.utils.timing import extract_month


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
    # Choosing the columns to analyze and creating dataframes with these columns
    colums_analyze = ["DT_SIN_PRI"]

    # Loading the datasets and choosing the right columns
    df1 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2021.csv'), usecols=colums_analyze, chunksize=20000)
    df2 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2022.csv'), usecols=colums_analyze, chunksize=20000)
    df3 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2023.csv'), usecols=colums_analyze, chunksize=20000)
    df4 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2024.csv'), usecols=colums_analyze, chunksize=20000)

    # Extracting the month from 'DT_SIN_PRI' (begin of the symptoms) and adding it as a new column 'MESES' in each dataframe
    df1["MESES"] = extract_month(df1, "DT_SIN_PRI")
    df2["MESES"] = extract_month(df2, "DT_SIN_PRI")
    df3["MESES"] = extract_month(df3, "DT_SIN_PRI")
    df4["MESES"] = extract_month(df4, "DT_SIN_PRI")
    df["MESES"] = extract_month(df, "DT_SIN_PRI")

    # Ploting the histograms by months (each year and total)
    dfs1 = [df1["MESES"], df2["MESES"], df3["MESES"], df4["MESES"]]
    ano1 = 2021
    for i, _df in enumerate(dfs1):
        sns.set_style("white")
        sns.histplot(_df, bins=12, color='red')
        plt.title(f"CASOS DE DENGUE {ano1} (dividido por mês)")
        plt.xlabel("Mês")
        plt.ylabel("Número de ocorrências")
        plt.xticks(range(1, 13))
        plt.savefig(os.path.join(OUTPUT_FOLDER(), f'Ocorrencia-1-{i}.png'))

        ano1 += 1

    sns.set_style("white")
    sns.histplot(df["MESES"], bins=12, color='red')
    plt.title("CASOS DE DENGUE TOTAL (dividido por mês)")
    plt.xlabel("Mês")
    plt.ylabel("Número de ocorrências")
    plt.xticks(range(1, 13))
    plt.savefig(os.path.join(OUTPUT_FOLDER(), f'Caso_De_Dengue_Por_Mes.png'))


    # Ploting the histograms by periods (each year and total)
    dfs2 = [df1["DT_SIN_PRI"], df2["DT_SIN_PRI"], df3["DT_SIN_PRI"], df4["DT_SIN_PRI"]]
    ano2 = 2021
    for i, _df in enumerate(dfs2):
        sns.set_style("white")
        sns.histplot(_df, kde=True, stat='count')
        plt.title(f"CASOS DE DENGUE {ano2} (detalhado)")
        plt.xlabel("Período")
        plt.ylabel("Número de ocorrências")
        plt.savefig(os.path.join(OUTPUT_FOLDER(), f'Ocorrencia-2-{i}.png'))
        ano2 += 1

    sns.set_style("white")
    sns.histplot(df["DT_SIN_PRI"], kde=True, stat='count')
    plt.title("CASOS DE DENGUE TOTAL (detalhado)")
    plt.xlabel("Período")
    plt.ylabel("Número de ocorrências")
    plt.savefig(os.path.join(OUTPUT_FOLDER(), 'Caso_Dengue_Total.png'))


'''PART 2'''
def count_dengue_cases_by_state(df: pd.DataFrame, columns:list) -> pd.DataFrame:
        """
        Function that will crate a dataframe with the total amount of dengue cases by each uf

        Args:
            filepath (pd.DataFrame): Dataframe that will be analysed
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
        cities = pd.read_csv(os.path.join(FILES_FOLDER(), "ufs.csv"), usecols=["SG_UF_NOT","SIGLA_UF"], low_memory=False)
        
        # Inicializing a empty list to keep the chunks
        df_list = []
        
        # Load the total dengue dataset
        df_total = df[columns]
        
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


def hypothesis2_part2(df:pd.DataFrame):
    # Calculate the total amount of dengue cases by uf 
    dengue = count_dengue_cases_by_state(df, ["SG_UF_NOT", "EVOLUCAO", "SIGLA_UF"])

    # Reading Brazil's shapefile and merging the total dengue cases
    mapa_brasil = gpd.read_file(os.path.join(FILES_FOLDER(), "BR_UF_2022.shp"))
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
    plt.savefig(os.path.join(OUTPUT_FOLDER(), 'Distribuicao_Casos_De_Dengue_Brasil.png'))

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
    plt.savefig(os.path.join(OUTPUT_FOLDER(), 'Distribuicao_Proporcoes_De_Mortes_Brasil.png'))

