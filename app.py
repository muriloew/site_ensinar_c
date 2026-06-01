from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
import subprocess
import tempfile
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-dev-ensinar-c")

DB_PATH = os.environ.get("DB_PATH", "instance/ensinar_c.db")


MODULOS = [
    {
        "id": 1,
        "titulo": "Introdução ao C",
        "descricao": "Conheça a linguagem C, sua importância e a estrutura básica de um programa.",
        "icone": "💻",
        "licoes": [
            {
                "id": 1,
                "titulo": "O que é a linguagem C?",
                "conteudo": "A linguagem C é uma linguagem compilada, conhecida por sua eficiência, desempenho e controle de memória.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Olá, mundo!\\n");\n    return 0;\n}',
                "pergunta": "Qual função inicia a execução de um programa em C?",
                "alternativas": ["printf", "scanf", "main", "include"],
                "resposta": "main",
                "exercicio_codigo": "Faça um programa em C que mostre seu nome na tela usando printf.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    // escreva seu código aqui\n\n    return 0;\n}"
            },
            {
                "id": 2,
                "titulo": "Estrutura básica",
                "conteudo": "Um programa em C normalmente possui bibliotecas, a função main, comandos dentro de chaves e um retorno ao final.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Meu primeiro programa em C\\n");\n    return 0;\n}',
                "pergunta": "Qual biblioteca permite usar printf e scanf?",
                "alternativas": ["stdio.h", "math.h", "string.h", "time.h"],
                "resposta": "stdio.h",
                "exercicio_codigo": "Crie um programa que mostre duas mensagens diferentes na tela.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    // mostre duas mensagens\n\n    return 0;\n}"
            }
        ]
    },
    {
        "id": 2,
        "titulo": "printf e scanf",
        "descricao": "Aprenda a exibir dados na tela e receber entradas do usuário.",
        "icone": "📘",
        "licoes": [
            {
                "id": 3,
                "titulo": "Usando printf",
                "conteudo": "A função printf é utilizada para mostrar mensagens, valores de variáveis e resultados na tela.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    printf("Idade: %d\\n", idade);\n    return 0;\n}',
                "pergunta": "Qual especificador mostra números inteiros?",
                "alternativas": ["%f", "%c", "%d", "%s"],
                "resposta": "%d",
                "exercicio_codigo": "Faça um programa que declare uma idade e mostre essa idade usando printf.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int idade;\n\n    return 0;\n}"
            },
            {
                "id": 4,
                "titulo": "Usando scanf",
                "conteudo": "A função scanf permite ler dados digitados pelo usuário e armazená-los em variáveis.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade;\n    printf("Digite sua idade: ");\n    scanf("%d", &idade);\n    printf("Idade digitada: %d\\n", idade);\n    return 0;\n}',
                "pergunta": "Por que usamos & no scanf?",
                "alternativas": ["Para somar", "Para indicar endereço da variável", "Para imprimir", "Para encerrar"],
                "resposta": "Para indicar endereço da variável",
                "exercicio_codigo": "Faça um programa que leia um número inteiro e mostre esse número na tela.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int numero;\n\n    return 0;\n}"
            }
        ]
    },
    {
        "id": 3,
        "titulo": "Variáveis",
        "descricao": "Entenda os principais tipos de dados e como armazenar informações.",
        "icone": "🔢",
        "licoes": [
            {
                "id": 5,
                "titulo": "Tipo int",
                "conteudo": "O tipo int armazena números inteiros, como 1, 10, -5 e 200.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int numero = 10;\n    printf("%d\\n", numero);\n    return 0;\n}',
                "pergunta": "Qual tipo armazena números inteiros?",
                "alternativas": ["float", "char", "int", "double"],
                "resposta": "int",
                "exercicio_codigo": "Crie duas variáveis inteiras e mostre a soma delas.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int a;\n    int b;\n\n    return 0;\n}"
            },
            {
                "id": 6,
                "titulo": "float, double e char",
                "conteudo": "float e double armazenam números com casas decimais. char armazena um caractere.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    float nota = 8.5;\n    char conceito = \'A\';\n    printf("Nota: %.1f - Conceito: %c\\n", nota, conceito);\n    return 0;\n}',
                "pergunta": "Qual tipo armazena um caractere?",
                "alternativas": ["int", "float", "char", "double"],
                "resposta": "char",
                "exercicio_codigo": "Crie uma variável float para uma nota e uma variável char para um conceito. Mostre as duas na tela.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    float nota;\n    char conceito;\n\n    return 0;\n}"
            }
        ]
    },
    {
        "id": 4,
        "titulo": "Operadores",
        "descricao": "Use operadores aritméticos, relacionais e lógicos.",
        "icone": "➗",
        "licoes": [
            {
                "id": 7,
                "titulo": "Operadores matemáticos",
                "conteudo": "Os operadores matemáticos permitem realizar soma, subtração, multiplicação, divisão e resto.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int a = 10;\n    int b = 3;\n    printf("Soma: %d\\n", a + b);\n    printf("Multiplicacao: %d\\n", a * b);\n    return 0;\n}',
                "pergunta": "Qual operador realiza multiplicação?",
                "alternativas": ["+", "-", "*", "/"],
                "resposta": "*",
                "exercicio_codigo": "Faça um programa que declare dois números e mostre soma, subtração e multiplicação.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int a;\n    int b;\n\n    return 0;\n}"
            }
        ]
    },
    {
        "id": 5,
        "titulo": "Estruturas de Decisão",
        "descricao": "Utilize if, else, else if e switch.",
        "icone": "🔀",
        "licoes": [
            {
                "id": 8,
                "titulo": "if e else",
                "conteudo": "O if executa um bloco se a condição for verdadeira. O else executa outro bloco se for falsa.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n\n    if (idade >= 18) {\n        printf("Maior de idade\\n");\n    } else {\n        printf("Menor de idade\\n");\n    }\n\n    return 0;\n}',
                "pergunta": "Qual comando testa uma condição?",
                "alternativas": ["for", "if", "scanf", "return"],
                "resposta": "if",
                "exercicio_codigo": "Faça um programa que verifique se um número é positivo ou negativo.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int numero;\n\n    return 0;\n}"
            }
        ]
    },
    {
        "id": 6,
        "titulo": "Estruturas de Repetição",
        "descricao": "Aprenda while, do while, for, break e continue.",
        "icone": "🔁",
        "licoes": [
            {
                "id": 9,
                "titulo": "Laço for",
                "conteudo": "O for é usado quando sabemos quantas vezes queremos repetir um comando.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    for (int i = 1; i <= 5; i++) {\n        printf("%d\\n", i);\n    }\n    return 0;\n}',
                "pergunta": "Qual estrutura é indicada para repetição com contador?",
                "alternativas": ["if", "else", "for", "switch"],
                "resposta": "for",
                "exercicio_codigo": "Faça um programa que use for para mostrar os números de 1 até 10.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    // use for aqui\n\n    return 0;\n}"
            }
        ]
    }
]


