import numpy as np
import pandas as pd
import seaborn as sb


# Confiura o pandas para printar nome inteiro
pd.set_option('display.expand_frame_repr', False)

# Configuração das colunas
usecols = ['ID_OCUPA_N', 'CLASSI_FIN', 'HOSPITALIZ', 'COMUNINF', 'DOENCA_TRA', 'DT_OBITO'] 
dtype = {'ID_OCUPA_N': 'str', 'CLASSI_FIN': 'str', 'HOSPITALIZ': 'str' '', 'CS_SEXO': 'str', 'ID_MUNICIP': 'int', 'DOENCA_TRA': 'str', 'DT_OBITO': 'str'}


path_csv = 'data/sinan_dengue_sample_total.csv'    
df = pd.read_csv(path_csv, usecols=usecols, dtype=dtype)

  
def hypothesis4(df):

    count_id_ocupa = df['ID_OCUPA_N' = ].    

    return print(df.head(100)+ "/n" + count_id_ocupa)


hypothesis4(df)











































