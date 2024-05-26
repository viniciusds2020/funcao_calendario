# Função de Transformação de Data e Hora

**Versão 1.0.0**

## Descrição

Este repositório contém uma função de transformação de data e hora, projetada para criar um DataFrame pandas com informações detalhadas sobre cada dia de um ano especificado. O DataFrame inclui informações como dia da semana, mês, se é feriado, estação do ano e mais. A função utiliza a biblioteca `holidays` para verificar feriados no Brasil, especificamente nos estados do Rio de Janeiro (RJ) e São Paulo (SP).

## Funcionalidades

### 1. estacao_do_ano(mes)

```python
def estacao_do_ano(mes):
    """
    Retorna a estação do ano com base no número do mês.

    Parâmetros:
        mes (int): Número do mês (1-12).

    Retorna:
        str: Estação do ano correspondente ('Verão', 'Outono', 'Inverno' ou 'Primavera').
    """
```
Esta função determina a estação do ano (Verão, Outono, Inverno ou Primavera) com base no número do mês fornecido.

### 2. traduzir_dia_da_semana(dia)

```python
def traduzir_dia_da_semana(dia):
    """
    Traduz o nome do dia da semana de inglês para português.

    Parâmetros:
        dia (str): Nome do dia da semana em inglês.

    Retorna:
        str: Nome do dia da semana em português.
    """
```
Esta função traduz os dias da semana de inglês para português.

### 3. quinzena_do_mes(dia)

```python
def quinzena_do_mes(dia):
    """
    Determina em qual quinzena do mês o dia se encontra (primeira ou segunda).

    Parâmetros:
        dia (int): Dia do mês (1-31).

    Retorna:
        str: 'Primeira quinzena' ou 'Segunda quinzena'.
    """
```
Esta função identifica se um determinado dia do mês está na primeira ou segunda quinzena.

### 4. criar_calendario(ano)

```python
def criar_calendario(ano):
    """
    Cria um DataFrame pandas contendo informações sobre cada dia do ano especificado.

    Parâmetros:
        ano (int): Ano para o qual o calendário será criado.

    Retorna:
        pandas.DataFrame: DataFrame contendo informações detalhadas de cada dia do ano.
    """
```
Esta função gera um DataFrame pandas que inclui:
- Dia da semana
- Mês
- Se é feriado (considerando feriados nacionais e específicos para RJ e SP)
- Estação do ano
- Quinzena do mês
- Outros detalhes relevantes

## Dependências

Certifique-se de ter as seguintes bibliotecas Python instaladas:

```sh
pip install pandas holidays
```

## Exemplo de Uso

```python
import pandas as pd
from holidays import Brazil

# Supondo que as funções descritas acima estão definidas em um módulo chamado calendario

from calendario import estacao_do_ano, traduzir_dia_da_semana, quinzena_do_mes, criar_calendario

# Criar o calendário para o ano de 2024
calendario_2024 = criar_calendario(2024)

# Exibir as primeiras linhas do DataFrame
print(calendario_2024.head())
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais informações.

---

**Autor:** Vinicius de Sousa 
**Contato:** viniciusds1020@gmail.com
