import pandas as pd
import numpy as np
import os 

way = r"C:\Users\thalis\tudomeu\faculdade\2_semestre\lp\analisedengue\analise-dengue\data\sinan_dengue_sample_total.csv"

# Checking if the path exists
if not os.path.exists(way):
    raise FileNotFoundError(f"The file was not found at the path: {way}")

# Reading the CSV file
df = pd.read_csv(way, low_memory=False)

# Set a list with the important dates
columns_list = ['DT_NOTIFIC', 'DT_SIN_PRI', 'DT_INVEST', 'DT_CHIK_S1', 'DT_CHIK_S2', 'DT_PRNT', 
                 'DT_SORO', 'DT_NS1', 'DT_VIRAL', 'DT_PCR', 'DT_INTERNA', 'DT_OBITO', 
                 'DT_ENCERRA', 'DT_ALRM', 'DT_GRAV', 'DT_DIGITA']
df_date = df[columns_list]

def analyze_case_open_days_v2(df, date_limit, period='before'):
    """
    Analyzes the difference in days for each case and returns statistical information 
    for cases either before or after a given date limit (in this case, consider the day of the end).
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    date_limit (str): The date limit in the format 'YYYY-MM-DD'.
    period (str): Defines whether to analyze 'before' or 'after' the date limit. Default is 'before'.
    
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

print(analyze_case_open_days_v2(df_date, '2022-11-30', period='after'))
print(analyze_case_open_days_v2(df_date, '2022-11-30', period='before'))

# Create this function to filter the most taken exam
def top_3_counts_numpy(df, columns):
    """
    Analyzes the DataFrame to identify the top 3 most taken exams based on non-null values.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the exam data.
    columns (list of str): A list of column names to compare for counting non-null values.

    Returns:
    list: A list of tuples, each containing the column name and its respective count of non-null values,
    representing the top 3 most taken exams.
    """
    # Check if the provided columns are valid
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Missing column in DataFrame: {col}")

    counts = {}
    # Loop over each column and count non-null values using NumPy
    for col in columns:
        # Convert the column to a NumPy array and count non-nan values
        column_data = df[col].to_numpy()
        counts[col] = np.count_nonzero(~pd.isna(column_data))
    
    # Sort the counts dictionary by values (counts) in descending order and return the top 3
    top_3 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return top_3

# List of columns to check
columns = ['DT_CHIK_S1', 'DT_CHIK_S2', 'DT_SORO', 'DT_NS1', 'DT_PRNT', 'DT_VIRAL', 'DT_PCR', 'DT_ALRM', 'DT_GRAV']

# Using the same mock data for demonstration
top_3_results_numpy = top_3_counts_numpy(df_date, columns)
print(top_3_results_numpy)

# With the most taken exam, we do the analysis: Is there a greater difference in days between the most taken exam (dengue) during the post-COVID and COVID periods?
# Doing the same analytics, but now just with the people who did the most taken exam
df_filtered_to_ns1 = df_date.dropna(subset=['DT_NS1'])
rows_did_ns1 = df_filtered_to_ns1.shape[0] 
print(analyze_case_open_days_v2(df_filtered_to_ns1, '2022-11-30', period='before'))
print(analyze_case_open_days_v2(df_filtered_to_ns1, '2022-11-30', period='after'))
