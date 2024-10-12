"""Arquivo que deve ser executado para rodar os testes"""
import unittest

# Testes das funções estatísticas
from utils.statistic import ChiSquareTest, CrammerVTest, ContigencyCoefficientTest, Top3CountsNumpyTest

# Testes das funções de tempo
from utils.timing import MeasureFunctionExecutionTest


if __name__ == "__main__":
    unittest.main()
