import pandas as pd
import numpy as np
import os
from filtering import filter_dataset
from config import DATASET_LOCAL


def main():
    # Lendo o DATASET
    df = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_total.csv'))

    # Função que limpa para ter apenas as colunas necessárias para as hipóteses
    df = filter_dataset(df)
    df.to_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_filtrado.csv'))

    # Função que concatena todos os datasets
    ...

    # Limpando para ter apenas as colunas necessárias:
    ...

    # Testando cada hipótese (Usando multithreading)
    ...


if __name__ == '__main__':
    main()
