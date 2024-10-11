import numpy as np
import pandas as pd
from typing import Tuple


# Expandir o DataFrame para a largura total da tela
pd.set_option('display.expand_frame_repr', False)

def discover_occupation() -> pd.DataFrame:
    """
    Filtra ocupações rurais a partir de um arquivo CSV contendo a Classificação Brasileira de Ocupações (CBO).

    Returns:
        pd.DataFrame: Um DataFrame contendo as ocupações rurais após aplicar os filtros.
    """
    path_occupation_csv = 'src/utils/CBO2002_Ocupacao.csv'
    
    # Lê o arquivo de ocupações
    df2_occup = pd.read_csv(path_occupation_csv, encoding='ISO-8859-1', sep=';')

    # Filtra por termos relacionados ao meio rural
    keywords = ['rural', 'agri', 'pecu', 'agro']
    df2_agriculture = df2_occup[df2_occup['TITULO'].str.contains('|'.join(keywords), case=False, na=False)]

    # Elimina ocupações relacionadas a áreas de gestão e pesquisa
    unwanted_keywords = ['engenheiro', 'gerente', 'administrador', 'pesquisador', 'analista', 'tec', 'téc', 'economista', 'diretor']
    df2_agriculture = df2_agriculture[~df2_agriculture['TITULO'].str.contains('|'.join(unwanted_keywords), case=False, na=False)]
    
    return df2_agriculture


def hypothesis4(df: pd.DataFrame, df2_agriculture: pd.DataFrame) -> Tuple[float, float, float]:
    """
    Realiza análise de hipóteses para verificar a frequência de ocupações rurais e não rurais
    entre os pacientes, além de calcular o teste de qui-quadrado.

    Args:
        df (pd.DataFrame): DataFrame contendo dados dos casos de dengue, com colunas relevantes.
        df2_agriculture (pd.DataFrame): DataFrame contendo ocupações rurais filtradas.

    Returns:
        Tuple[float, float, float]: Média de razões das ocupações gerais, média das ocupações rurais, valor do teste qui-quadrado.
    """

    df['ID_OCUPA_N'] = df['ID_OCUPA_N'].replace(['NA', 'na', ''], np.nan)
    df = df[df['ID_OCUPA_N'].notnull()]

    # Conta a frequência das ocupações
    count_occup_freq = df['ID_OCUPA_N'].value_counts()

    # Faz a razão de cada frequência das ocupações pelo total
    total = count_occup_freq.sum()
    reasons = count_occup_freq / total

    # Soma todas razões e calcula a média
    reasons_sum = reasons.sum()  
    reasons_average = reasons_sum / len(reasons)

    # Cria uma lista com os códigos de ocupações rurais
    df2_agriculture_ids = df2_agriculture['CODIGO']
    list_codes_rural = [str(cod) for cod in df2_agriculture_ids.values]

    # Conta a frequência das ocupações rurais
    df_filtered_codes_rural = df[df['ID_OCUPA_N'].isin(list_codes_rural)]
    count_occup_freq_rural = df_filtered_codes_rural['ID_OCUPA_N'].value_counts()

    # Faz a razão de cada frequência das ocupações rurais pelo total
    total_rural = count_occup_freq_rural.sum()
    reasons_rural = count_occup_freq_rural / total_rural

    # Soma todas razões e calcula a média
    reasons_rural_sum = reasons_rural.sum()
    reasons_rural_average = reasons_rural_sum / len(reasons_rural)

    def verify_chi_square(df: pd.DataFrame, list_codes_rural: list) -> float:
        """
        Calcula o teste de qui-quadrado entre ocupações rurais e os resultados de exames de dengue.

        Args:
            df (pd.DataFrame): DataFrame contendo os resultados de testes de dengue e ocupações.
            list_codes_rural (list): Lista com os códigos de ocupações rurais.

        Returns:
            float: Valor calculado do teste de qui-quadrado.
        """

        results = [
            'RESUL_SORO',
            'RESUL_NS1',
            'RESUL_VI_N',
            'RESUL_PCR_',
            'SOROTIPO',
            'HISTOPA_N',
            'IMUNOH_N',
        ]

        df.loc[:, results] = df[results].replace(['NA', 'na', ''], np.nan)

        # Filtra linhas que têm pelo menos uma coluna válida
        df_filtered = df[df[results].isin(['1', '2']).any(axis=1)]

        # Pessoas que positivaram em algum teste, que tiveram Dengue
        df_positive = df_filtered[df_filtered[results].isin(['1']).any(axis=1)]  

        # Pessoas que negativaram em algum teste, que não tiveram Dengue
        df_negative = df_filtered[df_filtered[results].isin(['2']).any(axis=1)]  

        df_positive_rural = df_positive[df_positive['ID_OCUPA_N'].isin(list_codes_rural)]
        df_positive_others = df_positive[~df_positive['ID_OCUPA_N'].isin(list_codes_rural)]    
        df_negative_rural = df_negative[df_negative['ID_OCUPA_N'].isin(list_codes_rural)]
        df_negative_others = df_negative[~df_negative['ID_OCUPA_N'].isin(list_codes_rural)]

        a = len(df_positive_rural)  # Positivos rurais
        b = len(df_negative_rural)  # Negativos rurais
        c = len(df_positive_others) # Positivos não rurais
        d = len(df_negative_others) # Negativos não rurais

        n = a + b + c + d

        total_line1 = a + b  # Total rurais
        total_line2 = c + d  # Total não rurais
        total_col1 = a + c   # Total positivos
        total_col2 = b + d   # Total negativos

        # Calcula os esperados
        E_a = (total_line1 * total_col1) / n
        E_b = (total_line1 * total_col2) / n
        E_c = (total_line2 * total_col1) / n
        E_d = (total_line2 * total_col2) / n

        # Calcula o somatório dos qui-quadrados
        chi_square = ((a - E_a) ** 2) / E_a + \
                     ((b - E_b) ** 2) / E_b + \
                     ((c - E_c) ** 2) / E_c + \
                     ((d - E_d) ** 2) / E_d

        return chi_square

    chi_square = verify_chi_square(df, list_codes_rural)

    return reasons_average, reasons_rural_average, chi_square


# Simula parâmetros para serem mandados para as funções
usecols = [
    'ID_OCUPA_N',
    'DOENCA_TRA',
    'RESUL_SORO',
    'RESUL_NS1',
    'RESUL_VI_N',
    'RESUL_PCR_',
    'SOROTIPO',
    'HISTOPA_N',
    'IMUNOH_N',
]
dtype = {
    'ID_OCUPA_N': 'str',
    'DOENCA_TRA': 'str',
    'RESUL_SORO': 'str',
    'RESUL_NS1': 'str',
    'RESUL_VI_N': 'str',
    'RESUL_PCR_': 'str',
    'SOROTIPO': 'str',
    'HISTOPA_N': 'str',
    'IMUNOH_N': 'str'
}
path_csv = 'data/sinan_dengue_sample_complete.csv'
df = pd.read_csv(path_csv, usecols=usecols, dtype=dtype)

print(hypothesis4(df, discover_occupation()))
