"""Painel inicial, missões diárias, perfil, metas, backup e simulado."""

import io
import json
from datetime import date, datetime

from flask import Blueprint, redirect, render_template, request, send_file, url_for

from backend.aluno.gamificacao import (
    calendario_atividade,
    estado_nivel,
    liga_por_xp,
    obter_missoes_diarias,
    registrar_atividade,
    resgatar_missao,
    sincronizar_conquistas,
)
from backend.aluno.metas import progresso_metas, salvar_metas
from backend.aluno.relatorios import dados_backup, questoes_simulado, relatorio_modulos, resumo_desempenho
from backend.aluno.revisao import sincronizar_revisoes
from backend.aluno.situacao import SituacaoAluno
from backend.banco.conexao import transacao
from backend.conteudo.trilha import TOTAL_LICOES, encontrar_licao
from backend.sessao import usuario_logado

bp = Blueprint("painel", __name__)


def _porcentagem_geral(situacao):
    return int((situacao.total_concluidas / TOTAL_LICOES) * 100)


@bp.route("/dashboard")
def dashboard():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    usuario_id = usuario["id"]

    with transacao() as conn:
        situacao = SituacaoAluno(usuario_id, conn)
        sincronizar_conquistas(conn, usuario_id)
        sincronizar_revisoes(conn, usuario_id)
        desafios_disponiveis, _ = situacao.desafios_disponiveis()
        conquistas = conn.execute(
            "SELECT * FROM conquistas_usuario WHERE usuario_id = ? ORDER BY id DESC",
            (usuario_id,),
        ).fetchall()
        ranking = conn.execute(
            "SELECT nome, xp, nivel FROM usuarios ORDER BY xp DESC, nivel DESC LIMIT 5"
        ).fetchall()
        missoes = obter_missoes_diarias(conn, usuario_id, bool(desafios_disponiveis))
        calendario = calendario_atividade(conn, usuario_id)
        revisoes_pendentes = conn.execute(
            """
            SELECT COUNT(*) AS total FROM revisoes_usuario
            WHERE usuario_id = ? AND proxima_revisao <= ?
            """,
            (usuario_id, date.today().isoformat()),
        ).fetchone()["total"]

    proxima_licao = situacao.proxima_licao()
    inicio_destaques = max(0, proxima_licao["modulo_id"] - 2)
    modulos_destaque = situacao.modulos_com_estado()[inicio_destaques:inicio_destaques + 3]

    return render_template(
        "painel/dashboard.html",
        concluidas=situacao.total_concluidas,
        conquistas=conquistas,
        ranking=ranking,
        missoes=missoes,
        calendario=calendario,
        nivel_jogo=estado_nivel(usuario["xp"]),
        liga=liga_por_xp(usuario["xp"]),
        proxima_licao=proxima_licao,
        modulos_destaque=modulos_destaque,
        recompensa_mensagem=request.args.get("recompensa", ""),
        aviso_mensagem=request.args.get("aviso", ""),
        revisoes_pendentes=revisoes_pendentes,
    )


@bp.route("/missoes/<missao_id>/resgatar", methods=["POST"])
def resgatar_recompensa_diaria(missao_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    with transacao() as conn:
        desafios_disponiveis, _ = SituacaoAluno(usuario["id"], conn).desafios_disponiveis()
        resultado = resgatar_missao(conn, usuario["id"], missao_id, bool(desafios_disponiveis))
        if resultado["ok"]:
            sincronizar_conquistas(conn, usuario["id"])

    if resultado["ok"]:
        return redirect(url_for("painel.dashboard", recompensa=resultado["mensagem"]))
    return redirect(url_for("painel.dashboard", aviso=resultado["mensagem"]))


@bp.route("/perfil")
def perfil():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    usuario_id = usuario["id"]

    with transacao() as conn:
        situacao = SituacaoAluno(usuario_id, conn)
        sincronizar_conquistas(conn, usuario_id)
        desempenho = resumo_desempenho(conn, usuario_id)
        metas = progresso_metas(conn, usuario_id)
        modulos_relatorio = relatorio_modulos(conn, usuario_id, situacao)
        conquistas = conn.execute(
            "SELECT * FROM conquistas_usuario WHERE usuario_id = ? ORDER BY id DESC",
            (usuario_id,),
        ).fetchall()
        calendario = calendario_atividade(conn, usuario_id)

    return render_template(
        "painel/perfil.html",
        concluidas=situacao.total_concluidas,
        porcentagem=_porcentagem_geral(situacao),
        desempenho=desempenho,
        metas=metas,
        modulos_relatorio=modulos_relatorio,
        conquistas=conquistas,
        calendario=calendario,
        liga=liga_por_xp(usuario["xp"]),
        nivel_jogo=estado_nivel(usuario["xp"]),
    )


@bp.route("/metas", methods=["POST"])
def metas():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    with transacao() as conn:
        salvar_metas(conn, usuario["id"], request.form)
    return redirect(url_for("painel.perfil"))


@bp.route("/backup-progresso")
def baixar_backup_progresso():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))

    with transacao() as conn:
        dados = dados_backup(conn, usuario["id"])
    arquivo = io.BytesIO(json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8"))
    return send_file(
        arquivo,
        mimetype="application/json",
        as_attachment=True,
        download_name=f"backup_progresso_{usuario['id']}_{date.today()}.json",
    )


@bp.route("/simulado", methods=["GET", "POST"])
def simulado():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    usuario_id = usuario["id"]

    resultado = None
    resultados = []
    if request.method == "POST":
        for valor in request.form.getlist("questoes"):
            try:
                licao_id = int(valor)
            except ValueError:
                continue
            modulo, licao = encontrar_licao(licao_id)
            if not licao:
                continue
            resposta = request.form.get(f"q_{licao_id}", "")
            resultados.append({
                "modulo": modulo["titulo"],
                "licao": licao["titulo"],
                "pergunta": licao["pergunta"],
                "resposta_usuario": resposta or "Sem resposta",
                "resposta_correta": licao["resposta"],
                "correta": resposta == licao["resposta"],
            })

        total = len(resultados)
        acertos = sum(1 for item in resultados if item["correta"])
        percentual = int((acertos / total) * 100) if total else 0
        resultado = {"acertos": acertos, "total": total, "percentual": percentual}

        with transacao() as conn:
            conn.execute(
                """
                INSERT INTO simulados_usuario (usuario_id, acertos, total, percentual, criado_em)
                VALUES (?, ?, ?, ?, ?)
                """,
                (usuario_id, acertos, total, percentual, datetime.now().isoformat(timespec="seconds")),
            )
            registrar_atividade(conn, usuario_id)
            sincronizar_conquistas(conn, usuario_id)

    return render_template(
        "painel/simulado.html",
        questoes=questoes_simulado(usuario_id, SituacaoAluno(usuario_id)),
        resultado=resultado,
        resultados=resultados,
    )
