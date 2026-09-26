import os
import shutil
import subprocess
import tempfile
import unittest

from backend.compilador import executor
from backend.compilador.correcao import avaliar_codigo
from backend.conteudo.solucoes import SOLUCOES
from backend.conteudo.trilha import MODULOS

LICOES_PRATICAS = [licao for modulo in MODULOS for licao in modulo["licoes"] if licao["pratica_codigo"]]


class SolucoesTest(unittest.TestCase):
    def test_toda_licao_pratica_tem_solucao(self):
        titulos = {licao["titulo"] for licao in LICOES_PRATICAS}
        self.assertEqual(titulos, set(SOLUCOES))
        for licao in LICOES_PRATICAS:
            self.assertEqual(licao["solucao"]["codigo"], SOLUCOES[licao["titulo"]][0])
            self.assertTrue(licao["solucao"]["explicacao"])

    @unittest.skipUnless(shutil.which("gcc"), "precisa do gcc instalado")
    def test_solucoes_compilam_sem_avisos_e_passam_na_correcao(self):
        for licao in LICOES_PRATICAS:
            codigo = SOLUCOES[licao["titulo"]][0]
            with self.subTest(licao=licao["titulo"]):
                with tempfile.TemporaryDirectory() as pasta:
                    arquivo = os.path.join(pasta, "solucao.c")
                    with open(arquivo, "w", encoding="utf-8") as saida:
                        saida.write(codigo)
                    compilacao = subprocess.run(
                        ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic", "-Werror",
                         arquivo, "-o", os.path.join(pasta, "solucao"), "-lm"],
                        capture_output=True, text=True,
                    )
                self.assertEqual(compilacao.returncode, 0, compilacao.stderr)

                resultado = executor.executar_codigo(codigo, "")
                avaliacao = avaliar_codigo(
                    codigo, resultado.get("ok", False), resultado.get("saida", ""), licao["correcao"]
                )
                self.assertTrue(avaliacao["ok"], avaliacao["mensagem"])


if __name__ == "__main__":
    unittest.main()
