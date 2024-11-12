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

        refactored_chunk = pd.DataFrame(new_chunk[AGE_COLUMN], columns=[AGE_COLUMN, 'SINTOMA_CLASSIFIC'])

        for symptom in DANGER_SYMTOMPS_DICT['serious']:
            # Se tiver alguém com sintomas graves
            refactored_chunk['SINTOMA_CLASSIFIC'] = (refactored_chunk['SINTOMA_CLASSIFIC'] | (new_chunk[symptom]==1)).apply(
                lambda x: 'GRAVE' if x else None  # Vai ter a classificação do sintoma como GRAVE
            )
        
        for symptom in DANGER_SYMTOMPS_DICT['worrying']:
            # Se tiver alguém com sintomas preocupantes
            worrying_symtpoms_serie = (new_chunk[symptom]==1).apply(lambda x: 'PREOCUPANTE' if x else None)
            refactored_chunk['SINTOMA_CLASSIFIC'] = refactored_chunk['SINTOMA_CLASSIFIC'].combine_first(worrying_symtpoms_serie)
        

        common_symtpoms_serie = pd.Series(np.tile(['COMUM'], len(refactored_chunk['SINTOMA_CLASSIFIC'])))
        
        refactored_chunk['SINTOMA_CLASSIFIC'] = refactored_chunk['SINTOMA_CLASSIFIC'].combine_first(common_symtpoms_serie)
        
        print(refactored_chunk['SINTOMA_CLASSIFIC'])
    
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

