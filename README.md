# Trabalho A1 de Análise e Visualização de Dados

Esse trabalho tem como objetivo analisar e responder hipóteses acerca do dataset disponibilizado pelo SINAN (Sistema de Informação de Agravos de Notificação) sobre casos de Dengue nos anos de 2021-2024

## Instalação do Projeto

`pip install -r ./requirements.txt`

## Estrutura do Projeto

```
|- public
|- data
|- files
|- output
|- src
    |- config
    |- filtering
    |- hypothesis
    |- utils
|- test
```

- **Data**: Arquivos com os datasets a serem analisados
- **Files**: Arquivos que foram úteis para o projeto
- **Output**: Arquivos resultados da execução das funções de hipótese
- **Src**: Arquivos principais
  - **Config**: Funções e variáveis de configuração
  - **Utils**: Funções que podem ser úteis para desenvolvimento
  - **Hypothesis**: Módulo que tem as funções principais relacionadas a cada hipótese
  - **Filtering**: Módulo de filtrgem do dataset
- **Test**: Funções de teste unitário

## Como acessar os datasets?

Vá até o link: [Kaggle](https://www.kaggle.com/datasets/henriquerezermosqur/dados-sus-sinan-dengue-2021-2024), clique em Download e extraia os datasets na pasta **data** (são 4, relativos aos anos de 2021, 2022, 2023 e 2024). Depois, acesse o seguinte link: [Drive](https://drive.google.com/drive/folders/11MEDd8xSyRuERJ5zT6JofruelcOklTZk) e faça download do dataset unificado, e coloque no mesmo local

## Como realizar os testes?

Cada arquivo de hipótese deve ser executado separadamente, pois executar todos juntos é muito custoso e demora por conta do tamanho do dataset!

Linux:

```
python3 src/hypothesis_{i}py
```

Python:

```
python src\hypothesis_{i}.py
```
