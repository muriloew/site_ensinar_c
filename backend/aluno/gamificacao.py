"""Regras de progresso, sequencia, missoes e conquistas do curso."""

from datetime import date, datetime, timedelta

from backend.conteudo.trilha import MODULOS, TOTAL_LICOES

XP_POR_NIVEL = 250


MISSOES_BASE = (
    {
        "id": "aquecimento",
        "titulo": "Aquecimento",
        "descricao": "Acerte 3 desafios teóricos.",
        "campo": "quizzes",
        "alvo": 3,
        "recompensa": 10,
        "icone": "Q",
    },
    {
        "id": "passo_da_trilha",
        "titulo": "Passo da trilha",
        "descricao": "Conclua 1 lição.",
        "campo": "licoes",
        "alvo": 1,
        "recompensa": 20,
        "icone": "L",
    },
)


MISSAO_DESAFIO = {
    "id": "desafio_do_dia",
    "titulo": "Desafio do dia",
    "descricao": "Conclua o desafio diário de código.",
    "campo": "desafios",
    "alvo": 1,
    "recompensa": 30,
    "icone": "C",
}


MISSAO_INICIAL = {
    "id": "base_solida",
    "titulo": "Base sólida",
    "descricao": "Acerte 6 desafios teóricos no módulo inicial.",
    "campo": "quizzes",
    "alvo": 6,
    "recompensa": 20,
    "icone": "6",
}


CONQUISTAS = (
    {
        "nome": "Primeiros Passos",
        "icone": "1",
        "descricao": "Concluiu a primeira lição da trilha.",
        "raridade": "comum",
        "condicao": lambda m: m["licoes"] >= 1,
    },
    {
        "nome": "Foco Total",
        "icone": "3",
        "descricao": "Concluiu pelo menos 3 lições.",
        "raridade": "comum",
        "condicao": lambda m: m["licoes"] >= 3,
    },
    {
        "nome": "Base Concluída",
        "icone": "C",
        "descricao": "Terminou todo o módulo Começando a Programar.",
        "raridade": "rara",
        "condicao": lambda m: m["modulo_inicial_concluido"],
    },
    {
        "nome": "Desafio Diário",
        "icone": "D",
        "descricao": "Resolveu o primeiro desafio diário de código.",
        "raridade": "comum",
        "condicao": lambda m: m["desafios"] >= 1,
    },
    {
        "nome": "Ritmo de 3 Dias",
        "icone": "3D",
        "descricao": "Estudou por 3 dias em sequência.",
        "raridade": "rara",
        "condicao": lambda m: m["melhor_sequencia"] >= 3,
    },
    {
        "nome": "Semana de Código",
        "icone": "7D",
        "descricao": "Manteve uma sequência de 7 dias de estudo.",
        "raridade": "epica",
        "condicao": lambda m: m["melhor_sequencia"] >= 7,
    },
    {
        "nome": "Colecionador de XP",
        "icone": "XP",
        "descricao": "Alcançou 500 XP na plataforma.",
        "raridade": "rara",
        "condicao": lambda m: m["xp"] >= 500,
    },
    {
        "nome": "Boa Prova",
        "icone": "A",
        "descricao": "Conseguiu pelo menos 70 por cento em um simulado.",
        "raridade": "rara",
        "condicao": lambda m: m["boa_prova"],
    },
    {
        "nome": "Trilha Inicial",
        "icone": "21",
        "descricao": "Concluiu todas as lições do curso.",
        "raridade": "lendaria",
        "condicao": lambda m: m["licoes"] >= m["total_licoes"],
    },
)


