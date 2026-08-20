import os
import shutil
import unittest
from unittest.mock import Mock, patch

from backend import compilador


class CompilerSecurityTest(unittest.TestCase):
    def test_piston_rejeita_erro_de_compilacao(self):
        resposta = Mock()
        resposta.raise_for_status.return_value = None
        resposta.json.return_value = {
            "compile": {
                "code": 1,
                "stderr": "erro de sintaxe",
                "status": None,
            }
        }

        with patch.dict(os.environ, {"PISTON_URL": "https://executor.test/api/v2/piston"}):
            with patch.object(compilador.requests, "post", return_value=resposta):
                resultado = compilador.executar_piston("codigo invalido")

        self.assertFalse(resultado["ok"])
        self.assertIn("erro de sintaxe", resultado["build"])

    def test_piston_rejeita_erro_de_execucao(self):
        resposta = Mock()
        resposta.raise_for_status.return_value = None
        resposta.json.return_value = {
            "compile": {"code": 0, "stdout": "", "stderr": "", "status": None},
            "run": {"code": 1, "stdout": "teste", "stderr": "", "status": "RE"},
        }

        with patch.dict(os.environ, {"PISTON_URL": "https://executor.test/api/v2/piston"}):
            with patch.object(compilador.requests, "post", return_value=resposta):
                resultado = compilador.executar_piston("int main(void){return 1;}")

        self.assertFalse(resultado["ok"])
        self.assertIn("Process returned 1", resultado["saida"])

    def test_limites_de_codigo_e_entrada(self):
        self.assertIn("100 KB", compilador.validar_codigo("a" * 100_001))
        self.assertIn(
            "100 KB",
            compilador.validar_codigo("int main(void){return 0;}", "a" * 100_001),
        )

    def test_limites_de_tempo_adequados_ao_render(self):
        self.assertGreaterEqual(compilador.TEMPO_COMPILACAO, 30)
        self.assertGreaterEqual(compilador.TEMPO_INTERATIVO, 120)
        self.assertGreater(compilador.MAX_EXECUTAVEL_BYTES, compilador.MAX_SAIDA_BYTES)

        comando = compilador.comando_gcc("programa.c", "programa")
        self.assertIn("-pipe", comando)
        self.assertIn("-fdiagnostics-color=never", comando)

    def test_build_log_informa_tempo_real(self):
        sucesso = compilador._build_log({
            "codigo": 0,
            "texto": "",
            "tempo_excedido": False,
            "duracao_segundos": 1.25,
        })
        self.assertIn("1.25s", sucesso)

        excedido = compilador._build_log({
            "codigo": -1,
            "texto": "",
            "tempo_excedido": True,
            "duracao_segundos": compilador.TEMPO_COMPILACAO,
        })
        self.assertIn(str(compilador.TEMPO_COMPILACAO), excedido)

    @unittest.skipUnless(shutil.which("gcc"), "GCC nao esta instalado neste Windows")
    def test_gcc_local_compila_executa_e_rejeita_erro(self):
        sucesso = compilador.executar_codigo_local(
            '#include <stdio.h>\nint main(void){printf("OK\\n");return 0;}'
        )
        self.assertTrue(sucesso["ok"], sucesso)
        self.assertIn("OK", sucesso["saida"])

        erro = compilador.executar_codigo_local("int main(void) { isto nao compila }")
        self.assertFalse(erro["ok"])
        self.assertIn("Build failed", erro["build"])


if __name__ == "__main__":
    unittest.main()
