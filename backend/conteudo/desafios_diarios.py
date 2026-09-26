"""Desafios diários: catálogo próprio por módulo e sorteio do desafio de cada dia."""

from datetime import date

from backend.conteudo.catalogo_desafios import CATALOGO
from backend.conteudo.trilha import encontrar_licao

POR_MODULO = 5


def _montar(item):
    modulo, licao = encontrar_licao(item["licao_id"])
    return {
        **item,
        "id": f"m{item['modulo_id']:02d}-d{item['numero_no_modulo']:02d}",
        "modulo_titulo": modulo["titulo"],
        "assunto": licao["titulo"],
    }


DESAFIOS_DIARIOS = [_montar(item) for item in CATALOGO]


def desafios_disponiveis_por_progresso(desafios, modulo_maximo):
    """Desafios do módulo 2 até o maior módulo liberado; o módulo 1 é só teoria."""
    if modulo_maximo < 2:
        return []
    return [desafio for desafio in desafios if 2 <= desafio["modulo_id"] <= modulo_maximo]


def desafio_por_id(desafios, desafio_id):
    return next((desafio for desafio in desafios if desafio["id"] == desafio_id), None)


def escolher_desafio_do_dia(desafios, data_texto=None, concluidos=()):
    """Sorteio fixo por data que prefere desafios ainda não concluídos pelo aluno."""
    if not desafios:
        return None

    pendentes = [desafio for desafio in desafios if desafio["id"] not in concluidos] or desafios
    data_base = date.fromisoformat(data_texto) if data_texto else date.today()
    return pendentes[data_base.toordinal() % len(pendentes)]
