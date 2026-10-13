"""Desafios diários: catálogo próprio por módulo e sorteio do desafio de cada dia."""

from datetime import date

from backend.conteudo.catalogo_desafios import CATALOGO
from backend.conteudo.trilha import encontrar_licao
from backend import relogio

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


def _licoes_necessarias(licao_id):
    """A lição do desafio e as que vêm antes dela no mesmo módulo."""
    modulo, licao = encontrar_licao(licao_id)
    ids = [item["id"] for item in modulo["licoes"]]
    return ids[: ids.index(licao["id"]) + 1]


NECESSARIAS = {desafio["id"]: _licoes_necessarias(desafio["licao_id"]) for desafio in DESAFIOS_DIARIOS}


def desafios_disponiveis_por_licoes(desafios, concluidas):
    """Desafios cujos assuntos o aluno já estudou; o módulo 1 é só teoria.

    Um desafio aparece quando a lição dele e as anteriores do mesmo módulo estão concluídas, para não cobrar,
    logo depois de liberar um módulo, um assunto que só é explicado mais adiante nele.
    """
    return [
        desafio for desafio in desafios
        if desafio["modulo_id"] >= 2 and all(licao_id in concluidas for licao_id in NECESSARIAS[desafio["id"]])
    ]


def desafio_por_id(desafios, desafio_id):
    return next((desafio for desafio in desafios if desafio["id"] == desafio_id), None)


def escolher_desafio_do_dia(desafios, data_texto=None, concluidos=()):
    """Sorteio fixo por data que prefere desafios ainda não concluídos pelo aluno."""
    if not desafios:
        return None

    pendentes = [desafio for desafio in desafios if desafio["id"] not in concluidos] or desafios
    data_base = date.fromisoformat(data_texto) if data_texto else relogio.hoje()
    return pendentes[data_base.toordinal() % len(pendentes)]
