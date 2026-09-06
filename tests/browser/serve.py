import os
import sys
from pathlib import Path
from datetime import date
from tempfile import TemporaryDirectory

TEMP = TemporaryDirectory(prefix="ensinar-c-browser-")
HERE = Path(TEMP.name)
PROJECT = Path(__file__).resolve().parents[2]
os.environ["DB_PATH"] = str(HERE / "review.db")
os.environ["BACKUP_DIR"] = str(HERE / "backups")
sys.path.insert(0, str(PROJECT))

import app as site
from werkzeug.security import generate_password_hash

site.app.config.update(TESTING=True, TEMPLATES_AUTO_RELOAD=True, SECRET_KEY="local-layout-review")
conn = site.conectar()
if not conn.execute("SELECT id FROM usuarios WHERE id = 1").fetchone():
    conn.execute(
        "INSERT INTO usuarios (id, nome, email, senha, xp, nivel) VALUES (?, ?, ?, ?, ?, ?)",
        (1, "Aluno de Teste Responsivo", "teste@example.test", generate_password_hash("layout-test"), 480, 4),
    )
    for modulo in site.MODULOS[:2]:
        for licao in modulo["licoes"]:
            conn.execute(
                "INSERT INTO progresso (usuario_id, licao_id, modulo_id, quiz_correto, quiz_respondido, codigo_enviado, concluida, codigo_validado, atualizado_em) VALUES (1, ?, ?, 1, 1, 1, 1, 1, ?)",
                (licao["id"], modulo["id"], str(date.today())),
            )
    conn.execute("INSERT INTO favoritos_usuario (usuario_id, licao_id, criado_em) VALUES (1, 1, ?)", (str(date.today()),))
    conn.execute("INSERT INTO revisoes_usuario (usuario_id, licao_id, nivel, proxima_revisao) VALUES (1, 1, 1, ?)", (str(date.today()),))
    conn.commit()
conn.close()
if __name__ == "__main__":
    try:
        site.socketio.run(site.app, host="127.0.0.1", port=5113, debug=False, allow_unsafe_werkzeug=True)
    finally:
        TEMP.cleanup()
