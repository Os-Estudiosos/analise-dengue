import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis import hypothesis_3
from src.config import DATASETS

def main():
    # dataset2021 = pd.read_csv(DATASETS()[0])
    print (DATASETS()[0])
    # hypothesis_3(dataset2021)


if __name__ == "__main__":
    main()
