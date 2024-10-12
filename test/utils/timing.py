import unittest
import os
import sys
import time
from random import randint
sys.path.append(os.getcwd())
from src.utils.timing import measure_function_execution


class MeasureFunctionExecutionTest(unittest.TestCase):
    def test_executing_correctly_without_parameters(self):
        LAZY_TIME = randint(1, 5)  # Randomize the test function's time execution

        @measure_function_execution
        def testing_function():
            time.sleep(LAZY_TIME)
        
        self.assertAlmostEqual(testing_function(), LAZY_TIME, delta=0.1)
    
    def test_using_parameters(self):
        LAZY_TIME = randint(1, 5)  # Randomize the test function's time execution

        @measure_function_execution
        def infinite_sum(a: int, b: int) -> int:
            time.sleep(LAZY_TIME)
            return a+b

        @measure_function_execution
        def named_args(**kwargs):
            time.sleep(LAZY_TIME)
        
        self.assertAlmostEqual(infinite_sum(1,3), LAZY_TIME, delta=0.1)
        self.assertAlmostEqual(named_args(teste="ola", teste2="ola"), LAZY_TIME, delta=0.1)
    
    def test_not_passing_functions(self):
        with self.assertRaises(TypeError):
            measure_function_execution('olá')
            measure_function_execution(1)
            measure_function_execution((1, 2, 3))
            measure_function_execution([1, 2, 3])
