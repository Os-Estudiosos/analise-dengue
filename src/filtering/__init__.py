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
    if not isinstance(age, int) and not isinstance(age, str):
        raise TypeError('Passe um argumento válido para a função')
    try:
        int(age)  # Serve para levantar erro se passar argumento tipo "2.34"
    except TypeError as err:
        raise ValueError('O Valor passado está incorreto') from err

    age_structure = [str(age)[0], float(str(age)[1:len(str(age))])]

    if age_structure[0] == '4':
        return age_structure[1]
    elif age_structure[0] == '3':
        return age_structure[1]/12
    elif age_structure[0] == '2':
        return age_structure[1]/365
    else:
        return age_structure[1]/8766


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
    
    df['IDADE_ANOS'] = df['NU_IDADE_N'].apply(convert_age)
    
    return df[[*REQUIRED_COLUMNS, 'IDADE_ANOS']]
