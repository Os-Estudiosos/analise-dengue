import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.getcwd())
from src.config import DATASET_LOCAL
from src.utils.statistic import top_3_counts_numpy


def analyze_case_days_open(df: pd.DataFrame, date_limit: str, period:str='before') -> dict:
    """Analyzes the difference in days for each case and returns statistical information 
    for cases either before or after a given date limit (in this case, consider the day of the end).

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        date_limit (str): The date limit in the format 'YYYY-MM-DD'
        period (str, optional): Defines whether to analyze 'before' or 'after' the date limit. Default is 'before'.

    Raises:
        ValueError: Raises if required columns are missing
        ValueError: Raises if the date is at an invalid format
        ValueError: Raises if the period is not 'before' or 'after'

    Returns:
        dict: A dictionary containing the calculated statistics.
    """
    
    # Check if required columns are present
    required_columns = ['DT_ENCERRA', 'DT_NOTIFIC']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert date_limit to datetime and check validity
    try:
        date_limit = pd.to_datetime(date_limit)
    except ValueError:
        raise ValueError("Invalid date format for date_limit. Use 'YYYY-MM-DD'.")

    # Calculate the difference in days for each record
    df['number of days case open'] = (pd.to_datetime(df['DT_ENCERRA']) - pd.to_datetime(df['DT_NOTIFIC'])).dt.days
    
    # Remove rows where the number of days is negative
    df = df[df['number of days case open'] >= 0]

    # Filter records based on the 'period' parameter
    if period == 'before':
        df_filtered = df[pd.to_datetime(df['DT_NOTIFIC']) <= date_limit]
    elif period == 'after':
        df_filtered = df[pd.to_datetime(df['DT_NOTIFIC']) > date_limit]
    else:
        raise ValueError("Invalid period. Use 'before' or 'after'.")
    
    # Count the number of records
    record_count = df_filtered.shape[0]

    # Calculate sum and average
    sum_of_days = df_filtered['number of days case open'].sum()
    average_days = sum_of_days / record_count if record_count > 0 else 0  # Avoid division by zero

    # Calculate other statistics
    stats = {
        'std_dev': df_filtered['number of days case open'].std() if record_count > 0 else 0,
        'median': df_filtered['number of days case open'].median() if record_count > 0 else 0,
        'q1': df_filtered['number of days case open'].quantile(0.25) if record_count > 0 else 0,
        'q3': df_filtered['number of days case open'].quantile(0.75) if record_count > 0 else 0,
        'min': df_filtered['number of days case open'].min() if record_count > 0 else 0,
        'max': df_filtered['number of days case open'].max() if record_count > 0 else 0,
        'total_records': record_count,
        'sum_of_days': sum_of_days,
        'average_days': average_days
    }

    return stats


def hypothesis5(df: pd.DataFrame):
    columns_list = ['DT_NOTIFIC', 'DT_SIN_PRI', 'DT_INVEST', 'DT_CHIK_S1', 'DT_CHIK_S2', 'DT_PRNT', 
                    'DT_SORO', 'DT_NS1', 'DT_VIRAL', 'DT_PCR', 'DT_INTERNA', 'DT_OBITO', 
                    'DT_ENCERRA', 'DT_ALRM', 'DT_GRAV', 'DT_DIGITA']

    df_date = df[columns_list]

    #take the data
    #print(analyze_case_days_open(df_date, '2022-11-30', period='after'))
    #print(analyze_case_days_open(df_date, '2022-11-30', period='before'))

    # List of columns to check and count(exams)
    columns = ['DT_CHIK_S1', 'DT_CHIK_S2', 'DT_SORO', 'DT_NS1', 'DT_PRNT', 'DT_VIRAL', 'DT_PCR', 'DT_ALRM', 'DT_GRAV']

    # Using the data to calculate the 3 most taken
    top_3_results_numpy = top_3_counts_numpy(df_date, columns)
    #print(top_3_results_numpy)

    # With the most taken exam, we do the analysis: Is there a greater difference in days between the most taken exam (dengue) during the post-COVID and COVID periods?
    # Doing the same analytics, but now just with the people who did the most taken exam
    df_filtered_to_ns1 = df_date.dropna(subset=['DT_NS1'])

    #calculate to confirmate
    rows_did_ns1 = df_filtered_to_ns1.shape[0]

    #take the data
    #print(analyze_case_days_open(df_filtered_to_ns1, '2022-11-30', period='before'))
    #print(analyze_case_days_open(df_filtered_to_ns1, '2022-11-30', period='after'))

    df['number of days case open'] = (pd.to_datetime(df['DT_ENCERRA']) - pd.to_datetime(df['DT_NOTIFIC'])).dt.days
    df_to_plot = df[['number of days case open', 'DT_NOTIFIC']]

    df_filtered_to_ns1['number of days case open'] = (pd.to_datetime(df['DT_ENCERRA']) - pd.to_datetime(df['DT_NOTIFIC'])).dt.days
    df_filtered_to_ns1_plot = df_filtered_to_ns1[['DT_NS1', 'number of days case open']]

    #returns the dataframe to plot with seaborn
    return df_to_plot, df_filtered_to_ns1_plot