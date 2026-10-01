"""Notificações do aluno: novo desafio do dia, módulo liberado, revisões pendentes e avisos do professor.

As notificações automáticas são criadas enquanto o aluno usa o site (no máximo uma verificação por minuto), sem
tarefas agendadas no servidor. Cada uma tem uma chave única por aluno, como "desafio:2026-10-01", então não se repete.
"""

from datetime import timedelta

from backend import relogio
from backend.aluno.situacao import SituacaoAluno
from backend.conteudo.trilha import modulo_por_id

INTERVALO_VERIFICACAO = 60  # segundos entre duas verificações automáticas do mesmo aluno
DIAS_AVISO = 30  # avisos do professor mais antigos que isso não chegam a quem entrou depois
LIMITE_LISTA = 50
TAMANHO_TITULO = 80
TAMANHO_MENSAGEM = 500

ICONES = {"desafio": "🎯", "modulo": "🔓", "revisao": "↻", "aviso": "📣"}


def criar(conn, usuario_id, chave, tipo, titulo, mensagem="", link=""):
    conn.execute(
        """
        INSERT INTO notificacoes (usuario_id, chave, tipo, titulo, mensagem, link, criada_em, lida)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        ON CONFLICT (usuario_id, chave) DO NOTHING
        """,
        (usuario_id, chave, tipo, titulo, mensagem, link, relogio.agora().isoformat(timespec="seconds")),
    )


def gerar(conn, usuario_id, lembretes=True):
    """Cria as notificações que ainda faltam para o aluno; as que já existem são ignoradas."""
    hoje = relogio.hoje().isoformat()
    situacao = SituacaoAluno(usuario_id, conn)

    # O professor já vê a trilha inteira liberada, então avisar módulos liberados não faz sentido para ele.
    if not situacao.professor:
        maximo = situacao.modulo_maximo_liberado()
        if maximo > 1:
            modulo = modulo_por_id(maximo)
            criar(conn, usuario_id, f"modulo:{maximo}", "modulo", f"Módulo {maximo} liberado: {modulo['titulo']}",
                  modulo["descricao"], f"/estudar/{maximo}")

    if lembretes:
        desafios, _ = situacao.desafios_disponiveis()
        registro = conn.execute(
            "SELECT concluido FROM desafios_diarios WHERE usuario_id = ? AND data = ?", (usuario_id, hoje)
        ).fetchone()
        if desafios and not (registro and registro["concluido"]):
            desafio = situacao.desafio_do_dia(hoje)
            criar(conn, usuario_id, f"desafio:{hoje}", "desafio", "Novo desafio diário",
                  f"{desafio['titulo']} ({desafio['nivel']}) já está esperando por você.", "/desafio-diario")

        pendentes = conn.execute(
            "SELECT COUNT(*) AS total FROM revisoes_usuario WHERE usuario_id = ? AND proxima_revisao <= ?",
            (usuario_id, hoje),
        ).fetchone()["total"]
        if pendentes:
            plural = "lição para revisar" if pendentes == 1 else "lições para revisar"
            criar(conn, usuario_id, f"revisao:{hoje}", "revisao", "Revisões de hoje",
                  f"Você tem {pendentes} {plural} hoje.", "/revisao")

    desde = (relogio.agora() - timedelta(days=DIAS_AVISO)).isoformat(timespec="seconds")
    for aviso in conn.execute("SELECT * FROM avisos WHERE criado_em >= ? ORDER BY id", (desde,)).fetchall():
        criar(conn, usuario_id, f"aviso:{aviso['id']}", "aviso", aviso["titulo"], aviso["mensagem"],
              aviso["link"] or "")


def contar_nao_lidas(conn, usuario_id):
    return conn.execute(
        "SELECT COUNT(*) AS total FROM notificacoes WHERE usuario_id = ? AND lida = 0", (usuario_id,)
    ).fetchone()["total"]


def listar(conn, usuario_id):
    linhas = conn.execute(
        f"SELECT * FROM notificacoes WHERE usuario_id = ? ORDER BY id DESC LIMIT {LIMITE_LISTA}", (usuario_id,)
    ).fetchall()
    return [{**dict(zip(linha.keys(), linha)), "icone": ICONES.get(linha["tipo"], "🔔")} for linha in linhas]


def marcar_lida(conn, usuario_id, notificacao_id):
    """Marca uma notificação como lida e devolve o link dela (ou None se não for do aluno)."""
    linha = conn.execute(
        "SELECT link FROM notificacoes WHERE id = ? AND usuario_id = ?", (notificacao_id, usuario_id)
    ).fetchone()
    if not linha:
        return None
    conn.execute("UPDATE notificacoes SET lida = 1 WHERE id = ?", (notificacao_id,))
    return linha["link"] or ""


def marcar_todas_lidas(conn, usuario_id):
    conn.execute("UPDATE notificacoes SET lida = 1 WHERE usuario_id = ? AND lida = 0", (usuario_id,))


def link_interno(link):
    """Só aceita caminhos do próprio site, como /modulos, para um aviso não levar o aluno a outro site."""
    link = (link or "").strip()
    return link if link.startswith("/") and not link.startswith("//") else ""


def publicar_aviso(conn, autor_id, titulo, mensagem, link=""):
    titulo, mensagem = titulo.strip(), mensagem.strip()
    if not titulo or not mensagem:
        return "Preencha o título e a mensagem do aviso."
    if len(titulo) > TAMANHO_TITULO or len(mensagem) > TAMANHO_MENSAGEM:
        return f"O título pode ter até {TAMANHO_TITULO} caracteres e a mensagem até {TAMANHO_MENSAGEM}."
    if link.strip() and not link_interno(link):
        return "O link deve ser uma página do próprio site, começando com /, como /modulos."
    conn.execute(
        "INSERT INTO avisos (autor_id, titulo, mensagem, link, criado_em) VALUES (?, ?, ?, ?, ?)",
        (autor_id, titulo, mensagem, link_interno(link), relogio.agora().isoformat(timespec="seconds")),
    )
    return ""


def excluir_aviso(conn, aviso_id):
    conn.execute("DELETE FROM notificacoes WHERE chave = ?", (f"aviso:{aviso_id}",))
    conn.execute("DELETE FROM avisos WHERE id = ?", (aviso_id,))


def avisos_recentes(conn, limite=10):
    return conn.execute(f"SELECT * FROM avisos ORDER BY id DESC LIMIT {limite}").fetchall()
