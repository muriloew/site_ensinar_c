"""Configurações da conta: dados, segurança, preferências e exclusão da conta."""

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from backend.banco.conexao import transacao
from backend.preferencias import ler_preferencias, preferencias_do_formulario, salvar_preferencias
from backend.sessao import usuario_logado
from backend.usuarios import (
    definir_senha,
    encerrar_outras_sessoes,
    excluir_usuario,
    validar_email,
    validar_nome,
    validar_nova_senha,
)

bp = Blueprint("conta", __name__)

AVISOS = {
    "senha_temporaria": "Você entrou com uma senha temporária. Crie uma senha nova para continuar usando sua conta com segurança.",
}


def _pagina(usuario, status=200, **mensagens):
    aviso = AVISOS.get(request.args.get("aviso", ""), "")
    if usuario["senha_temporaria"] and not aviso:
        aviso = AVISOS["senha_temporaria"]
    with transacao() as conn:
        total_historico = conn.execute(
            "SELECT COUNT(*) AS total FROM compilador_historico WHERE usuario_id = ?", (usuario["id"],)
        ).fetchone()["total"]
    return render_template(
        "conta/configuracoes.html", aviso=aviso, total_historico=total_historico, **mensagens
    ), status


def _versao_da_sessao(conn, usuario_id):
    """Mantém esta sessão aberta depois de uma ação que encerra as sessões antigas."""
    linha = conn.execute("SELECT sessao_versao FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    session["sessao_versao"] = linha["sessao_versao"] or 0


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
        return redirect(url_for("conta.configuracoes", salvo="perfil", _anchor="conta"))

    if acao == "senha":
        erro = "" if _senha_confere(usuario["id"], senha_atual) else "A senha atual está incorreta."
        erro = erro or validar_nova_senha(
            request.form.get("nova_senha", ""), request.form.get("confirmar_senha", "")
        )
        if erro:
            return _pagina(usuario, 400, erro_senha=erro)
        with transacao() as conn:
            definir_senha(conn, usuario["id"], request.form["nova_senha"])
            _versao_da_sessao(conn, usuario["id"])
        return redirect(url_for("conta.configuracoes", salvo="senha", _anchor="seguranca"))

    if acao == "preferencias":
        with transacao() as conn:
            preferencias = preferencias_do_formulario(request.form, ler_preferencias(conn, usuario["id"]))
            salvar_preferencias(conn, usuario["id"], preferencias)
        if request.accept_mimetypes.best == "application/json":
            return jsonify({"ok": True, "preferencias": preferencias})
        secao = request.form.get("secao", "")
        secao = secao if secao in ("aparencia", "editor", "estudo") else "aparencia"
        return redirect(url_for("conta.configuracoes", salvo="preferencias", _anchor=secao))

    if acao == "sair_outros":
        with transacao() as conn:
            encerrar_outras_sessoes(conn, usuario["id"])
            _versao_da_sessao(conn, usuario["id"])
        return redirect(url_for("conta.configuracoes", salvo="sessoes", _anchor="seguranca"))

    if acao == "limpar_historico":
        with transacao() as conn:
            conn.execute("DELETE FROM compilador_historico WHERE usuario_id = ?", (usuario["id"],))
        return redirect(url_for("conta.configuracoes", salvo="historico", _anchor="dados"))

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
