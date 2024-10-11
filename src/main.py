import pandas as pd
import numpy as np
import os
from filtering import filter_dataset
from config import DATASET_LOCAL, REQUIRED_COLUMNS, CHUNKS_SIZE
from utils.reading import processing_total_dataset


def main():
    # Lendo o DATASET (Como é um dataset grande, a função demora um pouco, lê partes do dataset e unifica tudo, já filtrando apenas as colunas que serão utilizadas para fazer as hipóteses)
    processing_total_dataset()

    # Função que concatena todos os datasets
    ...

    # Limpando para ter apenas as colunas necessárias:
    ...

    # Testando cada hipótese (Usando multithreading)
    ...


if __name__ == '__main__':
    main()
