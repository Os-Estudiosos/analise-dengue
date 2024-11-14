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


def FILES_FOLDER() -> str:
    """Function that returns the path of the 'Files' folder

    Returns:
        str: 'Files' folder's path
    """
    return os.path.join(os.getcwd(), 'files')


def OUTPUT_FOLDER() -> str:
    """Function that returns the path of the 'Output' folder

    Returns:
        str: 'Output' folder's path
    """
    return os.path.join(os.getcwd(), 'output')


REQUIRED_COLUMNS = [  # Required columns for every hypothesis
    # Colunas de Data
    'DT_INVEST', 'DT_VIRAL', 'DT_PCR', 'DT_ENCERRA', 'DT_SIN_PRI', 'DT_SORO', 'DT_NOTIFIC',
    'DT_OBITO', 'DT_DIGITA', 'DOR_COSTAS', 'DT_CHIK_S1', 'DT_INTERNA', 'DT_NS1', 'DT_CHIK_S2',

    # Colunas de Sintomas
    'FEBRE', 'DOR_RETRO', 'LEUCOPENIA', 'PETEQUIA_N', 'CEFALEIA', 'ARTRITE', 'DT_ALRM',
    'DT_GRAV', 'DT_PRNT', 'ACIDO_PEPT', 'HEPATOPAT', 'EXANTEMA', 'MIALGIA', 'CONJUNTVIT',
    'DIABETES', 'VOMITO', 'RENAL', 'NAUSEA', 'HIPERTENSA', 'ARTRALGIA',

    # Colunas de Exames
    'RESUL_NS1', 'AUTO_IMUNE', 'RESUL_PCR_', 'LACO', 'RESUL_VI_N',

    # Colunas Gerais
    'SG_UF_NOT','CLASSI_FIN', 'HOSPITALIZ', 'EVOLUCAO',  'NU_IDADE_N',
    'HEMATOLOG', 'RESUL_SORO', 'SIGLA_UF', 'SG_UF_NOT', 'ID_OCUPA_N', 'SOROTIPO'
]

CHUNKS_SIZE = 5 * 10**4  # Chunks used when reading the Total Dataset

MAX_SET_SIZE = 3  # Maximum size of symptom sets to consider
