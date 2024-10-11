"""Arquivo que deve ser executado para rodar os testes"""
import unittest
import os
import sys
sys.path.append(os.getcwd())

# Testes das funções estatísticas
from test.utils.statistic import ChiSquareTest, CrammerVTest, ContigencyCoefficientTest


if __name__ == "__main__":
    unittest.main()
