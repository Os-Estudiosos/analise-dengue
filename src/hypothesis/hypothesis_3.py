import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.getcwd())
from src.config import DATASET_LOCAL, DATASETS

def hypotesis3(df: pd.DataFrame) -> None:
    EXAMS = [
        "RESUL_VI_N",  # RESULTADO DO EXAME VIRAL
        "RESUL_NS1",  # RESULTADO DO EXAME NS1
        "RESUL_PCR_",  # RESULTADO DO EXAME PCR
        "RESUL_SORO", # RESUTLADO DO EXAME SOROLÓGICO
    ]

    SYMPTOMS = [
        # PRESENÇA DE SINTOMAS:
        "FEBRE",
        "MIALGIA",
        "CEFALEIA",
        "EXANTEMA",
        "VOMITO",
        "NAUSEA",
        "DOR_COSTAS",
        "CONJUNTVIT",
        "ARTRITE",
        "ARTRALGIA",
        "PETEQUIA_N",
        "LEUCOPENIA",
        "DOR_RETRO",
        "DIABETES",
        "HEMATOLOG",
        "HEPATOPAT",
        "RENAL",
        "HIPERTENSA",
        "ACIDO_PEPT",
        "AUTO_IMUNE"
    ]

    # # Retira apenas as colunas necessárias
    # new_dataset = df[COLUMNS_NEEDED]
    # new_dataset.to_csv(f'{DATASET_LOCAL()}/sinan_dengue_sintomas_e_exames.csv')
    new_df = df

    # Vou fazer tabelas e medir o Coeficiente de Contigência entre cada exame e cada teste,
    # assim eu filtro aqueles que tem relação com os que não tem nenhuma
    # Exame Viral

    # for exam in EXAMS:
    #     for symptom in SYMPTOMS:
    #         print('-'*50)
    #         exam_symptom_table = pd.crosstab(df[exam], df[symptom])
    #         print(exam_symptom_table)
    #         print(exam_symptom_table[1.0])

    exam_symptom_table = pd.crosstab(new_df[EXAMS[0]], new_df[SYMPTOMS[0]], margins=True)

    frequency_table = exam_symptom_table.copy()
    frequency_table[1.0] = exam_symptom_table[1.0]/exam_symptom_table['All']
    frequency_table[2.0] = exam_symptom_table[2.0]/exam_symptom_table['All']
    frequency_table['All'] = frequency_table[1.0]+frequency_table[2.0]

    expected_values_table = exam_symptom_table.copy()

    expected_values_table[1.0] = frequency_table.loc['All', 1.0] * exam_symptom_table['All']
    expected_values_table[2.0] = frequency_table.loc['All', 2.0] * exam_symptom_table['All']
    expected_values_table['All'] = expected_values_table[1.0] + expected_values_table[2.0]

    # difference_table = exam_symptom_table.copy()

    print(exam_symptom_table)
    print(frequency_table)
    print(expected_values_table)

    # viral_exam_1 = pd.crosstab(df[EXAMS[0]], df[SYPTOMS[1]])
    # print(viral_exam_1)
