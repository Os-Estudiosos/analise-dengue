import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_4 import hypothesis4
from src.utils.reading import processing_total_dataset

def main():
    dataset = processing_total_dataset()
    hypothesis4(dataset)


if __name__ == "__main__":
    main()
