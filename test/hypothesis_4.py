import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math as mt
from typing import Tuple, List

# Expandir o DataFrame para a largura total da tela
pd.set_option('display.expand_frame_repr', False)

def discover_occupation() -> pd.DataFrame:
    """
    Descobre as ocupações rurais filtrando um CSV baseado em palavras-chave relacionadas ao campo rural.

    Returns:
        pd.DataFrame: DataFrame filtrado contendo apenas ocupações rurais de interesse.
    """
    try:
        path_occupation_csv = 'files/CBO2002_Ocupacao.csv'
        df2_occup = pd.read_csv(path_occupation_csv, encoding='ISO-8859-1', sep=';')

        # Filtra por termos relacionados ao meio rural
        keywords = ['rural', 'agri', 'pecu', 'agro']
        df2_agriculture = df2_occup[df2_occup['TITULO'].str.contains('|'.join(keywords), case=False, na=False)]

        # Elimina ocupações que não contribuem para a hipótese
        unwanted_keywords = ['engenheiro', 'gerente', 'administrador', 'pesquisador', 'analista', 'tec', 'téc', 'economista', 'diretor']
        df2_agriculture = df2_agriculture[~df2_agriculture['TITULO'].str.contains('|'.join(unwanted_keywords), case=False, na=False)]

        return df2_agriculture

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {path_occupation_csv}")
    except Exception as e:
        raise RuntimeError(f"Erro ao processar o arquivo: {e}")

def hypothesis4(df: pd.DataFrame, df2_agriculture: pd.DataFrame) -> Tuple[float, float, float, float]:
    """
    Valida a hipótese de correlação entre ocupações rurais e infecção por dengue.

    Args:
        df (pd.DataFrame): DataFrame principal contendo informações dos pacientes.
        df2_agriculture (pd.DataFrame): DataFrame com ocupações rurais.

    Returns:
        Tuple[float, float, float, float]: Média das proporções gerais, média das proporções rurais, valor do qui-quadrado e coeficiente de contingência.
    """
    try:
        df['ID_OCUPA_N'] = df['ID_OCUPA_N'].replace(['NA', 'na', ''], np.nan)
        df = df[df['ID_OCUPA_N'].notnull()]

        count_occup_freq = df['ID_OCUPA_N'].value_counts()
        total = count_occup_freq.sum()
        reasons = count_occup_freq / total

        reasons_sum = reasons.sum()  
        reasons_average = reasons_sum / len(reasons)

        # Cria uma lista com os códigos de ocupações rurais
        list_codes_rural = df2_agriculture['CODIGO'].astype(str).tolist()

        df_filtered_codes_rural = df[df['ID_OCUPA_N'].isin(list_codes_rural)]
        count_occup_freq_rural = df_filtered_codes_rural['ID_OCUPA_N'].value_counts()

        total_rural = count_occup_freq_rural.sum()
        reasons_rural = count_occup_freq_rural / total

        reasons_rural_sum = reasons_rural.sum()
        reasons_rural_averge = reasons_rural_sum / len(reasons_rural)

        def verify_chi_square(df: pd.DataFrame, list_codes_rural: List[str]) -> Tuple[float, int]:
            """
            Calcula o valor do qui-quadrado para as ocupações rurais e não rurais com base nos resultados dos testes de dengue.

            Args:
                df (pd.DataFrame): DataFrame principal com informações dos pacientes.
                list_codes_rural (List[str]): Lista com códigos de ocupações rurais.

            Returns:
                Tuple[float, int]: Valor do qui-quadrado e número total de amostras.
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
            df_filtered = df[df[results].isin(['1', '2']).any(axis=1)]

            df_positive = df_filtered[df_filtered[results].isin(['1']).any(axis=1)]  
            df_negative = df_filtered[df_filtered[results].isin(['2']).any(axis=1)]  

            df_positive_rural = df_positive[df_positive['ID_OCUPA_N'].isin(list_codes_rural)]
            df_positive_others = df_positive[~df_positive['ID_OCUPA_N'].isin(list_codes_rural)]    
            df_negative_rural = df_negative[df_negative['ID_OCUPA_N'].isin(list_codes_rural)]
            df_negative_others = df_negative[~df_negative['ID_OCUPA_N'].isin(list_codes_rural)]

            a = len(df_positive_rural)
            b = len(df_negative_rural)
            c = len(df_positive_others)
            d = len(df_negative_others)

            n = a + b + c + d

            total_line1 = a + b
            total_line2 = c + d
            total_col1 = a + c
            total_col2 = b + d

            # Calcula os esperados
            E_a = (total_line1 * total_col1) / n
            E_b = (total_line1 * total_col2) / n
            E_c = (total_line2 * total_col1) / n
            E_d = (total_line2 * total_col2) / n

            chi_square = ((a - E_a) ** 2) / E_a + \
                         ((b - E_b) ** 2) / E_b + \
                         ((c - E_c) ** 2) / E_c + \
                         ((d - E_d) ** 2) / E_d

            return (chi_square, n)

        def verify_contingency_coefficient(infos: Tuple[float, int]) -> float:
            """
            Calcula o coeficiente de contingência baseado no valor do qui-quadrado.

            Args:
                infos (Tuple[float, int]): Valor do qui-quadrado e número total de amostras.

            Returns:
                float: Coeficiente de contingência.
            """
            chi_square = infos[0]
            n = infos[1]
            con_coe = mt.sqrt(chi_square / (chi_square + n))

            return con_coe

        infos = verify_chi_square(df, list_codes_rural)
        con_coe = verify_contingency_coefficient(infos)
        chi_square = infos[0]

        return (reasons_average, reasons_rural_averge, chi_square, con_coe)

    except Exception as e:
        raise RuntimeError(f"Erro ao processar a hipótese: {e}")

def test_plot_temp(reasons):

    reasons_average = reasons[0] 
    reasons_rural_average = reasons[1]

    data = {
        'Categoria': ['Outras ocupações', 'Ocupações Rurais'],
        'Proporção dos casos': [reasons_average, reasons_rural_average]
    }

    df_plot = pd.DataFrame(data)

    sns.barplot(x='Categoria', y='Proporção dos casos', data=df_plot)

    plt.title('Comparação dos casos possíveis de dengue, trabalhadores rurais X gerais')
    plt.ylabel('Proporção dos casos')
    plt.xlabel('Categoria')

    plt.show()


# Simula os parâmetros que serão passados para a função #####################
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

test_plot_temp(hypothesis4(df, discover_occupation()))