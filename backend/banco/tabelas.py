"""Criação das tabelas e atualização de bancos criados por versões antigas do site."""

from backend.banco.conexao import transacao

CHAVE_PRIMARIA = "INTEGER PRIMARY KEY AUTOINCREMENT"

TABELAS = (
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id {chave},
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        xp INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        sequencia INTEGER DEFAULT 0,
        ultimo_acesso TEXT,
        melhor_sequencia INTEGER DEFAULT 0,
        ultima_atividade TEXT,
        protecoes_sequencia INTEGER DEFAULT 1
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS progresso (
        id {chave},
        usuario_id INTEGER NOT NULL,
        licao_id INTEGER NOT NULL,
        modulo_id INTEGER NOT NULL,
        quiz_correto INTEGER DEFAULT 0,
        quiz_respondido INTEGER DEFAULT 0,
        resposta_teorica TEXT,
        codigo_enviado INTEGER DEFAULT 0,
        concluida INTEGER DEFAULT 0,
        concluida_em TEXT,
        codigo_usuario TEXT,
        saida_codigo TEXT,
        entrada_codigo TEXT,
        codigo_validado INTEGER DEFAULT 0,
        feedback_codigo TEXT,
        atualizado_em TEXT,
        UNIQUE(usuario_id, licao_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS conquistas_usuario (
        id {chave},
        usuario_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        icone TEXT NOT NULL,
        descricao TEXT,
        raridade TEXT DEFAULT 'comum',
        desbloqueada_em TEXT,
        UNIQUE(usuario_id, nome)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS desafios_diarios (
        id {chave},
        usuario_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        desafio_id TEXT,
        codigo_usuario TEXT,
        saida_codigo TEXT,
        entrada_codigo TEXT,
        codigo_validado INTEGER DEFAULT 0,
        feedback_codigo TEXT,
        concluido INTEGER DEFAULT 0,
        UNIQUE(usuario_id, data)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS compilador_historico (
        id {chave},
        usuario_id INTEGER NOT NULL,
        codigo TEXT,
        entrada TEXT,
        saida TEXT,
        build_log TEXT,
        criado_em TEXT,
        contexto TEXT DEFAULT 'livre',
        licao_id INTEGER,
        modulo_id INTEGER,
        aprovado INTEGER DEFAULT 0,
        origem TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS metas_usuario (
        id {chave},
        usuario_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        alvo_licoes INTEGER DEFAULT 1,
        alvo_desafios INTEGER DEFAULT 0,
        atualizado_em TEXT,
        UNIQUE(usuario_id, tipo)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS simulados_usuario (
        id {chave},
        usuario_id INTEGER NOT NULL,
        acertos INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0,
        percentual INTEGER DEFAULT 0,
        criado_em TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS atividades_estudo (
        id {chave},
        usuario_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        quizzes INTEGER DEFAULT 0,
        licoes INTEGER DEFAULT 0,
        desafios INTEGER DEFAULT 0,
        xp_ganho INTEGER DEFAULT 0,
        UNIQUE(usuario_id, data)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS recompensas_diarias (
        id {chave},
        usuario_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        missao_id TEXT NOT NULL,
        xp INTEGER DEFAULT 0,
        recebida_em TEXT,
        UNIQUE(usuario_id, data, missao_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS favoritos_usuario (
        id {chave},
        usuario_id INTEGER NOT NULL,
        licao_id INTEGER NOT NULL,
        criado_em TEXT NOT NULL,
        UNIQUE(usuario_id, licao_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS revisoes_usuario (
        id {chave},
        usuario_id INTEGER NOT NULL,
        licao_id INTEGER NOT NULL,
        nivel INTEGER DEFAULT 0,
        proxima_revisao TEXT NOT NULL,
        ultima_revisao TEXT,
        acertos INTEGER DEFAULT 0,
        erros INTEGER DEFAULT 0,
        UNIQUE(usuario_id, licao_id)
    )
    """,
)

INDICES = (
    "CREATE INDEX IF NOT EXISTS idx_atividades_usuario_data ON atividades_estudo(usuario_id, data)",
    "CREATE INDEX IF NOT EXISTS idx_recompensas_usuario_data ON recompensas_diarias(usuario_id, data)",
    "CREATE INDEX IF NOT EXISTS idx_progresso_usuario_modulo ON progresso(usuario_id, modulo_id, concluida)",
    "CREATE INDEX IF NOT EXISTS idx_historico_usuario_data ON compilador_historico(usuario_id, id DESC)",
    "CREATE INDEX IF NOT EXISTS idx_favoritos_usuario ON favoritos_usuario(usuario_id, licao_id)",
    "CREATE INDEX IF NOT EXISTS idx_revisoes_usuario_data ON revisoes_usuario(usuario_id, proxima_revisao)",
)

# Colunas que surgiram depois da primeira versão; bancos SQLite antigos as recebem aqui.
COLUNAS_ADICIONADAS = (
    ("progresso", "quiz_correto", "INTEGER DEFAULT 0"),
    ("progresso", "quiz_respondido", "INTEGER DEFAULT 0"),
    ("progresso", "resposta_teorica", "TEXT"),
    ("progresso", "codigo_enviado", "INTEGER DEFAULT 0"),
    ("progresso", "concluida_em", "TEXT"),
    ("progresso", "codigo_usuario", "TEXT"),
    ("progresso", "saida_codigo", "TEXT"),
    ("progresso", "entrada_codigo", "TEXT"),
    ("progresso", "codigo_validado", "INTEGER DEFAULT 0"),
    ("progresso", "feedback_codigo", "TEXT"),
    ("progresso", "atualizado_em", "TEXT"),
    ("usuarios", "xp", "INTEGER DEFAULT 0"),
    ("usuarios", "nivel", "INTEGER DEFAULT 1"),
    ("usuarios", "sequencia", "INTEGER DEFAULT 1"),
    ("usuarios", "ultimo_acesso", "TEXT"),
    ("usuarios", "melhor_sequencia", "INTEGER DEFAULT 0"),
    ("usuarios", "ultima_atividade", "TEXT"),
    ("usuarios", "protecoes_sequencia", "INTEGER DEFAULT 1"),
    ("desafios_diarios", "desafio_id", "TEXT"),
    ("desafios_diarios", "entrada_codigo", "TEXT"),
    ("desafios_diarios", "codigo_validado", "INTEGER DEFAULT 0"),
    ("desafios_diarios", "feedback_codigo", "TEXT"),
    ("conquistas_usuario", "descricao", "TEXT"),
    ("conquistas_usuario", "raridade", "TEXT DEFAULT 'comum'"),
    ("conquistas_usuario", "desbloqueada_em", "TEXT"),
    ("compilador_historico", "contexto", "TEXT DEFAULT 'livre'"),
    ("compilador_historico", "licao_id", "INTEGER"),
    ("compilador_historico", "modulo_id", "INTEGER"),
    ("compilador_historico", "aprovado", "INTEGER DEFAULT 0"),
    ("compilador_historico", "origem", "TEXT"),
)


def _colunas_sqlite(conn, tabela):
    return {linha["name"] for linha in conn.execute(f"PRAGMA table_info({tabela})").fetchall()}


def _atualizar_sqlite_antigo(conn):
    for tabela, coluna, definicao in COLUNAS_ADICIONADAS:
        if coluna not in _colunas_sqlite(conn, tabela):
            conn.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")

    conn.execute("""
        UPDATE usuarios
        SET melhor_sequencia = MAX(COALESCE(melhor_sequencia, 0), COALESCE(sequencia, 0))
    """)
    # Lições concluídas em versões antigas continuam liberando o avanço.
    conn.execute("""
        UPDATE progresso SET quiz_correto = 1
        WHERE concluida = 1 AND (quiz_correto IS NULL OR quiz_correto = 0)
    """)
    conn.execute("""
        UPDATE progresso SET concluida_em = atualizado_em
        WHERE concluida = 1 AND concluida_em IS NULL
    """)


def criar_tabelas():
    with transacao() as conn:
        for sql in TABELAS:
            conn.execute(sql.format(chave=CHAVE_PRIMARIA))
        _atualizar_sqlite_antigo(conn)
        for sql in INDICES:
            conn.execute(sql)
        conn.execute("PRAGMA optimize")
