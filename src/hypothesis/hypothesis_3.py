import pandas as pd
from pandas.io.parsers import TextFileReader
import numpy as np
import concurrent
from src.filtering import filter_dataset
# from src.utils.statistic import contigency_coefficient
# from src.config import OUTPUT_FOLDER


def hypothesis3(chunks: TextFileReader) -> None:
    AGE_COLUMN = 'IDADE_ANOS'  # Coluna da idade que vou utilizar
    DANGER_SYMTOMPS_DICT = {  # Dicionário separando os sintomas em suas respectivas classificações
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
        """Função resposável por pegar as informações que posteriormente usarei para calcular o R²

        Args:
            chunk (pd.DataFrame): _description_
        """
        new_chunk = filter_dataset(chunk)[[  # Eu pego o chunk filtrado e utilizo apenas as colunas de sintomase  idade que eu defini anterioremente
            AGE_COLUMN,
            *DANGER_SYMTOMPS_DICT['common'],
            *DANGER_SYMTOMPS_DICT['worrying'],
            *DANGER_SYMTOMPS_DICT['serious'],
        ]]

        # O Novo chunk que vou trabalhar que tem apenas a coluna de idades e uma que vai dizer a classificação dos sintomas do paciente
        refactored_chunk = pd.DataFrame(new_chunk[AGE_COLUMN], columns=[AGE_COLUMN, 'SINTOMA_CLASSIFIC'])

        # Vou analisar se a pessoa tem algum sintoma grave
        for symptom in DANGER_SYMTOMPS_DICT['serious']:
            refactored_chunk['SINTOMA_CLASSIFIC'] = (refactored_chunk['SINTOMA_CLASSIFIC'] | (new_chunk[symptom]==1)).apply(
                lambda x: 'GRAVE' if x else None  # Vai ter a classificação do sintoma como GRAVE se existir algum valor TRUE
            )
        
        # Também vou analisar se tem sintomas preocupantes
        for symptom in DANGER_SYMTOMPS_DICT['worrying']:
            worrying_symtpoms_serie = (new_chunk[symptom]==1).apply(lambda x: 'PREOCUPANTE' if x else None)
            refactored_chunk['SINTOMA_CLASSIFIC'] = refactored_chunk['SINTOMA_CLASSIFIC'].combine_first(worrying_symtpoms_serie)
            # Combino com a nova Série dos sintomas preocupantes, assim, eu classifico apenas aqueles que
            # Tem sintomas preocupantes mas não tem nenhum sintoma grave
        

        common_symtpoms_serie = pd.Series(np.tile(
            ['COMUM'],
            len(refactored_chunk['SINTOMA_CLASSIFIC'])
        ))
        refactored_chunk['SINTOMA_CLASSIFIC'] = refactored_chunk['SINTOMA_CLASSIFIC'].combine_first(common_symtpoms_serie)
        # O resto que não teve classificação, tem apenas sintomas comuns ou são assintomáticos, então eu crio
        # uma série que tem o tamanho do meu dataset e preencho todas as classificações sobrantes como COMUM
        
    

    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_running: list[concurrent.futures.Future] = []

        for chunk in chunks:  # Para cada chunk
            # Eu adiciono minha função de pegar as informações do dataset ao executor de threads
            threads_running.append(
                executor.submit(
                    get_chunk_informations,
                    chunk
                )
            )

        concurrent.futures.wait(threads_running)  # Espero todas rodarem

        for pending_thread in threads_running:  # Pego o resultado de cada uma
            pending_thread.result()

