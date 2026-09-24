"""Metas diárias e semanais de lições e desafios."""

from datetime import date, datetime, timedelta

METAS_PADRAO = {
    "diaria": {
        "tipo": "diaria",
        "titulo": "Meta diária",
        "periodo": "Hoje",
        "alvo_licoes": 1,
        "alvo_desafios": 1,
        "max_licoes": 10,
        "max_desafios": 5,
    },
    "semanal": {
        "tipo": "semanal",
        "titulo": "Meta semanal",
        "periodo": "Semana atual",
        "alvo_licoes": 5,
        "alvo_desafios": 3,
        "max_licoes": 30,
        "max_desafios": 14,
    },
}


def limitar_inteiro(valor, padrao, minimo, maximo):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        numero = padrao
    return max(minimo, min(maximo, numero))


def _porcentagem(valor, alvo):
    if alvo <= 0:
        return 100 if valor > 0 else 0
    return min(100, int((valor / alvo) * 100))


def salvar_metas(conn, usuario_id, formulario):
    agora = datetime.now().isoformat(timespec="seconds")
    for tipo, meta in METAS_PADRAO.items():
        alvo_licoes = limitar_inteiro(
            formulario.get(f"{tipo}_licoes"), meta["alvo_licoes"], 0, meta["max_licoes"]
        )
        alvo_desafios = limitar_inteiro(
            formulario.get(f"{tipo}_desafios"), meta["alvo_desafios"], 0, meta["max_desafios"]
        )
        conn.execute(
            """
            INSERT INTO metas_usuario (usuario_id, tipo, alvo_licoes, alvo_desafios, atualizado_em)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(usuario_id, tipo)
            DO UPDATE SET alvo_licoes = excluded.alvo_licoes,
                          alvo_desafios = excluded.alvo_desafios,
                          atualizado_em = excluded.atualizado_em
            """,
            (usuario_id, tipo, alvo_licoes, alvo_desafios, agora),
        )


def progresso_metas(conn, usuario_id):
    metas = {tipo: dict(meta) for tipo, meta in METAS_PADRAO.items()}
    for registro in conn.execute(
        "SELECT tipo, alvo_licoes, alvo_desafios FROM metas_usuario WHERE usuario_id = ?",
        (usuario_id,),
    ).fetchall():
        if registro["tipo"] in metas:
            metas[registro["tipo"]]["alvo_licoes"] = registro["alvo_licoes"]
            metas[registro["tipo"]]["alvo_desafios"] = registro["alvo_desafios"]

    hoje = date.today()
    inicios = {"diaria": hoje, "semanal": hoje - timedelta(days=hoje.weekday())}

    resultado = []
    for tipo, meta in metas.items():
        inicio = inicios[tipo].isoformat()
        licoes = conn.execute(
            """
            SELECT COUNT(*) AS total FROM progresso
            WHERE usuario_id = ? AND concluida = 1 AND COALESCE(concluida_em, atualizado_em) >= ?
            """,
            (usuario_id, inicio),
        ).fetchone()["total"]
        desafios = conn.execute(
            """
            SELECT COUNT(*) AS total FROM desafios_diarios
            WHERE usuario_id = ? AND concluido = 1 AND data >= ?
            """,
            (usuario_id, inicio),
        ).fetchone()["total"]
        resultado.append({
            **meta,
            "feito_licoes": licoes,
            "feito_desafios": desafios,
            "percentual_licoes": _porcentagem(licoes, meta["alvo_licoes"]),
            "percentual_desafios": _porcentagem(desafios, meta["alvo_desafios"]),
        })
    return resultado
