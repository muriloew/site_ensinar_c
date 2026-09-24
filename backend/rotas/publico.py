"""Página inicial, cadastro, login e saída."""

from datetime import date

from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.banco.conexao import transacao
from backend.seguranca import FALHAS_POR_EMAIL, FALHAS_POR_IP
from backend.sessao import usuario_logado
from backend.usuarios import emails_professores, validar_email, validar_nome, validar_nova_senha

bp = Blueprint("publico", __name__)


def _iniciar_sessao(usuario_id, lembrar):
    session.clear()
    session["usuario_id"] = usuario_id
    session.permanent = lembrar


@bp.route("/")
def index():
    if usuario_logado():
        return redirect(url_for("painel.dashboard"))
    return render_template("publico/index.html", conta_excluida=request.args.get("conta") == "excluida")


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("publico/cadastro.html")

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    confirmacao = request.form.get("confirmar_senha", senha)
    erro = validar_nome(nome) or validar_email(email) or validar_nova_senha(senha, confirmacao)
    if erro:
        return render_template("publico/cadastro.html", erro=erro, nome=nome, email=email)

    with transacao() as conn:
        if conn.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone():
            return render_template(
                "publico/cadastro.html",
                erro="Este e-mail já está cadastrado. Entre na conta em vez de criar outra.",
                nome=nome,
                email=email,
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

    _iniciar_sessao(novo_id, lembrar=True)
    return redirect(url_for("painel.dashboard"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    ha_professor = bool(emails_professores())
    if request.method == "GET":
        return render_template("publico/login.html", ha_professor=ha_professor)

    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    chave_email, chave_ip = f"email:{email}", f"ip:{request.remote_addr}"
    if FALHAS_POR_EMAIL.bloqueado(chave_email) or FALHAS_POR_IP.bloqueado(chave_ip):
        return render_template(
            "publico/login.html",
            erro="Muitas tentativas erradas. Aguarde 15 minutos e tente de novo.",
            email=email,
            ha_professor=ha_professor,
        ), 429

    with transacao() as conn:
        usuario = conn.execute(
            "SELECT id, senha, senha_temporaria FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        if not usuario or not check_password_hash(usuario["senha"], senha):
            FALHAS_POR_EMAIL.registrar_falha(chave_email)
            FALHAS_POR_IP.registrar_falha(chave_ip)
            return render_template(
                "publico/login.html", erro="E-mail ou senha incorretos.", email=email, ha_professor=ha_professor
            )
        conn.execute(
            "UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?",
            (str(date.today()), usuario["id"]),
        )

    FALHAS_POR_EMAIL.esquecer(chave_email)
    _iniciar_sessao(usuario["id"], lembrar=bool(request.form.get("lembrar")))
    if usuario["senha_temporaria"]:
        return redirect(url_for("conta.configuracoes", aviso="senha_temporaria"))
    return redirect(url_for("painel.dashboard"))


@bp.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("publico.index"))
