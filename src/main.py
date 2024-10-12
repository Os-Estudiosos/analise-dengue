import pandas as pd
import numpy as np
import concurrent.futures
import typing
from utils.reading import processing_total_dataset
from utils.timing import measure_function_execution

# Importing the hypothesis functions
from hypothesis.hypothesis_1 import hypothesis1
from hypothesis.hypothesis_3 import hypothesis3
from hypothesis.hypothesis_4 import hypothesis4
from hypothesis.hypothesis_5 import hypothesis5


@measure_function_execution
def main():
    # Reading the DATASET
    # Already filtered and only the necessary columns
    print('Processando o DATASET')
    df = processing_total_dataset()

    # Testing each hypothesis
    print('Analisando (Hipótese 1)')
    hypothesis1(df)

    print('Analisando (Hipótese 3)')
    hypothesis3(df)

    print('Analisando (Hipótese 4)')
    hypothesis_4_return = hypothesis4(df)

    print('Analisando (Hipótese 5)')
    hypothesis_5_return = hypothesis5(df)


if __name__ == '__main__':
    main()
