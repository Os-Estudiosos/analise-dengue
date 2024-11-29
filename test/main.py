"""Arquivo que deve ser executado para rodar os testes"""
import unittest

# Testes das funções estatísticas
from utils.statistic import *

# Testes das funções de tempo
from utils.timing import MeasureFunctionExecutionTest
from filtering import AgeConversionTest


if __name__ == "__main__":
    unittest.main(verbosity=2)