def registrar_atividade(
    conn,
    usuario_id,
    quizzes=0,
    licoes=0,
    desafios=0,
    xp_ganho=0,
    data_atividade=None,
):
    data_atual = date.fromisoformat(data_atividade) if data_atividade else date.today()
    data_texto = data_atual.isoformat()
    usuario = conn.execute(
        """
        SELECT sequencia, melhor_sequencia, ultima_atividade, protecoes_sequencia
        FROM usuarios WHERE id = ?
        """,
        (usuario_id,),
    ).fetchone()
    if not usuario:
        return None

    sequencia = int(usuario["sequencia"] or 0)
    melhor = int(usuario["melhor_sequencia"] or 0)
    protecoes = int(usuario["protecoes_sequencia"] or 0)
    ultima = date.fromisoformat(usuario["ultima_atividade"]) if usuario["ultima_atividade"] else None

    if ultima is None:
        sequencia = max(1, sequencia)
    elif data_atual > ultima:
        intervalo = (data_atual - ultima).days
        if intervalo == 1:
            sequencia += 1
        elif intervalo == 2 and protecoes > 0:
            protecoes -= 1
            sequencia += 1
        else:
            sequencia = 1

        if sequencia >= 7 and sequencia % 7 == 0:
            protecoes = min(2, protecoes + 1)

    melhor = max(melhor, sequencia)

    if ultima is None or data_atual > ultima:
        conn.execute(
            """
            UPDATE usuarios
            SET sequencia = ?, melhor_sequencia = ?, ultima_atividade = ?,
                protecoes_sequencia = ?
            WHERE id = ?
            """,
            (sequencia, melhor, data_texto, protecoes, usuario_id),
        )

    conn.execute(
        """
        INSERT INTO atividades_estudo
            (usuario_id, data, quizzes, licoes, desafios, xp_ganho)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(usuario_id, data)
        DO UPDATE SET quizzes = atividades_estudo.quizzes + excluded.quizzes,
                      licoes = atividades_estudo.licoes + excluded.licoes,
                      desafios = atividades_estudo.desafios + excluded.desafios,
                      xp_ganho = atividades_estudo.xp_ganho + excluded.xp_ganho
        """,
        (usuario_id, data_texto, quizzes, licoes, desafios, xp_ganho),
    )

    return {
        "sequencia": sequencia,
        "melhor_sequencia": melhor,
        "protecoes_sequencia": protecoes,
        "data": data_texto,
    }


def definicoes_missoes(desafio_liberado):
    terceira = MISSAO_DESAFIO if desafio_liberado else MISSAO_INICIAL
    return (*MISSOES_BASE, terceira)


def obter_missoes_diarias(conn, usuario_id, desafio_liberado, data_texto=None):
    hoje = data_texto or date.today().isoformat()
    atividade = conn.execute(
        "SELECT * FROM atividades_estudo WHERE usuario_id = ? AND data = ?",
        (usuario_id, hoje),
    ).fetchone()
    recebidas = {
        linha["missao_id"]
        for linha in conn.execute(
            "SELECT missao_id FROM recompensas_diarias WHERE usuario_id = ? AND data = ?",
            (usuario_id, hoje),
        ).fetchall()
    }

    missoes = []
    for definicao in definicoes_missoes(desafio_liberado):
        progresso = int(atividade[definicao["campo"]] or 0) if atividade else 0
        alvo = definicao["alvo"]
        concluida = progresso >= alvo
        missoes.append({
            **definicao,
            "progresso": min(progresso, alvo),
            "percentual": min(100, int((progresso / alvo) * 100)),
            "concluida": concluida,
            "resgatada": definicao["id"] in recebidas,
        })

    return missoes


