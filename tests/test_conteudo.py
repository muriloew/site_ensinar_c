import os
import shutil
import subprocess
import tempfile
import unittest

from backend.conteudo.aprofundamento import APROFUNDAMENTO
from backend.conteudo.exemplos import EXEMPLOS
from backend.conteudo.trilha import MODULOS


def _sem_espacos_no_fim(texto):
    return "\n".join(linha.rstrip() for linha in texto.strip().splitlines())


class ConteudoTest(unittest.TestCase):
    def test_toda_licao_tem_aprofundamento(self):
        for modulo in MODULOS:
            for licao in modulo["licoes"]:
                with self.subTest(licao=licao["titulo"]):
                    extra = licao["aprofundamento"]
                    self.assertGreaterEqual(len(extra["passos"]), 2)
                    self.assertTrue(extra["saida"].strip())
                    self.assertGreater(len(extra["alem"]), 150)
                    # Crases abertas e fechadas: senão o texto aparece quebrado na página.
                    for texto in extra["passos"] + [extra["alem"]]:
                        self.assertEqual(texto.count("`") % 2, 0, texto)

    @unittest.skipUnless(shutil.which("gcc"), "precisa do gcc instalado")
    def test_exemplos_compilam_sem_avisos_e_mostram_a_saida_documentada(self):
        for titulo, codigo in EXEMPLOS.items():
            extra = APROFUNDAMENTO[titulo]
            with self.subTest(licao=titulo), tempfile.TemporaryDirectory() as pasta:
                arquivo = os.path.join(pasta, "exemplo.c")
                with open(arquivo, "w", encoding="utf-8") as saida:
                    saida.write(codigo)
                compilacao = subprocess.run(
                    ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic", "-Werror",
                     arquivo, "-o", os.path.join(pasta, "exemplo"), "-lm"],
                    capture_output=True, text=True,
                )
                self.assertEqual(compilacao.returncode, 0, compilacao.stderr)

                entrada = extra["entrada"]
                execucao = subprocess.run(
                    [os.path.join(pasta, "exemplo")], cwd=pasta, capture_output=True, text=True,
                    input=f"{entrada}\n" if entrada else "", timeout=5,
                )
                self.assertEqual(execucao.returncode, 0)
                # Na página, a saída mostra também o que foi digitado, como no terminal.
                esperado = extra["saida"].replace(f"{entrada}\n", "", 1) if entrada else extra["saida"]
                self.assertEqual(_sem_espacos_no_fim(execucao.stdout), _sem_espacos_no_fim(esperado))


if __name__ == "__main__":
    unittest.main()
