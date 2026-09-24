"""Página inicial, cadastro, login e saída."""

from datetime import date

from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.banco.conexao import transacao
from backend.seguranca import FALHAS_POR_EMAIL, FALHAS_POR_IP
from backend.sessao import usuario_logado

bp = Blueprint("publico", __name__)

TAMANHO_MINIMO_SENHA = 8


@bp.route("/")
def index():
    if usuario_logado():
        return redirect(url_for("painel.dashboard"))
    return render_template("publico/index.html")


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("publico/cadastro.html")

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    if not nome or not email or not senha:
        return render_template("publico/cadastro.html", erro="Preencha nome, e-mail e senha.")
    if len(senha) < TAMANHO_MINIMO_SENHA:
        return render_template(
            "publico/cadastro.html",
            erro=f"A senha precisa ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres.",
        )

    with transacao() as conn:
        if conn.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone():
            return render_template(
                "publico/cadastro.html",
                erro="Este e-mail já está cadastrado. Entre na conta em vez de criar outra.",
            )
        novo_id = conn.execute(
            """
            INSERT INTO usuarios
                (nome, email, senha, sequencia, melhor_sequencia, protecoes_sequencia, ultimo_acesso)
            VALUES (?, ?, ?, 0, 0, 1, ?)
            RETURNING id
            """,
            (nome, email, generate_password_hash(senha), str(date.today())),
        ).fetchone()["id"]

    session.clear()
    session["usuario_id"] = novo_id
    return redirect(url_for("painel.dashboard"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("publico/login.html")

    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    chave_email, chave_ip = f"email:{email}", f"ip:{request.remote_addr}"
    if FALHAS_POR_EMAIL.bloqueado(chave_email) or FALHAS_POR_IP.bloqueado(chave_ip):
        return render_template(
            "publico/login.html",
            erro="Muitas tentativas erradas. Aguarde 15 minutos e tente de novo.",
        ), 429

    with transacao() as conn:
        usuario = conn.execute("SELECT id, senha FROM usuarios WHERE email = ?", (email,)).fetchone()
        if not usuario or not check_password_hash(usuario["senha"], senha):
            FALHAS_POR_EMAIL.registrar_falha(chave_email)
            FALHAS_POR_IP.registrar_falha(chave_ip)
            return render_template("publico/login.html", erro="E-mail ou senha incorretos.")
        conn.execute(
            "UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?",
            (str(date.today()), usuario["id"]),
        )

    FALHAS_POR_EMAIL.esquecer(chave_email)
    session.clear()
    session["usuario_id"] = usuario["id"]
    return redirect(url_for("painel.dashboard"))


@bp.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("publico.index"))
