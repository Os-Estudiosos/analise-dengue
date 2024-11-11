import pandas as pd
import numpy as np
import os
import sys
# import concurrent.futures
sys.path.append(os.getcwd())
# from src.utils.statistic import contigency_coefficient
# from src.config import OUTPUT_FOLDER


def hypothesis3(df: pd.DataFrame) -> None:
    AGE_COLUMN = 'NU_IDADE_N'  # Lista das colunas que vou utilizar
    
    # Retiro apenas as colunas necessárias
    new_df = df[AGE_COLUMN]

    print(new_df[AGE_COLUMN[0]].value_counts())

    # Vou fazer tabelas e medir o Coeficiente de Contigência entre cada exame e cada teste,
    # assim eu filtro aqueles que tem relação com os que não tem nenhuma
    
    # contigency_table = pd.DataFrame(index=COMPLICATIONS.keys(), columns=EVOLUTIONS.keys(), dtype=pd.Float32Dtype())
