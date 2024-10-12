import pandas as pd
import os
import sys
import concurrent.futures
sys.path.append(os.getcwd())
from src.config import DATASET_LOCAL, CHUNKS_SIZE, FILES_FOLDER
from src.filtering import filter_dataset


def processing_partial_dataset(filepath:str, usecols:list, chunksize:int=1) -> pd.DataFrame:
        """
        Function that will process the total dataframe costing less memory

        Args:
            filepath (str): Add the file path
            usecols (list): Add a list with the columns that you will use
            chunksize (int, optional): Define the size of the chunks. Defaults to 1.

        Returns:
            pd.DataFrame: Output the final processed dataframe

        >>> processing_total_dataframe("analise-dengue/data/sinan_dengue_sample_total.csv", usecols=colums_analyze, chunksize=30000)
        DT_SIN_PRI  FEBRE  MIALGIA  CEFALEIA  EXANTEMA  VOMITO  NAUSEA  CONJUNTVIT
        0   2021-02-20    1.0      1.0       1.0       1.0     1.0     1.0         2.0
        1   2021-02-20    1.0      2.0       1.0       1.0     2.0     2.0         1.0
        2   2021-01-12    1.0      1.0       1.0       2.0     2.0     1.0         2.0
        3   2021-01-29    1.0      2.0       1.0       2.0     2.0     1.0         2.0
        4   2021-02-26    1.0      2.0       1.0       1.0     2.0     1.0         2.0
        5   2021-02-15    1.0      1.0       1.0       1.0     1.0     2.0         1.0
        6   2021-01-27    1.0      2.0       1.0       2.0     2.0     2.0         1.0
        7   2021-02-17    1.0      2.0       1.0       2.0     2.0     1.0         2.0
        8   2021-02-05    1.0      2.0       1.0       2.0     2.0     2.0         2.0
        9   2021-03-08    1.0      2.0       1.0       2.0     2.0     1.0         2.0
        10  2021-02-15    1.0      1.0       1.0       2.0     2.0     2.0         2.0
        11  2021-03-08    1.0      1.0       1.0       1.0     2.0     2.0         2.0
        12  2021-02-15    1.0      1.0       1.0       2.0     2.0     1.0         2.0
        13  2021-01-23    1.0      1.0       1.0       2.0     2.0     1.0         1.0
        14  2021-03-25    1.0      2.0       1.0       2.0     2.0     2.0         2.0
        15  2021-03-07    1.0      1.0       1.0       2.0     2.0     1.0         2.0
        16  2021-03-05    1.0      2.0       1.0       1.0     2.0     2.0         2.0
        17  2021-01-23    1.0      1.0       1.0       2.0     2.0     2.0         1.0
        18  2021-01-15    1.0      1.0       1.0       1.0     2.0     1.0         1.0
        19  2021-01-08    2.0      2.0       1.0       2.0     2.0     1.0         2.0
        """

        # Read the dataset with chunks
        df = pd.read_csv(filepath, usecols=usecols, low_memory=False, chunksize=chunksize)

        # Set a empty list to keep the chunks
        df_list = []

        # Append each chunk in a list
        for chunk in df:
            df_list.append(chunk)

        # Concatenate the list in a dataframe
        df_total = pd.concat(df_list, ignore_index=True)

        return df_total


def processing_total_dataset() -> pd.DataFrame:
    """
    Function that will process the total dataset costing less memory, uses the columns specified on the CONFIG file

    Returns:
        pd.DataFrame: Output the final processed dataframe
    """
    try:
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
                
                merged_data = pd.merge(chunk, cities, on="SG_UF_NOT", how="left")

                threads_running.append(
                    executor.submit(
                        filter_dataset,
                        merged_data
                    )
                )

            concurrent.futures.wait(threads_running)

            for pending_thread in threads_running:
                dataframes.append(pending_thread.result())

        return pd.concat(dataframes)
    except Exception as e:
        print(e)
