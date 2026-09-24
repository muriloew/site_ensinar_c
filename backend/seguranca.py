"""Proteções do site: token CSRF nos envios e limite de tentativas de login."""

import hmac
import secrets
import threading
import time
from collections import defaultdict, deque

from flask import current_app, jsonify, render_template, request, session

METODOS_SEGUROS = {"GET", "HEAD", "OPTIONS"}


def token_csrf():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def verificar_csrf():
    """Recusa envios que não trazem o token da sessão (evita ações disparadas por outros sites)."""
    if request.method in METODOS_SEGUROS or not current_app.config.get("VERIFICAR_CSRF", True):
        return None

    enviado = request.form.get("csrf_token") or request.headers.get("X-CSRFToken", "")
    esperado = session.get("csrf_token", "")
    if esperado and hmac.compare_digest(enviado, esperado):
        return None

    mensagem = "Sua sessão expirou. Recarregue a página e tente novamente."
    if request.is_json or request.accept_mimetypes.best == "application/json":
        return jsonify({"ok": False, "correta": False, "mensagem": mensagem}), 400
    return render_template("publico/erro.html", mensagem=mensagem), 400


class LimiteTentativas:
    """Conta falhas recentes por chave; o site roda em um único processo, então a memória basta."""

    def __init__(self, maximo, janela_segundos):
        self.maximo = maximo
        self.janela = janela_segundos
        self._falhas = defaultdict(deque)
        self._lock = threading.Lock()

    def _limpar_antigas(self, chave, agora):
        falhas = self._falhas[chave]
        while falhas and agora - falhas[0] >= self.janela:
            falhas.popleft()
        return falhas

    def bloqueado(self, chave):
        with self._lock:
            return len(self._limpar_antigas(chave, time.monotonic())) >= self.maximo

    def registrar_falha(self, chave):
        with self._lock:
            agora = time.monotonic()
            self._limpar_antigas(chave, agora).append(agora)

    def esquecer(self, chave):
        with self._lock:
            self._falhas.pop(chave, None)


FALHAS_POR_EMAIL = LimiteTentativas(maximo=5, janela_segundos=15 * 60)
FALHAS_POR_IP = LimiteTentativas(maximo=20, janela_segundos=15 * 60)
PEDIDOS_SENHA_POR_EMAIL = LimiteTentativas(maximo=3, janela_segundos=60 * 60)
PEDIDOS_SENHA_POR_IP = LimiteTentativas(maximo=10, janela_segundos=60 * 60)
