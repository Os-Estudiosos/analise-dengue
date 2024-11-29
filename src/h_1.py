import pandas as pd
import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_1 import hypothesis1
from src.utils.reading import processing_total_dataset


def main():
    df = processing_total_dataset()
    hypothesis1(df)


if __name__ == '__main__':
    main()
