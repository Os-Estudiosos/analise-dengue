import pandas as pd
import itertools
import numpy as np
import os
import sys
sys.path.append(os.getcwd())
from src.config import MAX_SET_SIZE, OUTPUT_FOLDER


def symptomsSets(df, values):
    """
    Organizes symptoms into sets of various sizes and counts occurrences.

    Parameters:
        df (DataFrame): A data frame containing symptom data.
        values (list): A list of values to filter the data frame based on the last column.

    Returns:
        list: A list containing up to MAXSETSIZE dictionaries. Each dictionary has symptom sets as keys and their occurrences as values.
    """
    # Dictionary for mapping symptom codes to their readable names
    symptoms_dict = {
        "VOMITO": "Vômito",
        "FEBRE": "Febre",
        "MIALGIA": "Mialgia",
        "CEFALEIA": "Cefaleia",
        "EXANTEMA": "Exantema",
        "NAUSEA": "Náusea",
        "DOR_COSTAS": "Dor nas Costas",
        "CONJUNTVIT": "Conjuntivite",
        "ARTRITE": "Artrite",
        "ARTRALGIA": "Artralgia",
        "PETEQUIA_N": "Petequias",
        "LEUCOPENIA": "Leucopenia",
        "DOR_RETRO": "Dor Retro",
        "HEMATOLOG": "Hematológico",
        "HEPATOPAT": "Hepatopatia",
        "RENAL": "Renal",
        "HIPERTENSA": "Hipertensão",
    }  

    name = df.columns[-1]  # Extract the last column name for filtering
    symptoms = "VOMITO FEBRE MIALGIA CEFALEIA EXANTEMA NAUSEA DOR_COSTAS CONJUNTVIT ARTRITE ARTRALGIA PETEQUIA_N LEUCOPENIA DOR_RETRO HEMATOLOG HEPATOPAT RENAL HIPERTENSA".split(' ') 
    setsPoints = []  # Stores the occurrence counts of each symptom set.

    # Initialize dictionaries for each set size
    for n in range(MAX_SET_SIZE):
        dicio = {}  # Dictionary to hold counts for symptom sets of size 'n'
        subsets = list(itertools.combinations(symptoms, n + 1))  # Generate combinations of symptoms of size 'n + 1'
        for symptom_set in subsets:
            dicio[symptom_set] = 0  # Initialize count for each symptom set to zero

        setsPoints.append(dicio)  # Append the initialized dictionary to the list

    # Count occurrences of symptom sets in the DataFrame
    for index, row in df.iterrows():
        if row[name] not in values:  # Ignore rows where the last column value is not in the specified values
            continue

        positive = []
        for symptom in symptoms:
            if pd.notnull(row[symptom]) and row[symptom] == 1:  # Check if the symptom is present
                positive.append(symptom)        

        # Update counts for each set size based on positive symptoms
        for n in range(MAX_SET_SIZE):
            if len(positive) < n + 1:  # Ensure enough positive symptoms to form sets
                continue

            subsets = list(itertools.combinations(positive, n + 1))  # Generate symptom combinations from positive symptoms
            for symptom_set in subsets:
                setsPoints[n][symptom_set] += 1  # Increment occurrence count for the symptom set
    
    final = []
    # Format the results into a readable form
    for dicio in setsPoints:
        diTemp = {}
        for symptom_set, value in dicio.items():
            symptoms_list = [symptoms_dict[symptom] for symptom in symptom_set]  # Convert symptom codes to readable names
            diTemp[' | '.join(symptoms_list)] = value  # Join names into a single string as key
        final.append(diTemp)    

    # Sort the symptom sets by occurrences
    for n in range(MAX_SET_SIZE):
        final[n] = dict(sorted(final[n].items(), key=lambda item: item[1]))  
     
    return final  


def finalAnswer(hospitalizFinal, evolucaoFinal):
    """
    Combines hospitalization and evolution data for final analysis.

    Parameters:
        hospitalizFinal (list): List of dictionaries for hospitalization.
        evolucaoFinal (list): List of dictionaries for evolution.

    Returns:
        list: A list of combined results, sorted by death ratios.
    """
    final = []
    for n in range(MAX_SET_SIZE):
        tempDictionary = {}
        for symptom_set, deaths in evolucaoFinal[n].items():
            tempDictionary[symptom_set] = [deaths, hospitalizFinal[n][symptom_set]]  # Combine deaths and hospitalizations

        tempDictionary = dict(sorted(tempDictionary.items(), key=lambda item: item[1]))  # Sort by occurrences
        final.append(tempDictionary)
    
    return final


def hypothesis1(df: pd.DataFrame):
    """
    Processes the data to generate symptoms sets and their statistics.

    Parameters:
        path (str): The path to the CSV file containing the data.

    Returns:
        None: Outputs the results to a CSV file and prints the DataFrame.
    """
    try:
        # Clean the DataFrame and get symptom sets for hospitalizations and evolutions
        # Clean the data frame for hospitalizations and evolutions
        hospitaliz = df.dropna(subset=['HOSPITALIZ']).drop(['EVOLUCAO'], axis=1)  # Removes rows with NaN in 'HOSPITALIZ' and drops 'EVOLUCAO'.
        evolucao = df.dropna(subset=['EVOLUCAO']).drop(['HOSPITALIZ'], axis=1)  # Removes rows with NaN in 'EVOLUCAO' and drops 'HOSPITALIZ'.

        hospitalizFinal = symptomsSets(hospitaliz, [1])  
        evolucaoFinal = symptomsSets(evolucao, [2])  

        final = finalAnswer(hospitalizFinal, evolucaoFinal)  # Combine results
        
        # Process and output results for each set size
        for index, dictionary in enumerate(final):
            result_list = []  # List to store formatted results
            dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1][0] / item[1][1] if item[1][1] > 0 else 0))  # Sort by death ratio
            for key, value in dictionary.items():
                # Append the symptom set, deaths, occurrences, and ratio percentage to the results list
                result_list.append([key, value[0], value[1], (value[0] / value[1] * 100) if value[1] > 0 else 0])
            
            # Convert the results list to a NumPy array and then to a DataFrame
            data = np.array(result_list)
            dataFrame = pd.DataFrame(data, columns=['Symptoms Set', 'Deaths', 'Occurrences', 'Ratio %'])
            print(dataFrame.head())  # Print the first few rows of the DataFrame
            dataFrame.to_csv(os.path.join(OUTPUT_FOLDER(), f'SymptomsSetsofSize{index + 1}.csv'), index=False)  # Output the results to a CSV file
    
    except Exception as e:
        print(f"Error: An unexpected error occurred during processing: {e}")
