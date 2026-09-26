"""Histórico das últimas execuções de código de cada aluno."""

from datetime import datetime

LIMITE_HISTORICO = 100


def registrar_historico_codigo(
    conn,
    usuario_id,
    codigo,
    entrada,
    saida,
    build_log,
    contexto="livre",
    licao_id=None,
    modulo_id=None,
    aprovado=False,
    origem="",
):
    conn.execute(
        """
        INSERT INTO compilador_historico
            (usuario_id, codigo, entrada, saida, build_log, criado_em,
             contexto, licao_id, modulo_id, aprovado, origem)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            usuario_id,
            codigo,
            entrada,
            saida,
            build_log,
            datetime.now().isoformat(timespec="seconds"),
            contexto,
            licao_id,
            modulo_id,
            1 if aprovado else 0,
            origem,
        ),
    )
    conn.execute(
        """
        DELETE FROM compilador_historico
        WHERE usuario_id = ? AND id NOT IN (
            SELECT id FROM compilador_historico
            WHERE usuario_id = ? ORDER BY id DESC LIMIT ?
        )
        """,
        (usuario_id, usuario_id, LIMITE_HISTORICO),
    )
