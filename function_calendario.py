import holidays
import pandas as pd

def estacao_do_ano(mes):
    """Determina a estação do ano com base no número do mês.

    Args:
        mes (int): Número do mês (1 a 12).

    Returns:
        str: Estação correspondente ('verão', 'outono', 'inverno', 'primavera').
    """
    if mes in [12, 1, 2]:
        return 'verão'
    elif mes in [3, 4, 5]:
        return 'outono'
    elif mes in [6, 7, 8]:
        return 'inverno'
    elif mes in [9, 10, 11]:
        return 'primavera'

def traduzir_dia_da_semana(dia):
    """Traduz o nome do dia da semana de inglês para português.

    Args:
        dia (str): Nome do dia da semana em inglês.

    Returns:
        str: Nome do dia da semana em português.
    """
    dias = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    return dias[dia]

def quinzena_do_mes(dia):
    """Determina em qual quinzena do mês o dia se encontra.

    Args:
        dia (int): Dia do mês (1 a 31).

    Returns:
        int: 1 se o dia é da primeira quinzena, 2 se o dia é da segunda quinzena.
    """
    if dia <= 15:
        return 1
    else:
        return 2

def criar_calendario(ano):
    """Cria um DataFrame representando um calendário para o ano especificado.

    Args:
        ano (int): Ano para o qual o calendário será criado.

    Returns:
        pandas.DataFrame: DataFrame contendo informações sobre cada dia do ano.
    """
    # Criar DataFrame com todas as datas do ano
    calendario = pd.DataFrame(pd.date_range(start=f"{ano}-01-01", end=f"{ano}-12-31"), columns=['data'])

    # Adicionar colunas de dia, semana, mês e ano
    calendario['dia'] = calendario['data'].dt.day
    calendario['semana'] = calendario['data'].dt.isocalendar().week
    calendario['mes'] = calendario['data'].dt.month
    calendario['ano'] = calendario['data'].dt.year

    # Adicionar coluna de dia da semana em inglês
    calendario['dia_da_semana_en'] = calendario['data'].dt.day_name()

    # Traduzir para português
    calendario['dia_da_semana'] = calendario['dia_da_semana_en'].apply(traduzir_dia_da_semana)

    # Adicionar coluna de feriados
    br_holidays = holidays.Brazil()
    rj_holidays = holidays.BR(state='RJ')
    sp_holidays = holidays.BR(state='SP')

    calendario['feriado_br'] = calendario['data'].apply(lambda x: x in br_holidays)
    calendario['feriado_rj'] = calendario['data'].apply(lambda x: x in rj_holidays)
    calendario['feriado_sp'] = calendario['data'].apply(lambda x: x in sp_holidays)

    # Adicionar coluna de estação do ano
    calendario['estacao'] = calendario['mes'].apply(estacao_do_ano)

    # Adicionar coluna de final de semana (sábado ou domingo)
    calendario['final_de_semana'] = calendario['data'].dt.weekday.isin([5, 6])

    # Adicionar coluna de dia útil
    calendario['dia_util'] = calendario['data'].isin(pd.bdate_range(start=f"{ano}-01-01", end=f"{ano}-12-31"))

    # Adicionar colunas de trimestre, quadrimestre e semestre
    calendario['trimestre'] = calendario['data'].dt.quarter
    calendario['quadrimestre'] = calendario['mes'].apply(lambda x: (x - 1) // 4 + 1)
    calendario['semestre'] = calendario['mes'].apply(lambda x: (x - 1) // 6 + 1)

    # Adicionar coluna de ano bissexto
    calendario['ano_bissexto'] = calendario['ano'].apply(lambda x: pd.Timestamp(f"{x}-02-29").is_leap_year)

    # Adicionar coluna de quinzena
    calendario['quinzena'] = calendario['dia'].apply(quinzena_do_mes)

    return calendario
    