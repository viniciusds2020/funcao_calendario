# Função de Transformação de Data e Hora

Este repositório fornece uma função para gerar um `DataFrame` pandas com informações detalhadas de cada dia de um ano específico, incluindo calendário, sazonalidade, indicadores de progresso e feriados no Brasil (nacional + RJ + SP).

## Requisitos

- Python 3.10+
- pandas
- holidays

Instalação:

```bash
pip install -r requirements.txt
```

## Uso

```python
from datetime_transform import build_calendar_dataframe

df = build_calendar_dataframe(2026)
print(df.head())
```

### Parâmetros

- `year` (int): ano desejado.
- `tz` (str): fuso horário IANA. Padrão: `America/Sao_Paulo`.

## Colunas geradas (resumo)

- Datas e calendário: `data`, `data_local`, `ano`, `mes`, `dia`, `dia_do_ano`
- Semana e mês: `numero_dia_semana`, `nome_dia_semana`, `semana_do_ano`, `semana_do_mes`
- Mês e trimestre: `nome_mes`, `trimestre`, `semestre`
- Limites: `inicio_mes`, `fim_mes`, `inicio_trimestre`, `fim_trimestre`, `inicio_ano`, `fim_ano`
- Progresso: `progresso_ano`, `progresso_mes`, `dias_desde_inicio_mes`, `dias_ate_fim_mes`, `dias_ate_fim_ano`
- Estação (hemisfério sul): `estacao`
- Feriados: `feriado_br`, `nome_feriado_br`, `feriado_rj`, `nome_feriado_rj`, `feriado_sp`, `nome_feriado_sp`, `feriado_mg`, `nome_feriado_mg`, `feriado_es`, `nome_feriado_es`, `feriado_rs`, `nome_feriado_rs`, `feriado_sc`, `nome_feriado_sc`, `feriado_pr`, `nome_feriado_pr`
- Dias úteis: `dia_util`
- Metadados de tempo: `fuso_horario`, `deslocamento_utc_horas`

## Notas

- Estações são aproximadas por datas fixas (hemisfério sul).
- `is_business_day` considera apenas feriados nacionais e fins de semana.
