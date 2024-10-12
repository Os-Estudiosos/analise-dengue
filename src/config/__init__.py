"""Módulo contendo funções e variáveis importantes de configuração"""
import os


def DATASET_LOCAL() -> str:
    """Return the absolute path of the datasets

    Returns:
        str: Dataset's path
    """
    return os.path.join(os.getcwd(), 'data')


def DATASETS() -> list[str]:
    """Function that returns a list with all files inside the DATA path

    Returns:
        list[str]: Files list
    """
    return os.listdir(DATASET_LOCAL())


REQUIRED_COLUMNS = [  # Required columns for every hypothesis
    'DT_INVEST', 'FEBRE', 'DOR_RETRO', 'LEUCOPENIA', 'PETEQUIA_N', 'DT_VIRAL', 
    'RESUL_NS1', 'ACIDO_PEPT', 'DT_PCR', 'AUTO_IMUNE', 'CEFALEIA', 'ARTRITE', 
    'DT_ENCERRA', 'DT_SIN_PRI', 'MIALGIA', 'CONJUNTVIT', 'DT_NS1', 'DIABETES', 
    'DT_SORO', 'RESUL_PCR_', 'DT_CHIK_S1', 'DT_INTERNA', 'HEPATOPAT', 'EXANTEMA', 
    'SG_UF_NOT', 'ARTRALGIA', 'CLASSI_FIN', 'RENAL', 'HOSPITALIZ', 'VOMITO', 
    'RESUL_VI_N', 'DT_NOTIFIC', 'DT_OBITO', 'DT_DIGITA', 'DOR_COSTAS', 'LACO', 
    'DT_CHIK_S2', 'NAUSEA', 'HIPERTENSA', 'DT_ALRM', 'DT_GRAV', 'DT_PRNT', 
    'EVOLUCAO', 'HEMATOLOG', 'RESUL_SORO'
]


CHUNKS_SIZE = 5 * 10**4  # Chunks used when reading the Total Dataset
