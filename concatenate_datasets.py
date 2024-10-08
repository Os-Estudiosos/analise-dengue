import pandas as pd

# Função que concatena datasets
def concatenate(dataframes: list) -> pd.DataFrame:
    """
    Função que concatena dataframes.

    Args:
        dataframes (list): Lista de DataFrames a serem concatenados.

    Returns:
        pd.DataFrame: DataFrame resultante da concatenação de todos os outros.
    """
    return pd.concat(dataframes, axis=0, ignore_index=True)

# Lendo os .csv
df1 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2021.csv", low_memory=False)
df2 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2022.csv", low_memory=False)
df3 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2023.csv", low_memory=False)
df4 = pd.read_csv("analise-dengue/data/sinan_dengue_sample_2024.csv", low_memory=False)

# Criando um dataframe concatenado com todos os DataFrames
df_total = concatenate([df1, df2, df3, df4])

# Salvando o DataFrame concatenado em um novo arquivo CSV
df_total.to_csv("analise-dengue/data/sinan_dengue_sample_total.csv", index=False)
