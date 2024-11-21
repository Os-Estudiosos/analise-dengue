import os
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from src.config import *


def discover_occupation() -> list:
    """
    Carrega o arquivo 'CBO2002_Ocupacao.csv' e retorna uma lista de códigos de ocupações
    rurais, excluindo as ocupações que não agregam à hipótese de interesse.

    Retorna:
        list: Lista de códigos de ocupações rurais (strings).
    Levanta:
        FileNotFoundError: Se o arquivo 'CBO2002_Ocupacao.csv' não for encontrado.
    """
    try:
        df2_occup = pd.read_csv(os.path.join(FILES_FOLDER(), 'CBO2002_Ocupacao.csv'), encoding='ISO-8859-1', sep=';')

        # Filtra palavras chaves de ocupaçproporcoes_dengueões rurais
        keywords = ['rural', 'agri', 'pecu', 'agro']
        df2_agriculture = df2_occup[df2_occup['TITULO'].str.contains('|'.join(keywords), case=False, na=False)]

        # Desconsidera casos que não agregam à hipótese
        unwanted_keywords = ['engenheiro', 'gerente', 'administrador', 'pesquisador', 'analista', 'tec', 'téc', 'economista', 'diretor']
        df2_agriculture = df2_agriculture[~df2_agriculture['TITULO'].str.contains('|'.join(unwanted_keywords), case=False, na=False)]

        # Cria uma lista com os códigos de ocupações rurais
        list_codes_rural = df2_agriculture['CODIGO'].astype(str).tolist()

        return list_codes_rural 

    except FileNotFoundError:
        raise FileNotFoundError("Arquivo não encontrado: CBO2002_Ocupacao.csv")


def hypothesis4(df: pd.DataFrame, list_codes_rural: list) -> tuple:
    """
    Avalia a proporção de casos confirmados de dengue entre ocupações rurais e não rurais.

    Parâmetros:
        df (pd.DataFrame): DataFrame contendo os dados de casos de dengue, incluindo ocupação e resultados de exames.
        list_codes_rural (list): Lista de códigos de ocupações consideradas rurais.

    Retorna:
        tuple: Proporções de casos confirmados em ocupações não rurais e rurais.
    
    Levanta:
        RuntimeError: Em caso de erro durante o processamento.
    """
    try:
        # Remove linhas nulas na coluna de ocupação e converte para string
        df['ID_OCUPA_N'] = df['ID_OCUPA_N'].replace(['NA', 'na', ''], np.nan)
        df = df[df['ID_OCUPA_N'].notnull()]
        df['ID_OCUPA_N'] = df['ID_OCUPA_N'].astype(str)

        # Define colunas de teste
        test_columns = ['RESUL_SORO', 'RESUL_NS1', 'RESUL_VI_N', 'RESUL_PCR_', 'SOROTIPO', 'HISTOPA_N', 'IMUNOH_N']
        
        # Identifica casos confirmados e negativos
        df['dengue_confirmed'] = df[test_columns].apply(lambda row: 1 if (row == 1).any() else (2 if (row == 2).all() else np.nan), axis=1)
        df = df[df['dengue_confirmed'].notna()]

        # Filtra para ocupações rurais com casos positivos
        df_confirmed_rural = df[(df['ID_OCUPA_N'].isin(list_codes_rural)) & (df['dengue_confirmed'] == 1)]

        # Calcula proporções de casos rurais e não rurais
        total_confirmed = len(df[df['dengue_confirmed'] == 1])
        rural_confirmed = len(df_confirmed_rural)
        rural_proportion = 100 * (rural_confirmed / total_confirmed)
        total_proportion = 100 - rural_proportion
        
        return total_proportion, rural_proportion

    except Exception as e:
        raise RuntimeError(f"Erro ao processar a hipótese: {e}")
