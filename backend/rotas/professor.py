"""Painel do professor: progresso da turma, exercícios difíceis e redefinição de senha."""

import secrets
from datetime import date, timedelta

from flask import Blueprint, abort, render_template

from backend.banco.conexao import transacao
from backend.conteudo.trilha import TOTAL_LICOES, encontrar_licao
from backend.sessao import usuario_logado
from backend.usuarios import definir_senha, eh_professor

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

    semana = (date.today() - timedelta(days=6)).isoformat()
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


@bp.route("/professor")
def painel():
    _exigir_professor()
    with transacao() as conn:
        resumo, alunos, dificuldades = _dados_da_turma(conn)
    return render_template(
        "professor/painel.html", resumo=resumo, alunos=alunos, dificuldades=dificuldades, total=TOTAL_LICOES
    )


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
        resumo, alunos, dificuldades = _dados_da_turma(conn)
    return render_template(
        "professor/painel.html",
        resumo=resumo,
        alunos=alunos,
        dificuldades=dificuldades,
        total=TOTAL_LICOES,
        senha_nova={"nome": aluno["nome"], "email": aluno["email"], "senha": senha},
    )
