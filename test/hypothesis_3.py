import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_3 import hypothesis3
from src.config import DATASET_LOCAL

def main():
    dataset = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2021.csv'), low_memory=False)
    hypothesis3(dataset)


if __name__ == "__main__":
    main()
