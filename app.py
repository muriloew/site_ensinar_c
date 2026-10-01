"""Ponto de entrada do site Ensinar C. O Gunicorn carrega o objeto `app` deste arquivo."""

import os
import re
import secrets
import time
from datetime import timedelta

from flask import Flask, render_template, request, session
from markupsafe import Markup, escape
from werkzeug.middleware.proxy_fix import ProxyFix

from backend.aluno import notificacoes
from backend.banco.tabelas import criar_tabelas
from backend.compilador.terminal import socketio
from backend.banco.conexao import transacao
from backend.conteudo.trilha import TOTAL_LICOES
from backend.preferencias import PADROES, ler_preferencias
from backend.rotas import registrar_rotas
from backend.seguranca import token_csrf, verificar_csrf
from backend.sessao import usuario_logado
from backend.usuarios import eh_professor


def criar_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.config.update(
        MAX_CONTENT_LENGTH=256 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=bool(os.environ.get("RENDER")),
        PERMANENT_SESSION_LIFETIME=timedelta(days=30),
    )
    if os.environ.get("RENDER"):
        # O Render repassa o IP do visitante no cabeçalho X-Forwarded-For.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    app.before_request(verificar_csrf)

    @app.url_defaults
    def versionar_arquivo_estatico(endpoint, valores):
        # A data de modificação na URL faz o navegador baixar CSS e JS atualizados.
        if endpoint != "static" or "v" in valores or not valores.get("filename"):
            return
        try:
            valores["v"] = str(os.stat(os.path.join(app.static_folder, valores["filename"])).st_mtime_ns)
        except OSError:
            pass

    @app.after_request
    def cabecalhos_de_seguranca(resposta):
        resposta.headers.setdefault("X-Content-Type-Options", "nosniff")
        resposta.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resposta.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        return resposta

    @app.context_processor
    def dados_do_menu():
        # Se o banco falhar aqui, a página (inclusive a de erro) ainda aparece, como se ninguém estivesse logado.
        usuario = None
        preferencias = dict(PADROES)
        nao_lidas = 0
        try:
            usuario = usuario_logado()
            if usuario:
                with transacao() as conn:
                    preferencias = ler_preferencias(conn, usuario["id"])
        except Exception:
            app.logger.exception("Falha ao ler o usuário para montar o menu")
            usuario = None
        if usuario:
            # As notificações automáticas são verificadas no máximo uma vez por minuto; se falharem, a página abre.
            try:
                with transacao() as conn:
                    if time.time() - session.get("notificacoes_verificadas", 0) > notificacoes.INTERVALO_VERIFICACAO:
                        notificacoes.gerar(conn, usuario["id"], preferencias["lembretes"] == "sim")
                        session["notificacoes_verificadas"] = time.time()
                    nao_lidas = notificacoes.contar_nao_lidas(conn, usuario["id"])
            except Exception:
                app.logger.exception("Falha ao verificar as notificações")
        return {
            "usuario": usuario,
            "preferencias": preferencias,
            "notificacoes_nao_lidas": nao_lidas,
            "professor": eh_professor(usuario),
            "total_licoes": TOTAL_LICOES,
            "csrf_token": token_csrf,
        }

    @app.template_filter("data_hora")
    def data_hora(texto):
        """'2026-10-01T12:16:05' vira '01/10/2026 às 12:16'."""
        texto = str(texto or "")
        if len(texto) < 16:
            return texto
        return f"{texto[8:10]}/{texto[5:7]}/{texto[:4]} às {texto[11:16]}"

    @app.template_filter("codigo_inline")
    def codigo_inline(texto):
        """Mostra os trechos entre crases do conteúdo das lições como código."""
        return Markup(re.sub(r"`([^`]+)`", r"<code>\1</code>", str(escape(texto))))

    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template("publico/erro.html", mensagem="Página não encontrada."), 404

    @app.errorhandler(500)
    def erro_interno(erro):
        # O código aparece para o usuário e no log do Render junto com a causa, para achar o erro rápido.
        codigo = secrets.token_hex(3).upper()
        app.logger.error(
            "ERRO %s em %s %s", codigo, request.method, request.path,
            exc_info=getattr(erro, "original_exception", None) or erro,
        )
        mensagem = "Tivemos um problema ao abrir esta página. Tente recarregar em alguns segundos."
        return render_template("publico/erro.html", mensagem=mensagem, codigo_erro=codigo), 500

    registrar_rotas(app)

    opcoes_socket = {"async_mode": "threading"}
    origens = os.environ.get("SOCKETIO_CORS_ORIGINS", "").strip()
    if origens:
        opcoes_socket["cors_allowed_origins"] = [
            origem.strip() for origem in origens.split(",") if origem.strip()
        ]
    socketio.init_app(app, **opcoes_socket)

    criar_tabelas()
    return app


app = criar_app()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
