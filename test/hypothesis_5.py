import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_5 import hypothesis5
from src.config import DATASETS, DATASET_LOCAL

def main():
    dataset = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_total.csv'), low_memory=False)
    hypothesis5(dataset)


if __name__ == "__main__":
    main()