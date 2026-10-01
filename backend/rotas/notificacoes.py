"""Notificações do aluno: lista, abrir uma notificação e marcar todas como lidas."""

import time

from flask import Blueprint, redirect, render_template, session, url_for

from backend.aluno import notificacoes
from backend.banco.conexao import transacao
from backend.preferencias import ler_preferencias
from backend.sessao import usuario_logado

bp = Blueprint("notificacoes", __name__)


@bp.route("/notificacoes")
def lista():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    with transacao() as conn:
        lembretes = ler_preferencias(conn, usuario["id"])["lembretes"] == "sim"
        notificacoes.gerar(conn, usuario["id"], lembretes)
        itens = notificacoes.listar(conn, usuario["id"])
    session["notificacoes_verificadas"] = time.time()
    return render_template("notificacoes/lista.html", itens=itens, nao_lidas=sum(1 for i in itens if not i["lida"]))


@bp.route("/notificacoes/<int:notificacao_id>")
def abrir(notificacao_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    with transacao() as conn:
        link = notificacoes.marcar_lida(conn, usuario["id"], notificacao_id)
    return redirect(notificacoes.link_interno(link) or url_for("notificacoes.lista"))


@bp.route("/notificacoes/lidas", methods=["POST"])
def marcar_todas():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    with transacao() as conn:
        notificacoes.marcar_todas_lidas(conn, usuario["id"])
    return redirect(url_for("notificacoes.lista"))
