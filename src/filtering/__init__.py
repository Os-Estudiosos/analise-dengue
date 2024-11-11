import pandas as pd
import os
import sys
sys.path.append(os.getcwd())
from src.config import REQUIRED_COLUMNS


def convert_age(age: str|int) -> float:
    """A idade é registrada de uma forma específica no dataset, então essa função é feita para converter o esquema do dataset para uma idade numérica fixa
    
    Esquema do Dataset:
    - 1º dígito:
    1. Hora
    2. Dia
    3. Mês
    4. Ano
    - Exemplo:
    * 3001 = Paciênte com 1 mês de idade
    * 4008 = Paciênte com 8 anos de idade

    Args:
        age (str): A idade conforme o critério passado anteriormente

    Returns:
        float: A idade de forma precisa (Exemplo: 12.5 é 12 anos e 6 meses)
    """

    return 0


def filter_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Function responsible for filtering the complete dataframe and get only the required columns mentioned in the CONFIG file
    
    Args:
        df (pd.DataFrame): Dataframe that will be filtered

    Raises:
        ValueError: Raised if the dataframe doesn't have any column required in the config file

    Returns:
        pd.DataFrame: The filtered dataframe
    """
    not_in_columns = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            not_in_columns.append(column)
    
    if len(not_in_columns) > 0:
        raise ValueError(f'The passed dataframe doesn\'t have all the required columns mentioned in the config: {not_in_columns}')
    
    return df[REQUIRED_COLUMNS]
