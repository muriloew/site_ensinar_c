"""Painel do professor: progresso da turma, exercícios difíceis, redefinição de senha e avisos para a turma."""

import secrets
from datetime import timedelta

from flask import Blueprint, abort, redirect, render_template, request, url_for

from backend.aluno import notificacoes
from backend.banco.conexao import transacao
from backend.conteudo.trilha import TOTAL_LICOES, encontrar_licao
from backend.sessao import usuario_logado
from backend.usuarios import definir_senha, eh_professor, emails_professores
from backend import relogio

bp = Blueprint("professor", __name__)


def _exigir_professor():
    usuario = usuario_logado()
    if not eh_professor(usuario):
        abort(404)
    return usuario


def _dados_da_turma(conn):
    alunos = conn.execute(
        """
        SELECT u.id, u.nome, u.email, u.xp, u.nivel, u.ultima_atividade, u.ultimo_acesso,
               COALESCE(SUM(CASE WHEN p.concluida = 1 THEN 1 ELSE 0 END), 0) AS concluidas
        FROM usuarios u
        LEFT JOIN progresso p ON p.usuario_id = u.id
        GROUP BY u.id, u.nome, u.email, u.xp, u.nivel, u.ultima_atividade, u.ultimo_acesso
        ORDER BY u.nome
        """
    ).fetchall()
    tentativas = conn.execute(
        """
        SELECT licao_id, COUNT(*) AS tentativas,
               SUM(CASE WHEN aprovado = 1 THEN 1 ELSE 0 END) AS aprovadas,
               COUNT(DISTINCT usuario_id) AS alunos
        FROM compilador_historico
        WHERE contexto = 'licao' AND licao_id IS NOT NULL
        GROUP BY licao_id
        """
    ).fetchall()

    semana = (relogio.hoje() - timedelta(days=6)).isoformat()
    professores = emails_professores()
    alunos = [aluno for aluno in alunos if aluno["email"] not in professores]
    lista = [
        {
            "id": aluno["id"],
            "nome": aluno["nome"],
            "email": aluno["email"],
            "xp": aluno["xp"] or 0,
            "concluidas": aluno["concluidas"],
            "progresso": int((aluno["concluidas"] / TOTAL_LICOES) * 100),
            "ultima_atividade": aluno["ultima_atividade"] or aluno["ultimo_acesso"] or "—",
            "ativo": (aluno["ultima_atividade"] or "") >= semana,
        }
        for aluno in alunos
    ]

    dificuldades = []
    for linha in tentativas:
        modulo, licao = encontrar_licao(linha["licao_id"])
        falhas = linha["tentativas"] - (linha["aprovadas"] or 0)
        if licao and falhas > 0:
            dificuldades.append({
                "modulo": modulo["titulo"],
                "licao": licao["titulo"],
                "tentativas": linha["tentativas"],
                "falhas": falhas,
                "alunos": linha["alunos"],
                "taxa_sucesso": int(((linha["aprovadas"] or 0) / linha["tentativas"]) * 100),
            })
    dificuldades.sort(key=lambda item: (-item["falhas"], item["taxa_sucesso"]))

    resumo = {
        "alunos": len(lista),
        "ativos": sum(1 for aluno in lista if aluno["ativo"]),
        "licoes_concluidas": sum(aluno["concluidas"] for aluno in lista),
        "progresso_medio": int(sum(aluno["progresso"] for aluno in lista) / len(lista)) if lista else 0,
    }
    return resumo, lista, dificuldades[:10]


def _pagina(conn, status=200, **extras):
    resumo, alunos, dificuldades = _dados_da_turma(conn)
    return render_template(
        "professor/painel.html",
        resumo=resumo,
        alunos=alunos,
        dificuldades=dificuldades,
        total=TOTAL_LICOES,
        avisos=notificacoes.avisos_recentes(conn),
        **extras,
    ), status


@bp.route("/professor")
def painel():
    _exigir_professor()
    with transacao() as conn:
        return _pagina(conn, aviso_publicado=request.args.get("aviso") == "publicado")


@bp.route("/professor/avisos", methods=["POST"])
def publicar_aviso():
    professor = _exigir_professor()
    formulario = {campo: request.form.get(campo, "") for campo in ("titulo", "mensagem", "link")}
    with transacao() as conn:
        erro = notificacoes.publicar_aviso(conn, professor["id"], **formulario)
        if erro:
            return _pagina(conn, 400, erro_aviso=erro, aviso_form=formulario)
    return redirect(url_for("professor.painel", aviso="publicado") + "#avisos")


@bp.route("/professor/avisos/<int:aviso_id>/excluir", methods=["POST"])
def excluir_aviso(aviso_id):
    _exigir_professor()
    with transacao() as conn:
        notificacoes.excluir_aviso(conn, aviso_id)
    return redirect(url_for("professor.painel") + "#avisos")


@bp.route("/professor/alunos/<int:aluno_id>/redefinir-senha", methods=["POST"])
def redefinir_senha(aluno_id):
    _exigir_professor()
    senha = secrets.token_urlsafe(9)
    with transacao() as conn:
        aluno = conn.execute("SELECT id, nome, email FROM usuarios WHERE id = ?", (aluno_id,)).fetchone()
        if not aluno:
            abort(404)
        # O aluno entra com esta senha e é levado a criar outra em Configurações.
        definir_senha(conn, aluno_id, senha, temporaria=True)
        return _pagina(conn, senha_nova={"nome": aluno["nome"], "email": aluno["email"], "senha": senha})
