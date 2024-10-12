import pandas as pd
import numpy as np
import concurrent.futures
import typing
from utils.reading import processing_total_dataset
from utils.timing import measure_function_execution

# Importing the hypothesis functions
from hypothesis.hypothesis_1 import hypothesis1
from hypothesis.hypothesis_2 import hypothesis2_part1, hypothesis2_part2
from hypothesis.hypothesis_3 import hypothesis3
from hypothesis.hypothesis_4 import hypothesis4
from hypothesis.hypothesis_5 import hypothesis5


@measure_function_execution
def main():
    # Reading the DATASET
    # Already filtered and only the necessary columns
    print('Processando o DATASET')
    df = processing_total_dataset()

    # Testing each hypothesis
    hypothesis_list: list[typing.Callable] = [
        hypothesis1,
        hypothesis3,
        hypothesis2_part1,
        hypothesis2_part2,
        hypothesis4,
        hypothesis5
    ]

    hypothesis_results = {
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        hypothesis_running: dict[str, concurrent.futures.Future] = {}

        for i, hypothesis in enumerate(hypothesis_list):
            hypothesis_running[f'hypothesis{i}'] = executor.submit( hypothesis,  df )
        
        concurrent.futures.wait(hypothesis_running)

        for hyp_name, hypothesis_finished in hypothesis_running.values():
            hypothesis_results[hyp_name] = hypothesis_finished.result()
        
        print(hypothesis_results)


if __name__ == '__main__':
    main()
