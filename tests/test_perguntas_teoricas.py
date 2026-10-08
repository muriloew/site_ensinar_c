"""Confere as perguntas dos desafios teóricos: estrutura, variedade e, com o gcc, as respostas dos programas."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter

from backend.conteudo.perguntas import PERGUNTAS, TIPOS
from backend.conteudo.trilha import MODULOS

LICOES = [licao for modulo in MODULOS for licao in modulo["licoes"]]

# A apresentação da linguagem e o Makefile (que não é código C) só têm perguntas de conceito.
SO_CONCEITO = {"O que é C", "makefile"}


def normalizar(texto):
    linhas = texto.replace("\r\n", "\n").split("\n")
    return "\n".join(linha.rstrip() for linha in linhas).strip("\n")


class EstruturaPerguntasTest(unittest.TestCase):
    def test_cada_licao_tem_quatro_perguntas_proprias(self):
        self.assertEqual(set(PERGUNTAS), {licao["titulo"] for licao in LICOES})
        for licao in LICOES:
            with self.subTest(licao=licao["titulo"]):
                desafios = licao["desafios_teoricos"]
                self.assertEqual(len(desafios), 4)
                self.assertEqual(len({d["id"] for d in desafios}), 4)
                if licao["titulo"] not in SO_CONCEITO:
                    self.assertGreaterEqual(len({d["tipo"] for d in desafios}), 2, "use tipos de pergunta variados")
                for desafio in desafios:
                    self.assertIn(desafio["tipo"], TIPOS)
                    self.assertTrue(desafio["pergunta"].strip())
                    self.assertTrue(desafio["explicacao"].strip())
                    self.assertEqual(len(desafio["alternativas"]), 4)
                    self.assertEqual(len(set(desafio["alternativas"])), 4)
                    self.assertIn(desafio["resposta"], desafio["alternativas"])
                    if desafio["tipo"] != "conceito":
                        self.assertTrue(desafio["codigo"].strip())

    def test_alternativas_erradas_nao_se_repetem_entre_licoes(self):
        # As antigas perguntas usavam as mesmas frases erradas em todas as lições, e dava para acertar por eliminação.
        onde = {}
        for licao in LICOES:
            for desafio in licao["desafios_teoricos"]:
                if desafio["tipo"] != "conceito":
                    continue
                for alternativa in desafio["alternativas"]:
                    if alternativa != desafio["resposta"] and len(alternativa) > 25:
                        onde.setdefault(alternativa, set()).add(licao["titulo"])
        repetidas = {texto: licoes for texto, licoes in onde.items() if len(licoes) > 1}
        self.assertFalse(repetidas)

    def test_posicao_da_resposta_certa_e_equilibrada(self):
        posicoes = Counter(
            desafio["alternativas"].index(desafio["resposta"])
            for licao in LICOES for desafio in licao["desafios_teoricos"]
        )
        total = sum(posicoes.values())
        for posicao in range(4):
            self.assertGreater(posicoes[posicao] / total, 0.18, posicoes)
            self.assertLess(posicoes[posicao] / total, 0.32, posicoes)

    def test_tamanho_da_resposta_nao_entrega_a_certa(self):
        # Nem "a mais longa é a certa", nem "a mais longa nunca é a certa".
        conceitos = [d for licao in LICOES for d in licao["desafios_teoricos"] if d["tipo"] == "conceito"]
        mais_longa = sum(
            1 for d in conceitos
            if all(len(d["resposta"]) > len(outra) for outra in d["alternativas"] if outra != d["resposta"])
        )
        self.assertGreater(mais_longa / len(conceitos), 0.12, f"{mais_longa} de {len(conceitos)}")
        self.assertLess(mais_longa / len(conceitos), 0.4, f"{mais_longa} de {len(conceitos)}")


@unittest.skipUnless(shutil.which("gcc"), "precisa do gcc instalado")
class ProgramasPerguntasTest(unittest.TestCase):
    """Compila e executa os programas das perguntas para o gabarito nunca estar errado."""

    OPCOES = ["-std=c11", "-Wall", "-Wextra"]
    if sys.platform == "win32":
        OPCOES.append("-D__USE_MINGW_ANSI_STDIO=1")  # %zu e afins no gcc do Windows (MinGW)

    def setUp(self):
        self.pasta = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.pasta, ignore_errors=True)
        self.compilados = 0

    def _compilar(self, codigo, sem_avisos=False):
        # Um nome por programa: no Windows, o antivírus às vezes ainda segura o executável anterior.
        self.compilados += 1
        fonte = os.path.join(self.pasta, f"pergunta{self.compilados}.c")
        executavel = os.path.join(self.pasta, f"pergunta{self.compilados}")
        with open(fonte, "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo)
        opcoes = self.OPCOES + (["-pedantic", "-Werror"] if sem_avisos else [])
        resultado = subprocess.run(["gcc", *opcoes, fonte, "-o", executavel, "-lm"], capture_output=True, text=True)
        return resultado, executavel

    def _executar(self, executavel, entrada, limite=5):
        try:
            resultado = subprocess.run([executavel], input=entrada, capture_output=True, text=True,
                                       timeout=limite, cwd=self.pasta)
        except subprocess.TimeoutExpired:
            return None
        return normalizar(resultado.stdout)

    def _desafios(self, tipo):
        for licao in LICOES:
            for desafio in licao["desafios_teoricos"]:
                if desafio.get("tipo") == tipo:
                    yield licao["titulo"], desafio

    def test_saida_certa_e_a_saida_real_do_programa(self):
        for titulo, desafio in self._desafios("saida"):
            with self.subTest(licao=titulo, pergunta=desafio["id"]):
                compilacao, executavel = self._compilar(desafio["codigo"])
                self.assertEqual(compilacao.returncode, 0, compilacao.stderr)
                obtida = self._executar(executavel, desafio["entrada"])
                self.assertEqual(obtida, normalizar(desafio["resposta"]))

    def test_lacuna_so_a_alternativa_certa_chega_a_saida(self):
        for titulo, desafio in self._desafios("lacuna"):
            for alternativa in desafio["alternativas"]:
                with self.subTest(licao=titulo, pergunta=desafio["id"], alternativa=alternativa):
                    certa = alternativa == desafio["resposta"]
                    codigo = desafio["codigo"].replace("____", alternativa)
                    compilacao, executavel = self._compilar(codigo, sem_avisos=certa)
                    if certa:
                        self.assertEqual(compilacao.returncode, 0, compilacao.stderr)
                    elif compilacao.returncode != 0:
                        continue
                    obtida = self._executar(executavel, desafio["entrada"], limite=5 if certa else 2)
                    if certa:
                        self.assertEqual(obtida, normalizar(desafio["saida_esperada"]))
                    else:
                        self.assertNotEqual(obtida, normalizar(desafio["saida_esperada"]))

    def test_codigo_com_erro_compila_ou_nao_como_indicado(self):
        for titulo, desafio in self._desafios("erro"):
            with self.subTest(licao=titulo, pergunta=desafio["id"]):
                compilacao, _ = self._compilar(desafio["codigo"])
                if desafio["compila"]:
                    self.assertEqual(compilacao.returncode, 0, compilacao.stderr)
                else:
                    self.assertNotEqual(compilacao.returncode, 0, "o código deveria falhar na compilação")
