"""Usuário logado na requisição atual."""

from flask import g, session

from backend.banco.conexao import transacao


def usuario_logado():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return None

    # A mesma requisição consulta o usuário na rota e no menu; basta ler uma vez.
    if g.get("usuario_id_carregado") != usuario_id:
        with transacao() as conn:
            g.usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
        g.usuario_id_carregado = usuario_id
    return g.usuario
