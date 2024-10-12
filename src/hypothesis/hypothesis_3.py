import pandas as pd
import numpy as np
import os
import sys
import concurrent.futures
sys.path.append(os.getcwd())
from src.utils.statistic import contigency_coefficient
from src.config import OUTPUT_FOLDER


def hypothesis3(df: pd.DataFrame) -> None:
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
    new_df = df[[*EXAMS, *SYMPTOMS]]

    # Vou fazer tabelas e medir o Coeficiente de Contigência entre cada exame e cada teste,
    # assim eu filtro aqueles que tem relação com os que não tem nenhuma

    contigency_table = pd.DataFrame(index=EXAMS, columns=SYMPTOMS, dtype=pd.Float32Dtype())  # Tabela que vai ter cada coeficiente de contigência entre cada exame e sintoma

    def calcular_qui_quadrado(exam: str, symptom: str) -> dict:
        """Function that calculate Square Chi between an exam and a symptom and returns a dictionary (Made to use with multithread)

        Args:
            exam (str): Exam
            symptom (str): Symptom

        Returns:
            dict: Dictionary with both
        """
        ct = contigency_coefficient(new_df[exam], new_df[symptom])
        return { 'exam': exam, 'symptom': symptom, 'ct': ct }
        

    with concurrent.futures.ThreadPoolExecutor() as executor:  # Estrutura do multithreading
        threads_running: list[concurrent.futures.Future] = []

        for exam in EXAMS:
            for symptom in SYMPTOMS:
                threads_running.append(
                    executor.submit(
                        calcular_qui_quadrado,
                        exam,
                        symptom
                    )
                )

        concurrent.futures.wait(threads_running)  # Esperando todas as tasks executarem

        for pending in threads_running:
            result = pending.result()
            contigency_table.loc[result['exam'], result['symptom']] = result['ct']
    
    contigency_table.to_csv(os.path.join(OUTPUT_FOLDER(), 'contigency_table_exams_and_symptoms.csv'))
