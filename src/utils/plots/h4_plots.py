"""Módulo com funções de plotagem da hipótese 4"""
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from config import *


def plot_proportions(proportions: tuple, filename: str = 'proporcoes_dengue.png') -> None:
    """
    Gera um gráfico de barras com a proporção de casos confirmados em ocupações rurais e não rurais.

    Parâmetros:
        proportions (tuple): Proporções de casos confirmados em ocupações não rurais e rurais.
        filename (str): Nome do arquivo para salvar o gráfico.
    """
    labels = ['Não Rurais', 'Rurais']
    data = {'Categoria': labels, 'Proporção (%)': proportions}
    df_proportions = pd.DataFrame(data)
    
    sns.barplot(data=df_proportions, x='Categoria', y='Proporção (%)')
    plt.title('Proporção de Casos Confirmados de Dengue')
    plt.ylabel('Proporção (%)')
    plt.xlabel('Tipo de Ocupação')
    plt.savefig(os.path.join(OUTPUT_FOLDER(), filename))
    plt.close()