DESAFIO_DIARIO = {
    "titulo": "Desafio diário: média simples",
    "descricao": "Crie um programa que declare duas notas, calcule a média e mostre o resultado na tela.",
    "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    float nota1 = 8.0;\n    float nota2 = 7.0;\n\n    // calcule a média aqui\n\n    return 0;\n}',
    "dica": "Use uma variável chamada media e faça: media = (nota1 + nota2) / 2;"
}


def conectar():
    pasta = os.path.dirname(DB_PATH)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def coluna_existe(conn, tabela, coluna):
    colunas = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
    return any(c["name"] == coluna for c in colunas)


def adicionar_coluna(conn, tabela, coluna, definicao):
    if not coluna_existe(conn, tabela, coluna):
        conn.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")


def iniciar_banco():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            xp INTEGER DEFAULT 0,
            nivel INTEGER DEFAULT 1,
            sequencia INTEGER DEFAULT 1,
            ultimo_acesso TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            licao_id INTEGER NOT NULL,
            modulo_id INTEGER NOT NULL,
            quiz_correto INTEGER DEFAULT 0,
            codigo_enviado INTEGER DEFAULT 0,
            concluida INTEGER DEFAULT 0,
            codigo_usuario TEXT,
            saida_codigo TEXT,
            entrada_codigo TEXT,
            atualizado_em TEXT,
            UNIQUE(usuario_id, licao_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS conquistas_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            icone TEXT NOT NULL,
            UNIQUE(usuario_id, nome)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS desafios_diarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            codigo_usuario TEXT,
            saida_codigo TEXT,
            entrada_codigo TEXT,
            concluido INTEGER DEFAULT 0,
            UNIQUE(usuario_id, data)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS compilador_historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            codigo TEXT,
            entrada TEXT,
            saida TEXT,
            build_log TEXT,
            criado_em TEXT
        )
    """)

    # Migração para bancos antigos já criados antes das novas funções.
    adicionar_coluna(conn, "progresso", "quiz_correto", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "progresso", "codigo_enviado", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "progresso", "codigo_usuario", "TEXT")
    adicionar_coluna(conn, "progresso", "saida_codigo", "TEXT")
    adicionar_coluna(conn, "progresso", "entrada_codigo", "TEXT")
    adicionar_coluna(conn, "progresso", "atualizado_em", "TEXT")

    adicionar_coluna(conn, "usuarios", "xp", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "usuarios", "nivel", "INTEGER DEFAULT 1")
    adicionar_coluna(conn, "usuarios", "sequencia", "INTEGER DEFAULT 1")
    adicionar_coluna(conn, "usuarios", "ultimo_acesso", "TEXT")
    adicionar_coluna(conn, "desafios_diarios", "entrada_codigo", "TEXT")

    # Quem já concluiu lição em versão antiga recebe permissão de rever e continuar.
    conn.execute("""
        UPDATE progresso
        SET quiz_correto = 1
        WHERE concluida = 1 AND (quiz_correto IS NULL OR quiz_correto = 0)
    """)

    conn.commit()
    conn.close()

def usuario_logado():
    if "usuario_id" not in session:
        return None

    conn = conectar()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (session["usuario_id"],)).fetchone()
    conn.close()
    return usuario


def total_licoes():
    return sum(len(m["licoes"]) for m in MODULOS)


def contar_concluidas(usuario_id):
    conn = conectar()
    total = conn.execute(
        "SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND concluida = 1",
        (usuario_id,)
    ).fetchone()["total"]
    conn.close()
    return total


def encontrar_licao(licao_id):
    for modulo in MODULOS:
        for licao in modulo["licoes"]:
            if licao["id"] == licao_id:
                return modulo, licao
    return None, None


def modulo_liberado(usuario_id, modulo_id):
    if modulo_id == 1:
        return True

    modulo_anterior = next((m for m in MODULOS if m["id"] == modulo_id - 1), None)
    if not modulo_anterior:
        return False

    ids_licoes = [l["id"] for l in modulo_anterior["licoes"]]
    placeholders = ",".join("?" for _ in ids_licoes)

    conn = conectar()
    params = [usuario_id] + ids_licoes
    concluidas = conn.execute(
        f"SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND licao_id IN ({placeholders}) AND concluida = 1",
        params
    ).fetchone()["total"]
    conn.close()

    return concluidas == len(ids_licoes)


def modulo_acessivel(usuario_id, modulo_id):
    """
    Permite acessar:
    - módulos liberados;
    - módulos que o usuário já começou;
    - módulos com lições já concluídas.
    Assim o usuário consegue voltar em lições já feitas.
    """
    if modulo_liberado(usuario_id, modulo_id):
        return True

    conn = conectar()
    registro = conn.execute(
        "SELECT id FROM progresso WHERE usuario_id = ? AND modulo_id = ? LIMIT 1",
        (usuario_id, modulo_id)
    ).fetchone()
    conn.close()

    return registro is not None


def progresso_modulo(usuario_id, modulo):
    ids = [l["id"] for l in modulo["licoes"]]
    if not ids:
        return 0

    placeholders = ",".join("?" for _ in ids)
    params = [usuario_id] + ids

    conn = conectar()
    concluidas = conn.execute(
        f"SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND licao_id IN ({placeholders}) AND concluida = 1",
        params
    ).fetchone()["total"]
    conn.close()

    return int((concluidas / len(ids)) * 100)


def atualizar_nivel(usuario_id):
    conn = conectar()
    usuario = conn.execute("SELECT xp FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
    nivel = max(1, usuario["xp"] // 250 + 1)
    conn.execute("UPDATE usuarios SET nivel = ? WHERE id = ?", (nivel, usuario_id))
    conn.commit()
    conn.close()


def conceder_conquistas(usuario_id):
    concluidas = contar_concluidas(usuario_id)
    conn = conectar()

    if concluidas >= 1:
        conn.execute(
            "INSERT OR IGNORE INTO conquistas_usuario (usuario_id, nome, icone) VALUES (?, ?, ?)",
            (usuario_id, "Primeiros Passos", "🚀")
        )

    if concluidas >= 3:
        conn.execute(
            "INSERT OR IGNORE INTO conquistas_usuario (usuario_id, nome, icone) VALUES (?, ?, ?)",
            (usuario_id, "Foco Total", "🔥")
        )

    if concluidas >= total_licoes():
        conn.execute(
            "INSERT OR IGNORE INTO conquistas_usuario (usuario_id, nome, icone) VALUES (?, ?, ?)",
            (usuario_id, "Trilha Inicial", "🏆")
        )

    conn.commit()
    conn.close()



def executar_com_piston(codigo, entrada=""):
    url = "https://emkc.org/api/v2/piston/execute"

    payload = {
        "language": "c",
        "version": "10.2.0",
        "files": [{"name": "main.c", "content": codigo}],
        "stdin": entrada or "",
        "args": [],
        "compile_timeout": 10000,
        "run_timeout": 5000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1
    }

    resposta = requests.post(url, json=payload, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()

    compile_out = dados.get("compile", {}) or {}
    run_out = dados.get("run", {}) or {}

    build_log = ""
    if compile_out.get("stdout"):
        build_log += compile_out.get("stdout", "")
    if compile_out.get("stderr"):
        build_log += compile_out.get("stderr", "")

    saida = ""
    if run_out.get("stdout"):
        saida += run_out.get("stdout", "")
    if run_out.get("stderr"):
        saida += "\nErros:\n" + run_out.get("stderr", "")

    if not build_log.strip():
        build_log = "Build finished successfully.\n0 errors, 0 warnings."

    if not saida.strip():
        saida = "Programa executado sem saída na tela."

    return {
        "ok": run_out.get("code", 0) == 0,
        "build": build_log,
        "saida": montar_terminal_unificado(saida, entrada),
        "origem": "Piston API"
    }


def executar_compilador_online(codigo, entrada=""):
    try:
        return executar_com_piston(codigo, entrada)
    except Exception as erro_api:
        resultado_local = executar_codigo_c(codigo, entrada)

        if "GCC não está disponível" in resultado_local.get("saida", "") or "GCC não está disponível" in resultado_local.get("build", ""):
            return {
                "ok": False,
                "build": "Não foi possível usar o compilador online.\n\nAPI externa indisponível ou bloqueada:\n" + str(erro_api),
                "saida": "O código foi salvo, mas não foi possível executar agora.\n\nTente novamente mais tarde ou rode localmente no Code::Blocks.",
                "origem": "Erro"
            }

        resultado_local["origem"] = "GCC local"
        return resultado_local


def compilar_codigo_c(codigo):
    """
    Compila o código C e retorna apenas o build log.
    Parecido com a etapa Build do Code::Blocks.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        arquivo_c = os.path.join(temp_dir, "programa.c")
        arquivo_saida = os.path.join(temp_dir, "programa")

        with open(arquivo_c, "w", encoding="utf-8") as f:
            f.write(codigo)

        try:
            compilacao = subprocess.run(
                ["gcc", arquivo_c, "-o", arquivo_saida],
                capture_output=True,
                text=True,
                timeout=8
            )

            if compilacao.returncode != 0:
                return {
                    "ok": False,
                    "build": "Build failed.\n\n" + compilacao.stderr,
                    "saida": ""
                }

            return {
                "ok": True,
                "build": "Build finished successfully.\n0 errors, 0 warnings.",
                "saida": ""
            }

        except FileNotFoundError:
            return {
                "ok": False,
                "build": "Não foi possível compilar: GCC não está disponível no servidor.\n\nNo Render gratuito, normalmente o ambiente não vem preparado para compilar C. Para produção, use uma API externa de compilação ou configure um ambiente com GCC.",
                "saida": ""
            }
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "build": "Tempo de compilação excedido.",
                "saida": ""
            }
        except Exception as erro:
            return {
                "ok": False,
                "build": f"Erro ao compilar: {erro}",
                "saida": ""
            }


