import sys
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend import relogio  # noqa: E402


def relogio_parado_em(instante_utc):
    """Substitui datetime.now no módulo do relógio por um instante fixo (em UTC)."""

    class DatetimeParado(datetime):
        @classmethod
        def now(cls, tz=None):
            return instante_utc.astimezone(tz) if tz else instante_utc.replace(tzinfo=None)

    return patch.object(relogio, "datetime", DatetimeParado)


class RelogioTest(unittest.TestCase):
    def test_dia_so_vira_a_meia_noite_de_brasilia(self):
        # 22h30 em Brasília já é 01h30 do dia seguinte em UTC, o horário do servidor do Render.
        with relogio_parado_em(datetime(2026, 10, 2, 1, 30, tzinfo=timezone.utc)):
            self.assertEqual(relogio.hoje(), date(2026, 10, 1))
            self.assertEqual(relogio.agora().isoformat(timespec="minutes"), "2026-10-01T22:30")

        with relogio_parado_em(datetime(2026, 10, 2, 3, 0, tzinfo=timezone.utc)):
            self.assertEqual(relogio.hoje(), date(2026, 10, 2))

    def test_agora_tem_o_mesmo_formato_ja_gravado_no_banco(self):
        self.assertIsNone(relogio.agora().tzinfo)

    def test_backend_nao_usa_o_relogio_do_servidor(self):
        backend = Path(__file__).resolve().parents[1] / "backend"
        for arquivo in backend.rglob("*.py"):
            if arquivo.name == "relogio.py":
                continue
            codigo = arquivo.read_text(encoding="utf-8")
            with self.subTest(arquivo=arquivo.name):
                self.assertNotIn("date.today()", codigo)
                self.assertNotIn("datetime.now()", codigo)


if __name__ == "__main__":
    unittest.main()
