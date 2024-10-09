import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_3 import hypotesis3
from src.config import DATASETS, DATASET_LOCAL

def main():
    dataset = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sintomas_e_exames.csv'), low_memory=False)
    hypotesis3(dataset)


if __name__ == "__main__":
    main()
