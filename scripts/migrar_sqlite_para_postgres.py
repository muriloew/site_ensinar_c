"""Copia os dados de um banco SQLite antigo do Ensinar C para o PostgreSQL.

Uso (na pasta do projeto):
    DATABASE_URL="postgresql://usuario:senha@servidor/banco" python scripts/migrar_sqlite_para_postgres.py [instance/ensinar_c.db]

No Windows (PowerShell):
    $env:DATABASE_URL="postgresql://usuario:senha@servidor/banco"
    python scripts/migrar_sqlite_para_postgres.py instance/ensinar_c.db

O PostgreSQL de destino precisa estar vazio (sem usuários), para não misturar contas.
"""

import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.banco.conexao import transacao, usando_postgres  # noqa: E402
from backend.banco.tabelas import criar_tabelas  # noqa: E402

# Ordem das tabelas; o usuário vem primeiro porque as outras apontam para ele.
TABELAS = (
    "usuarios",
    "progresso",
    "conquistas_usuario",
    "desafios_diarios",
    "compilador_historico",
    "metas_usuario",
    "simulados_usuario",
    "atividades_estudo",
    "recompensas_diarias",
    "favoritos_usuario",
    "revisoes_usuario",
    "anotacoes_usuario",
)


def colunas_postgres(conn, tabela):
    return {
        linha["column_name"]
        for linha in conn.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = ?",
            (tabela,),
        ).fetchall()
    }


def main():
    if not usando_postgres():
        sys.exit("Defina a variável DATABASE_URL com o endereço do PostgreSQL de destino.")

    caminho = Path(sys.argv[1] if len(sys.argv) > 1 else os.path.join("instance", "ensinar_c.db"))
    if not caminho.exists():
        sys.exit(f"Arquivo SQLite não encontrado: {caminho}")

    origem = sqlite3.connect(caminho)
    origem.row_factory = sqlite3.Row
    tabelas_origem = {
        linha["name"] for linha in origem.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }

    criar_tabelas()
    with transacao() as destino:
        if destino.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()["total"]:
            sys.exit("O PostgreSQL de destino já tem usuários. Use um banco vazio para a migração.")

        for tabela in TABELAS:
            if tabela not in tabelas_origem:
                print(f"{tabela}: não existe no SQLite, ignorada")
                continue

            colunas_origem = [linha["name"] for linha in origem.execute(f"PRAGMA table_info({tabela})")]
            colunas = [coluna for coluna in colunas_origem if coluna in colunas_postgres(destino, tabela)]
            lista = ", ".join(colunas)
            marcadores = ", ".join("?" for _ in colunas)
            linhas = origem.execute(f"SELECT {lista} FROM {tabela} ORDER BY id").fetchall()
            for linha in linhas:
                destino.execute(
                    f"INSERT INTO {tabela} ({lista}) VALUES ({marcadores})",
                    tuple(linha[coluna] for coluna in colunas),
                )

            # Os próximos cadastros continuam a numeração depois do maior id copiado.
            destino.execute(
                f"SELECT setval(pg_get_serial_sequence('{tabela}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {tabela}), 0) + 1, false)"
            )
            print(f"{tabela}: {len(linhas)} registro(s) copiado(s)")

    origem.close()
    print("Migração concluída.")


if __name__ == "__main__":
    main()
