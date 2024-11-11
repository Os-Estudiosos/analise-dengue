import pandas as pd
import concurrent.futures
import os
import sys
sys.path.append(os.getcwd())
from src.hypothesis.hypothesis_3 import hypothesis3
from src.config import *
from src.filtering import filter_dataset
from src.utils.timing import measure_function_execution
# from src.utils.reading import processing_total_dataset


def hyp3_runner(chunk: pd.DataFrame):
    df = filter_dataset(chunk)
    # print(df)
    hypothesis3(chunk)


@measure_function_execution
def main(year):
    try:
        # Vou ler o dataset por chunks
        chunks = pd.read_csv(os.path.join(DATASET_LOCAL(), f'sinan_dengue_sample_{year}.csv'), low_memory=False, chunksize=CHUNKS_SIZE)
        
        # Carrego o arquivo com UF e acrônimos
        cities = pd.read_csv(os.path.join(FILES_FOLDER(), "ufs.csv"), usecols=["SG_UF_NOT","SIGLA_UF"], low_memory=False)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            threads_running: list[concurrent.futures.Future] = []

            for chunk in chunks:  # Para cada chunk
                merged_data = pd.merge(chunk, cities, on="SG_UF_NOT", how="left")
                # Eu junto o dataset das siglas com o dataset original (Chunk)

                threads_running.append(
                    executor.submit(
                        hyp3_runner,
                        merged_data
                    )
                )

            concurrent.futures.wait(threads_running)

            for pending_thread in threads_running:
                pending_thread.result()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(2024)