def executar_codigo_c(codigo, entrada=""):
    """
    Compila e executa o código C.
    A entrada simula o que seria digitado no terminal quando o programa usa scanf.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        arquivo_c = os.path.join(temp_dir, "programa.c")
        arquivo_saida = os.path.join(temp_dir, "programa")

        with open(arquivo_c, "w", encoding="utf-8") as f:
            f.write(codigo)

        try:
            compilacao = subprocess.run(
                ["gcc", arquivo_c, "-o", arquivo_saida],
                capture_output=True,
                text=True,
                timeout=8
            )

            if compilacao.returncode != 0:
                return {
                    "ok": False,
                    "build": "Build failed.\n\n" + compilacao.stderr,
                    "saida": ""
                }

            execucao = subprocess.run(
                [arquivo_saida],
                capture_output=True,
                text=True,
                timeout=5,
                input=entrada
            )

            saida = execucao.stdout

            if execucao.stderr:
                saida += "\nErros:\n" + execucao.stderr

            if not saida.strip():
                saida = "Process returned 0.\nO programa executou, mas não mostrou nenhuma saída."

            return {
                "ok": True,
                "build": "Build finished successfully.\n0 errors, 0 warnings.",
                "saida": saida + "\n\nProcess returned 0."
            }

        except FileNotFoundError:
            return {
                "ok": False,
                "build": "Não foi possível compilar: GCC não está disponível no servidor.",
                "saida": "O código foi salvo, mas o servidor não possui GCC para executar.\n\nPara ter compilação real online, será necessário configurar GCC no Render ou usar uma API externa segura de compilação.\n\nA entrada do terminal ficará salva para quando a execução estiver disponível."
            }
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "build": "Build/Run interrompido por tempo excedido.",
                "saida": "Tempo de execução excedido.\nVerifique se há loop infinito ou se faltou entrada para scanf."
            }
        except Exception as erro:
            return {
                "ok": False,
                "build": "Erro durante build/run.",
                "saida": f"Erro ao executar o código: {erro}"
            }


@app.context_processor
def contexto():
    return {
        "usuario": usuario_logado(),
        "total_licoes": total_licoes()
    }


@app.route("/")
def index():
    if usuario_logado():
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        conn = conectar()
        usuario_existente = conn.execute("SELECT id FROM usuarios WHERE email = ?", (email,)).fetchone()

        if usuario_existente:
            conn.close()
            return render_template("cadastro.html", erro="Este e-mail já está cadastrado. Entre na conta em vez de criar outra.")

        senha_hash = generate_password_hash(senha)

        cur = conn.execute(
            "INSERT INTO usuarios (nome, email, senha, ultimo_acesso) VALUES (?, ?, ?, ?)",
            (nome, email, senha_hash, str(date.today()))
        )
        conn.commit()

        session.clear()
        session["usuario_id"] = cur.lastrowid

        conn.close()
        return redirect(url_for("dashboard"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        conn = conectar()
        usuario = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

        if usuario and check_password_hash(usuario["senha"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
            conn.execute("UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?", (str(date.today()), usuario["id"]))
            conn.commit()
            conn.close()
            return redirect(url_for("dashboard"))

        conn.close()
        return render_template("login.html", erro="E-mail ou senha incorretos.")

    return render_template("login.html")


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    concluidas = contar_concluidas(usuario["id"])
    porcentagem = int((concluidas / total_licoes()) * 100)

    conn = conectar()
    conquistas = conn.execute(
        "SELECT * FROM conquistas_usuario WHERE usuario_id = ?",
        (usuario["id"],)
    ).fetchall()

    ranking = conn.execute(
        "SELECT nome, xp, nivel FROM usuarios ORDER BY xp DESC, nivel DESC LIMIT 5"
    ).fetchall()
    conn.close()

    modulos_view = []
    for modulo in MODULOS:
        modulos_view.append({
            **modulo,
            "progresso": progresso_modulo(usuario["id"], modulo),
            "liberado": modulo_liberado(usuario["id"], modulo["id"])
        })

    return render_template(
        "dashboard.html",
        concluidas=concluidas,
        porcentagem=porcentagem,
        modulos=modulos_view,
        conquistas=conquistas,
        ranking=ranking
    )


@app.route("/modulos")
def modulos():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    modulos_view = []
    for modulo in MODULOS:
        modulos_view.append({
            **modulo,
            "progresso": progresso_modulo(usuario["id"], modulo),
            "liberado": modulo_liberado(usuario["id"], modulo["id"])
        })

    return render_template("modulos.html", modulos=modulos_view)



@app.route("/compilador")
def compilador():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    licao_id = request.args.get("licao_id", type=int)
    codigo_inicial = '#include <stdio.h>\n\nint main() {\n    // escreva seu código aqui\n\n    return 0;\n}'
    titulo = "Compilador Online"

    if licao_id:
        modulo, licao = encontrar_licao(licao_id)
        if licao:
            codigo_inicial = licao.get("codigo_minimo", licao["codigo"])
            titulo = f"Compilador - {licao['titulo']}"

    conn = conectar()
    historico = conn.execute(
        "SELECT * FROM compilador_historico WHERE usuario_id = ? ORDER BY id DESC LIMIT 5",
        (usuario["id"],)
    ).fetchall()
    conn.close()

    return render_template(
        "compilador.html",
        codigo_inicial=codigo_inicial,
        titulo=titulo,
        historico=historico
    )


@app.route("/api/compilador/executar", methods=["POST"])
def api_compilador_executar():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "build": "Usuário não logado.", "saida": ""}), 401

    dados = request.get_json()
    codigo = dados.get("codigo", "")
    entrada = dados.get("entrada", "")

    resultado = executar_compilador_online(codigo, entrada)

    conn = conectar()
    conn.execute(
        """
        INSERT INTO compilador_historico (usuario_id, codigo, entrada, saida, build_log, criado_em)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (usuario["id"], codigo, entrada, resultado.get("saida", ""), resultado.get("build", ""), str(date.today()))
    )
    conn.commit()
    conn.close()

    return jsonify(resultado)


