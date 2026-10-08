"""Desafios teóricos das lições: quatro perguntas escritas para cada lição (veja base.py)."""

import hashlib

from backend.conteudo.perguntas import modulos_01_04, modulos_05_08, modulos_09_14, modulos_15_21

TIPOS = ("conceito", "saida", "erro", "lacuna")

PERGUNTAS = {}
for _parte in (modulos_01_04, modulos_05_08, modulos_09_14, modulos_15_21):
    _repetidas = set(_parte.PERGUNTAS) & set(PERGUNTAS)
    assert not _repetidas, _repetidas
    PERGUNTAS.update(_parte.PERGUNTAS)


def _sorteio(texto):
    return int(hashlib.sha256(texto.encode("utf-8")).hexdigest(), 16)


def montar_desafios_teoricos(titulo, semente):
    """As perguntas da lição prontas para a página, com a resposta certa em uma posição fixa, mas variada."""
    desafios = []
    for numero, pergunta in enumerate(PERGUNTAS[titulo], start=1):
        chave = f"{semente}:{titulo}:{numero}"
        erradas = sorted(pergunta["erradas"], key=lambda texto: _sorteio(f"{chave}|{texto}"))
        posicao = _sorteio(chave) % 4
        desafio = {campo: valor for campo, valor in pergunta.items() if campo != "erradas"}
        desafio["id"] = f"p{numero}"
        desafio["alternativas"] = erradas[:posicao] + [pergunta["resposta"]] + erradas[posicao:]
        desafios.append(desafio)
    return desafios
