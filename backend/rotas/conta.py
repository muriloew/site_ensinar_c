"""Configurações da conta: perfil, senha, preferências e exclusão da conta."""

from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from backend.banco.conexao import transacao
from backend.sessao import usuario_logado
from backend.usuarios import definir_senha, excluir_usuario, validar_email, validar_nome, validar_nova_senha

bp = Blueprint("conta", __name__)

AVISOS = {
    "senha_temporaria": "Você entrou com uma senha temporária. Crie uma senha nova para continuar usando sua conta com segurança.",
}


def _pagina(usuario, status=200, **mensagens):
    aviso = AVISOS.get(request.args.get("aviso", ""), "")
    if usuario["senha_temporaria"] and not aviso:
        aviso = AVISOS["senha_temporaria"]
    return render_template("conta/configuracoes.html", aviso=aviso, **mensagens), status


def _senha_confere(usuario_id, senha):
    with transacao() as conn:
        linha = conn.execute("SELECT senha FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    return bool(linha) and check_password_hash(linha["senha"], senha)


@bp.route("/configuracoes", methods=["GET", "POST"])
def configuracoes():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("publico.login"))
    if request.method == "GET":
        return _pagina(usuario)

    acao = request.form.get("acao", "")
    senha_atual = request.form.get("senha_atual", "")

    if acao == "perfil":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        erro = validar_nome(nome) or validar_email(email)
        if not erro and email != usuario["email"] and not _senha_confere(usuario["id"], senha_atual):
            erro = "Para trocar o e-mail, confirme sua senha atual."
        if not erro:
            with transacao() as conn:
                ocupado = conn.execute(
                    "SELECT id FROM usuarios WHERE email = ? AND id <> ?", (email, usuario["id"])
                ).fetchone()
                if ocupado:
                    erro = "Este e-mail já é usado por outra conta."
                else:
                    conn.execute(
                        "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?", (nome, email, usuario["id"])
                    )
        if erro:
            return _pagina(usuario, 400, erro_perfil=erro)
        return redirect(url_for("conta.configuracoes", salvo="perfil"))

    if acao == "senha":
        erro = "" if _senha_confere(usuario["id"], senha_atual) else "A senha atual está incorreta."
        erro = erro or validar_nova_senha(
            request.form.get("nova_senha", ""), request.form.get("confirmar_senha", "")
        )
        if erro:
            return _pagina(usuario, 400, erro_senha=erro)
        with transacao() as conn:
            definir_senha(conn, usuario["id"], request.form["nova_senha"])
        return redirect(url_for("conta.configuracoes", salvo="senha"))

    if acao == "excluir":
        if request.form.get("confirmacao", "").strip().upper() != "EXCLUIR":
            return _pagina(usuario, 400, erro_excluir='Digite EXCLUIR para confirmar.')
        if not _senha_confere(usuario["id"], senha_atual):
            return _pagina(usuario, 400, erro_excluir="A senha atual está incorreta.")
        with transacao() as conn:
            excluir_usuario(conn, usuario["id"])
        session.clear()
        return redirect(url_for("publico.index", conta="excluida"))

    return _pagina(usuario, 400)
