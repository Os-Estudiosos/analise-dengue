import pandas as pd
import itertools

MAXSETSIZE = 8

def cleanDataFrame(df):
    columns = "VOMITO FEBRE MIALGIA CEFALEIA EXANTEMA NAUSEA DOR_COSTAS CONJUNTVIT ARTRITE ARTRALGIA PETEQUIA_N LEUCOPENIA DOR_RETRO HEMATOLOG HEPATOPAT RENAL HIPERTENSA HOSPITALIZ EVOLUCAO".split(' ')
    symptons = df[columns]
    
    hospitaliz = symptons.dropna(subset=['HOSPITALIZ']).drop(['EVOLUCAO'], axis = 1)
    evolucao = symptons.dropna(subset=['EVOLUCAO']).drop(['HOSPITALIZ'], axis = 1)
    
    hospitaliz.to_csv('hospitaliz.csv')
    evolucao.to_csv('evolucao.csv')
    print(hospitaliz.head())
    print(evolucao.head())


def doIT(df, values):
    
    symptoms_dict = {
        "VOMITO": "Vomiting",
        "FEBRE": "Fever",
        "MIALGIA": "Myalgia",
        "CEFALEIA": "Headache",
        "EXANTEMA": "Exanthem",
        "NAUSEA": "Nausea",
        "DOR_COSTAS": "Back Pain",
        "CONJUNTVIT": "Conjunctivitis",
        "ARTRITE": "Arthritis",
        "ARTRALGIA": "Arthralgia",
        "PETEQUIA_N": "Petechiae",
        "LEUCOPENIA": "Leukopenia",
        "DOR_RETRO": "Retro Pain",
        "HEMATOLOG": "Hematological",
        "HEPATOPAT": "Hepatopathy",
        "RENAL": "Renal",
        "HIPERTENSA": "Hypertension",
        "ACIDO_PEPT": "Peptic Acid"
    }
    
    name = df.columns[-1]
    symptoms = "VOMITO FEBRE MIALGIA CEFALEIA EXANTEMA NAUSEA DOR_COSTAS CONJUNTVIT ARTRITE ARTRALGIA PETEQUIA_N LEUCOPENIA DOR_RETRO HEMATOLOG HEPATOPAT RENAL HIPERTENSA".split(' ')
    
    
    setsPoints = []

    for n in range(MAXSETSIZE):
        dicio = {}
        subsets = list(itertools.combinations(symptoms, n+1))
        for set in subsets:
            dicio[set] = 0
        setsPoints.append(dicio)

    for index, row in df.iterrows():
        if row[name] not in values:
            continue

        positive = []
        for symptom in symptoms:
            if (row[symptom] == 1):
                positive.append(symptom)        

        for n in range(MAXSETSIZE):
            if len(positive) < n :
                continue

            subsets = list(itertools.combinations(positive, n+1))
            for set in subsets:
                setsPoints[n][set] += 1
    
    final = []
    for dicio in setsPoints:
        diTemp = {}
        for set, value in dicio.items():
            l = []
            for symptom in set:
                l.append(symptoms_dict[symptom])
            diTemp[' | '.join(l)] = value
        final.append(diTemp)    

    for n in range(MAXSETSIZE):
        final[n] = dict(sorted(final[n].items(), key=lambda item: item[1]))
        for set,value in final[n].items():
            print(f"{set} = {value} ", end = '\n\n')          
    return final

#hospitaliz = pd.read_csv('hospitaliz.csv')
evolucao = pd.read_csv('evolucao.csv')
#hospitalizFinal = doIT(hospitaliz,[1])

evolucaoFinal = doIT(evolucao,[2])
print()
print("The symptoms that kills the most : ")
for n in range(MAXSETSIZE):
    print(n+1,end = '\n\n')
    for i in range(5):
        print(list(evolucaoFinal[n].items())[-(i+1)])
      
print("\n\n")
print("The symptoms that kills the less : ")
for n in range(MAXSETSIZE):
    print(n+1,end = '\n\n')
    for i in range(5):
        print(list(evolucaoFinal[n].items())[(i)])