"""Jornada de módulos, página da lição, exercício de código, desafios teóricos e conclusão."""

from datetime import date, datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from backend.aluno.gamificacao import adicionar_xp, estado_nivel, registrar_atividade, sincronizar_conquistas
from backend.aluno.revisao import agendar_primeira_revisao
from backend.aluno.situacao import SituacaoAluno
from backend.aluno.teoria import atualizar_resposta_teorica, preparar_desafios_teoricos_view
from backend.banco.conexao import transacao
from backend.compilador.correcao import normalizar_texto
from backend.conteudo import referencia
from backend.conteudo.trilha import licoes_vizinhas, modulo_por_id, url_da_licao
from backend.sessao import usuario_logado

bp = Blueprint("estudo", __name__)

XP_POR_LICAO = 50
TAMANHO_MAXIMO_ANOTACAO = 5000


def _link_da_licao(situacao, par):
    modulo, licao = par
    if not licao:
        return None
    return {
        "titulo": licao["titulo"],
        "url": url_da_licao(modulo, licao),
        "liberada": situacao.modulo_acessivel(modulo["id"]),
    }


@bp.route("/modulos")
def modulos():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    situacao = SituacaoAluno(usuario["id"])
    modulos_view = [
        {
            **modulo,
            "busca": normalizar_texto(" ".join(
                [modulo["titulo"], modulo["descricao"]] + [licao["titulo"] for licao in modulo["licoes"]]
            )),
        }
        for modulo in situacao.modulos_com_estado()
    ]
    return render_template(
        "estudo/modulos.html",
        modulos=modulos_view,
        proxima_licao=situacao.proxima_licao(),
        nivel_jogo=estado_nivel(usuario["xp"]),
    )


@bp.route("/referencia")
def consulta_rapida():
    # Aberta também para visitantes: serve como material de consulta durante os estudos.
    return render_template("estudo/referencia.html", ref=referencia)


@bp.route("/estudar/<int:modulo_id>")
def estudar(modulo_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    modulo = modulo_por_id(modulo_id)
    with transacao() as conn:
        situacao = SituacaoAluno(usuario["id"], conn)
        if not modulo or not situacao.modulo_acessivel(modulo_id):
            return redirect(url_for("estudo.modulos"))

        licao_id = request.args.get("licao", type=int)
        licao = next((item for item in modulo["licoes"] if item["id"] == licao_id), modulo["licoes"][0])
        registro = conn.execute(
            "SELECT quiz_correto, resposta_teorica FROM progresso WHERE usuario_id = ? AND licao_id = ?",
            (usuario["id"], licao["id"]),
        ).fetchone()
        favorita = conn.execute(
            "SELECT 1 FROM favoritos_usuario WHERE usuario_id = ? AND licao_id = ?",
            (usuario["id"], licao["id"]),
        ).fetchone() is not None
        anotacao = conn.execute(
            "SELECT texto FROM anotacoes_usuario WHERE usuario_id = ? AND licao_id = ?",
            (usuario["id"], licao["id"]),
        ).fetchone()

    anterior, proxima = licoes_vizinhas(licao["id"])

    estado_teorico = preparar_desafios_teoricos_view(
        licao,
        (registro and registro["resposta_teorica"]) or "",
        int(registro["quiz_correto"] or 0) if registro else 0,
    )
    return render_template(
        "estudo/estudar.html",
        modulo=modulo,
        licao=licao,
        concluidas_ids=situacao.concluidas,
        desafios_teoricos=estado_teorico["desafios"],
        desafios_teoricos_corretos=estado_teorico["corretos"],
        total_desafios_teoricos=estado_teorico["total"],
        favorita=favorita,
        anotacao=anotacao["texto"] if anotacao else "",
        posicao=modulo["licoes"].index(licao) + 1,
        anterior=_link_da_licao(situacao, anterior),
        proxima=_link_da_licao(situacao, proxima),
    )


@bp.route("/exercicio/<int:licao_id>")
def exercicio(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    modulo, licao, erro = SituacaoAluno(usuario["id"]).licao_acessivel(licao_id)
    if erro:
        return redirect(url_for("estudo.modulos"))
    if not licao["pratica_codigo"]:
        return redirect(url_for("estudo.estudar", modulo_id=modulo["id"], licao=licao_id))

    with transacao() as conn:
        registro = conn.execute(
            """
            SELECT codigo_usuario, codigo_validado, feedback_codigo, concluida
            FROM progresso WHERE usuario_id = ? AND licao_id = ?
            """,
            (usuario["id"], licao_id),
        ).fetchone()

    return render_template(
        "estudo/exercicio.html",
        modulo=modulo,
        licao=licao,
        codigo_salvo=(registro and registro["codigo_usuario"]) or licao["codigo_minimo"],
        codigo_validado=registro["codigo_validado"] if registro else 0,
        feedback_codigo=(registro and registro["feedback_codigo"]) or "",
        solucao_liberada=bool(registro and (registro["codigo_validado"] or registro["concluida"])),
    )


@bp.route("/api/exercicio/salvar-rascunho", methods=["POST"])
def salvar_rascunho_exercicio():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "mensagem": "Usuário não logado."}), 401

    dados = request.get_json(silent=True) or {}
    modulo, licao, erro = SituacaoAluno(usuario["id"]).licao_acessivel(
        dados.get("licao_id"), exigir_pratica=True
    )
    if erro:
        mensagem, status = erro
        return jsonify({"ok": False, "mensagem": mensagem}), status

    # Mudar o código apaga a aprovação anterior: a correção vale só para o código testado.
    with transacao() as conn:
        conn.execute(
            """
            INSERT INTO progresso (usuario_id, licao_id, modulo_id, codigo_usuario, atualizado_em)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(usuario_id, licao_id)
            DO UPDATE SET codigo_validado = CASE WHEN COALESCE(progresso.codigo_usuario, '') = excluded.codigo_usuario
                                                 THEN progresso.codigo_validado ELSE 0 END,
                          codigo_enviado = CASE WHEN COALESCE(progresso.codigo_usuario, '') = excluded.codigo_usuario
                                                THEN progresso.codigo_enviado ELSE 0 END,
                          feedback_codigo = CASE WHEN COALESCE(progresso.codigo_usuario, '') = excluded.codigo_usuario
                                                 THEN progresso.feedback_codigo ELSE NULL END,
                          saida_codigo = CASE WHEN COALESCE(progresso.codigo_usuario, '') = excluded.codigo_usuario
                                              THEN progresso.saida_codigo ELSE NULL END,
                          codigo_usuario = excluded.codigo_usuario,
                          atualizado_em = excluded.atualizado_em
            """,
            (usuario["id"], licao["id"], modulo["id"], str(dados.get("codigo", "")), str(date.today())),
        )
    return jsonify({"ok": True, "mensagem": "Rascunho salvo."})


