import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]


class LearningFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        os.environ["DB_PATH"] = str(Path(cls.temp_dir.name) / "test.db")
        sys.path.insert(0, str(PROJECT_DIR))

        cls.site = importlib.import_module("app")
        cls.site.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        cls.client = cls.site.app.test_client()

    @classmethod
    def tearDownClass(cls):
        sys.modules.pop("app", None)
        if str(PROJECT_DIR) in sys.path:
            sys.path.remove(str(PROJECT_DIR))
        cls.temp_dir.cleanup()

    def setUp(self):
        conn = self.site.conectar()
        for tabela in (
            "progresso",
            "desafios_diarios",
            "conquistas_usuario",
            "backups_progresso",
            "usuarios",
        ):
            conn.execute(f"DELETE FROM {tabela}")
        conn.execute(
            "INSERT INTO usuarios (id, nome, email, senha) VALUES (?, ?, ?, ?)",
            (1, "Aluno Teste", "aluno@example.com", "senha"),
        )
        conn.commit()
        conn.close()

        with self.client.session_transaction() as sessao:
            sessao["usuario_id"] = 1

    def responder_licao(self, licao):
        ultimo_resultado = None
        for desafio in licao["desafios_teoricos"]:
            resposta = self.client.post(
                "/verificar",
                json={
                    "licao_id": licao["id"],
                    "desafio_id": desafio["id"],
                    "resposta": desafio["resposta"],
                },
            )
            self.assertEqual(resposta.status_code, 200)
            ultimo_resultado = resposta.get_json()
            self.assertTrue(ultimo_resultado["correta"])
        return ultimo_resultado

    def test_catalogo_tem_perguntas_variadas_e_dez_desafios_por_modulo(self):
        self.assertEqual(len(self.site.DESAFIOS_DIARIOS), 200)
        self.assertTrue(
            all(not licao["pratica_codigo"] for licao in self.site.MODULOS[0]["licoes"])
        )

        for modulo_id in range(2, 22):
            desafios = [
                item for item in self.site.DESAFIOS_DIARIOS
                if item["modulo_id"] == modulo_id
            ]
            self.assertEqual(len(desafios), 10)

        posicoes_corretas = []
        for modulo in self.site.MODULOS:
            for licao in modulo["licoes"]:
                self.assertEqual(len(licao["desafios_teoricos"]), 3)
                self.assertEqual(
                    licao["desafios_teoricos"][2]["resposta"],
                    licao["exercicio_codigo"],
                )
                for desafio in licao["desafios_teoricos"]:
                    posicoes_corretas.append(
                        desafio["alternativas"].index(desafio["resposta"])
                    )

        self.assertGreater(len(set(posicoes_corretas)), 1)
        self.assertTrue(any(posicao != 0 for posicao in posicoes_corretas))

    def test_paginas_principais_renderizam(self):
        for rota in (
            "/dashboard",
            "/perfil",
            "/simulado",
            "/modulos",
            "/compilador",
            "/estudar/1",
            "/desafio-diario",
        ):
            with self.subTest(rota=rota):
                resposta = self.client.get(rota, follow_redirects=True)
                self.assertEqual(resposta.status_code, 200)

        pratica_livre = self.client.get("/compilador").get_data(as_text=True)
        self.assertIn("clique em Compilar apenas quando quiser executar", pratica_livre)

    def test_fluxo_do_modulo_inicial_ate_desafios_diarios(self):
        pagina_licao = self.client.get("/estudar/1")
        self.assertEqual(pagina_licao.status_code, 200)
        html_licao = pagina_licao.get_data(as_text=True)
        self.assertIn("Desafios teóricos da lição", html_licao)
        self.assertEqual(html_licao.count('class="theory-challenge-item'), 3)

        pagina_bloqueada = self.client.get("/desafio-diario")
        self.assertIn(
            "Desafios diários bloqueados",
            pagina_bloqueada.get_data(as_text=True),
        )

        acesso_adiantado = self.client.post(
            "/verificar",
            json={"licao_id": self.site.MODULOS[1]["licoes"][0]["id"], "resposta": "x"},
        )
        self.assertEqual(acesso_adiantado.status_code, 403)

        compilacao_bloqueada = self.client.post(
            "/executar-codigo",
            json={"tipo": "diario", "codigo": "int main(void){return 0;}"},
        )
        self.assertEqual(compilacao_bloqueada.status_code, 403)

        modulo_inicial = self.site.MODULOS[0]
        for licao in modulo_inicial["licoes"]:
            resultado = self.responder_licao(licao)
            self.assertTrue(resultado["todos_corretos"])
            self.assertEqual(resultado["corretos"], 3)

            conclusao = self.client.post(f"/concluir/{licao['id']}")
            self.assertEqual(conclusao.status_code, 200)
            self.assertTrue(conclusao.get_json()["ok"])

        desafios, modulo_maximo = self.site.desafios_diarios_do_usuario(1)
        self.assertEqual(modulo_maximo, 2)
        self.assertEqual(len(desafios), 10)
        self.assertTrue(all(item["modulo_id"] == 2 for item in desafios))

        pagina_liberada = self.client.get("/desafio-diario")
        html_liberado = pagina_liberada.get_data(as_text=True)
        self.assertNotIn("Desafios diários bloqueados", html_liberado)
        self.assertIn("Módulo 2", html_liberado)
        self.assertIn("10 desafios do módulo 2", html_liberado)

        modulo_tres = self.site.MODULOS[2]["licoes"][0]
        acesso_modulo_tres = self.client.post(
            "/verificar",
            json={
                "licao_id": modulo_tres["id"],
                "desafio_id": modulo_tres["desafios_teoricos"][0]["id"],
                "resposta": modulo_tres["desafios_teoricos"][0]["resposta"],
            },
        )
        self.assertEqual(acesso_modulo_tres.status_code, 403)

    def test_resposta_invalida_e_progresso_antigo(self):
        licao = self.site.MODULOS[0]["licoes"][0]
        invalida = self.client.post(
            "/verificar",
            json={
                "licao_id": licao["id"],
                "desafio_id": "conceito",
                "resposta": "alternativa inventada",
            },
        )
        self.assertEqual(invalida.status_code, 400)

        estado_antigo = self.site.preparar_desafios_teoricos_view(
            licao,
            resposta_salva="",
            quiz_correto=1,
        )
        self.assertTrue(estado_antigo["todos_corretos"])
        self.assertEqual(estado_antigo["corretos"], 3)


if __name__ == "__main__":
    unittest.main()
