import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.getcwd())
from config import DATASET_LOCAL


def main():
    # Lendo o DATASET
    DATASET = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_total.csv'))

    # Limpando para ter apenas as colunas necessárias:
    ...

    # Testando cada hipótese (Usando multithreading)
    ...


if __name__ == '__main__':
    main()
