import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import geoplot.crs as gcrs
from matplotlib.colors import ListedColormap
import seaborn as sns
import os
import sys
sys.path.append(os.getcwd())
from src.config import FILES_FOLDER, OUTPUT_FOLDER, DATASET_LOCAL, CHUNKS_SIZE
from src.utils.reading import processing_partial_dataset
from src.utils.timing import extract_month
from src.utils.timing import count_dengue_cases_by_state


'''
Part 1:
Vamos plotar o total de casos de dengue dos anos 2021, 2022, 2023 e 2024 separados por mês.
Depois, vamos plotar um histograma com uma linha KDE para observar o padrão.

Part 2:
Vamos fazer uma tabela que possui o total de casos de dengue, total de óbitos e a taxa de mortalidade por estado.
Depois, vamos plotar um geoplot do Brasil com o total de casos por estado.
Por último, vamos plotar outro geoplot do Brasil, mas com as taxas de mortalidade por estado.
'''


'''PART 1'''
def hypothesis2_part1(df:pd.DataFrame):

    # Escolhendo as colunas para analisar
    colums_analyze = ["DT_SIN_PRI"]

    # Carregando os datasets com as colunas necessárias
    df1 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2021.csv'), usecols=colums_analyze, chunksize=CHUNKS_SIZE)
    df2 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2022.csv'), usecols=colums_analyze, chunksize=CHUNKS_SIZE)
    df3 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2023.csv'), usecols=colums_analyze, chunksize=CHUNKS_SIZE)
    df4 = processing_partial_dataset(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2024.csv'), usecols=colums_analyze, chunksize=CHUNKS_SIZE)

    # Extraído os meses da coluna DT_SIN_PRI e criando uma nova coluna chamada MESES
    df1 = extract_month(df1, "DT_SIN_PRI")
    df2 = extract_month(df2, "DT_SIN_PRI")
    df3 = extract_month(df3, "DT_SIN_PRI")
    df4 = extract_month(df4, "DT_SIN_PRI")
    df = extract_month(df, "DT_SIN_PRI")

    # Plotando os histogramas do total de casos de dengue de cada ano por mês
    order = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    dfs1 = [df1, df2, df3, df4]
    ano = 2021
    for data in dfs1:
        sns.set_style("white")
        sns.countplot(data=data, x="MESES", order=order, color='red', width=1)
        plt.title(f"CASOS DE DENGUE {ano} (dividido por mês)")
        plt.xlabel("Mês")
        plt.ylabel("Número de ocorrências")
        plt.show()

        # Salvando o plot na pasta output
        #plt.savefig(os.path.join(OUTPUT_FOLDER(), f"casos_dengue_{ano}.png"))
        ano +=1

    # Plotando o histograma com a linha KDE do período total para a visualização do padrão
    sns.set_style("white")
    sns.histplot(df["DT_SIN_PRI"], kde=True, stat='count')
    plt.title("CASOS DE DENGUE TOTAL (detalhado)")
    plt.xlabel("Período")
    plt.ylabel("Número de ocorrências")
    plt.show()

    # Salvando o plot na pasta output
    #plt.savefig(os.path.join(OUTPUT_FOLDER(), "casos_dengue_total.png"))


'''PART 2'''
def hypothesis2_part2(df:pd.DataFrame):

    # Fazendo a tabela com o total de casos, total de óbitos e taxa de mortalidade por cada estado 
    dengue = count_dengue_cases_by_state(df, ["SG_UF_NOT", "EVOLUCAO", "SIGLA_UF"])
    print(dengue)

    # Salvando a tabela na pasta output
    #dengue.to_csv(os.path.join(OUTPUT_FOLDER(), "tabela_por_estado.csv"), index=False)

    # Lendo o shapefile dos estados do Brasil e fazendo merge nas colunas para plotagem
    mapa_brasil = gpd.read_file(os.path.join(FILES_FOLDER(), "BR_UF_2022.shp"))
    mapa_brasil = mapa_brasil.merge(dengue, left_on='SIGLA_UF', right_on='SIGLA_UF')

    # Fazendo a coloração da legenda
    colors = ["#fee0d2", "#fcbba1", "#fb6a4a", "#cb181d","#a50f15"]
    cmap_red = ListedColormap(colors)

    # Plotando o geoplot dos casos totais por estado
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
        hue="TOTAL CASOS",
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
    ax1.set_title("CASOS TOTAIS DE DENGUE NO BRASIL (2021-2024)", fontsize=18)
    plt.show()

    # Salvando o plot na pasta output
    #plt.savefig(os.path.join(OUTPUT_FOLDER(), "geoplot_total.png"))

    # Plotando o geoplot da taxa de mortalidade por estado
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
        hue="MORTALIDADE(%)",
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
    ax2.set_title("TAXA DE MORTALIDADE DA DENGUE NO BRASIL (2021-2024)", fontsize=18)
    plt.show()
    
    # Salvando o plot na pasta output
    #plt.savefig(os.path.join(OUTPUT_FOLDER(), "geoplot_mortalidade.png"))