@app.route("/estudar/<int:modulo_id>")
def estudar(modulo_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    if not modulo_acessivel(usuario["id"], modulo_id):
        return redirect(url_for("modulos"))

    modulo = next((m for m in MODULOS if m["id"] == modulo_id), None)
    if not modulo:
        return redirect(url_for("modulos"))

    licao_id = request.args.get("licao", type=int)
    if licao_id:
        licao = next((l for l in modulo["licoes"] if l["id"] == licao_id), modulo["licoes"][0])
    else:
        licao = modulo["licoes"][0]

    conn = conectar()
    registros = conn.execute(
        "SELECT * FROM progresso WHERE usuario_id = ? AND modulo_id = ?",
        (usuario["id"], modulo_id)
    ).fetchall()

    registro_licao = conn.execute(
        "SELECT * FROM progresso WHERE usuario_id = ? AND licao_id = ?",
        (usuario["id"], licao["id"])
    ).fetchone()

    conn.close()

    concluidas_ids = [r["licao_id"] for r in registros if r["concluida"] == 1]

    codigo_padrao = licao.get("codigo_minimo", licao["codigo"])
    codigo_salvo = registro_licao["codigo_usuario"] if registro_licao and "codigo_usuario" in registro_licao.keys() and registro_licao["codigo_usuario"] else codigo_padrao
    saida_salva = registro_licao["saida_codigo"] if registro_licao and "saida_codigo" in registro_licao.keys() and registro_licao["saida_codigo"] else "A saída do compilador aparecerá aqui."

    return render_template(
        "estudar.html",
        modulo=modulo,
        licao=licao,
        concluidas_ids=concluidas_ids,
        codigo_salvo=codigo_salvo,
        saida_salva=saida_salva
    )



@app.route("/exercicio/<int:licao_id>")
def exercicio(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    modulo, licao = encontrar_licao(licao_id)
    if not licao:
        return redirect(url_for("modulos"))

    if not modulo_acessivel(usuario["id"], modulo["id"]):
        return redirect(url_for("modulos"))

    conn = conectar()
    registro = conn.execute(
        "SELECT * FROM progresso WHERE usuario_id = ? AND licao_id = ?",
        (usuario["id"], licao_id)
    ).fetchone()
    conn.close()

    codigo_padrao = licao.get("codigo_minimo", "#include <stdio.h>\n\nint main() {\n    return 0;\n}")
    codigo_salvo = registro["codigo_usuario"] if registro and registro["codigo_usuario"] else codigo_padrao
    saida_salva = registro["saida_codigo"] if registro and "saida_codigo" in registro.keys() and registro["saida_codigo"] else "A saída do compilador aparecerá aqui."
    entrada_salva = registro["entrada_codigo"] if registro and "entrada_codigo" in registro.keys() and registro["entrada_codigo"] else ""
    return render_template(
        "exercicio.html",
        modulo=modulo,
        licao=licao,
        codigo_salvo=codigo_salvo,
        saida_salva=saida_salva,
        entrada_salva=entrada_salva
    )


@app.route("/desafio-diario")
def desafio_diario():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    hoje = str(date.today())
    conn = conectar()
    registro = conn.execute(
        "SELECT * FROM desafios_diarios WHERE usuario_id = ? AND data = ?",
        (usuario["id"], hoje)
    ).fetchone()
    conn.close()

    codigo = registro["codigo_usuario"] if registro and registro["codigo_usuario"] else DESAFIO_DIARIO["codigo_inicial"]
    saida = registro["saida_codigo"] if registro and registro["saida_codigo"] else "A saída do desafio aparecerá aqui."
    entrada = registro["entrada_codigo"] if registro and "entrada_codigo" in registro.keys() and registro["entrada_codigo"] else ""
    concluido = registro["concluido"] if registro else 0
    return render_template("desafio_diario.html", desafio=DESAFIO_DIARIO, codigo=codigo, saida=saida, entrada=entrada, concluido=concluido)


@app.route("/verificar", methods=["POST"])
def verificar():
    dados = request.get_json()
    licao_id = int(dados.get("licao_id"))
    resposta = dados.get("resposta", "")

    modulo, licao = encontrar_licao(licao_id)
    if not licao:
        return jsonify({"correta": False, "mensagem": "Lição não encontrada."})

    correta = resposta == licao["resposta"]

    if correta and usuario_logado():
        try:
            conn = conectar()
            conn.execute(
                """
                INSERT INTO progresso (usuario_id, licao_id, modulo_id, quiz_correto, atualizado_em)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(usuario_id, licao_id)
                DO UPDATE SET quiz_correto = 1, atualizado_em = excluded.atualizado_em
                """,
                (usuario_logado()["id"], licao_id, modulo["id"], str(date.today()))
            )
            conn.commit()
            conn.close()
        except Exception as erro:
            return jsonify({
                "correta": False,
                "mensagem": f"Erro ao salvar resposta: {erro}"
            }), 500

    return jsonify({
        "correta": correta,
        "mensagem": "Resposta correta! Agora faça o exercício de código para concluir." if correta else "Resposta incorreta. Revise o conteúdo e tente novamente."
    })



@app.route("/compilar-codigo", methods=["POST"])
def compilar_codigo():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "build": "Usuário não logado.", "saida": ""}), 401

    dados = request.get_json()
    codigo = dados.get("codigo", "")

    resultado = compilar_codigo_c(codigo)
    return jsonify(resultado)


