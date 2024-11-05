"""This module contains functions that can measure function running time"""
import time
from typing import Callable
import pandas as pd
import os
from src.config import *

def measure_function_execution(func: Callable):
    """This function measures the time the function passed takes to finish. This function needs to be used as a DECORATOR

    Args:
        func (function): Function to be executed

    Raises:
        TypeError: Raises if you doesn't pass a function

    Returns:
        Float: If used correctly as a decorator, it returns the passed function's execution time. (It's not supposed to return the passed function's return)
    """
    if not callable(func):
        raise TypeError('You need to pass a Function to this work')
    
    def wrapper(*args, **kwargs):
        initial_time = time.time()
        func(*args, **kwargs)
        final_time = time.time()

        print(f"O resultado foi {final_time - initial_time}")

        return final_time - initial_time
        
    return wrapper


def extract_month(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Função que irá extrair os meses dos casos de dengue (início dos sintomas) (função específica)

    Args:
        dataframe (pd.DataFrame): O dataframe que estamos usando
        column (str): A coluna que usaremos para extrair os meses

    Returns:
        pd.DataFrame: Um dataframe que terá os meses extraídos

    >>> extract_month(df1, "DT_SIN_PRI")
        0           Fev
        1           Fev
        2           Jan
        3           Jan
        4           Fev
                ...
        1010354    Dez
        1010355    Dez
        1010356    Dez
        1010357    Nov
        1010358    Dez
    """
    # Converto a coluna para datetime, se não o estiver
    dataframe[column] = pd.to_datetime(dataframe.loc[:, column], errors='coerce')
    
    # Extraio o mês e crio uma nova coluna com eles
    dataframe["MESES"] = dataframe.loc[:, column].dt.month

    # Troco os valores pelas abreviações dos meses
    dataframe["MESES"] = dataframe["MESES"].replace({
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 
        6: "Jun", 7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 
        11: "Nov", 12: "Dez"
    })

    # Define a ordem desejada dos meses
    order = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    # Transforma a coluna "MESES" em uma categoria com ordem definida
    dataframe["MESES"] = pd.Categorical(dataframe["MESES"], categories=order, ordered=True)    
    return dataframe

def count_dengue_cases_by_state(df: pd.DataFrame, columns:list) -> pd.DataFrame:
        """
        Função que irá criar um dataframe com o total de casos, total de óbitos e taxa de mortalidade de cada estado (função específica)

        Args:
            filepath (pd.DataFrame): Dataframe que será analisado
            columns (list): Adiciono as colunas que contêm os dados

        Returns:
            pd.DataFrame: Dataframe com o total de casos, total de óbitos e taxa de mortalidade de cada estado

        >>> count_dengue_cases_by_state("analise-dengue/data/sinan_dengue_sample_total.csv", ["SG_UF_NOT","EVOLUCAO"])
            SIGLA_UF  TOTAL CASOS  TOTAL ÓBITOS  MORTALIDADE(%)
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
        
        # Carrego apenas as colunas utilizadas
        df_total = df[columns]
        
        # Criando um novo dataframe com os casos totais de dengue por estado
        cases_by_state = df_total.groupby("SIGLA_UF").size().reset_index(name='TOTAL CASOS')

        # Criando um novo dataframe com o total de óbitos por estado
        deaths_by_state = df_total[df_total["EVOLUCAO"].isin([2, 2.0])]
        deaths_by_state = deaths_by_state.groupby("SIGLA_UF").size().reset_index(name='TOTAL ÓBITOS')

        # Fazendo o merge de ambos os dataframe
        df = pd.merge(cases_by_state, deaths_by_state, on="SIGLA_UF", how="left")

        # Substituíndo os valores vazios por 0
        df['TOTAL ÓBITOS'] = df['TOTAL ÓBITOS'].fillna(0)
        df['TOTAL CASOS'] = df['TOTAL CASOS'].fillna(0)

        # Criando a coluna da taxa de mortalidade
        df["MORTALIDADE(%)"] = df["TOTAL ÓBITOS"]/df["TOTAL CASOS"]*100

        return df
