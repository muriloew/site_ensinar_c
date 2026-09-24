"""Abre conexões com o banco de dados do site.

Com a variável DATABASE_URL definida, usa PostgreSQL (produção). Sem ela, usa um
arquivo SQLite local, o que dispensa instalar um servidor de banco para estudar o código.
"""

import os
import sqlite3
import threading
from contextlib import contextmanager
from functools import lru_cache

CAMINHO_SQLITE_PADRAO = os.path.join("instance", "ensinar_c.db")

_pool = None
_pool_url = None
_pool_lock = threading.Lock()


class Linha:
    """Resultado de consulta acessível pelo nome da coluna ou pela posição."""

    __slots__ = ("_indices", "_valores")

    def __init__(self, indices, valores):
        self._indices = indices
        self._valores = tuple(valores)

    def __getitem__(self, chave):
        if isinstance(chave, str):
            return self._valores[self._indices[chave]]
        return self._valores[chave]

    def keys(self):
        return list(self._indices)

    def __iter__(self):
        return iter(self._valores)

    def __len__(self):
        return len(self._valores)

    def __repr__(self):
        return f"Linha({dict(self)!r})"


def usando_postgres():
    return bool(os.environ.get("DATABASE_URL", "").strip())


def _linha_sqlite(cursor, valores):
    return Linha({coluna[0]: posicao for posicao, coluna in enumerate(cursor.description)}, valores)


def _linha_postgres(cursor):
    indices = {coluna.name: posicao for posicao, coluna in enumerate(cursor.description or ())}
    return lambda valores: Linha(indices, valores)


@lru_cache(maxsize=512)
def _sql_postgres(sql):
    """Troca os marcadores "?" do SQLite pelos "%s" do PostgreSQL."""
    partes = []
    dentro_de_texto = False
    for caractere in sql:
        if caractere == "'":
            dentro_de_texto = not dentro_de_texto
            partes.append(caractere)
        elif caractere == "%":
            partes.append("%%")
        elif caractere == "?" and not dentro_de_texto:
            partes.append("%s")
        else:
            partes.append(caractere)
    return "".join(partes)


class ConexaoPostgres:
    """Conexão emprestada do pool com a mesma interface usada no SQLite."""

    def __init__(self, pool):
        self._pool = pool
        self._conn = pool.getconn()

    def execute(self, sql, parametros=()):
        return self._conn.execute(_sql_postgres(sql), tuple(parametros))

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        if self._conn is None:
            return
        conn, self._conn = self._conn, None
        try:
            # Descarta o que não foi confirmado antes de devolver a conexão ao pool.
            conn.rollback()
        except Exception:
            pass
        self._pool.putconn(conn)


def _obter_pool():
    global _pool, _pool_url
    url = os.environ["DATABASE_URL"].strip()
    with _pool_lock:
        if _pool is None or _pool_url != url:
            from psycopg_pool import ConnectionPool

            if _pool is not None:
                _pool.close()
            _pool = ConnectionPool(
                url,
                min_size=1,
                max_size=int(os.environ.get("DB_POOL_MAX", "5")),
                kwargs={"row_factory": _linha_postgres, "prepare_threshold": None},
                # Serviços gratuitos encerram conexões ociosas; o teste evita usar uma já fechada.
                check=ConnectionPool.check_connection,
                max_idle=300,
                timeout=15,
                open=True,
            )
            _pool_url = url
        return _pool


def conectar():
    if usando_postgres():
        return ConexaoPostgres(_obter_pool())

    caminho = os.environ.get("DB_PATH") or CAMINHO_SQLITE_PADRAO
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    conn = sqlite3.connect(caminho)
    conn.row_factory = _linha_sqlite
    return conn


@contextmanager
def transacao():
    """Confirma as alterações ao final do bloco ou desfaz tudo se houver erro."""
    conn = conectar()
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()
