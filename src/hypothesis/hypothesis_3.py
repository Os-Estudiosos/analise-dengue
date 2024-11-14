import pandas as pd
from pandas.io.parsers import TextFileReader
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import concurrent
from src.filtering import filter_dataset
from config import *
# from src.utils.statistic import contigency_coefficient
# from src.config import OUTPUT_FOLDER


def hypothesis3(chunks: TextFileReader) -> None:
    AGE_COLUMN = 'IDADE_ANOS'  # Coluna da idade que vou utilizar
    SYMPTO_CLASSFICIATION = 'SINTOMA_CLASSIFIC'
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


    def get_chunk_informations(chunk: pd.DataFrame) -> pd.DataFrame:
        """Função resposável por pegar as informações que posteriormente usarei para calcular o R²

        Args:
            chunk (pd.DataFrame): Dataframe que eu vou pegar as informações

        Returns:
            (pd.Dataframe): Um Dataframe contendo as idades associadas com a coluna de CLASSIFICAÇÃO DOS SINTOMAS
        """
        new_chunk = filter_dataset(chunk)[[  # Eu pego o chunk filtrado e utilizo apenas as colunas de sintomase  idade que eu defini anterioremente
            AGE_COLUMN,
            *DANGER_SYMTOMPS_DICT['common'],            
            *DANGER_SYMTOMPS_DICT['worrying'],
            *DANGER_SYMTOMPS_DICT['serious'],
        ]]
        
        # O Novo chunk que vou trabalhar que tem apenas a coluna de idades e uma que vai dizer a classificação dos sintomas do paciente
        refactored_chunk = pd.DataFrame(new_chunk[AGE_COLUMN], columns=[AGE_COLUMN, SYMPTO_CLASSFICIATION])

        # Vou analisar se a pessoa tem algum sintoma grave
        for symptom in DANGER_SYMTOMPS_DICT['serious']:
            refactored_chunk[SYMPTO_CLASSFICIATION] = (new_chunk[symptom]==1).apply(
                lambda x: 'GRAVE' if x else None  # Vai ter a classificação do sintoma como GRAVE se existir algum valor TRUE
            )

        # Também vou analisar se tem sintomas preocupantes
        for symptom in DANGER_SYMTOMPS_DICT['worrying']:
            worrying_symtpoms_serie = (new_chunk[symptom]==1).apply(lambda x: 'PREOCUPANTE' if x else None)
            refactored_chunk[SYMPTO_CLASSFICIATION] = refactored_chunk[SYMPTO_CLASSFICIATION].combine_first(worrying_symtpoms_serie)
            # Combino com a nova Série dos sintomas preocupantes, assim, eu classifico apenas aqueles que
            # Tem sintomas preocupantes mas não tem nenhum sintoma grave
        

        common_symtpoms_serie = pd.Series(np.tile(
            ['COMUM'],
            len(refactored_chunk[SYMPTO_CLASSFICIATION])
        ))
        refactored_chunk[SYMPTO_CLASSFICIATION] = refactored_chunk[SYMPTO_CLASSFICIATION].combine_first(common_symtpoms_serie)
        # O resto que não teve classificação, tem apenas sintomas comuns ou são assintomáticos, então eu crio
        # uma série que tem o tamanho do meu dataset e preencho todas as classificações sobrantes como COMUM

        return refactored_chunk


    chunks_information_list = []  # Lista com as informações que vou obter de cada chunk

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
            chunks_information_list.append(pending_thread.result())

    
    unic_df = pd.concat(chunks_information_list, ignore_index=True)


    # Dividindo o dataframe total nos valores possiveis da
    # variável qualitativa CLASSIFICAÇÃO DO SINTOMA
    people_with_serious_symptoms = unic_df[unic_df[SYMPTO_CLASSFICIATION] == 'GRAVE']
    people_with_worries_symptoms = unic_df[unic_df[SYMPTO_CLASSFICIATION] == 'PREOCUPANTE']
    people_with_common_symptoms = unic_df[unic_df[SYMPTO_CLASSFICIATION] == 'COMUM']

    # Calculando a variância média
    mean_variance = (
        people_with_common_symptoms[AGE_COLUMN].var()*len(people_with_common_symptoms[AGE_COLUMN])
        +
        people_with_serious_symptoms[AGE_COLUMN].var()*len(people_with_serious_symptoms[AGE_COLUMN])
        +
        people_with_worries_symptoms[AGE_COLUMN].var()*len(people_with_worries_symptoms[AGE_COLUMN])
    ) / len(unic_df[AGE_COLUMN])

    # Calculando o R²
    squared_r = 1 - (mean_variance/unic_df[AGE_COLUMN].var())

    print(squared_r)

    # Plotando os gráficos de boxplot
    sns.set_style('whitegrid')

    plt.figure(figsize=(10,6))
    sns.boxplot(data=unic_df, x=SYMPTO_CLASSFICIATION, y=AGE_COLUMN, palette='pastel', hue=SYMPTO_CLASSFICIATION, legend=False)

    plt.xlabel('Classificação dos Sintomas')  # Nome do eixo x
    plt.ylabel('Idades')     # Nome do eixo y
    plt.title('Distribuição das idades por cada categoria de Sintoma')  # Título do gráfico
    plt.savefig(os.path.join(OUTPUT_FOLDER(), 'ages_per_symptom_classification.png'), format='png')
    plt.show()
