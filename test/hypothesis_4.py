import numpy as np
import pandas as pd
import seaborn as sns

# Expandir o DataFrame para a largura total da tela
pd.set_option('display.expand_frame_repr', False)

def discover_occupation():

    path_occupation_csv = 'src/utils/CBO2002_Ocupacao.csv'

    df2_occup = pd.read_csv(path_occupation_csv, encoding='ISO-8859-1', sep=';')

    # Filtra por termos relacionados ao meio rural
    keywords = ['rural', 'agri', 'pecu', 'agro']
    df2_agriculture = df2_occup[df2_occup['TITULO'].str.contains('|'.join(keywords), case=False, na=False)]

    # Elimina ocupações relacionadas a área mas que não contribuem para hipótese
    unwanted_keywords = ['engenheiro', 'gerente', 'administrador', 'pesquisador', 'analista', 'tec', 'téc', 'economista', 'diretor']
    df2_agriculture = df2_agriculture[~df2_agriculture['TITULO'].str.contains('|'.join(unwanted_keywords), case=False, na=False)]
    
    #print(df2_agriculture)
    
    return df2_agriculture


def hypothesis4(df, df2_agriculture):

    df['ID_OCUPA_N'] = df['ID_OCUPA_N'].replace(['NA', 'na', ''], np.nan)
    df = df[df['ID_OCUPA_N'].notnull()]

    # Usando loc[] para evitar o SettingWithCopyWarning
    # df.loc[df['DOENCA_TRA'].notnull(), 'DOENCA_TRA'] = df['DOENCA_TRA'].replace(['NA', 'na', ''], np.nan)
    # df = df[df['DOENCA_TRA'].notnull()]

    # OBS: a intersecção de valores válidos das colunas DOENCA_TRA E ID_OCUPA_N é nula!!
    # Portanto, não será possível verificar se existe indícios de relação entre pessoas
    # que ocupam o meio rural pegaram a doença no trabalho. 

    count_occup_freq = df['ID_OCUPA_N'].value_counts()

    total = count_occup_freq.sum()
    reasons = count_occup_freq / total

    reasons_sum = reasons.sum()  
    reasons_average = reasons_sum / len(reasons)

    




    print(reasons_average)    
    
    

    # Cria uma lista com as strings dos códigos de ocupações rurais
    df2_agriculture_ids = df2_agriculture['CODIGO']
    list_codes_rural = []
    for cod in df2_agriculture_ids.values:
        str_cod = "" + str(cod) + ""
        list_codes_rural.append(str_cod)


def test_plot_temp():
    pass
    

# Simula os parâmetros que serão passados para a função #####################
usecols = ['ID_OCUPA_N', 'CLASSI_FIN', 'HOSPITALIZ', 'COMUNINF', 'DOENCA_TRA', 'DT_OBITO']
dtype = {'ID_OCUPA_N': 'str', 'CLASSI_FIN': 'str', 'HOSPITALIZ': 'str', 'DOENCA_TRA': 'str', 'DT_OBITO': 'str'}

path_csv = 'data/sinan_dengue_sample_total.csv'
df = pd.read_csv(path_csv, usecols=usecols, dtype=dtype)


hypothesis4(df, discover_occupation())
#############################################################################


