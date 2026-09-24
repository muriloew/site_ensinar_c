"""Revisão espaçada das lições concluídas e lista de lições favoritas."""

from datetime import date, datetime

from flask import Blueprint, redirect, render_template, request, url_for

from backend.aluno.gamificacao import registrar_atividade
from backend.aluno.revisao import proximo_agendamento, sincronizar_revisoes
from backend.aluno.situacao import SituacaoAluno
from backend.banco.conexao import transacao
from backend.conteudo.trilha import encontrar_licao
from backend.sessao import usuario_logado

bp = Blueprint("revisao", __name__)


@bp.route("/revisao")
def revisao():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    hoje = date.today().isoformat()
    with transacao() as conn:
        sincronizar_revisoes(conn, usuario["id"])
        pendentes = conn.execute(
            """
            SELECT * FROM revisoes_usuario
            WHERE usuario_id = ? AND proxima_revisao <= ?
            ORDER BY proxima_revisao, id LIMIT 10
            """,
            (usuario["id"], hoje),
        ).fetchall()
        proximas = conn.execute(
            """
            SELECT * FROM revisoes_usuario
            WHERE usuario_id = ? AND proxima_revisao > ?
            ORDER BY proxima_revisao LIMIT 6
            """,
            (usuario["id"], hoje),
        ).fetchall()

    def montar_item(registro):
        modulo, licao = encontrar_licao(registro["licao_id"])
        return {"registro": registro, "modulo": modulo, "licao": licao}

    return render_template(
        "revisao/revisao.html",
        pendentes=[montar_item(item) for item in pendentes],
        proximas=[montar_item(item) for item in proximas],
        mensagem=request.args.get("mensagem", ""),
        resultado=request.args.get("resultado", ""),
    )


@bp.route("/revisao/<int:licao_id>", methods=["POST"])
def responder_revisao(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    _, licao = encontrar_licao(licao_id)
    if not licao:
        return redirect(url_for("revisao.revisao"))

    with transacao() as conn:
        registro = conn.execute(
            """
            SELECT r.nivel FROM revisoes_usuario r
            JOIN progresso p ON p.usuario_id = r.usuario_id AND p.licao_id = r.licao_id
            WHERE r.usuario_id = ? AND r.licao_id = ? AND p.concluida = 1
            """,
            (usuario["id"], licao_id),
        ).fetchone()
        if not registro:
            return redirect(url_for("revisao.revisao"))

        correta = request.form.get("resposta", "") == licao["resposta"]
        novo_nivel, intervalo, proxima = proximo_agendamento(int(registro["nivel"] or 0), correta)
        conn.execute(
            """
            UPDATE revisoes_usuario
            SET nivel = ?, proxima_revisao = ?, ultima_revisao = ?,
                acertos = acertos + ?, erros = erros + ?
            WHERE usuario_id = ? AND licao_id = ?
            """,
            (
                novo_nivel,
                proxima,
                datetime.now().isoformat(timespec="seconds"),
                1 if correta else 0,
                0 if correta else 1,
                usuario["id"],
                licao_id,
            ),
        )
        if correta:
            registrar_atividade(conn, usuario["id"], quizzes=1)

    mensagem = (
        f"Resposta correta. Próxima revisão em {intervalo} dia(s)."
        if correta
        else "Resposta incorreta. Revise a explicação e tente novamente amanhã."
    )
    return redirect(url_for(
        "revisao.revisao", mensagem=mensagem, resultado="correto" if correta else "incorreto"
    ))


@bp.route("/favoritos")
def favoritos():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    with transacao() as conn:
        situacao = SituacaoAluno(usuario["id"], conn)
        registros = conn.execute(
            "SELECT licao_id, criado_em FROM favoritos_usuario WHERE usuario_id = ? ORDER BY id DESC",
            (usuario["id"],),
        ).fetchall()

    lista = []
    for registro in registros:
        modulo, licao = encontrar_licao(registro["licao_id"])
        if licao:
            lista.append({
                "modulo": modulo,
                "licao": licao,
                "criado_em": registro["criado_em"],
                "liberado": situacao.modulo_acessivel(modulo["id"]),
            })
    return render_template("revisao/favoritos.html", favoritos=lista)


@bp.route("/favoritos/<int:licao_id>", methods=["POST"])
def alternar_favorito(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    _, _, erro = SituacaoAluno(usuario["id"]).licao_acessivel(licao_id)
    if erro:
        return redirect(url_for("estudo.modulos"))

    with transacao() as conn:
        apagado = conn.execute(
            "DELETE FROM favoritos_usuario WHERE usuario_id = ? AND licao_id = ?",
            (usuario["id"], licao_id),
        ).rowcount
        if not apagado:
            conn.execute(
                "INSERT INTO favoritos_usuario (usuario_id, licao_id, criado_em) VALUES (?, ?, ?)",
                (usuario["id"], licao_id, datetime.now().isoformat(timespec="seconds")),
            )

    destino = request.form.get("destino", "")
    # Só aceita caminhos do próprio site; "//x" e "/\x" levariam a outro domínio.
    if not destino.startswith("/") or destino.startswith(("//", "/\\")):
        destino = url_for("revisao.favoritos")
    return redirect(destino)
