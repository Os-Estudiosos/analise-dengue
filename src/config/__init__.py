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
    'DT_INVEST', 'FEBRE', 'DOR_RETRO', 'LEUCOPENIA', 'PETEQUIA_N', 'DT_VIRAL', 
    'RESUL_NS1', 'ACIDO_PEPT', 'DT_PCR', 'AUTO_IMUNE', 'CEFALEIA', 'ARTRITE', 
    'DT_ENCERRA', 'DT_SIN_PRI', 'MIALGIA', 'CONJUNTVIT', 'DT_NS1', 'DIABETES', 
    'DT_SORO', 'RESUL_PCR_', 'DT_CHIK_S1', 'DT_INTERNA', 'HEPATOPAT', 'EXANTEMA', 
    'SG_UF_NOT', 'ARTRALGIA', 'CLASSI_FIN', 'RENAL', 'HOSPITALIZ', 'VOMITO', 
    'RESUL_VI_N', 'DT_NOTIFIC', 'DT_OBITO', 'DT_DIGITA', 'DOR_COSTAS', 'LACO', 
    'DT_CHIK_S2', 'NAUSEA', 'HIPERTENSA', 'DT_ALRM', 'DT_GRAV', 'DT_PRNT', 
    'EVOLUCAO', 'HEMATOLOG', 'RESUL_SORO'
]


CHUNKS_SIZE = 5 * 10**4
