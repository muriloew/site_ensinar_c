"""Data e hora do site no horário de Brasília.

O servidor do Render trabalha em UTC: com date.today(), o dia do desafio diário, da sequência de estudos, das
metas e das revisões virava às 21h de Brasília. Todo o backend pega "hoje" e "agora" daqui.
"""

from datetime import date, datetime
from zoneinfo import ZoneInfo

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")


def agora() -> datetime:
    """Data e hora atuais em Brasília, sem fuso no valor (o mesmo formato já gravado no banco)."""
    return datetime.now(FUSO_HORARIO).replace(tzinfo=None)


def hoje() -> date:
    """Data de hoje em Brasília."""
    return agora().date()
