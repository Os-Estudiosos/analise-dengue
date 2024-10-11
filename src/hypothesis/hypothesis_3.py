import pandas as pd
import numpy as np
import os
import sys
import concurrent.futures
sys.path.append(os.getcwd())
from src.config import DATASET_LOCAL, DATASETS
from src.utils import chi_square_test, contigency_coefficient

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
    new_df = pd.concat(df[EXAMS], df[SYMPTOMS])

    print(new_df.head())

    # Vou fazer tabelas e medir o Coeficiente de Contigência entre cada exame e cada teste,
    # assim eu filtro aqueles que tem relação com os que não tem nenhuma

    def mostrar_qui_quadrado(exam, symptom):
        print(f"Teste entre {exam} e {symptom}: {contigency_coefficient(new_df[exam], new_df[symptom])}")

    with concurrent.futures.ThreadPoolExecutor() as executor:  # Estrutura do multithreading
        threads_running: list[concurrent.futures.Future] = []

        for exam in EXAMS:
            for symptom in SYMPTOMS:
                threads_running.append(
                    executor.submit(
                        mostrar_qui_quadrado,
                        exam,
                        symptom
                    )
                )

        concurrent.futures.wait(threads_running)  # Esperando todas as tasks executarem

        # for pending_thread in threads_running:
        #     result = pending_thread.result()
        #     print(result)
