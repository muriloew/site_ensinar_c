import os
import shutil
import subprocess
import tempfile
import unittest
from collections import Counter

from backend.compilador import executor
from backend.compilador.correcao import avaliar_codigo, normalizar_texto
from backend.conteudo.desafios_diarios import (
    DESAFIOS_DIARIOS,
    POR_MODULO,
    escolher_desafio_do_dia,
)
from backend.conteudo.trilha import MODULOS, encontrar_licao


class CatalogoDesafiosTest(unittest.TestCase):
    def test_cinco_desafios_proprios_por_modulo(self):
        contagem = Counter(desafio["modulo_id"] for desafio in DESAFIOS_DIARIOS)
        esperados = {modulo["id"] for modulo in MODULOS if modulo["id"] >= 2}
        self.assertEqual(set(contagem), esperados)
        self.assertTrue(all(total == POR_MODULO for total in contagem.values()), contagem)

        ids = [desafio["id"] for desafio in DESAFIOS_DIARIOS]
        self.assertEqual(len(ids), len(set(ids)))
        titulos = [desafio["titulo"] for desafio in DESAFIOS_DIARIOS]
        self.assertEqual(len(titulos), len(set(titulos)), "títulos repetidos")

    def test_campos_completos_e_licao_do_proprio_modulo(self):
        for desafio in DESAFIOS_DIARIOS:
            with self.subTest(desafio=desafio["id"]):
                self.assertIn(desafio["nivel"], ("Fácil", "Médio", "Desafiador"))
                self.assertTrue(desafio["enunciado"].strip())
                self.assertEqual(len(desafio["dicas"]), 3)
                self.assertTrue(desafio["solucao"]["explicacao"].strip())
                self.assertIsNotNone(desafio["exemplo"])
                modulo, licao = encontrar_licao(desafio["licao_id"])
                self.assertIsNotNone(licao)
                self.assertEqual(modulo["id"], desafio["modulo_id"])
                self.assertNotEqual(desafio["codigo_inicial"], desafio["solucao"]["codigo"])

    def test_sorteio_evita_desafios_ja_concluidos(self):
        modulo_dois = [desafio for desafio in DESAFIOS_DIARIOS if desafio["modulo_id"] == 2]
        feitos = {desafio["id"] for desafio in modulo_dois[:-1]}
        for dia in range(1, 20):
            escolhido = escolher_desafio_do_dia(modulo_dois, f"2026-09-{dia:02d}", feitos)
            self.assertEqual(escolhido["id"], modulo_dois[-1]["id"])

        todos = {desafio["id"] for desafio in modulo_dois}
        self.assertIn(escolher_desafio_do_dia(modulo_dois, "2026-09-01", todos), modulo_dois)

        sorteados = {escolher_desafio_do_dia(modulo_dois, f"2026-09-{dia:02d}")["id"] for dia in range(1, 11)}
        self.assertEqual(sorteados, todos, "em dias seguidos o sorteio deve passar por todos")


@unittest.skipUnless(shutil.which("gcc"), "precisa do gcc instalado")
class SolucoesDesafiosTest(unittest.TestCase):
    def _compilar_sem_avisos(self, codigo):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = os.path.join(pasta, "desafio.c")
            with open(arquivo, "w", encoding="utf-8") as saida:
                saida.write(codigo)
            return subprocess.run(
                ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic", "-Werror",
                 arquivo, "-o", os.path.join(pasta, "desafio"), "-lm"],
                capture_output=True, text=True,
            )

    def test_solucoes_compilam_sem_avisos_e_passam_na_correcao(self):
        for desafio in DESAFIOS_DIARIOS:
            codigo = desafio["solucao"]["codigo"]
            with self.subTest(desafio=desafio["id"]):
                compilacao = self._compilar_sem_avisos(codigo)
                self.assertEqual(compilacao.returncode, 0, compilacao.stderr)

                entrada = (desafio["exemplo"][0] + "\n") if desafio["exemplo"][0] else ""
                resultado = executor.executar_codigo(codigo, entrada)
                self.assertTrue(resultado.get("ok"), resultado.get("saida"))
                avaliacao = avaliar_codigo(codigo, True, resultado.get("saida", ""), desafio["correcao"])
                self.assertTrue(avaliacao["ok"], avaliacao["mensagem"])

                # O exemplo mostrado no enunciado precisa bater com a saída real da solução.
                saida = normalizar_texto(resultado.get("saida", ""))
                for linha in desafio["exemplo"][1].splitlines():
                    if linha.strip() and linha.strip() != "...":
                        self.assertIn(normalizar_texto(linha.strip()), saida)

    def test_codigo_inicial_ainda_nao_passa(self):
        for desafio in DESAFIOS_DIARIOS:
            codigo = desafio["codigo_inicial"]
            with self.subTest(desafio=desafio["id"]):
                entrada = (desafio["exemplo"][0] + "\n") if desafio["exemplo"][0] else ""
                resultado = executor.executar_codigo(codigo, entrada)
                avaliacao = avaliar_codigo(
                    codigo, resultado.get("ok", False), resultado.get("saida", ""), desafio["correcao"]
                )
                self.assertFalse(avaliacao["ok"], "o código inicial já resolve o desafio")


if __name__ == "__main__":
    unittest.main()
