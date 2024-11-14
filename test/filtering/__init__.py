import unittest
import os
import sys
sys.path.append(os.getcwd())
from src.filtering import convert_age


class AgeConversionTest(unittest.TestCase):
    def test_years_conversion(self):
        """Testando se a função 'convert_age' está convertendo os valores de ano corretamente
        """
        valores_a_converter = [
            '4003',
            4012,
            '4008',
            4112,
            4031
        ]

        for valor in valores_a_converter:
            self.assertEqual(convert_age(valor), float(str(valor)[1:4]))
    
    def test_months_conversion(self):
        """Testando se a função 'convert_age' está convertendo os valores de mês corretamente
        """
        valores_a_converter = [
            3003,
            '3008',
            3011,
            3001
        ]

        for valor in valores_a_converter:
            self.assertAlmostEqual(convert_age(valor), int(str(valor)[1:4])/12, delta=0.0001)
    
    def test_days_conversion(self):
        """Testando se a função 'convert_age' está convertendo os valores de dias corretamente
        """
        valores_a_converter = [
            2003,
            '2008',
            2011,
            2001
        ]

        for valor in valores_a_converter:
            self.assertAlmostEqual(convert_age(valor), int(str(valor)[1:4])/365, delta=0.0001)
    
    def test_hours_conversion(self):
        """Testando se a função 'convert_age' está convertendo os valores de dias corretamente
        """
        valores_a_converter = [
            1003,
            '1008',
            1011,
            1001
        ]

        for valor in valores_a_converter:
            self.assertAlmostEqual(convert_age(valor), int(str(valor)[1:4])/8766, delta=0.000001)
    
    def test_type_errors(self):
        """Testando se a função está levantando os erros de Tipo corretamente
        """

        with self.assertRaises(TypeError):
            convert_age(24.5)
            convert_age([])
            convert_age({})
            convert_age(())
            convert_age(complex(23, 2))
        
    
    def value_errors(self):
        """Testando se a função está levantando os erros de Tipo corretamente
        """

        with self.assertRaises(TypeError):
            convert_age('24.5')
            convert_age('21432')
            convert_age(12030)
            convert_age(0)
            convert_age(123)
