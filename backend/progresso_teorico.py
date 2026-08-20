"""Helpers para respostas dos desafios teoricos de cada licao."""

import json


def _desafios_da_licao(licao):
    desafios = licao.get("desafios_teoricos") or []
    if desafios:
        return desafios

    return [{
        "id": "conceito",
        "pergunta": licao.get("pergunta", ""),
        "alternativas": licao.get("alternativas", []),
        "resposta": licao.get("resposta", ""),
        "explicacao": "Revise o conteudo teorico desta licao.",
    }]


def carregar_respostas_teoricas(valor, licao=None, quiz_correto=0):
    desafios = _desafios_da_licao(licao) if licao else []

    if not valor:
        if quiz_correto and desafios:
            return {
                desafio["id"]: {
                    "resposta": desafio.get("resposta", ""),
                    "correta": True,
                }
                for desafio in desafios
            }
        return {}

    try:
        dados = json.loads(valor)
    except (TypeError, json.JSONDecodeError):
        if not desafios:
            return {}

        if quiz_correto:
            return {
                desafio["id"]: {
                    "resposta": desafio.get("resposta", ""),
                    "correta": True,
                }
                for desafio in desafios
            }

        primeiro = desafios[0]
        return {
            primeiro["id"]: {
                "resposta": valor,
                "correta": bool(quiz_correto) or valor == primeiro.get("resposta"),
            }
        }

    if not isinstance(dados, dict):
        return {}

    respostas = dados.get("respostas", dados)
    if not isinstance(respostas, dict):
        return {}

    if quiz_correto and desafios:
        for desafio in desafios:
            respostas.setdefault(desafio["id"], {
                "resposta": desafio.get("resposta", ""),
                "correta": True,
            })

    return respostas


def serializar_respostas_teoricas(respostas):
    return json.dumps({"respostas": respostas}, ensure_ascii=False)


def preparar_desafios_teoricos_view(licao, resposta_salva="", quiz_correto=0):
    respostas = carregar_respostas_teoricas(resposta_salva, licao, quiz_correto)
    desafios = []

    for desafio in _desafios_da_licao(licao):
        desafio_id = desafio["id"]
        registro = respostas.get(desafio_id, {})
        resposta_usuario = registro.get("resposta", "")
        correta = bool(registro.get("correta")) and resposta_usuario == desafio.get("resposta")

        desafios.append({
            **desafio,
            "resposta_salva": resposta_usuario,
            "correta": correta,
        })

    corretos = sum(1 for desafio in desafios if desafio["correta"])

    return {
        "desafios": desafios,
        "corretos": corretos,
        "total": len(desafios),
        "todos_corretos": bool(desafios) and corretos == len(desafios),
    }


def atualizar_resposta_teorica(licao, valor_atual, desafio_id, resposta, quiz_correto=0):
    desafios = _desafios_da_licao(licao)
    desafio = next((item for item in desafios if item["id"] == desafio_id), None)
    if not desafio:
        return None

    if resposta not in desafio.get("alternativas", []):
        return {"erro": "Resposta inválida para este desafio."}

    respostas = carregar_respostas_teoricas(valor_atual, licao, quiz_correto)
    correta = resposta == desafio.get("resposta")

    respostas[desafio_id] = {
        "resposta": resposta,
        "correta": correta,
    }

    total = len(desafios)
    corretos = 0
    for item in desafios:
        registro = respostas.get(item["id"], {})
        if registro.get("correta") and registro.get("resposta") == item.get("resposta"):
            corretos += 1

    return {
        "respostas": respostas,
        "resposta_json": serializar_respostas_teoricas(respostas),
        "correta": correta,
        "corretos": corretos,
        "total": total,
        "todos_corretos": total > 0 and corretos == total,
        "explicacao": desafio.get("explicacao", ""),
    }
