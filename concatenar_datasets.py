import pandas as pd

def concatenar_datasets(datasets:list) -> pd.DataFrame:
    """
    Função que concatena os datasets utilizados

    Args:
        datasets (list): Lista dos caminhos dos datasets

    Returns:
        pd.DataFrame: Dataset total concatenado
    
    >>>  concatenar_datasets(['data/sinan_dengue_sample_2021.csv', 'data/sinan_dengue_sample_2022.csv'])
                TP_NOT ID_AGRAVO  DT_NOTIFIC  SEM_NOT  NU_ANO  SG_UF_NOT  ...  TP_SISTEMA  NDUPLIC_N   DT_DIGITA CS_FLXRET  FLXRECEBI  MIGRADO_W
    0             2       A90  2021-02-23   202108    2021         12  ...         2.0        NaN  2021-05-11       NaN        NaN        NaN
    1             2       A90  2021-03-15   202111    2021         12  ...         2.0        NaN  2021-04-08       NaN        NaN        NaN
    2             2       A90  2021-01-28   202104    2021         12  ...         2.0        NaN  2021-02-10       NaN        NaN        NaN
    3             2       A90  2021-02-10   202106    2021         12  ...         2.0        NaN  2021-03-22       NaN        NaN        NaN
    4             2       A90  2021-03-03   202109    2021         12  ...         2.0        NaN  2021-04-05       NaN        NaN        NaN
    ...         ...       ...         ...      ...     ...        ...  ...         ...        ...         ...       ...        ...        ...
    """

    # Estrutura para ler e armazenar os dataframes
    dataframes_list = []
    for dataset in datasets:
        archive = pd.read_csv(dataset, low_memory=False)
        df = pd.DataFrame(archive)
        dataframes_list.append(df)
    
    # Concateno todos os dataframes
    df_total = pd.concat(dataframes_list)

    return df_total

datasets = ['data/sinan_dengue_sample_2021.csv', 'data/sinan_dengue_sample_2022.csv', 'data/sinan_dengue_sample_2023.csv', 'data/sinan_dengue_sample_2024.csv']
df_total = concatenar_datasets(datasets=datasets)

# Salvo o dataset total na pasta data
df_total.to_csv('data/sinan_dengue_sample_total.csv', index=False)
