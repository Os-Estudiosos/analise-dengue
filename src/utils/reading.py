import pandas as pd
import os
import sys
import concurrent.futures
sys.path.append(os.getcwd())
from src.config import DATASET_LOCAL, CHUNKS_SIZE, FILES_FOLDER
from src.filtering import filter_dataset


def processing_total_dataset(complete: bool = True, concatenated_dfs: bool = False) -> pd.DataFrame:
    """Função que processa todo o dataframe

    Args:
        hypothesis (int): Indica a hipótese que vai ser processada.
        complete (bool, optional): Função que indica se eu vou retornar uma lista de chunks (False) ou um dataframe completo (True). Defaults to True.
        concatenated_dfs (bool, optional): Função que indica se eu retorno um dataframe auxiliares ou não. Defaults to False.

    Returns:
        pd.DataFrame|list[pd.DataFrame]: Lista de dataframes ou um dataframe completo
    """
    # Read the dataset with chunks
    chunks = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_total.csv'), low_memory=False, chunksize=CHUNKS_SIZE)
    
    # Load the file with the uf codes and acronyms
    cities = pd.read_csv(os.path.join(FILES_FOLDER(), "ufs.csv"), usecols=["SG_UF_NOT","SIGLA_UF"], low_memory=False)

    dataframes: list[pd.DataFrame] = []

    # Create the multithread structure to process each chunk
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threads_running: list[concurrent.futures.Future] = []

        for chunk in chunks:
            # Mergin the data on the acronyms
            if concatenated_dfs:
                merged_data = pd.merge(chunk, cities, on="SG_UF_NOT", how="left")
                threads_running.append(
                    executor.submit(
                        filter_dataset,
                        merged_data
                    )
                )
            else:
                threads_running.append(
                    executor.submit(
                        filter_dataset,
                        chunk
                    )
                )

        concurrent.futures.wait(threads_running)

        for pending_thread in threads_running:
            dataframes.append(pending_thread.result())

    if complete:
        return pd.concat(dataframes)
    else:
        return dataframes
