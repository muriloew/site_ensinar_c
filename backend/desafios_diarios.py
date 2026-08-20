"""Geração e seleção dos desafios diários conforme o progresso do aluno."""

from datetime import date


VARIACOES_DESAFIOS = [
    "Resolva o objetivo usando valores simples e fáceis de conferir.",
    "Monte uma versão curta do programa e mostre o resultado no terminal.",
    "Crie um exemplo direto que demonstre o conteúdo estudado.",
    "Use nomes claros e produza exatamente a saída solicitada.",
    "Escreva o programa completo, da função main até o return 0.",
    "Teste a ideia com dados pequenos antes de finalizar.",
    "Resolva usando somente recursos que já apareceram na trilha.",
    "Mostre uma saída objetiva para permitir a correção automática.",
    "Organize o código para que outra pessoa consiga acompanhar a solução.",
    "Refaça o objetivo com seus próprios nomes de variáveis.",
]


def gerar_desafios_diarios(modulos, quantidade_por_modulo=10):
    desafios = []

    for modulo in modulos:
        modulo_id = modulo.get("id", 0)
        if modulo_id < 2:
            continue

        licoes = [
            licao for licao in modulo.get("licoes", [])
            if licao.get("pratica_codigo", True)
        ] or modulo.get("licoes", [])

        if not licoes:
            continue

        for indice in range(quantidade_por_modulo):
            licao = licoes[indice % len(licoes)]
            variacao = VARIACOES_DESAFIOS[indice % len(VARIACOES_DESAFIOS)]
            objetivo = licao.get("exercicio_codigo") or f"Demonstre {licao.get('titulo', 'o conteudo')} em C."

            desafios.append({
                "id": f"m{modulo_id:02d}-l{licao['id']:03d}-d{indice + 1:02d}",
                "modulo_id": modulo_id,
                "modulo_titulo": modulo.get("titulo", f"Módulo {modulo_id}"),
                "licao_id": licao["id"],
                "assunto": licao["titulo"],
                "numero_no_modulo": indice + 1,
                "titulo": f"Desafio diário {modulo_id}.{indice + 1}: {licao['titulo']}",
                "descricao": f"{variacao} {objetivo}",
                "codigo_inicial": licao.get("codigo_minimo", licao.get("codigo", "")),
                "dica": (
                    f"Use apenas o que foi visto até o módulo {modulo_id}. "
                    f"Esta atividade revisa: {licao['titulo']}."
                ),
                "correcao": licao.get("correcao", {"saida_obrigatoria": True}),
            })

    return desafios


def desafios_disponiveis_por_progresso(desafios, modulo_maximo):
    if modulo_maximo < 2:
        return []

    return [
        desafio for desafio in desafios
        if 2 <= desafio.get("modulo_id", 0) <= modulo_maximo
    ]


def desafio_por_id(desafios, desafio_id):
    return next((desafio for desafio in desafios if desafio["id"] == desafio_id), None)


def escolher_desafio_do_dia(desafios, data_texto=None):
    if not desafios:
        return None

    data_base = date.fromisoformat(data_texto) if data_texto else date.today()
    indice = data_base.toordinal() % len(desafios)
    return desafios[indice]
