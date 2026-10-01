"""Desafio diário de código: página, rascunho e conclusão."""


from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from backend.aluno.gamificacao import adicionar_xp, registrar_atividade, sincronizar_conquistas
from backend.aluno.situacao import SituacaoAluno
from backend.banco.conexao import transacao
from backend.sessao import usuario_logado
from backend import relogio

bp = Blueprint("desafio_diario", __name__)

XP_POR_DESAFIO = 30
MENSAGEM_BLOQUEADO = "Conclua o módulo 1 para desbloquear os desafios diários."


@bp.route("/desafio-diario")
def desafio_diario():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    hoje = str(relogio.hoje())
    situacao = SituacaoAluno(usuario["id"])
    disponiveis, modulo_maximo = situacao.desafios_disponiveis()
    if not disponiveis:
        return render_template(
            "desafio_diario/desafio_diario.html",
            desafio_bloqueado=True,
            modulo_maximo_diario=modulo_maximo,
        )

    # O mesmo método decide o desafio na página, no rascunho, na compilação e na conclusão.
    desafio = situacao.desafio_do_dia(hoje)
    with transacao() as conn:
        registro = conn.execute(
            "SELECT * FROM desafios_diarios WHERE usuario_id = ? AND data = ?",
            (usuario["id"], hoje),
        ).fetchone()

    mesmo_desafio = bool(registro) and registro["desafio_id"] == desafio["id"]
    return render_template(
        "desafio_diario/desafio_diario.html",
        desafio=desafio,
        codigo=(mesmo_desafio and registro["codigo_usuario"]) or desafio["codigo_inicial"],
        saida=(mesmo_desafio and registro["saida_codigo"]) or "A saída do desafio aparecerá aqui.",
        concluido=registro["concluido"] if mesmo_desafio else 0,
        codigo_validado=registro["codigo_validado"] if mesmo_desafio else 0,
        feedback_codigo=(mesmo_desafio and registro["feedback_codigo"]) or "",
        desafio_bloqueado=False,
        modulo_maximo_diario=modulo_maximo,
        total_desafios_disponiveis=len(disponiveis),
        total_desafios_concluidos=situacao.desafios_concluidos_disponiveis(),
        xp_por_desafio=XP_POR_DESAFIO,
    )


@bp.route("/api/desafio/salvar-rascunho", methods=["POST"])
def salvar_rascunho_desafio():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "mensagem": "Usuário não logado."}), 401

    dados = request.get_json(silent=True) or {}
    hoje = str(relogio.hoje())
    desafio = SituacaoAluno(usuario["id"]).desafio_do_dia(hoje)
    if not desafio:
        return jsonify({"ok": False, "mensagem": MENSAGEM_BLOQUEADO}), 403

    # Mudar o código ou o desafio apaga a aprovação anterior.
    with transacao() as conn:
        conn.execute(
            """
            INSERT INTO desafios_diarios (usuario_id, data, desafio_id, codigo_usuario, concluido)
            VALUES (?, ?, ?, ?, 0)
            ON CONFLICT(usuario_id, data)
            DO UPDATE SET codigo_validado = CASE
                              WHEN COALESCE(desafios_diarios.codigo_usuario, '') = excluded.codigo_usuario
                               AND COALESCE(desafios_diarios.desafio_id, '') = excluded.desafio_id
                              THEN desafios_diarios.codigo_validado ELSE 0 END,
                          feedback_codigo = CASE
                              WHEN COALESCE(desafios_diarios.codigo_usuario, '') = excluded.codigo_usuario
                               AND COALESCE(desafios_diarios.desafio_id, '') = excluded.desafio_id
                              THEN desafios_diarios.feedback_codigo ELSE NULL END,
                          saida_codigo = CASE
                              WHEN COALESCE(desafios_diarios.codigo_usuario, '') = excluded.codigo_usuario
                               AND COALESCE(desafios_diarios.desafio_id, '') = excluded.desafio_id
                              THEN desafios_diarios.saida_codigo ELSE NULL END,
                          desafio_id = excluded.desafio_id,
                          codigo_usuario = excluded.codigo_usuario
            """,
            (usuario["id"], hoje, desafio["id"], str(dados.get("codigo", ""))),
        )
    return jsonify({"ok": True, "mensagem": "Rascunho salvo."})


@bp.route("/concluir-desafio-diario", methods=["POST"])
def concluir_desafio_diario():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "mensagem": "Usuário não logado."}), 401

    hoje = str(relogio.hoje())
    desafio = SituacaoAluno(usuario["id"]).desafio_do_dia(hoje)
    if not desafio:
        return jsonify({"ok": False, "mensagem": MENSAGEM_BLOQUEADO}), 403

    with transacao() as conn:
        registro = conn.execute(
            "SELECT * FROM desafios_diarios WHERE usuario_id = ? AND data = ?",
            (usuario["id"], hoje),
        ).fetchone()

        if not registro or not registro["codigo_usuario"] or registro["desafio_id"] != desafio["id"]:
            return jsonify({"ok": False, "mensagem": "Execute um código antes de concluir o desafio diário."})
        if registro["codigo_validado"] != 1:
            return jsonify({
                "ok": False,
                "mensagem": registro["feedback_codigo"] or "Passe na correção automática antes de concluir o desafio diário.",
            })

        if registro["concluido"] != 1:
            conn.execute(
                "UPDATE desafios_diarios SET concluido = 1 WHERE usuario_id = ? AND data = ?",
                (usuario["id"], hoje),
            )
            adicionar_xp(conn, usuario["id"], XP_POR_DESAFIO)
            registrar_atividade(conn, usuario["id"], desafios=1, xp_ganho=XP_POR_DESAFIO)
        sincronizar_conquistas(conn, usuario["id"])

    return jsonify({"ok": True, "mensagem": f"Desafio diário concluído! +{XP_POR_DESAFIO} XP"})
