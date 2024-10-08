import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis import hypothesis_3
from src.config import DATASETS, DATASET_LOCAL

def main():
    dataset = pd.read_csv(os.path.join(DATASET_LOCAL(), DATASETS()[0]), low_memory=False)
    hypothesis_3(dataset)


if __name__ == "__main__":
    main()
