import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_4 import hypothesis4
from src.config import DATASET_LOCAL

def main():
   
    dataset = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_2021.csv'), low_memory=False)
    hypothesis4(dataset)


if __name__ == "__main__":
    main()
