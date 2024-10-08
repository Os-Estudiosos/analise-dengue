# Trabalho A1 de Análise e Visualização de Dados
Inserir descrição do Trabalho

## Instalação do Projeto
`pip install -r ./requirements.txt`

## Estrutura do Projeto
```
|- public
|- data
|- src
    |- view
    |- utils
|- test
```
- **Data**: Arquivos com os datasets a serem analisados
- **Public**: Outros arquivos sobre o projeto
- **Source**: Arquivos principais
    - **Utils**: Funções que podem ser úteis para desenvolvimento
    - **View**: Funções relacionadas ao plot e visualização dos dados
- **Test**: Funções de teste unitário

## Como acessar os datasets?
Vá até o link: https://www.kaggle.com/datasets/henriquerezermosqur/dados-sus-sinan-dengue-2021-2024.
Clique em Download e extraia os datasets (são 4, relativos aos anos de 2021, 2022, 2023 e 2024).
Crie uma pasta chamada 'data' na raiz do repositório e cole os datasets nela.


## Como realizar os testes?
Executar o seguinte arquivo?
```
python3 test/main.py
```
