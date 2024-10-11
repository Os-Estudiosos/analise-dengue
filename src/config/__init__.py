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


REQUIRED_COLUMNS = [
    'DT_SIN_PRI', 'SG_UF_NOT', 'FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 'NAUSEA',
    'DOR_COSTAS', 'CONJUNTVIT', 'ARTRITE', 'ARTRALGIA', 'PETEQUIA_N', 'LEUCOPENIA', 'DOR_RETRO',
    'DIABETES', 'HEMATOLOG', 'HEPATOPAT', 'RENAL', 'HIPERTENSA', 'ACIDO_PEPT', 'AUTO_IMUNE',
    'DT_NOTIFIC', 'DT_SIN_PRI', 'DT_INVEST', 'DT_CHIK_S1', 'DT_CHIK_S2', 'DT_PRNT', 'DT_SORO',
    'DT_NS1', 'DT_VIRAL', 'DT_PCR', 'DT_INTERNA', 'DT_OBITO', 'DT_ENCERRA', 'DT_ALRM', 'DT_GRAV',
    'DT_DIGITA', 'DT_CHIK_S1', 'DT_CHIK_S2', 'DT_SORO', 'DT_NS1', 'DT_PRNT', 'DT_VIRAL', 'DT_PCR',
    'DT_ALRM', 'DT_GRAV', 'DT_ENCERRA', 'DT_NOTIFIC', 'VOMITO', 'FEBRE', 'MIALGIA', 'CEFALEIA',
    'EXANTEMA', 'NAUSEA', 'DOR_COSTAS', 'CONJUNTVIT', 'ATRITE', 'ARTALGIA', 'PETEQUIA_N', 
    'LEUCOPENIA', 'LACO', 'DOR_RETRO', 'DIABETES', 'HEMATOLOG', 'HEPATOPAT', 'RENAL', 'HIPERTENSA', 
    'ACIDO_PEPT', 'CLASSI_FIN', 'HOSPITALIZ', 'EVOLUCAO'
]

