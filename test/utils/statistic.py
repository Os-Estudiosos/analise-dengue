import unittest
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.getcwd())

from src.utils.statistic import top_3_counts_numpy
from src.utils.random import generate_random_dataframe

class Top3CountsNumpyTest(unittest.TestCase):
    def test_wrong_arguments(self):
        with self.assertRaises(TypeError):
            top_3_counts_numpy(25, 45)
            top_3_counts_numpy(13, "123456")
            top_3_counts_numpy((1, 4, 5, 34), 112121)
    
    def test_working(self):
        np.random.seed(42)

        df1 = generate_random_dataframe()
        df2 = generate_random_dataframe()
        df3 = generate_random_dataframe()

        self.assertEqual(top_3_counts_numpy(df1, df1.columns), [('col_1', 10), ('col_2', 10), ('col_3', 10)])
        self.assertEqual(top_3_counts_numpy(df2, df2.columns), [('col_2', 10), ('col_3', 10), ('col_4', 10)])
        self.assertEqual(top_3_counts_numpy(df3, df3.columns), [('col_1', 10), ('col_2', 10), ('col_3', 10)])
