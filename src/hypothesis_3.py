import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_3 import hypothesis3
from src.config import DATASET_LOCAL
from src.utils.reading import processing_total_dataset

def main():
    dataset = processing_total_dataset()
    hypothesis3(dataset)


if __name__ == "__main__":
    main()
