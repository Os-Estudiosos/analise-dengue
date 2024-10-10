import numpy as np
import pandas as pd
import seaborn as sb

def discover_occupation():

    path_occupation_csv = 'src/utils/CBO2002_Ocupacao.csv'

    df_occup = pd.read_csv(path_occupation_csv, encoding='ISO-8859-1', sep=';')

    # Filtra por termos relacionados ao meio rural
    keywords = ['rural', 'agri', 'pecu', 'agro']
    df_agriculture = df_occup[df_occup['TITULO'].str.contains('|'.join(keywords), case=False, na=False)]

    # Elimina ocupações relacionadas a área mas que não contribuem para hipótese
    unwanted_keywords = ['engenheiro', 'gerente', 'administrador', 'pesquisador', 'analista', 'tec', 'téc', 'economista', 'diretor']
    df_agriculture = df_agriculture[~df_agriculture['TITULO'].str.contains('|'.join(unwanted_keywords), case=False, na=False)]

    return df_agriculture


def hypothesis4(df, df_agriculture):

    # Pega a coluna com os códigos rurais
    df_agriculture_ids = df_agriculture['CODIGO']
    
    # Cria uma lista com os códigos em string
    list_codes_rural = []
    for cod in df_agriculture_ids.values:
        str_cod = "" + str(cod) + ""
        list_codes_rural.append(str_cod)

    # Do dataframe original, pega as linhas que ID_OCUPA_N possui algum código rural
    rural_ocupations = df[df['ID_OCUPA_N'].isin(list_codes_rural)]
        
    count_id_ocupa_rural = len(rural_ocupations)
    print(f"{count_id_ocupa}")    
    



# Simula os parâmetros que serão passados para a função #####################
pd.set_option('display.expand_frame_repr', False)
usecols = ['ID_OCUPA_N', 'CLASSI_FIN', 'HOSPITALIZ', 'COMUNINF', 'DOENCA_TRA', 'DT_OBITO']
dtype = {'ID_OCUPA_N': 'str', 'CLASSI_FIN': 'str', 'HOSPITALIZ': 'str', 'DOENCA_TRA': 'str', 'DT_OBITO': 'str'}

path_csv = 'data/sinan_dengue_sample_total.csv'
df = pd.read_csv(path_csv, usecols=usecols, dtype=dtype)

hypothesis4(df, discover_occupation())
#############################################################################


