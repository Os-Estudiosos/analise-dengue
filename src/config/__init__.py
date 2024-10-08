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

    arquivos = []
    for i in range(2021, 2025):
        arquivos.append(os.path.join(DATASET_LOCAL(), f'sinan_dengue_sample_{i}'))
    return arquivos