@app.route("/executar-codigo", methods=["POST"])
def executar_codigo():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "saida": "Usuário não logado."}), 401

    dados = request.get_json()
    codigo = dados.get("codigo", "")
    entrada = dados.get("entrada", "")
    licao_id = dados.get("licao_id")
    tipo = dados.get("tipo", "licao")

    resultado = executar_codigo_c(codigo, entrada)

    if tipo == "licao" and licao_id:
        modulo, licao = encontrar_licao(int(licao_id))
        if modulo:
            try:
                conn = conectar()
                conn.execute(
                    """
                    INSERT INTO progresso (usuario_id, licao_id, modulo_id, codigo_usuario, saida_codigo, entrada_codigo, codigo_enviado, atualizado_em)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?)
                    ON CONFLICT(usuario_id, licao_id)
                    DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                                  saida_codigo = excluded.saida_codigo,
                                  entrada_codigo = excluded.entrada_codigo,
                                  codigo_enviado = 1,
                                  atualizado_em = excluded.atualizado_em
                    """,
                    (usuario["id"], int(licao_id), modulo["id"], codigo, resultado["saida"], entrada, str(date.today()))
                )
                conn.commit()
                conn.close()
            except Exception as erro:
                return jsonify({
                    "ok": False,
                    "saida": f"Erro ao salvar código no banco: {erro}"
                }), 500

    if tipo == "diario":
        hoje = str(date.today())
        conn = conectar()
        conn.execute(
            """
            INSERT INTO desafios_diarios (usuario_id, data, codigo_usuario, saida_codigo, entrada_codigo, concluido)
            VALUES (?, ?, ?, ?, ?, 0)
            ON CONFLICT(usuario_id, data)
            DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                          saida_codigo = excluded.saida_codigo,
                          entrada_codigo = excluded.entrada_codigo
            """,
            (usuario["id"], hoje, codigo, resultado["saida"], entrada)
        )
        conn.commit()
        conn.close()

    return jsonify(resultado)


