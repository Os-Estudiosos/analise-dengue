import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

    #df['DOENCA_TRA'] = df['DOENCA_TRA'].replace(['NA', 'na', ''], np.nan)
    #df= df[df['DOENCA_TRA'].notnull()]
    #print(df)
    # OBS: Não será possível cruzar os dados da ocupação com a coluna DOENCA_TRA
    # que avalia se a pessoa adquiriu a doenca no trabalho, pois a interseção de valores
    # válidos é nula entre as duas colunas

    df['ID_OCUPA_N'] = df['ID_OCUPA_N'].replace(['NA', 'na', ''], np.nan)
    df = df[df['ID_OCUPA_N'].notnull()]
    
    count_occup_freq = df['ID_OCUPA_N'].value_counts()

    total = count_occup_freq.sum()
    reasons = count_occup_freq / total

    reasons_sum = reasons.sum()  
    reasons_average = reasons_sum / len(reasons)
    
    #print(reasons_average)    
    # result print: 0.00042426813746287653

    # Cria uma lista com as strings dos códigos de ocupações rurais
    df2_agriculture_ids = df2_agriculture['CODIGO']
    list_codes_rural = []
    for cod in df2_agriculture_ids.values:
        str_cod = "" + str(cod) + ""
        list_codes_rural.append(str_cod)

    df_filtered_codes_rural = df[df['ID_OCUPA_N'].isin(list_codes_rural)]
    count_occup_freq_rural = df_filtered_codes_rural['ID_OCUPA_N'].value_counts()
    
    total_rural = count_occup_freq_rural.sum()
    reasons_rural = count_occup_freq_rural / total

    reasons_rural_sum = reasons_rural.sum()
    reasons_rural_averge = reasons_rural_sum / len(reasons_rural)

    #print(reasons_rural_averge)
    # result print: 0.0023231599510215237

    def verify_square_qui(df, list_codes_rural):
        #print(f"Quantidade de linhas com ocupações válidas: {len(df)}")
        # result 1.5M de linhas

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
        # Ignoro o 3 - inconclusivo e Ignoro o 4 - Não realizou algum teste
        df_filtered = df[df[results].isin(['1', '2']).any(axis=1)]

        # Pessoas que positivaram em algum teste, que tiveram Dengue
        df_positive = df_filtered[df_filtered[results].isin(['1']).any(axis=1)]  

        # Pessoas que negativaram em algum teste, que não tiveram Dengue
        df_negative = df_filtered[df_filtered[results].isin(['2']).any(axis=1)]  

        #print(f"Quantidade de pessoas que testaram positivo: {len(df_positive)}")
        #print(f"Quantidade de pessoas que testaram negativo: {len(df_negative)}")

        #print(df_positive)

        df_positive_rural = df_positive[df_positive['ID_OCUPA_N'].isin(list_codes_rural)]
        df_positive_others = df_positive[~df_positive['ID_OCUPA_N'].isin(list_codes_rural)]    
        df_negative_rural = df_negative[df_negative['ID_OCUPA_N'].isin(list_codes_rural)]
        df_negative_others = df_negative[~df_negative['ID_OCUPA_N'].isin(list_codes_rural)]

        a = len(df_positive_rural) # Positivos rurais
        b = len(df_negative_rural) # Negativos rurais
        c = len(df_positive_others) # Positivos não rurais
        d = len(df_negative_others) # Negativos não rurais

        n = a + b + c + d

        total_line1 = a + b # Total rurais
        total_line2 = c + d # Total não rurais
        total_col1 = a + c # Total positivos
        total_col2 = b + d # Total negativos

        # Calcula os esperados
        E_a = (total_line1 * total_col1) / n
        E_b = (total_line1 * total_col2) / n
        E_c = (total_line2 * total_col1) / n
        E_d = (total_line2 * total_col2) / n

        qui_square = ((a - E_a) ** 2) / E_a + \
             ((b - E_b) ** 2) / E_b + \
             ((c - E_c) ** 2) / E_c + \
             ((d - E_d) ** 2) / E_d

        return qui_square

    return  (reasons_average, reasons_rural_averge)


def test_plot_temp(reasons):

    reasons_average = reasons[0] 
    reasons_rural_average = reasons[1]

    data = {
        'Categoria': ['Outras ocupações', 'Ocupações Rurais'],
        'Média dos casos': [reasons_average, reasons_rural_average]
    }

    df_plot = pd.DataFrame(data)

    sns.barplot(x='Categoria', y='Média dos casos', data=df_plot)

    plt.title('Comparação dos casos possíveis de dengue, trabalhadores rurais X gerais')
    plt.ylabel('Média dos casos')
    plt.xlabel('Categoria')

    plt.show()


# Simula os parâmetros que serão passados para a função #####################

usecols=[
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
hypothesis4(df, discover_occupation())


#Test Plotar...
#reasons = hypothesis4(df, discover_occupation())
#test_plot_temp(reasons)
#############################################################################


