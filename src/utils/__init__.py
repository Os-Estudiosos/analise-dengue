"""Módulo que contém funções úteis, mas que não tem classificação para estar em outra pasta"""
import pandas as pd

def chi_square_test(qualitative_variable_1: pd.Series, qualitative_variable_2: pd.Series) -> float:
    """Essa função recebe duas séries pandas (De variáveis qualitativas) e realiza o teste do Qui-Quadrado

    Args:
        qualitative_variable_1 (pd.Series): Série contendo a segunda variável
        qualitative_variable_2 (pd.Series): Série contendo a primeira variável

    Raises:
        TypeError: Levanta esse erro se o usuário não passar Séries Pandas

    Returns:
        float: Valor Qui-Quadrado
    """
    # Checando os tipos das variáveis
    if not isinstance(qualitative_variable_1, pd.Series) or not isinstance(qualitative_variable_2, pd.Series):
        raise TypeError    

    exam_symptom_table = pd.crosstab(qualitative_variable_1, qualitative_variable_2, margins=True)

    frequency_table = exam_symptom_table.copy()
    frequency_table[1.0] = exam_symptom_table[1.0]/exam_symptom_table['All']
    frequency_table[2.0] = exam_symptom_table[2.0]/exam_symptom_table['All']
    frequency_table['All'] = frequency_table[1.0]+frequency_table[2.0]

    expected_values_table = exam_symptom_table.copy()

    expected_values_table[1.0] = frequency_table.loc['All', 1.0] * exam_symptom_table['All']
    expected_values_table[2.0] = frequency_table.loc['All', 2.0] * exam_symptom_table['All']
    expected_values_table['All'] = expected_values_table[1.0] + expected_values_table[2.0]

    difference_table = exam_symptom_table.copy()

    difference_table[1.0] = ((exam_symptom_table[1.0]-expected_values_table[1.0])**2)/expected_values_table[1.0]
    difference_table[2.0] = ((exam_symptom_table[2.0]-expected_values_table[2.0])**2)/expected_values_table[2.0]
    difference_table.drop('All', axis=1, inplace=True)
    difference_table.drop('All', inplace=True)

    square_chi = sum(difference_table[1.0] + difference_table[2.0])  # Qui-Quadrado