@app.route("/concluir/<int:licao_id>", methods=["POST"])
def concluir(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"erro": "Usuário não logado"}), 401

    modulo, licao = encontrar_licao(licao_id)
    if not licao:
        return jsonify({"erro": "Lição não encontrada"}), 404

    conn = conectar()
    registro = conn.execute(
        "SELECT * FROM progresso WHERE usuario_id = ? AND licao_id = ?",
        (usuario["id"], licao_id)
    ).fetchone()

    if not registro or registro["quiz_correto"] != 1:
        conn.close()
        return jsonify({"ok": False, "mensagem": "Responda corretamente o desafio teórico antes de concluir."})

    if not registro["codigo_usuario"]:
        conn.close()
        return jsonify({"ok": False, "mensagem": "Faça e execute o exercício de código antes de concluir."})

    ja_concluida = registro["concluida"] == 1

    conn.execute(
        "UPDATE progresso SET concluida = 1, codigo_enviado = 1, atualizado_em = ? WHERE usuario_id = ? AND licao_id = ?",
        (str(date.today()), usuario["id"], licao_id)
    )

    if not ja_concluida:
        conn.execute("UPDATE usuarios SET xp = xp + 50 WHERE id = ?", (usuario["id"],))

    conn.commit()
    conn.close()

    atualizar_nivel(usuario["id"])
    conceder_conquistas(usuario["id"])

    return jsonify({"ok": True, "mensagem": "Lição concluída! +50 XP"})


