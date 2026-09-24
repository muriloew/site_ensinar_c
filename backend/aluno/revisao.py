"""Revisão espaçada: cada acerto aumenta o intervalo até a próxima revisão da lição."""

from datetime import date, timedelta

INTERVALOS_REVISAO = (1, 3, 7, 14, 30, 60)


def agendar_primeira_revisao(conn, usuario_id, licao_id, data_base=None):
    proxima = (data_base or date.today()) + timedelta(days=INTERVALOS_REVISAO[0])
    conn.execute(
        """
        INSERT INTO revisoes_usuario
            (usuario_id, licao_id, nivel, proxima_revisao, acertos, erros)
        VALUES (?, ?, 0, ?, 0, 0)
        ON CONFLICT (usuario_id, licao_id) DO NOTHING
        """,
        (usuario_id, licao_id, proxima.isoformat()),
    )


def sincronizar_revisoes(conn, usuario_id):
    """Agenda revisão para lições concluídas que ainda não estão na lista."""
    agendadas = {
        linha["licao_id"]
        for linha in conn.execute(
            "SELECT licao_id FROM revisoes_usuario WHERE usuario_id = ?",
            (usuario_id,),
        ).fetchall()
    }
    concluidas = conn.execute(
        """
        SELECT licao_id, COALESCE(concluida_em, atualizado_em) AS concluida_em
        FROM progresso WHERE usuario_id = ? AND concluida = 1
        """,
        (usuario_id,),
    ).fetchall()

    for registro in concluidas:
        if registro["licao_id"] in agendadas:
            continue
        try:
            base = date.fromisoformat(str(registro["concluida_em"] or "")[:10])
        except ValueError:
            base = date.today()
        agendar_primeira_revisao(conn, usuario_id, registro["licao_id"], base)


def proximo_agendamento(nivel_atual, correta):
    novo_nivel = min(len(INTERVALOS_REVISAO) - 1, nivel_atual + 1) if correta else 0
    intervalo = INTERVALOS_REVISAO[novo_nivel]
    return novo_nivel, intervalo, (date.today() + timedelta(days=intervalo)).isoformat()
