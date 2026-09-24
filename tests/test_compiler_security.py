import os
import shutil
import unittest
from unittest.mock import Mock, patch

from backend.compilador import executor as compilador


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
        self.assertEqual(compilador.MAX_EXECUCOES_SIMULTANEAS, 1)
        self.assertLessEqual(compilador.MAX_PROCESSOS_POR_JOB, 8)

        comando = compilador.comando_gcc("programa.c", "programa")
        self.assertIn("-pipe", comando)
        self.assertIn("-fdiagnostics-color=never", comando)

        comando_alternativo = compilador.comando_tcc("programa.c", "programa")
        self.assertEqual(comando_alternativo[0], "tcc")

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

    def test_falha_de_recursos_do_gcc_aciona_compilador_alternativo(self):
        falha_gcc = {
            "codigo": 1,
            "texto": "gcc: fatal error: cannot execute cc1: vfork: Resource temporarily unavailable",
            "tempo_excedido": False,
            "saida_truncada": False,
            "duracao_segundos": 0.2,
        }
        sucesso_tcc = {
            "codigo": 0,
            "texto": "",
            "tempo_excedido": False,
            "saida_truncada": False,
            "duracao_segundos": 0.1,
        }

        with patch.object(
            compilador,
            "_comandos_compiladores",
            return_value=[("GCC", ["gcc"]), ("TCC", ["tcc"])],
        ):
            with patch.object(
                compilador,
                "_executar_processo",
                side_effect=[falha_gcc, falha_gcc.copy(), sucesso_tcc],
            ) as executar:
                resultado = compilador._compilar_workspace(".", "programa.c", "programa")

        self.assertTrue(resultado["ok"], resultado)
        self.assertEqual(resultado["compilador"], "TCC")
        self.assertIn("Compilador alternativo: TCC", resultado["build"])
        self.assertEqual(executar.call_count, 3)

    def test_limite_de_processos_considera_usuario_compartilhado(self):
        def localizar_programa(nome):
            return "/usr/bin/prlimit" if nome == "prlimit" else None

        with patch.object(compilador.os, "name", "posix"):
            with patch.object(compilador.shutil, "which", side_effect=localizar_programa):
                with patch.object(compilador, "_identidade_runner", return_value=None):
                    comando_nativo = compilador._com_limites(["gcc"], "compilar")
                with patch.object(compilador, "_identidade_runner", return_value=(1000, 1000)):
                    comando_docker = compilador._com_limites(["gcc"], "compilar")

        self.assertFalse(any(item.startswith("--nproc=") for item in comando_nativo))
        self.assertIn(f"--nproc={compilador.MAX_PROCESSOS_POR_JOB}", comando_docker)

    def test_erro_de_sintaxe_nao_aciona_compilador_alternativo(self):
        erro_sintaxe = {
            "codigo": 1,
            "texto": "programa.c: error: expected semicolon",
            "tempo_excedido": False,
            "saida_truncada": False,
            "duracao_segundos": 0.1,
        }

        with patch.object(
            compilador,
            "_comandos_compiladores",
            return_value=[("GCC", ["gcc"]), ("TCC", ["tcc"])],
        ):
            with patch.object(
                compilador,
                "_executar_processo",
                return_value=erro_sintaxe,
            ) as executar:
                resultado = compilador._compilar_workspace(".", "programa.c", "programa")

        self.assertFalse(resultado["ok"])
        self.assertIn("expected semicolon", resultado["build"])
        self.assertEqual(executar.call_count, 1)

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
