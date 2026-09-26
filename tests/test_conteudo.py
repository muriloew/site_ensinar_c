import unittest

from backend.conteudo.aprofundamento import APROFUNDAMENTO
from backend.conteudo.exemplos import EXEMPLOS
from backend.conteudo.exemplos_teoricos import EXEMPLOS as EXEMPLOS_TEORICOS
from backend.conteudo.trilha import MODULOS

LICOES = [licao for modulo in MODULOS for licao in modulo["licoes"]]


class ConteudoTest(unittest.TestCase):
    """A compilação e a saída de cada exemplo são conferidas em test_theory_content.py."""

    def test_cada_licao_tem_um_unico_exemplo(self):
        titulos = {licao["titulo"] for licao in LICOES}
        self.assertEqual(set(EXEMPLOS) | set(EXEMPLOS_TEORICOS), titulos)
        self.assertFalse(set(EXEMPLOS) & set(EXEMPLOS_TEORICOS))

    def test_toda_licao_tem_aprofundamento(self):
        for licao in LICOES:
            with self.subTest(licao=licao["titulo"]):
                extra = APROFUNDAMENTO[licao["titulo"]]
                self.assertGreater(len(extra["alem"]), 150)
                # Exemplos de exemplos.py precisam da saída; os de exemplos_teoricos.py já trazem a sua.
                self.assertEqual(extra["saida"] is None, licao["titulo"] in EXEMPLOS_TEORICOS)
                self.assertGreaterEqual(len(licao["passos_exemplo"]), 2)
                # Crases abertas e fechadas: senão o texto aparece quebrado na página.
                for texto in licao["passos_exemplo"] + [extra["alem"]]:
                    self.assertEqual(texto.count("`") % 2, 0, texto)

    def test_passo_a_passo_proprio_so_quando_o_exemplo_mudou(self):
        for licao in LICOES:
            extra = APROFUNDAMENTO[licao["titulo"]]
            if extra["passos"]:
                with self.subTest(licao=licao["titulo"]):
                    self.assertNotIn(licao["titulo"], EXEMPLOS_TEORICOS)
                    self.assertEqual(licao["passos_exemplo"], extra["passos"])


if __name__ == "__main__":
    unittest.main()
