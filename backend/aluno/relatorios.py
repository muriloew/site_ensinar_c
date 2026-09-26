"""Relatórios do perfil, questões do simulado e cópia do progresso para download."""

from datetime import date, datetime

from backend.conteudo.trilha import MODULOS, encontrar_licao


def resumo_desempenho(conn, usuario_id):
    def contar(sql):
        return conn.execute(sql, (usuario_id,)).fetchone()["total"]

    quiz_total = contar("SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND quiz_respondido = 1")
    quiz_corretos = contar("SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND quiz_correto = 1")
    codigos_validados = contar("SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND codigo_validado = 1")
    desafios_concluidos = contar("SELECT COUNT(*) AS total FROM desafios_diarios WHERE usuario_id = ? AND concluido = 1")
    ultimas_licoes = conn.execute(
        """
        SELECT licao_id, atualizado_em, codigo_validado, feedback_codigo
        FROM progresso
        WHERE usuario_id = ? AND atualizado_em IS NOT NULL
        ORDER BY atualizado_em DESC, id DESC
        LIMIT 6
        """,
        (usuario_id,),
    ).fetchall()
    simulados = conn.execute(
        "SELECT * FROM simulados_usuario WHERE usuario_id = ? ORDER BY id DESC LIMIT 5",
        (usuario_id,),
    ).fetchall()

    atividades = []
    for item in ultimas_licoes:
        modulo, licao = encontrar_licao(item["licao_id"])
        if licao:
            atividades.append({
                "modulo": modulo["titulo"],
                "licao": licao["titulo"],
                "data": item["atualizado_em"],
                "codigo_validado": item["codigo_validado"],
                "feedback": item["feedback_codigo"],
            })

    return {
        "quiz_total": quiz_total,
        "quiz_corretos": quiz_corretos,
        "taxa_quiz": int((quiz_corretos / max(quiz_total, 1)) * 100),
        "codigos_validados": codigos_validados,
        "desafios_concluidos": desafios_concluidos,
        "atividades": atividades,
        "simulados": simulados,
    }


def relatorio_modulos(conn, usuario_id, situacao):
    progresso_usuario = {
        linha["licao_id"]: linha
        for linha in conn.execute(
            "SELECT licao_id, concluida, quiz_correto, codigo_validado FROM progresso WHERE usuario_id = ?",
            (usuario_id,),
        ).fetchall()
    }
    favoritos = {
        linha["licao_id"]
        for linha in conn.execute(
            "SELECT licao_id FROM favoritos_usuario WHERE usuario_id = ?",
            (usuario_id,),
        ).fetchall()
    }
    tentativas_por_modulo = {
        linha["modulo_id"]: linha
        for linha in conn.execute(
            """
            SELECT modulo_id, COUNT(*) AS tentativas,
                   SUM(CASE WHEN aprovado = 1 THEN 1 ELSE 0 END) AS aprovadas
            FROM compilador_historico
            WHERE usuario_id = ? AND modulo_id IS NOT NULL
            GROUP BY modulo_id
            """,
            (usuario_id,),
        ).fetchall()
    }

    relatorio = []
    for modulo in MODULOS:
        registros = [
            progresso_usuario[licao["id"]]
            for licao in modulo["licoes"]
            if licao["id"] in progresso_usuario
        ]
        concluidas = sum(1 for item in registros if item["concluida"] == 1)
        tentativas = tentativas_por_modulo.get(modulo["id"])
        relatorio.append({
            "id": modulo["id"],
            "titulo": modulo["titulo"],
            "descricao": modulo["descricao"],
            "icone": modulo["icone"],
            "progresso": int((concluidas / len(modulo["licoes"])) * 100),
            "concluidas": concluidas,
            "total": len(modulo["licoes"]),
            "liberado": situacao.modulo_acessivel(modulo["id"]),
            "iniciadas": len(registros),
            "teorias_dominadas": sum(1 for item in registros if item["quiz_correto"] == 1),
            "praticas_aprovadas": sum(1 for item in registros if item["codigo_validado"] == 1),
            "praticas_total": sum(1 for licao in modulo["licoes"] if licao["pratica_codigo"]),
            "tentativas_codigo": tentativas["tentativas"] if tentativas else 0,
            "aprovacoes_codigo": tentativas["aprovadas"] if tentativas else 0,
            "favoritos": sum(1 for licao in modulo["licoes"] if licao["id"] in favoritos),
        })
    return relatorio


def questoes_simulado(usuario_id, situacao, quantidade=10):
    licoes = [
        (modulo, licao)
        for modulo in MODULOS
        if situacao.modulo_acessivel(modulo["id"])
        for licao in modulo["licoes"]
    ]
    if not licoes:
        return []

    # Gira a lista a cada dia para o simulado não repetir sempre as mesmas perguntas.
    deslocamento = (date.today().toordinal() + usuario_id) % len(licoes)
    licoes = licoes[deslocamento:] + licoes[:deslocamento]

    return [
        {
            "id": licao["id"],
            "modulo": modulo["titulo"],
            "pergunta": licao["pergunta"],
            "alternativas": licao["alternativas"],
            "resposta": licao["resposta"],
        }
        for modulo, licao in licoes[:quantidade]
    ]


def dados_backup(conn, usuario_id):
    """Todo o progresso do aluno em um dicionário pronto para virar JSON."""
    def linhas(sql):
        return [dict(linha) for linha in conn.execute(sql, (usuario_id,)).fetchall()]

    usuario = conn.execute(
        """
        SELECT id, nome, email, xp, nivel, sequencia, melhor_sequencia,
               ultima_atividade, protecoes_sequencia, ultimo_acesso
        FROM usuarios WHERE id = ?
        """,
        (usuario_id,),
    ).fetchone()

    return {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "usuario": dict(usuario) if usuario else None,
        "progresso": linhas("SELECT * FROM progresso WHERE usuario_id = ? ORDER BY modulo_id, licao_id"),
        "desafios_diarios": linhas("SELECT * FROM desafios_diarios WHERE usuario_id = ? ORDER BY data DESC"),
        "conquistas": linhas("SELECT * FROM conquistas_usuario WHERE usuario_id = ? ORDER BY id"),
        "metas": linhas("SELECT * FROM metas_usuario WHERE usuario_id = ? ORDER BY tipo"),
        "simulados": linhas("SELECT * FROM simulados_usuario WHERE usuario_id = ? ORDER BY id DESC"),
        "atividades_estudo": linhas("SELECT * FROM atividades_estudo WHERE usuario_id = ? ORDER BY data DESC"),
        "recompensas_diarias": linhas(
            "SELECT * FROM recompensas_diarias WHERE usuario_id = ? ORDER BY data DESC, id DESC"
        ),
        "historico_codigos": linhas(
            "SELECT * FROM compilador_historico WHERE usuario_id = ? ORDER BY id DESC LIMIT 100"
        ),
        "favoritos": linhas("SELECT * FROM favoritos_usuario WHERE usuario_id = ? ORDER BY id DESC"),
        "revisoes": linhas("SELECT * FROM revisoes_usuario WHERE usuario_id = ? ORDER BY proxima_revisao"),
        "anotacoes": linhas("SELECT * FROM anotacoes_usuario WHERE usuario_id = ? ORDER BY licao_id"),
    }
