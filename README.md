# Trabalho A1 de Análise e Visualização de Dados

Esse trabalho tem como objetivo analisar e responder hipóteses acerca do dataset disponibilizado pelo SINAN (Sistema de Informação de Agravos de Notificação) sobre casos de Dengue nos anos de 2021-2024, discorrendo sobre impactos em vários setores da sociedade.

## Clonando o repositório

Vá até o local desejado e execute o comando no terminal do *git bash*:
```bash
git clone https://github.com/Os-Estudiosos/analise-dengue.git
```

## Instalação do Projeto

Execute o comando para realizarf o download das bibliotecas utilizadas no projeto (recomendamos, antes de instalar o projeto, criar um [VIRTUAL ENVIROMENT](https://dev.to/franciscojdsjr/guia-completo-para-usar-o-virtual-environment-venv-no-python-57bo) para melhor organização):

```bash
pip install -r ./requirements.txt
```

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

Vá até o link: [Kaggle](https://www.kaggle.com/datasets/henriquerezermosqur/dados-sus-sinan-dengue-2021-2024), clique em Download e extraia os datasets na pasta **data** (são 4, relativos aos anos de 2021, 2022, 2023 e 2024). Depois, acesse o seguinte link: [Drive](https://drive.google.com/drive/folders/11MEDd8xSyRuERJ5zT6JofruelcOklTZk) e faça download do dataset unificado, e coloque no mesmo local.

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

Algumas hipóteses geram gráficos, arquivos de CSV, e outras apenas fazem alguns cálculos, não necessariamente mostrando algo na pasta output.

## Sobre o Paper

O Short Paper da análise realizada (tanto o código em *.Tex*, quanto o *PDF*), pode ser encontrado dentro da pasta _**Paper**_.
Nele, você encontrará visualizações feitas de autoria do grupo, uma contextualização da situação dos casos de dengue no Brasil e por qual razão é importante fazermos uma análise dos dados coletados e os raciocícios desenvolvidos em cada hipótese.
As hipóteses trabalhadas são:

- *Quais são os conjuntos de sintomas que mais levam à internação ou óbito do paciente?*
- *Existe um padrão temporal na ocorrência dos casos de dengue?A Região Norte do Brasil apresentou o maior número de casos de dengue? Em qual localidade a taxa de mortalidade é mais elevada?*
- *Sintomas mais graves se manifestam em um público mais velho?*
- *Pessoas em ocupações relacionadas a zona rural têm maiores chances de contrair a doença?*
- *Nos períodos de covid, houve alguma mudança em relação à quantidade de pessoas diagnosticadas com dengue? Além disso, nesses períodos, o tempo de demora entre a entrada no hospital e a hora do exame aumentou?*

## AVISO

A maioria das hipóteses demoram de um a cinco minutos para rodar por conta da enormidade da base de dados trabalhada. Além disso, nenhuma visualização e/ou tabela será mostrada na tela e/ou no terminal, podendo serem esncontradas na pasta _**Output**_.
Além disso, para efeitos de comparação, clique no link para ver o repositório antigo: [Repositório Antigo](https://github.com/jaopredo/analise-dengue).
