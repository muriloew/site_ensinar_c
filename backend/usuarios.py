"""Regras da conta: validação do cadastro, senha, exclusão da conta e acesso de professor."""

import os
import re

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
)


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
