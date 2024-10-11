import pandas as pd
import numpy as np
import os
from filtering import filter_dataset
from config import DATASET_LOCAL, REQUIRED_COLUMNS, CHUNKS_SIZE
from utils.reading import processing_total_dataset
from utils.timing import measure_function_execution


@measure_function_execution
def main():
    # Lendo o DATASET (Como é um dataset grande, a função demora um pouco, lê partes do dataset e unifica tudo, já filtrando apenas as colunas que serão utilizadas para fazer as hipóteses)
    df_list = processing_total_dataset()
    print(df_list)

    # Testando cada hipótese (Usando multithreading)
    ...


if __name__ == '__main__':
    main()