def resgatar_missao(conn, usuario_id, missao_id, desafio_liberado, data_texto=None):
    hoje = data_texto or date.today().isoformat()
    missoes = obter_missoes_diarias(conn, usuario_id, desafio_liberado, hoje)
    missao = next((item for item in missoes if item["id"] == missao_id), None)

    if not missao:
        return {"ok": False, "mensagem": "Missão não encontrada."}
    if not missao["concluida"]:
        return {"ok": False, "mensagem": "Conclua a missão antes de resgatar a recompensa."}
    if missao["resgatada"]:
        return {"ok": False, "mensagem": "Esta recompensa já foi resgatada hoje."}

    cursor = conn.execute(
        """
        INSERT INTO recompensas_diarias
            (usuario_id, data, missao_id, xp, recebida_em)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT (usuario_id, data, missao_id) DO NOTHING
        """,
        (
            usuario_id,
            hoje,
            missao_id,
            missao["recompensa"],
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    if cursor.rowcount != 1:
        return {"ok": False, "mensagem": "Esta recompensa já foi resgatada hoje."}

    adicionar_xp(conn, usuario_id, missao["recompensa"])
    registrar_atividade(conn, usuario_id, xp_ganho=missao["recompensa"], data_atividade=hoje)

    return {
        "ok": True,
        "mensagem": f"Recompensa resgatada: +{missao['recompensa']} XP.",
        "xp": missao["recompensa"],
    }


def calendario_atividade(conn, usuario_id, quantidade=7, data_referencia=None):
    hoje = date.fromisoformat(data_referencia) if data_referencia else date.today()
    inicio = hoje - timedelta(days=quantidade - 1)
    datas_ativas = {
        linha["data"]
        for linha in conn.execute(
            """
            SELECT data FROM atividades_estudo
            WHERE usuario_id = ? AND data BETWEEN ? AND ?
            """,
            (usuario_id, inicio.isoformat(), hoje.isoformat()),
        ).fetchall()
    }
    nomes = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom")

    return [
        {
            "data": (inicio + timedelta(days=indice)).isoformat(),
            "dia": (inicio + timedelta(days=indice)).day,
            "nome": nomes[(inicio + timedelta(days=indice)).weekday()],
            "ativo": (inicio + timedelta(days=indice)).isoformat() in datas_ativas,
            "hoje": inicio + timedelta(days=indice) == hoje,
        }
        for indice in range(quantidade)
    ]


def adicionar_xp(conn, usuario_id, quantidade):
    conn.execute(
        f"UPDATE usuarios SET xp = xp + ?, nivel = (xp + ?) / {XP_POR_NIVEL} + 1 WHERE id = ?",
        (quantidade, quantidade, usuario_id),
    )


def estado_nivel(xp):
    xp = max(0, int(xp or 0))
    atual = xp % XP_POR_NIVEL
    return {
        "nivel": xp // XP_POR_NIVEL + 1,
        "xp_atual": atual,
        "xp_alvo": XP_POR_NIVEL,
        "percentual": int((atual / XP_POR_NIVEL) * 100),
    }


def liga_por_xp(xp):
    xp = int(xp or 0)
    if xp >= 3000:
        return {"nome": "Liga Mestre", "classe": "mestre", "proximo": None}
    if xp >= 1500:
        return {"nome": "Liga Diamante", "classe": "diamante", "proximo": 3000}
    if xp >= 750:
        return {"nome": "Liga Ouro", "classe": "ouro", "proximo": 1500}
    if xp >= 250:
        return {"nome": "Liga Prata", "classe": "prata", "proximo": 750}
    return {"nome": "Liga Iniciante", "classe": "iniciante", "proximo": 250}


def sincronizar_conquistas(conn, usuario_id):
    """Desbloqueia as conquistas alcançadas e devolve os nomes das novas."""
    usuario = conn.execute(
        "SELECT xp, melhor_sequencia FROM usuarios WHERE id = ?",
        (usuario_id,),
    ).fetchone()
    if not usuario:
        return []

    licoes = conn.execute(
        "SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND concluida = 1",
        (usuario_id,),
    ).fetchone()["total"]
    licoes_iniciais = conn.execute(
        """
        SELECT COUNT(*) AS total FROM progresso
        WHERE usuario_id = ? AND modulo_id = 1 AND concluida = 1
        """,
        (usuario_id,),
    ).fetchone()["total"]
    desafios = conn.execute(
        "SELECT COUNT(*) AS total FROM desafios_diarios WHERE usuario_id = ? AND concluido = 1",
        (usuario_id,),
    ).fetchone()["total"]
    boa_prova = conn.execute(
        """
        SELECT 1 FROM simulados_usuario
        WHERE usuario_id = ? AND percentual >= 70 LIMIT 1
        """,
        (usuario_id,),
    ).fetchone() is not None

    metricas = {
        "licoes": licoes,
        "desafios": desafios,
        "xp": int(usuario["xp"] or 0),
        "melhor_sequencia": int(usuario["melhor_sequencia"] or 0),
        "modulo_inicial_concluido": licoes_iniciais >= len(MODULOS[0]["licoes"]),
        "boa_prova": boa_prova,
        "total_licoes": TOTAL_LICOES,
    }
    existentes = {
        linha["nome"]: linha
        for linha in conn.execute(
            "SELECT nome, icone, descricao, raridade FROM conquistas_usuario WHERE usuario_id = ?",
            (usuario_id,),
        ).fetchall()
    }
    novas = []

    for conquista in CONQUISTAS:
        if not conquista["condicao"](metricas):
            continue

        atual = existentes.get(conquista["nome"])
        dados = (conquista["icone"], conquista["descricao"], conquista["raridade"])
        if atual is None:
            cursor = conn.execute(
                """
                INSERT INTO conquistas_usuario
                    (usuario_id, nome, icone, descricao, raridade, desbloqueada_em)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (usuario_id, nome) DO NOTHING
                """,
                (usuario_id, conquista["nome"], *dados, date.today().isoformat()),
            )
            if cursor.rowcount == 1:
                novas.append(conquista["nome"])
        elif (atual["icone"], atual["descricao"], atual["raridade"]) != dados:
            conn.execute(
                """
                UPDATE conquistas_usuario
                SET icone = ?, descricao = ?, raridade = ?
                WHERE usuario_id = ? AND nome = ?
                """,
                (*dados, usuario_id, conquista["nome"]),
            )

    return novas
