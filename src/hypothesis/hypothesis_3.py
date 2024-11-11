import pandas as pd
from pandas.io.parsers import TextFileReader
import numpy as np
import concurrent
from src.filtering import filter_dataset
# from src.utils.statistic import contigency_coefficient
# from src.config import OUTPUT_FOLDER


def hypothesis3(chunks: TextFileReader) -> None:
    AGE_COLUMN = 'IDADE_ANOS'  # Lista das colunas que vou utilizar
    DANGER_SYMTOMPS_DICT = {
        'serious': [
            'RENAL',
            'HIPERTENSA',
            'HEPATOPAT',
            'LEUCOPENIA',
            'DIABETES'
        ],
        'worrying': [
            'VOMITO',
            'DOR_RETRO',
            'ARTRALGIA'
        ],
        'common': [
            'FEBRE',
            'PETEQUIA_N',
            'MIALGIA',
            'CEFALEIA',
            'CONJUNTVIT',
            'EXANTEMA',
            'ARTRITE',
            'NAUSEA'
        ], 
    }


    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            threads_running: list[concurrent.futures.Future] = []

            for chunk in chunks:  # Para cada chunk
                # Eu junto o dataset das siglas com o dataset original (Chunk)

                threads_running.append(
                    executor.submit(
                        hypothesis3,
                        chunk
                    )
                )

            concurrent.futures.wait(threads_running)

            for pending_thread in threads_running:
                pending_thread.result()
    except Exception as e:
        print(e)

