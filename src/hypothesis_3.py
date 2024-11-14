import pandas as pd
import concurrent.futures
import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_3 import hypothesis3
from src.config import *
from src.utils.timing import measure_function_execution
from src.utils.reading import processing_total_dataset


@measure_function_execution
def main():
    # Vou ler o dataset por chunks
    chunks = processing_total_dataset(complete=False)

    hypothesis3(chunks)

if __name__ == "__main__":
    main()
