import pandas as pd

import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_2 import hypothesis2_part1, hypothesis2_part2
from src.utils.reading import processing_total_dataset

def main():
    dataset = processing_total_dataset()
    hypothesis2_part1(dataset)
    hypothesis2_part2(dataset)


if __name__ == "__main__":
    main()
