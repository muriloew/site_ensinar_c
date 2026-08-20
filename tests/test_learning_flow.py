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
            "recompensas_diarias",
            "atividades_estudo",
            "revisoes_usuario",
            "favoritos_usuario",
            "progresso",
            "desafios_diarios",
            "conquistas_usuario",
            "backups_progresso",
            "metas_usuario",
            "simulados_usuario",
            "compilador_historico",
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
            self.assertEqual(
                resposta.status_code,
                200,
                resposta.get_data(as_text=True),
            )
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

    def test_licoes_com_entrada_usam_casos_ocultos(self):
        for conteudo, testes_extras in self.site.TESTES_EXTRAS_CORRECAO.items():
            with self.subTest(conteudo=conteudo):
                regra = self.site.regra_correcao_para_conteudo(conteudo)
                self.assertGreaterEqual(len(regra.get("testes", [])), 2)
                self.assertTrue(all(teste in regra["testes"] for teste in testes_extras))

        falhas = self.site.validar_saida(
            "Positivo\n",
            {"saida_nao_contem": ["Positivo"], "saida_obrigatoria": False},
        )
        self.assertTrue(falhas)
        self.assertFalse(
            self.site.validar_saida(
                "",
                {"saida_nao_contem": ["Positivo"], "saida_obrigatoria": False},
            )
        )

    def test_paginas_principais_renderizam(self):
        for rota in (
            "/dashboard",
            "/perfil",
            "/simulado",
            "/modulos",
            "/compilador",
            "/historico-codigos",
            "/favoritos",
            "/revisao",
            "/estudar/1",
            "/desafio-diario",
        ):
            with self.subTest(rota=rota):
                resposta = self.client.get(rota, follow_redirects=True)
                self.assertEqual(resposta.status_code, 200)

        pratica_livre = self.client.get("/compilador").get_data(as_text=True)
        self.assertIn("clique em Compilar apenas quando quiser executar", pratica_livre)
        self.assertIn("vendor/codemirror/lib/codemirror.min.js", pratica_livre)
        self.assertIn("js/editor-c.js", pratica_livre)

        dashboard = self.client.get("/dashboard").get_data(as_text=True)
        self.assertIn("Missões de hoje", dashboard)
        self.assertIn("Próxima missão", dashboard)

        jornada = self.client.get("/modulos").get_data(as_text=True)
        self.assertIn("Sua jornada em C", jornada)
        self.assertEqual(jornada.count('class="journey-step'), 21)

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

    def test_missao_diaria_paga_recompensa_uma_vez(self):
        licao = self.site.MODULOS[0]["licoes"][0]
        self.responder_licao(licao)

        primeiro = licao["desafios_teoricos"][0]
        resposta_errada = next(
            alternativa for alternativa in primeiro["alternativas"]
            if alternativa != primeiro["resposta"]
        )
        self.client.post(
            "/verificar",
            json={
                "licao_id": licao["id"],
                "desafio_id": primeiro["id"],
                "resposta": resposta_errada,
            },
        )
        self.client.post(
            "/verificar",
            json={
                "licao_id": licao["id"],
                "desafio_id": primeiro["id"],
                "resposta": primeiro["resposta"],
            },
        )

        conn = self.site.conectar()
        atividade = conn.execute(
            "SELECT * FROM atividades_estudo WHERE usuario_id = 1"
        ).fetchone()
        usuario = conn.execute("SELECT * FROM usuarios WHERE id = 1").fetchone()
        conn.close()

        self.assertEqual(atividade["quizzes"], 3)
        self.assertEqual(usuario["sequencia"], 1)

        primeira = self.client.post("/missoes/aquecimento/resgatar")
        self.assertEqual(primeira.status_code, 302)

        conn = self.site.conectar()
        xp_primeiro = conn.execute(
            "SELECT xp FROM usuarios WHERE id = 1"
        ).fetchone()["xp"]
        recompensas = conn.execute(
            "SELECT COUNT(*) AS total FROM recompensas_diarias WHERE usuario_id = 1"
        ).fetchone()["total"]
        conn.close()
        self.assertEqual(xp_primeiro, 10)
        self.assertEqual(recompensas, 1)

        segunda = self.client.post("/missoes/aquecimento/resgatar")
        self.assertEqual(segunda.status_code, 302)
        conn = self.site.conectar()
        xp_segundo = conn.execute(
            "SELECT xp FROM usuarios WHERE id = 1"
        ).fetchone()["xp"]
        conn.close()
        self.assertEqual(xp_segundo, 10)

    def test_sequencia_usa_protecao_e_depois_reinicia(self):
        conn = self.site.conectar()
        self.site.registrar_atividade(conn, 1, data_atividade="2026-08-01")
        self.site.registrar_atividade(conn, 1, data_atividade="2026-08-02")
        self.site.registrar_atividade(conn, 1, data_atividade="2026-08-04")
        usuario_protegido = conn.execute(
            "SELECT * FROM usuarios WHERE id = 1"
        ).fetchone()
        self.assertEqual(usuario_protegido["sequencia"], 3)
        self.assertEqual(usuario_protegido["protecoes_sequencia"], 0)

        self.site.registrar_atividade(conn, 1, data_atividade="2026-08-06")
        usuario_reiniciado = conn.execute(
            "SELECT * FROM usuarios WHERE id = 1"
        ).fetchone()
        conn.commit()
        conn.close()

        self.assertEqual(usuario_reiniciado["sequencia"], 1)
        self.assertEqual(usuario_reiniciado["melhor_sequencia"], 3)

    def test_rascunho_alterado_perde_aprovacao_anterior(self):
        modulo = self.site.MODULOS[1]
        licao = modulo["licoes"][0]
        conn = self.site.conectar()
        conn.execute(
            """
            INSERT INTO progresso
                (usuario_id, licao_id, modulo_id, codigo_usuario, entrada_codigo,
                 saida_codigo, codigo_enviado, codigo_validado, feedback_codigo)
            VALUES (?, ?, ?, ?, ?, ?, 1, 1, ?)
            """,
            (1, licao["id"], modulo["id"], "codigo aprovado", "", "saida", "Aprovado"),
        )
        conn.commit()
        conn.close()

        resposta = self.client.post(
            "/api/exercicio/salvar-rascunho",
            json={"licao_id": licao["id"], "codigo": "codigo alterado", "entrada": ""},
        )
        self.assertEqual(resposta.status_code, 200, resposta.get_data(as_text=True))

        conn = self.site.conectar()
        registro = conn.execute(
            "SELECT * FROM progresso WHERE usuario_id = 1 AND licao_id = ?",
            (licao["id"],),
        ).fetchone()
        conn.close()
        self.assertEqual(registro["codigo_validado"], 0)
        self.assertEqual(registro["codigo_enviado"], 0)
        self.assertIsNone(registro["feedback_codigo"])
        self.assertIsNone(registro["saida_codigo"])

    def test_comentario_nao_satisfaz_correcao_e_erro_nao_aprova(self):
        falhas = self.site.validar_regras_estaticas(
            "int main(void) { /* scanf */ return 0; }",
            {"codigo_contem": ["scanf"]},
        )
        self.assertTrue(falhas)

        modulo = self.site.MODULOS[1]
        licao = modulo["licoes"][0]
        conn = self.site.conectar()
        conn.execute(
            "INSERT INTO progresso (usuario_id, licao_id, modulo_id) VALUES (?, ?, ?)",
            (1, licao["id"], modulo["id"]),
        )
        conn.commit()
        conn.close()

        resultado = self.site.salvar_codigo_execucao(
            1,
            licao["id"],
            licao["codigo"],
            "",
            "saida esperada",
            execucao_ok=False,
        )
        self.assertFalse(resultado["ok"])

        conn = self.site.conectar()
        validado = conn.execute(
            "SELECT codigo_validado FROM progresso WHERE usuario_id = 1 AND licao_id = ?",
            (licao["id"],),
        ).fetchone()["codigo_validado"]
        conn.close()
        self.assertEqual(validado, 0)

    def test_favoritos_revisao_e_historico(self):
        licao = self.site.MODULOS[0]["licoes"][0]
        favorito = self.client.post(
            f"/favoritos/{licao['id']}",
            data={"destino": "/favoritos"},
        )
        self.assertEqual(favorito.status_code, 302)
        self.assertIn(licao["titulo"], self.client.get("/favoritos").get_data(as_text=True))

        conn = self.site.conectar()
        conn.execute(
            """
            INSERT INTO progresso
                (usuario_id, licao_id, modulo_id, concluida, quiz_correto, atualizado_em)
            VALUES (?, ?, 1, 1, 1, ?)
            """,
            (1, licao["id"], "2026-08-19"),
        )
        conn.execute(
            """
            INSERT INTO revisoes_usuario
                (usuario_id, licao_id, nivel, proxima_revisao, acertos, erros)
            VALUES (?, ?, 0, ?, 0, 0)
            """,
            (1, licao["id"], str(self.site.date.today())),
        )
        self.site.registrar_historico_codigo(
            conn, 1, "int main(void){return 0;}", "", "Process returned 0.",
            "Build finished successfully.", contexto="livre", aprovado=True,
            origem="Teste",
        )
        conn.commit()
        conn.close()

        revisao = self.client.get("/revisao").get_data(as_text=True)
        self.assertIn(licao["pergunta"], revisao)
        resposta = self.client.post(
            f"/revisao/{licao['id']}",
            data={"resposta": licao["resposta"]},
        )
        self.assertEqual(resposta.status_code, 302)

        historico = self.client.get("/historico-codigos").get_data(as_text=True)
        self.assertIn("int main(void){return 0;}", historico)
        self.assertIn("Aprovado", historico)


if __name__ == "__main__":
    unittest.main()
