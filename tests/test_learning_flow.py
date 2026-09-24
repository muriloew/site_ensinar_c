import importlib
import os
import sys
import tempfile
import unittest
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from flask import url_for


PROJECT_DIR = Path(__file__).resolve().parents[1]


class LearningFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        os.environ["DB_PATH"] = str(Path(cls.temp_dir.name) / "test.db")
        # Os testes apagam as tabelas: nunca usam a DATABASE_URL real, só TEST_DATABASE_URL.
        os.environ.pop("DATABASE_URL", None)
        if os.environ.get("TEST_DATABASE_URL"):
            os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
        sys.path.insert(0, str(PROJECT_DIR))

        cls.site = importlib.import_module("app")
        cls.site.app.config.update(TESTING=True, SECRET_KEY="test-secret", VERIFICAR_CSRF=False)
        cls.client = cls.site.app.test_client()

        from backend.aluno import gamificacao, situacao, teoria
        from backend.banco import conexao
        from backend.compilador import correcao, historico, terminal
        from backend.conteudo import desafios_diarios, trilha

        cls.MODULOS = trilha.MODULOS
        cls.DESAFIOS_DIARIOS = desafios_diarios.DESAFIOS_DIARIOS
        cls.conectar = staticmethod(conexao.conectar)
        cls.usando_postgres = staticmethod(conexao.usando_postgres)
        cls.gamificacao = gamificacao
        cls.SituacaoAluno = situacao.SituacaoAluno
        cls.teoria = teoria
        cls.correcao = correcao
        cls.historico = historico
        cls.terminal = terminal

    @classmethod
    def tearDownClass(cls):
        sys.modules.pop("app", None)
        if str(PROJECT_DIR) in sys.path:
            sys.path.remove(str(PROJECT_DIR))
        cls.temp_dir.cleanup()

    def setUp(self):
        conn = self.conectar()
        for tabela in (
            "anotacoes_usuario",
            "recompensas_diarias",
            "atividades_estudo",
            "revisoes_usuario",
            "favoritos_usuario",
            "progresso",
            "desafios_diarios",
            "conquistas_usuario",
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
        if self.usando_postgres():
            # O id foi escolhido à mão; o contador precisa seguir depois dele para os cadastros do teste.
            conn.execute("SELECT setval(pg_get_serial_sequence('usuarios', 'id'), 1)")
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
        self.assertEqual(len(self.DESAFIOS_DIARIOS), 200)
        self.assertTrue(
            all(not licao["pratica_codigo"] for licao in self.MODULOS[0]["licoes"])
        )

        for modulo_id in range(2, 22):
            desafios = [
                item for item in self.DESAFIOS_DIARIOS
                if item["modulo_id"] == modulo_id
            ]
            self.assertEqual(len(desafios), 10)

        posicoes_corretas = []
        for modulo in self.MODULOS:
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
        from backend.conteudo.exercicios import TESTES_OCULTOS

        licoes = {licao["titulo"]: licao for modulo in self.MODULOS for licao in modulo["licoes"]}
        for conteudo, testes_ocultos in TESTES_OCULTOS.items():
            with self.subTest(conteudo=conteudo):
                regra = licoes[conteudo]["correcao"]
                self.assertGreaterEqual(len(regra.get("testes", [])), 2)
                self.assertTrue(all(teste in regra["testes"] for teste in testes_ocultos))

        falhas = self.correcao.validar_saida(
            "Positivo\n",
            {"saida_nao_contem": ["Positivo"], "saida_obrigatoria": False},
        )
        self.assertTrue(falhas)
        self.assertFalse(
            self.correcao.validar_saida(
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
        self.assertIn("compilarCompiladorInterativo()", pratica_livre)
        self.assertIn("terminalInputCompilador", pratica_livre)
        self.assertIn("socket.io/4.7.5/socket.io.min.js", pratica_livre)
        self.assertNotIn('id="entradaCompilador"', pratica_livre)

        dashboard = self.client.get("/dashboard").get_data(as_text=True)
        self.assertIn("Missões de hoje", dashboard)
        self.assertIn("Próxima missão", dashboard)

        jornada = self.client.get("/modulos").get_data(as_text=True)
        self.assertIn("Sua jornada em C", jornada)
        self.assertEqual(jornada.count('class="journey-step'), 21)

    def test_compilador_livre_aceita_terminal_interativo(self):
        cliente_socket = self.site.socketio.test_client(
            self.site.app,
            flask_test_client=self.client,
        )
        self.assertTrue(cliente_socket.is_connected())

        cliente_socket.emit(
            "compilar_real",
            {
                "tipo": "compilador",
                "codigo": "#include <stdio.h>\nint main(void) { return 0; }",
            },
        )
        eventos = cliente_socket.get_received()
        cliente_socket.disconnect()

        builds = [
            evento["args"][0]
            for evento in eventos
            if evento["name"] == "build_log"
        ]
        self.assertTrue(builds)
        self.assertNotIn("Tipo de execução inválido", builds[0].get("texto", ""))

        self.terminal.salvar_execucao_livre(
            1,
            codigo="int main(void) { return 0; }",
            entrada="42\n",
            saida="Digite: 42\nResultado: 42\n",
            execucao_ok=True,
        )
        conn = self.conectar()
        historico = conn.execute(
            """
            SELECT contexto, entrada, saida, aprovado FROM compilador_historico
            WHERE usuario_id = ? AND codigo = ?
            """,
            (1, "int main(void) { return 0; }"),
        ).fetchone()
        conn.close()
        self.assertEqual(historico["contexto"], "livre")
        self.assertEqual(historico["entrada"], "42\n")
        self.assertIn("Resultado: 42", historico["saida"])
        self.assertEqual(historico["aprovado"], 1)

    def test_dependencias_locais_versionadas_e_ordem_do_estilo(self):
        class Recursos(HTMLParser):
            def __init__(self):
                super().__init__()
                self.urls = []

            def handle_starttag(self, tag, attrs):
                atributos = dict(attrs)
                if tag == "script" and "src" in atributos:
                    self.urls.append(atributos["src"])
                if tag == "link" and atributos.get("rel") == "stylesheet":
                    self.urls.append(atributos["href"])

        parser = Recursos()
        parser.feed(self.client.get("/compilador").get_data(as_text=True))
        caminhos = []
        for url in parser.urls:
            partes = urlsplit(url)
            self.assertFalse(partes.netloc, url)
            self.assertIn("v", parse_qs(partes.query), url)
            resposta = self.client.get(url)
            self.assertEqual(resposta.status_code, 200, url)
            resposta.close()
            caminhos.append(partes.path)
        self.assertIn("/static/vendor/socket.io/4.7.5/socket.io.min.js", caminhos)
        self.assertGreater(
            caminhos.index("/static/css/style.css"),
            caminhos.index("/static/vendor/codemirror/theme/material-darker.min.css"),
        )

    def test_url_estatica_muda_quando_o_arquivo_e_atualizado(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "teste.css"
            arquivo.write_text("body { color: white; }", encoding="utf-8")
            with patch.object(self.site.app, "_static_folder", pasta):
                with self.site.app.test_request_context():
                    antes = url_for("static", filename="teste.css")
                    horario = arquivo.stat().st_mtime_ns + 1_000_000_000
                    os.utime(arquivo, ns=(horario, horario))
                    depois = url_for("static", filename="teste.css")
                    self.assertNotEqual(antes, depois)
                    self.assertEqual(depois, url_for("static", filename="teste.css"))

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
            json={"licao_id": self.MODULOS[1]["licoes"][0]["id"], "resposta": "x"},
        )
        self.assertEqual(acesso_adiantado.status_code, 403)

        cliente_socket = self.site.socketio.test_client(self.site.app, flask_test_client=self.client)
        cliente_socket.emit("compilar_real", {"tipo": "diario", "codigo": "int main(void){return 0;}"})
        build = [evento["args"][0] for evento in cliente_socket.get_received() if evento["name"] == "build_log"]
        cliente_socket.disconnect()
        self.assertFalse(build[0]["ok"])
        self.assertIn("Conclua o módulo 1", build[0]["texto"])

        modulo_inicial = self.MODULOS[0]
        for licao in modulo_inicial["licoes"]:
            resultado = self.responder_licao(licao)
            self.assertTrue(resultado["todos_corretos"])
            self.assertEqual(resultado["corretos"], 3)

            conclusao = self.client.post(f"/concluir/{licao['id']}")
            self.assertEqual(conclusao.status_code, 200)
            self.assertTrue(conclusao.get_json()["ok"])

        desafios, modulo_maximo = self.SituacaoAluno(1).desafios_disponiveis()
        self.assertEqual(modulo_maximo, 2)
        self.assertEqual(len(desafios), 10)
        self.assertTrue(all(item["modulo_id"] == 2 for item in desafios))

        pagina_liberada = self.client.get("/desafio-diario")
        html_liberado = pagina_liberada.get_data(as_text=True)
        self.assertNotIn("Desafios diários bloqueados", html_liberado)
        self.assertIn("Módulo 2", html_liberado)
        self.assertIn("10 desafios do módulo 2", html_liberado)

        modulo_tres = self.MODULOS[2]["licoes"][0]
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
        licao = self.MODULOS[0]["licoes"][0]
        invalida = self.client.post(
            "/verificar",
            json={
                "licao_id": licao["id"],
                "desafio_id": "conceito",
                "resposta": "alternativa inventada",
            },
        )
        self.assertEqual(invalida.status_code, 400)

        estado_antigo = self.teoria.preparar_desafios_teoricos_view(
            licao,
            resposta_salva="",
            quiz_correto=1,
        )
        self.assertTrue(estado_antigo["todos_corretos"])
        self.assertEqual(estado_antigo["corretos"], 3)

    def test_missao_diaria_paga_recompensa_uma_vez(self):
        licao = self.MODULOS[0]["licoes"][0]
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

        conn = self.conectar()
        atividade = conn.execute(
            "SELECT * FROM atividades_estudo WHERE usuario_id = 1"
        ).fetchone()
        usuario = conn.execute("SELECT * FROM usuarios WHERE id = 1").fetchone()
        conn.close()

        self.assertEqual(atividade["quizzes"], 3)
        self.assertEqual(usuario["sequencia"], 1)

        primeira = self.client.post("/missoes/aquecimento/resgatar")
        self.assertEqual(primeira.status_code, 302)

        conn = self.conectar()
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
        conn = self.conectar()
        xp_segundo = conn.execute(
            "SELECT xp FROM usuarios WHERE id = 1"
        ).fetchone()["xp"]
        conn.close()
        self.assertEqual(xp_segundo, 10)

    def test_sequencia_usa_protecao_e_depois_reinicia(self):
        conn = self.conectar()
        self.gamificacao.registrar_atividade(conn, 1, data_atividade="2026-08-01")
        self.gamificacao.registrar_atividade(conn, 1, data_atividade="2026-08-02")
        self.gamificacao.registrar_atividade(conn, 1, data_atividade="2026-08-04")
        usuario_protegido = conn.execute(
            "SELECT * FROM usuarios WHERE id = 1"
        ).fetchone()
        self.assertEqual(usuario_protegido["sequencia"], 3)
        self.assertEqual(usuario_protegido["protecoes_sequencia"], 0)

        self.gamificacao.registrar_atividade(conn, 1, data_atividade="2026-08-06")
        usuario_reiniciado = conn.execute(
            "SELECT * FROM usuarios WHERE id = 1"
        ).fetchone()
        conn.commit()
        conn.close()

        self.assertEqual(usuario_reiniciado["sequencia"], 1)
        self.assertEqual(usuario_reiniciado["melhor_sequencia"], 3)

    def test_rascunho_alterado_perde_aprovacao_anterior(self):
        modulo = self.MODULOS[1]
        licao = modulo["licoes"][0]
        conn = self.conectar()
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

        conn = self.conectar()
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
        falhas = self.correcao.validar_regras_estaticas(
            "int main(void) { /* scanf */ return 0; }",
            {"codigo_contem": ["scanf"]},
        )
        self.assertTrue(falhas)

        modulo = self.MODULOS[1]
        licao = modulo["licoes"][0]
        conn = self.conectar()
        conn.execute(
            "INSERT INTO progresso (usuario_id, licao_id, modulo_id) VALUES (?, ?, ?)",
            (1, licao["id"], modulo["id"]),
        )
        conn.commit()
        conn.close()

        resultado = self.terminal.salvar_execucao_licao(
            1,
            licao["id"],
            codigo=licao["codigo"],
            entrada="",
            saida="saida esperada",
            execucao_ok=False,
        )
        self.assertFalse(resultado["ok"])

        conn = self.conectar()
        validado = conn.execute(
            "SELECT codigo_validado FROM progresso WHERE usuario_id = 1 AND licao_id = ?",
            (licao["id"],),
        ).fetchone()["codigo_validado"]
        conn.close()
        self.assertEqual(validado, 0)

    def test_favoritos_revisao_e_historico(self):
        licao = self.MODULOS[0]["licoes"][0]
        favorito = self.client.post(
            f"/favoritos/{licao['id']}",
            data={"destino": "/favoritos"},
        )
        self.assertEqual(favorito.status_code, 302)
        self.assertIn(licao["titulo"], self.client.get("/favoritos").get_data(as_text=True))

        conn = self.conectar()
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
            (1, licao["id"], str(date.today())),
        )
        self.historico.registrar_historico_codigo(
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

    def test_protecoes_de_csrf_senha_e_login(self):
        self.site.app.config["VERIFICAR_CSRF"] = True
        try:
            sem_token = self.client.post("/verificar", json={"licao_id": 1})
            self.assertEqual(sem_token.status_code, 400)

            with self.client.session_transaction() as sessao:
                sessao["csrf_token"] = "token-de-teste"
            com_token = self.client.post(
                "/verificar",
                json={"licao_id": 1, "desafio_id": "conceito", "resposta": "x"},
                headers={"X-CSRFToken": "token-de-teste"},
            )
            self.assertEqual(com_token.status_code, 400)
            self.assertIn("inválida", com_token.get_json()["mensagem"])
        finally:
            self.site.app.config["VERIFICAR_CSRF"] = False

        visitante = self.site.app.test_client()
        curta = visitante.post("/cadastro", data={"nome": "A", "email": "a@example.com", "senha": "1234567"})
        self.assertIn("pelo menos 8", curta.get_data(as_text=True))

        from backend.seguranca import FALHAS_POR_EMAIL, FALHAS_POR_IP

        dados = {"email": "aluno@example.com", "senha": "errada"}
        try:
            for _ in range(5):
                self.assertEqual(visitante.post("/login", data=dados).status_code, 200)
            self.assertEqual(visitante.post("/login", data=dados).status_code, 429)
        finally:
            FALHAS_POR_EMAIL.esquecer("email:aluno@example.com")
            FALHAS_POR_IP.esquecer("ip:127.0.0.1")

    def definir_senha_do_aluno(self, senha):
        from werkzeug.security import generate_password_hash

        conn = self.conectar()
        conn.execute("UPDATE usuarios SET senha = ? WHERE id = 1", (generate_password_hash(senha),))
        conn.commit()
        conn.close()

    def test_cadastro_valida_confirmacao_e_email(self):
        visitante = self.site.app.test_client()
        base = {"nome": "Ana", "email": "ana@example.com", "senha": "senha1234"}
        diferente = visitante.post("/cadastro", data={**base, "confirmar_senha": "outra1234"})
        self.assertIn("confirmação não é igual", diferente.get_data(as_text=True))
        invalido = visitante.post("/cadastro", data={**base, "email": "ana", "confirmar_senha": "senha1234"})
        self.assertIn("e-mail válido", invalido.get_data(as_text=True))
        criado = visitante.post("/cadastro", data={**base, "confirmar_senha": "senha1234"})
        self.assertEqual(criado.status_code, 302)
        with visitante.session_transaction() as sessao:
            self.assertTrue(sessao.permanent)

    def test_configuracoes_perfil_senha_e_exclusao(self):
        self.definir_senha_do_aluno("senha-antiga")
        pagina = self.client.get("/configuracoes").get_data(as_text=True)
        self.assertIn("Configurações", pagina)
        self.assertIn('data-preferencia="tema"', pagina)

        sem_senha = self.client.post("/configuracoes", data={"acao": "perfil", "nome": "Novo Nome", "email": "novo@example.com"})
        self.assertIn("confirme sua senha atual", sem_senha.get_data(as_text=True))
        so_nome = self.client.post("/configuracoes", data={"acao": "perfil", "nome": "Novo Nome", "email": "aluno@example.com"})
        self.assertEqual(so_nome.status_code, 302)

        errada = self.client.post("/configuracoes", data={
            "acao": "senha", "senha_atual": "x", "nova_senha": "nova-senha-1", "confirmar_senha": "nova-senha-1",
        })
        self.assertIn("senha atual está incorreta", errada.get_data(as_text=True))
        trocada = self.client.post("/configuracoes", data={
            "acao": "senha", "senha_atual": "senha-antiga", "nova_senha": "nova-senha-1", "confirmar_senha": "nova-senha-1",
        })
        self.assertEqual(trocada.status_code, 302)

        self.client.post("/favoritos/1", data={"destino": "/favoritos"})
        sem_confirmar = self.client.post("/configuracoes", data={"acao": "excluir", "confirmacao": "", "senha_atual": "nova-senha-1"})
        self.assertIn("Digite EXCLUIR", sem_confirmar.get_data(as_text=True))
        excluida = self.client.post("/configuracoes", data={"acao": "excluir", "confirmacao": "excluir", "senha_atual": "nova-senha-1"})
        self.assertIn("conta=excluida", excluida.location)

        conn = self.conectar()
        restantes = conn.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()["total"]
        favoritos = conn.execute("SELECT COUNT(*) AS total FROM favoritos_usuario").fetchone()["total"]
        conn.close()
        self.assertEqual((restantes, favoritos), (0, 0))

    def test_professor_ve_turma_e_redefine_senha(self):
        self.assertEqual(self.client.get("/professor").status_code, 404)
        with patch.dict(os.environ, {"ADMIN_EMAILS": "aluno@example.com"}):
            painel = self.client.get("/professor").get_data(as_text=True)
            self.assertIn("Acompanhamento da turma", painel)
            self.assertIn("Aluno Teste", painel)
            resposta = self.client.post("/professor/alunos/1/redefinir-senha").get_data(as_text=True)
        self.assertIn("Senha temporária", resposta)

        senha = resposta.split('class="temp-password">')[1].split("<")[0]
        visitante = self.site.app.test_client()
        entrada = visitante.post("/login", data={"email": "aluno@example.com", "senha": senha})
        self.assertIn("aviso=senha_temporaria", entrada.location)
        self.assertIn("senha temporária", visitante.get(entrada.location).get_data(as_text=True))

    def test_navegacao_anotacoes_e_proxima_licao(self):
        licao = self.MODULOS[0]["licoes"][0]
        pagina = self.client.get(f"/estudar/1?licao={licao['id']}").get_data(as_text=True)
        self.assertIn("Lição 1 de 4", pagina)
        self.assertIn(self.MODULOS[0]["licoes"][1]["titulo"] + " →", pagina)

        salva = self.client.post(f"/api/anotacoes/{licao['id']}", json={"texto": "scanf precisa de &"})
        self.assertTrue(salva.get_json()["ok"])
        self.assertIn("scanf precisa de &amp;", self.client.get("/estudar/1").get_data(as_text=True))
        bloqueada = self.client.post(f"/api/anotacoes/{self.MODULOS[2]['licoes'][0]['id']}", json={"texto": "x"})
        self.assertEqual(bloqueada.status_code, 403)

        self.responder_licao(licao)
        conclusao = self.client.post(f"/concluir/{licao['id']}").get_json()
        self.assertEqual(conclusao["proxima"], f"/estudar/1?licao={self.MODULOS[0]['licoes'][1]['id']}")

    def test_consulta_rapida_exemplo_e_cabecalhos(self):
        visitante = self.site.app.test_client()
        referencia = visitante.get("/referencia")
        self.assertEqual(referencia.status_code, 200)
        texto = referencia.get_data(as_text=True)
        for trecho in ("%lf", "strcmp", "undeclared", "Ponteiro"):
            self.assertIn(trecho, texto)
        self.assertEqual(referencia.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(referencia.headers["X-Frame-Options"], "SAMEORIGIN")

        licao = self.MODULOS[0]["licoes"][0]
        compilador = self.client.get(f"/compilador?exemplo={licao['id']}").get_data(as_text=True)
        self.assertIn(f"Exemplo - {licao['titulo']}", compilador)
        bloqueado = self.client.get(f"/compilador?exemplo={self.MODULOS[3]['licoes'][0]['id']}").get_data(as_text=True)
        self.assertIn("Compilador Online", bloqueado)


if __name__ == "__main__":
    unittest.main()
