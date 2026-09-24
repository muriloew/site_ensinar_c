"""Ponto de entrada do site Ensinar C. O Gunicorn carrega o objeto `app` deste arquivo."""

import os
import secrets
from datetime import timedelta

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from backend.banco.tabelas import criar_tabelas
from backend.compilador.terminal import socketio
from backend.conteudo.trilha import TOTAL_LICOES
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
        usuario = usuario_logado()
        return {
            "usuario": usuario,
            "professor": eh_professor(usuario),
            "total_licoes": TOTAL_LICOES,
            "csrf_token": token_csrf,
        }

    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template("publico/erro.html", mensagem="Página não encontrada."), 404

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
