"""Prática livre com o compilador e histórico das execuções."""

from flask import Blueprint, redirect, render_template, request, url_for

from backend.aluno.situacao import SituacaoAluno
from backend.banco.conexao import transacao
from backend.conteudo.trilha import encontrar_licao
from backend.sessao import usuario_logado

bp = Blueprint("compilador", __name__)

CODIGO_INICIAL = '#include <stdio.h>\n\nint main() {\n    // escreva seu código aqui\n\n    return 0;\n}'
CONTEXTOS_HISTORICO = {"todos", "livre", "licao", "diario"}


@bp.route("/compilador")
def compilador():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    codigo_inicial = CODIGO_INICIAL
    titulo = "Compilador Online"
    exemplo = request.args.get("exemplo", type=int)
    if exemplo:
        _, licao, erro = SituacaoAluno(usuario["id"]).licao_acessivel(exemplo)
        if not erro:
            codigo_inicial = licao["codigo"]
            titulo = f"Exemplo - {licao['titulo']}"

    with transacao() as conn:
        historico = conn.execute(
            "SELECT codigo, criado_em FROM compilador_historico WHERE usuario_id = ? ORDER BY id DESC LIMIT 5",
            (usuario["id"],),
        ).fetchall()

    return render_template(
        "compilador/compilador.html",
        codigo_inicial=codigo_inicial,
        titulo=titulo,
        historico=historico,
    )


@bp.route("/historico-codigos")
def historico_codigos():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    contexto = request.args.get("contexto", "todos")
    if contexto not in CONTEXTOS_HISTORICO:
        contexto = "todos"

    with transacao() as conn:
        if contexto == "todos":
            registros = conn.execute(
                "SELECT * FROM compilador_historico WHERE usuario_id = ? ORDER BY id DESC LIMIT 100",
                (usuario["id"],),
            ).fetchall()
        else:
            registros = conn.execute(
                """
                SELECT * FROM compilador_historico
                WHERE usuario_id = ? AND contexto = ? ORDER BY id DESC LIMIT 100
                """,
                (usuario["id"], contexto),
            ).fetchall()
        resumo = conn.execute(
            """
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN aprovado = 1 THEN 1 ELSE 0 END) AS aprovados
            FROM compilador_historico WHERE usuario_id = ?
            """,
            (usuario["id"],),
        ).fetchone()

    itens = []
    for registro in registros:
        modulo, licao = encontrar_licao(registro["licao_id"])
        itens.append({
            "registro": registro,
            "titulo": licao["titulo"] if licao else "Prática livre",
            "modulo": modulo["titulo"] if modulo else "Laboratório",
        })

    return render_template(
        "compilador/historico.html",
        itens=itens,
        contexto=contexto,
        total=resumo["total"] or 0,
        aprovados=resumo["aprovados"] or 0,
    )