@bp.route("/api/anotacoes/<int:licao_id>", methods=["POST"])
def salvar_anotacao(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "mensagem": "Usuário não logado."}), 401

    _, licao, erro = SituacaoAluno(usuario["id"]).licao_acessivel(licao_id)
    if erro:
        mensagem, status = erro
        return jsonify({"ok": False, "mensagem": mensagem}), status

    texto = str((request.get_json(silent=True) or {}).get("texto", ""))[:TAMANHO_MAXIMO_ANOTACAO]
    with transacao() as conn:
        if texto.strip():
            conn.execute(
                """
                INSERT INTO anotacoes_usuario (usuario_id, licao_id, texto, atualizado_em)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(usuario_id, licao_id)
                DO UPDATE SET texto = excluded.texto, atualizado_em = excluded.atualizado_em
                """,
                (usuario["id"], licao["id"], texto, datetime.now().isoformat(timespec="seconds")),
            )
        else:
            conn.execute(
                "DELETE FROM anotacoes_usuario WHERE usuario_id = ? AND licao_id = ?",
                (usuario["id"], licao["id"]),
            )
    return jsonify({"ok": True, "mensagem": "Anotação salva."})


@bp.route("/verificar", methods=["POST"])
def verificar():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"correta": False, "mensagem": "Usuário não logado."}), 401

    dados = request.get_json(silent=True) or {}
    modulo, licao, erro = SituacaoAluno(usuario["id"]).licao_acessivel(dados.get("licao_id"))
    if erro:
        mensagem, status = erro
        return jsonify({"correta": False, "mensagem": mensagem}), status

    with transacao() as conn:
        registro = conn.execute(
            "SELECT resposta_teorica, quiz_correto FROM progresso WHERE usuario_id = ? AND licao_id = ?",
            (usuario["id"], licao["id"]),
        ).fetchone()
        resultado = atualizar_resposta_teorica(
            licao,
            (registro and registro["resposta_teorica"]) or "",
            str(dados.get("desafio_id", "conceito")),
            str(dados.get("resposta", "")),
            (registro and registro["quiz_correto"]) or 0,
        )
        if not resultado:
            return jsonify({"correta": False, "mensagem": "Desafio teórico não encontrado."}), 404
        if resultado.get("erro"):
            return jsonify({"correta": False, "mensagem": resultado["erro"]}), 400

        conn.execute(
            """
            INSERT INTO progresso (usuario_id, licao_id, modulo_id, quiz_correto, quiz_respondido,
                                   resposta_teorica, atualizado_em)
            VALUES (?, ?, ?, ?, 1, ?, ?)
            ON CONFLICT(usuario_id, licao_id)
            DO UPDATE SET quiz_correto = excluded.quiz_correto,
                          quiz_respondido = 1,
                          resposta_teorica = excluded.resposta_teorica,
                          atualizado_em = excluded.atualizado_em
            """,
            (usuario["id"], licao["id"], modulo["id"], 1 if resultado["todos_corretos"] else 0,
             resultado["resposta_json"], str(date.today())),
        )
        if resultado["novo_acerto"]:
            registrar_atividade(conn, usuario["id"], quizzes=1)
            sincronizar_conquistas(conn, usuario["id"])

    if resultado["todos_corretos"] and not licao["pratica_codigo"]:
        mensagem = "Todos os desafios teóricos estão corretos. Agora você já pode concluir a lição."
    elif resultado["todos_corretos"]:
        mensagem = "Todos os desafios teóricos estão corretos. Agora faça o exercício de código para concluir."
    elif resultado["correta"]:
        faltam = resultado["total"] - resultado["corretos"]
        mensagem = f"Resposta salva: correta. Falta acertar {faltam} desafio(s)."
    else:
        mensagem = "Resposta salva: incorreta. Revise o conteúdo e tente novamente."

    return jsonify({
        "correta": resultado["correta"],
        "resposta_salva": True,
        "mensagem": mensagem,
        "explicacao": resultado["explicacao"],
        "corretos": resultado["corretos"],
        "total": resultado["total"],
        "todos_corretos": resultado["todos_corretos"],
    })


