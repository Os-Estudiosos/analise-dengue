import pandas as pd
import numpy as np
import concurrent.futures
import typing
from utils.reading import processing_total_dataset
from utils.timing import measure_function_execution

# Importing the hypothesis functions
from hypothesis.hypothesis_3 import hypothesis3


@measure_function_execution
def main():
    # Lendo o DATASET (Como é um dataset grande, a função demora um pouco, lê partes do dataset e unifica tudo, já filtrando apenas as colunas que serão utilizadas para fazer as hipóteses)
    df = processing_total_dataset()

    # Testando cada hipótese
    hypothesis3(df)    


if __name__ == '__main__':
    main()
