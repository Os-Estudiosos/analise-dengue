import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_4 import hypothesis4, discover_occupation
from src.utils.reading import processing_total_dataset
from src.utils.plots.h4_plots import plot_proportions

def main():
    # O que voce precisa para rodar o código:
    df_sinan_total = processing_total_dataset()
    list_codes_rural = discover_occupation()
    result = hypothesis4(df_sinan_total, list_codes_rural)
    
    plot_proportions(result)


if __name__ == "__main__":
    main()