@bp.route("/concluir/<int:licao_id>", methods=["POST"])
def concluir(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "mensagem": "Usuário não logado."}), 401

    _, licao, erro = SituacaoAluno(usuario["id"]).licao_acessivel(licao_id)
    if erro:
        mensagem, status = erro
        return jsonify({"ok": False, "mensagem": mensagem}), status

    exige_codigo = licao["pratica_codigo"]
    hoje = str(date.today())
    with transacao() as conn:
        registro = conn.execute(
            """
            SELECT quiz_correto, codigo_usuario, codigo_validado, feedback_codigo, concluida
            FROM progresso WHERE usuario_id = ? AND licao_id = ?
            """,
            (usuario["id"], licao_id),
        ).fetchone()

        if not registro or registro["quiz_correto"] != 1:
            return jsonify({"ok": False, "mensagem": "Responda corretamente todos os desafios teóricos antes de concluir."})
        if exige_codigo and not registro["codigo_usuario"]:
            return jsonify({"ok": False, "mensagem": "Faça e execute o exercício de código antes de concluir."})
        if exige_codigo and registro["codigo_validado"] != 1:
            return jsonify({
                "ok": False,
                "mensagem": registro["feedback_codigo"] or "Execute o código e passe na correção automática antes de concluir.",
            })

        ja_concluida = registro["concluida"] == 1
        conn.execute(
            """
            UPDATE progresso
            SET concluida = 1, codigo_enviado = ?, atualizado_em = ?,
                concluida_em = COALESCE(concluida_em, ?)
            WHERE usuario_id = ? AND licao_id = ?
            """,
            (1 if exige_codigo else 0, hoje, hoje, usuario["id"], licao_id),
        )
        if not ja_concluida:
            adicionar_xp(conn, usuario["id"], XP_POR_LICAO)
            registrar_atividade(conn, usuario["id"], licoes=1, xp_ganho=XP_POR_LICAO)
            agendar_primeira_revisao(conn, usuario["id"], licao_id)
        sincronizar_conquistas(conn, usuario["id"])

    # Depois de concluir, o aluno segue direto para a próxima lição que já estiver liberada.
    _, proxima = licoes_vizinhas(licao_id)
    link = _link_da_licao(SituacaoAluno(usuario["id"]), proxima)
    return jsonify({
        "ok": True,
        "mensagem": f"Lição concluída! +{XP_POR_LICAO} XP",
        "proxima": link["url"] if link and link["liberada"] else "/modulos",
    })
