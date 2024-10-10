import unittest
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.getcwd())

from src.utils import chi_square_test

np.random.seed(0)  # Setando a seed para 0 para não afetar os testes unitários

class ChiSquareTest(unittest.TestCase):
    def test_working_dataframe(self):
        """Testando se está retornando os valores de Qui Quadrado corretos
        """
        df1 = pd.DataFrame({'var1': np.random.rand(100), 'var2': np.random.rand(100)})
        df2 = pd.DataFrame({'var1': np.random.rand(100), 'var2': np.random.rand(100)})
        df3 = pd.DataFrame({'var1': np.random.rand(100), 'var2': np.random.rand(100)})
        df4 = pd.DataFrame({'var1': np.random.rand(100), 'var2': np.random.rand(100)})

        def discretizar(df):
            df_discretizado = df.apply(lambda x: pd.qcut(x, 4, labels=False))
            return df_discretizado
        
        df1 = discretizar(df1)
        df2 = discretizar(df2)
        df3 = discretizar(df3)
        df4 = discretizar(df4)

        # Informações do df1
        # Qui Quadrado: 7,2
        # V de Cramer: 0,1549
        # Contingência: 0,2592
        self.assertAlmostEqual(chi_square_test(df1['var1'], df1['var2']), 7.2)

        # Informações do df2
        # Qui Quadrado: 3,36
        # V de Cramer: 0,1058
        # Contingência: 0,1803
        self.assertAlmostEqual(chi_square_test(df2['var1'], df2['var2']), 3.36)

        # Informações do df3
        # Qui-Quadrado: 2.72
        # V de Cramer: 0.0952
        # Coeficiente de Contingência: 0.1627
        self.assertAlmostEqual(chi_square_test(df3['var1'], df3['var2']), 2.72)

        # Informações do df4
        # Qui-Quadrado: 8.16
        # V de Cramer: 0.1649
        # Coeficiente de Contingência: 0.2747
        self.assertAlmostEqual(chi_square_test(df4['var1'], df4['var2']), 8.16)
    

    def test_passing_wrong_argument_type(self):
        """Testa a função quando se passa os argumetos errados
        """
        df1 = pd.DataFrame({'var1': np.random.rand(100), 'var2': np.random.rand(100)})

        # Testando se a função está levantando TypeError quando necessário
        with self.assertRaises(TypeError):
            chi_square_test(df1, df1)
            chi_square_test(df1, 'Olá')
            chi_square_test(25, 38)
            chi_square_test("Apenas um Teste", 38)
