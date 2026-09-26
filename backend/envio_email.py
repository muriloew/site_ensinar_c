"""Envio de e-mails pela API HTTPS do Brevo (o Render gratuito bloqueia as portas SMTP)."""

import logging
import os

import requests

URL_BREVO = "https://api.brevo.com/v3/smtp/email"

registro = logging.getLogger(__name__)


def email_configurado():
    return bool(os.environ.get("BREVO_API_KEY", "").strip() and os.environ.get("EMAIL_REMETENTE", "").strip())


def enviar_email(destinatario, nome, assunto, texto, html):
    """Devolve True quando o Brevo aceitou a mensagem."""
    if not email_configurado():
        return False
    try:
        resposta = requests.post(
            URL_BREVO,
            headers={"api-key": os.environ["BREVO_API_KEY"].strip(), "accept": "application/json"},
            json={
                "sender": {
                    "email": os.environ["EMAIL_REMETENTE"].strip(),
                    "name": os.environ.get("EMAIL_REMETENTE_NOME", "Ensinar C"),
                },
                "to": [{"email": destinatario, "name": nome}],
                "subject": assunto,
                "textContent": texto,
                "htmlContent": html,
            },
            timeout=10,
        )
    except requests.RequestException as erro:
        registro.warning("Falha ao enviar e-mail: %s", erro)
        return False
    if not resposta.ok:
        registro.warning("Brevo recusou o e-mail (%s): %s", resposta.status_code, resposta.text[:300])
    return resposta.ok
