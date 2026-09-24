"""Abre conexões com o banco de dados do site."""

import os
import sqlite3
from contextlib import contextmanager

CAMINHO_SQLITE_PADRAO = os.path.join("instance", "ensinar_c.db")


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


def _indices_das_colunas(descricao):
    return {coluna[0]: posicao for posicao, coluna in enumerate(descricao or ())}


def _linha_sqlite(cursor, valores):
    return Linha(_indices_das_colunas(cursor.description), valores)


def conectar():
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
