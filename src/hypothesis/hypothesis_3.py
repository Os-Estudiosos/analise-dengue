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
            'LEUCOPENIA'
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


    def get_chunk_informations(chunk: pd.DataFrame):
        new_chunk = filter_dataset(chunk)[[
            AGE_COLUMN,
            *DANGER_SYMTOMPS_DICT['common'],
            *DANGER_SYMTOMPS_DICT['worrying'],
            *DANGER_SYMTOMPS_DICT['serious'],
        ]]

        conditions = [(new_chunk[col] == 1).all(axis=1) for col in DANGER_SYMTOMPS_DICT['serious']]
        results = [ 'GRAVE', 'PREOCUPANTE' ]
        new_chunk['SINTOMAS_CLASSIFICACAO'] = np.select(conditions, results, default='COMUM')

        print(new_chunk)

        # serious_symptoms_ages = new_chunk[DANGER_SYMTOMPS_DICT['serious']] == 1
        # worrying_symptoms_ages = new_chunk[new_chunk['WORRYING'] == 1][AGE_COLUMN]
        # common_symptoms_ages = new_chunk[new_chunk['COMMON'] == 1][AGE_COLUMN]

        # print(serious_symptoms_ages)
        # print(worrying_symptoms_ages)
        # print(common_symptoms_ages)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_running: list[concurrent.futures.Future] = []

        for chunk in chunks:  # Para cada chunk
            # Eu junto o dataset das siglas com o dataset original (Chunk)

            threads_running.append(
                executor.submit(
                    get_chunk_informations,
                    chunk
                )
            )

        concurrent.futures.wait(threads_running)

        for pending_thread in threads_running:
            pending_thread.result()

