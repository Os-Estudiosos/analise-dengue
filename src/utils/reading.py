import pandas as pd
import os
import sys
import concurrent.futures
sys.path.append(os.getcwd())
from src.config import DATASET_LOCAL, CHUNKS_SIZE, REQUIRED_COLUMNS
from src.filtering import filter_dataset
from src.utils.timing import measure_function_execution


def processing_total_dataset() -> pd.DataFrame:
    """
    Function that will process the total dataset costing less memory, uses the columns specified on the CONFIG file

    Returns:
        pd.DataFrame: Output the final processed dataframe
    """
    try:
        # Read the dataset with chunks
        chunks = pd.read_csv(os.path.join(DATASET_LOCAL(), 'sinan_dengue_sample_total.csv'), low_memory=False, chunksize=CHUNKS_SIZE)

        dataframes: list[pd.DataFrame] = []

        # Create the multithread structure to process each chunk
        with concurrent.futures.ThreadPoolExecutor() as executor:
            threads_running: list[concurrent.futures.Future] = []

            for chunk in chunks:
                threads_running.append(
                    executor.submit(
                        filter_dataset,
                        chunk
                    )
                )

            concurrent.futures.wait(threads_running)

            for pending_thread in threads_running:
                dataframes.append(pending_thread.result())

        return pd.concat(dataframes)
    except Exception as e:
        print(e)
