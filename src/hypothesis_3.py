import pandas as pd
import concurrent.futures
import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_3 import hypothesis3
from src.config import *
from src.filtering import filter_dataset
from src.utils.timing import measure_function_execution
from src.utils.reading import processing_total_dataset


@measure_function_execution
def main(year):
    # Vou ler o dataset por chunks
    chunks = pd.read_csv(os.path.join(DATASET_LOCAL(), f'sinan_dengue_sample_{year}.csv'), low_memory=False, chunksize=CHUNKS_SIZE)

    hypothesis3(chunks)

if __name__ == "__main__":
    main(2024)
