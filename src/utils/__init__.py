"""Módulo que contém funções úteis, mas que não tem classificação para estar em outra pasta"""
import pandas as pd
import numpy as np
from math import sqrt

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
        raise TypeError("Os argumentos passados não são Séries Pandas")

    cross_table = pd.crosstab(qualitative_variable_1, qualitative_variable_2, margins=True)

    # Criando a frequência esperada em cada elemento
    frequency_row = np.ndarray((1,len(cross_table.columns)), dtype=float)
    
    for i, element in enumerate(cross_table.loc['All']):
        frequency_row[0,i] = element/cross_table.loc['All', 'All']

    # Criando a tabela dos valores esperados
    expected_values = pd.DataFrame(index=cross_table.index, columns=cross_table.columns, dtype=pd.Float64Dtype())
    
    # Colocando o valor esperado em cada elemento ij da tabela
    for row in cross_table.index:
        for column in cross_table.columns:
            if column == 'All':
                expected_values.loc[row, column] = expected_values.loc[row].sum()
                continue
            expected_values.loc[row, column] = cross_table.loc[row, 'All']*frequency_row[0, column] 

    # Criando a tabela das diferenças entre os valores
    difference_table = pd.DataFrame(index=cross_table.index, columns=cross_table.columns, dtype=pd.Float64Dtype())
    for column in difference_table.columns:
        difference_table[column] = ((cross_table[column] - expected_values[column])**2)/expected_values[column]

    # Calculando Qui-Quadrado
    qui_quadrado = 0
    for row in difference_table.iloc:
        qui_quadrado += row.sum()

    return qui_quadrado


def crammer_V(qualitative_variable_1: pd.Series, qualitative_variable_2: pd.Series) -> float:
    """Função que calcula V de Crammer

    Args:
        qualitative_variable_1 (pd.Series): Série da variável qualitativa
        qualitative_variable_2 (pd.Series): Série da variável qualitativa

    Raises:
        TypeError: Levanta esse erro se não for passadas séries pandas como argumentos

    Returns:
        float: V de Crammer
    """
    if not isinstance(qualitative_variable_1, pd.Series) or not isinstance(qualitative_variable_2, pd.Series):
        raise TypeError
    
    qui_quadrado = chi_square_test(qualitative_variable_1, qualitative_variable_2)

    cross_table = pd.crosstab(qualitative_variable_1, qualitative_variable_2, margins=True)

    n = cross_table.loc['All', 'All']
    r = len(cross_table.index)-1
    s = len(cross_table.columns)-1

    return sqrt((qui_quadrado)/(n*min(r-1, s-1)))
