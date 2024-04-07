## Função de transformação de data e hora
Versão 1.0.0

## Explicação das principais partes do código:

1 - estacao_do_ano(mes): Retorna a estação do ano com base no número do mês.

2 - traduzir_dia_da_semana(dia): Traduz o nome do dia da semana de inglês para português.

3 - quinzena_do_mes(dia): Determina em qual quinzena do mês o dia se encontra (primeira ou segunda).

4 - criar_calendario(ano): Cria um DataFrame pandas contendo informações sobre cada dia do ano especificado, incluindo detalhes como dia da semana, mês, se é feriado, estação do ano, etc.

O código usa a biblioteca holidays para verificar feriados no Brasil, no estado do Rio de Janeiro (RJ) e em São Paulo (SP). O resultado final é um DataFrame que pode ser utilizado para análise e manipulação de dados relacionados ao calendário para o ano especificado.