@app.route("/concluir-desafio-diario", methods=["POST"])
def concluir_desafio_diario():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "mensagem": "Usuário não logado."}), 401

    hoje = str(date.today())
    conn = conectar()
    registro = conn.execute(
        "SELECT * FROM desafios_diarios WHERE usuario_id = ? AND data = ?",
        (usuario["id"], hoje)
    ).fetchone()

    if not registro or not registro["codigo_usuario"]:
        conn.close()
        return jsonify({"ok": False, "mensagem": "Execute um código antes de concluir o desafio diário."})

    if registro["concluido"] != 1:
        conn.execute(
            "UPDATE desafios_diarios SET concluido = 1 WHERE usuario_id = ? AND data = ?",
            (usuario["id"], hoje)
        )
        conn.execute("UPDATE usuarios SET xp = xp + 30 WHERE id = ?", (usuario["id"],))
        conn.execute(
            "INSERT OR IGNORE INTO conquistas_usuario (usuario_id, nome, icone) VALUES (?, ?, ?)",
            (usuario["id"], "Desafio Diário", "🎯")
        )

    conn.commit()
    conn.close()

    atualizar_nivel(usuario["id"])

    return jsonify({"ok": True, "mensagem": "Desafio diário concluído! +30 XP"})


# Importante para Render/Gunicorn: cria o banco ao importar o app.
iniciar_banco()

if __name__ == "__main__":
    app.run(debug=True)
