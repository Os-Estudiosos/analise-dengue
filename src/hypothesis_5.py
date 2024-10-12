import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_5 import hypothesis5
from src.utils.reading import processing_total_dataset


def main():
    dataset = processing_total_dataset()
    hypothesis5(dataset)


if __name__ == "__main__":
    main()