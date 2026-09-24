"""Regras da conta: validação do cadastro, senha, exclusão da conta e acesso de professor."""

import hashlib
import os
import re
import secrets
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

TAMANHO_MINIMO_SENHA = 8
TAMANHO_MAXIMO_SENHA = 128
TAMANHO_MAXIMO_NOME = 60
TAMANHO_MAXIMO_EMAIL = 120
FORMATO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Todas as tabelas com dados do aluno; a exclusão da conta apaga cada uma delas.
TABELAS_DO_USUARIO = (
    "progresso",
    "conquistas_usuario",
    "desafios_diarios",
    "compilador_historico",
    "metas_usuario",
    "simulados_usuario",
    "atividades_estudo",
    "recompensas_diarias",
    "favoritos_usuario",
    "revisoes_usuario",
    "anotacoes_usuario",
    "redefinicoes_senha",
)

VALIDADE_LINK_SENHA = timedelta(hours=1)


def validar_nome(nome):
    if not nome:
        return "Informe seu nome."
    if len(nome) > TAMANHO_MAXIMO_NOME:
        return f"O nome pode ter no máximo {TAMANHO_MAXIMO_NOME} caracteres."
    return ""


def validar_email(email):
    if not email or len(email) > TAMANHO_MAXIMO_EMAIL or not FORMATO_EMAIL.match(email):
        return "Informe um e-mail válido, como nome@exemplo.com."
    return ""


def validar_nova_senha(senha, confirmacao):
    if len(senha) < TAMANHO_MINIMO_SENHA:
        return f"A senha precisa ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres."
    if len(senha) > TAMANHO_MAXIMO_SENHA:
        return f"A senha pode ter no máximo {TAMANHO_MAXIMO_SENHA} caracteres."
    if senha != confirmacao:
        return "A confirmação não é igual à senha."
    return ""


def definir_senha(conn, usuario_id, senha, temporaria=False):
    conn.execute(
        "UPDATE usuarios SET senha = ?, senha_temporaria = ? WHERE id = ?",
        (generate_password_hash(senha), 1 if temporaria else 0, usuario_id),
    )


def excluir_usuario(conn, usuario_id):
    for tabela in TABELAS_DO_USUARIO:
        conn.execute(f"DELETE FROM {tabela} WHERE usuario_id = ?", (usuario_id,))
    conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))


def emails_professores():
    return {
        email.strip().lower()
        for email in os.environ.get("ADMIN_EMAILS", "").split(",")
        if email.strip()
    }


def eh_professor(usuario):
    return bool(usuario) and usuario["email"] in emails_professores()


def _agora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def criar_link_redefinicao(conn, usuario_id):
    """Cria um código de uso único; no banco fica só o hash, nunca o código do link."""
    conn.execute("UPDATE redefinicoes_senha SET usado = 1 WHERE usuario_id = ?", (usuario_id,))
    token = secrets.token_urlsafe(32)
    expira = (datetime.now(timezone.utc) + VALIDADE_LINK_SENHA).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO redefinicoes_senha (usuario_id, token_hash, expira_em, criado_em) VALUES (?, ?, ?, ?)",
        (usuario_id, _hash_token(token), expira, _agora()),
    )
    return token


def usuario_do_link(conn, token):
    linha = conn.execute(
        """
        SELECT usuario_id FROM redefinicoes_senha
        WHERE token_hash = ? AND usado = 0 AND expira_em > ?
        """,
        (_hash_token(token), _agora()),
    ).fetchone()
    return linha["usuario_id"] if linha else None


def encerrar_links_redefinicao(conn, usuario_id):
    conn.execute("UPDATE redefinicoes_senha SET usado = 1 WHERE usuario_id = ?", (usuario_id,))
