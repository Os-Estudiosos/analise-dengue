"""Módulo contendo funções e variáveis importantes de configuração"""
import os


def DATASET_LOCAL() -> str:
    """Função que retorna o caminho absoluto dos datasets

    Returns:
        str: Caminho dos Datasets
    """
    return os.path.join(os.getcwd(), 'data')


def DATASETS() -> list[str]:
    """Função que retorna uma lista com todos os arquivos de acordo com o local (Independente do Sistema)

    Returns:
        list[str]: Lista dos arquivos
    """

    return os.listdir(DATASET_LOCAL())
