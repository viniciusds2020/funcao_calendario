# -*- coding: utf-8 -*-
"""
Calendar transformation utilities.

Builds a pandas DataFrame with rich date/time attributes for each day
of a given year, including Brazil (BR) holidays for RJ, SP, ES, MG, PR, SC e RS.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd
import holidays


@dataclass(frozen=True)
class SeasonWindow:
    name: str
    start: tuple[int, int]  # (month, day)
    end: tuple[int, int]


# Southern hemisphere seasons (approximate, fixed dates)
SEASONS = [
    SeasonWindow("verao", (12, 21), (3, 20)),
    SeasonWindow("outono", (3, 21), (6, 20)),
    SeasonWindow("inverno", (6, 21), (9, 22)),
    SeasonWindow("primavera", (9, 23), (12, 20)),
]


def _season_for(d: date) -> str:
    m, day = d.month, d.day
    # Summer spans year boundary
    if (m == 12 and day >= 21) or (m <= 3 and (m < 3 or day <= 20)):
        return "verao"
    if (m == 3 and day >= 21) or (3 < m < 6) or (m == 6 and day <= 20):
        return "outono"
    if (m == 6 and day >= 21) or (6 < m < 9) or (m == 9 and day <= 22):
        return "inverno"
    return "primavera"


def _week_of_month(ts: pd.Timestamp) -> int:
    # Week of month starting at 1
    first = ts.replace(day=1)
    return int((ts.day + first.weekday()) // 7 + 1)


def build_calendar_dataframe(year: int, tz: str = "America/Sao_Paulo") -> pd.DataFrame:
    """
    Build a rich calendar DataFrame for a given year.

    Columns include:
    - core date fields
    - week/month/quarter boundaries
    - ISO week/year, week of month
    - season (southern hemisphere)
    - holidays for BR (national), RJ and SP
    - business day flags
    - progress metrics within month/year
    """
    if year < 1:
        raise ValueError("year must be >= 1")

    idx = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D", tz=tz)
    df = pd.DataFrame({"data": idx})

    df["data_local"] = df["data"].dt.tz_convert(tz).dt.normalize()
    df["ano"] = df["data_local"].dt.year
    df["mes"] = df["data_local"].dt.month
    df["dia"] = df["data_local"].dt.day
    df["dia_do_ano"] = df["data_local"].dt.dayofyear
    df["numero_dia_semana"] = df["data_local"].dt.weekday
    # Nomes em portugues (BR) sem depender de locale do SO
    weekday_pt = {
        0: "segunda-feira",
        1: "terca-feira",
        2: "quarta-feira",
        3: "quinta-feira",
        4: "sexta-feira",
        5: "sabado",
        6: "domingo",
    }
    month_pt = {
        1: "janeiro",
        2: "fevereiro",
        3: "marco",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }
    df["nome_dia_semana"] = df["numero_dia_semana"].map(weekday_pt)
    df["fim_de_semana"] = df["numero_dia_semana"].isin([5, 6])

    df["nome_mes"] = df["mes"].map(month_pt)
    df["trimestre"] = df["data_local"].dt.quarter
    df["semestre"] = ((df["mes"] - 1) // 6 + 1).astype(int)

    df["inicio_mes"] = df["data_local"].dt.is_month_start
    df["fim_mes"] = df["data_local"].dt.is_month_end
    df["inicio_trimestre"] = df["data_local"].dt.is_quarter_start
    df["fim_trimestre"] = df["data_local"].dt.is_quarter_end
    df["inicio_ano"] = df["data_local"].dt.is_year_start
    df["fim_ano"] = df["data_local"].dt.is_year_end

    df["dias_no_mes"] = df["data_local"].dt.days_in_month
    df["semana_do_ano"] = df["data_local"].dt.isocalendar().week.astype(int)
    df["ano_iso"] = df["data_local"].dt.isocalendar().year.astype(int)
    df["semana_do_mes"] = df["data_local"].apply(_week_of_month)

    df["inicio_mes_data"] = df["data_local"].dt.to_period("M").dt.start_time
    df["fim_mes_data"] = df["data_local"].dt.to_period("M").dt.end_time
    df["inicio_semana_data"] = df["data_local"].dt.to_period("W").dt.start_time
    df["fim_semana_data"] = df["data_local"].dt.to_period("W").dt.end_time

    df["dias_desde_inicio_mes"] = (df["data_local"].dt.day - 1)
    df["dias_ate_fim_mes"] = (df["dias_no_mes"] - df["data_local"].dt.day)
    df["dias_ate_fim_ano"] = (
        pd.Timestamp(f"{year}-12-31", tz=tz) - df["data_local"]
    ).dt.days

    year_days = 366 if pd.Timestamp(f"{year}-12-31").is_leap_year else 365
    df["progresso_ano"] = df["dia_do_ano"] / year_days
    df["progresso_mes"] = (df["dias_desde_inicio_mes"] + 1) / df["dias_no_mes"]
    df["ano_bissexto"] = pd.Timestamp(f"{year}-01-01").is_leap_year

    # Seasons
    df["estacao"] = df["data_local"].dt.date.apply(_season_for)

    # Holidays
    br = holidays.Brazil(years=[year])
    rj = holidays.Brazil(subdiv="RJ", years=[year])
    sp = holidays.Brazil(subdiv="SP", years=[year])
    mg = holidays.Brazil(subdiv="MG", years=[year])
    es = holidays.Brazil(subdiv="ES", years=[year])
    rs = holidays.Brazil(subdiv="RS", years=[year])
    sc = holidays.Brazil(subdiv="SC", years=[year])
    pr = holidays.Brazil(subdiv="PR", years=[year])

    df["feriado_br"] = df["data_local"].dt.date.isin(br)
    df["nome_feriado_br"] = df["data_local"].dt.date.map(br).fillna("")

    df["feriado_rj"] = df["data_local"].dt.date.isin(rj)
    df["nome_feriado_rj"] = df["data_local"].dt.date.map(rj).fillna("")

    df["feriado_sp"] = df["data_local"].dt.date.isin(sp)
    df["nome_feriado_sp"] = df["data_local"].dt.date.map(sp).fillna("")

    df["feriado_mg"] = df["data_local"].dt.date.isin(mg)
    df["nome_feriado_mg"] = df["data_local"].dt.date.map(mg).fillna("")

    df["feriado_es"] = df["data_local"].dt.date.isin(es)
    df["nome_feriado_es"] = df["data_local"].dt.date.map(es).fillna("")

    df["feriado_rs"] = df["data_local"].dt.date.isin(rs)
    df["nome_feriado_rs"] = df["data_local"].dt.date.map(rs).fillna("")

    df["feriado_sc"] = df["data_local"].dt.date.isin(sc)
    df["nome_feriado_sc"] = df["data_local"].dt.date.map(sc).fillna("")

    df["feriado_pr"] = df["data_local"].dt.date.isin(pr)
    df["nome_feriado_pr"] = df["data_local"].dt.date.map(pr).fillna("")

    df["dia_util"] = (~df["fim_de_semana"]) & (~df["feriado_br"])

    # Time metadata
    df["fuso_horario"] = tz
    df["deslocamento_utc_horas"] = (
        df["data"].dt.utcoffset().dt.total_seconds() / 3600
    )

    return df


__all__ = ["build_calendar_dataframe"]
