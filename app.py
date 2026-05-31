from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.secret_key = "troque-esta-chave-em-producao"

DB_PATH = "instance/ensinar_c.db"


MODULOS = [
    {
        "id": 1,
        "titulo": "Introdução ao C",
        "descricao": "Conheça a linguagem C, sua história, características e estrutura básica.",
        "icone": "💻",
        "xp": 100,
        "licoes": [
            {
                "id": 1,
                "titulo": "O que é a linguagem C?",
                "conteudo": "A linguagem C é uma linguagem compilada, conhecida por sua eficiência e controle de memória. Ela é usada em sistemas embarcados, sistemas operacionais e aplicações de alto desempenho.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Olá, mundo!");\n    return 0;\n}',
                "pergunta": "Qual função inicia a execução de um programa em C?",
                "alternativas": ["printf", "scanf", "main", "include"],
                "resposta": "main"
            },
            {
                "id": 2,
                "titulo": "Estrutura básica",
                "conteudo": "Um programa em C normalmente possui bibliotecas, a função main, comandos dentro de chaves e um retorno ao final.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Meu primeiro programa em C");\n    return 0;\n}',
                "pergunta": "Qual biblioteca permite usar printf e scanf?",
                "alternativas": ["stdio.h", "math.h", "string.h", "time.h"],
                "resposta": "stdio.h"
            }
        ]
    },
    {
        "id": 2,
        "titulo": "printf e scanf",
        "descricao": "Aprenda a exibir dados na tela e receber entradas do usuário.",
        "icone": "📘",
        "xp": 120,
        "licoes": [
            {
                "id": 3,
                "titulo": "Usando printf",
                "conteudo": "A função printf é utilizada para mostrar mensagens, valores de variáveis e resultados na tela.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    printf("Idade: %d", idade);\n    return 0;\n}',
                "pergunta": "Qual especificador mostra números inteiros?",
                "alternativas": ["%f", "%c", "%d", "%s"],
                "resposta": "%d"
            },
            {
                "id": 4,
                "titulo": "Usando scanf",
                "conteudo": "A função scanf permite ler dados digitados pelo usuário e armazená-los em variáveis.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade;\n    scanf("%d", &idade);\n    printf("Idade: %d", idade);\n    return 0;\n}',
                "pergunta": "Por que usamos & no scanf?",
                "alternativas": ["Para somar", "Para indicar endereço da variável", "Para imprimir", "Para encerrar"],
                "resposta": "Para indicar endereço da variável"
            }
        ]
    },
    {
        "id": 3,
        "titulo": "Variáveis",
        "descricao": "Entenda os principais tipos de dados e como armazenar informações.",
        "icone": "🔢",
        "xp": 140,
        "licoes": [
            {
                "id": 5,
                "titulo": "Tipo int",
                "conteudo": "O tipo int armazena números inteiros, como 1, 10, -5 e 200.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int numero = 10;\n    printf("%d", numero);\n    return 0;\n}',
                "pergunta": "Qual tipo armazena números inteiros?",
                "alternativas": ["float", "char", "int", "double"],
                "resposta": "int"
            },
            {
                "id": 6,
                "titulo": "float, double e char",
                "conteudo": "float e double armazenam números com casas decimais. char armazena um caractere.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    float nota = 8.5;\n    char conceito = \'A\';\n    printf("%.1f %c", nota, conceito);\n    return 0;\n}',
                "pergunta": "Qual tipo armazena um caractere?",
                "alternativas": ["int", "float", "char", "double"],
                "resposta": "char"
            }
        ]
    },
    {
        "id": 4,
        "titulo": "Operadores",
        "descricao": "Use operadores aritméticos, relacionais e lógicos.",
        "icone": "➗",
        "xp": 160,
        "licoes": [
            {
                "id": 7,
                "titulo": "Operadores matemáticos",
                "conteudo": "Os operadores matemáticos permitem realizar soma, subtração, multiplicação, divisão e resto.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int a = 10;\n    int b = 3;\n    printf("%d", a + b);\n    return 0;\n}',
                "pergunta": "Qual operador realiza multiplicação?",
                "alternativas": ["+", "-", "*", "/"],
                "resposta": "*"
            }
        ]
    },
    {
        "id": 5,
        "titulo": "Estruturas de Decisão",
        "descricao": "Utilize if, else, else if e switch.",
        "icone": "🔀",
        "xp": 180,
        "licoes": [
            {
                "id": 8,
                "titulo": "if e else",
                "conteudo": "O if executa um bloco se a condição for verdadeira. O else executa outro bloco se for falsa.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    if (idade >= 18) {\n        printf("Maior de idade");\n    } else {\n        printf("Menor de idade");\n    }\n    return 0;\n}',
                "pergunta": "Qual comando testa uma condição?",
                "alternativas": ["for", "if", "scanf", "return"],
                "resposta": "if"
            }
        ]
    },
    {
        "id": 6,
        "titulo": "Estruturas de Repetição",
        "descricao": "Aprenda while, do while, for, break e continue.",
        "icone": "🔁",
        "xp": 200,
        "licoes": [
            {
                "id": 9,
                "titulo": "Laço for",
                "conteudo": "O for é usado quando sabemos quantas vezes queremos repetir um comando.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    for (int i = 1; i <= 5; i++) {\n        printf("%d\\n", i);\n    }\n    return 0;\n}',
                "pergunta": "Qual estrutura é indicada para repetição com contador?",
                "alternativas": ["if", "else", "for", "switch"],
                "resposta": "for"
            }
        ]
    }
]

CONQUISTAS = [
    ("Primeiros Passos", "Concluiu a primeira lição", "🚀"),
    ("Código Correto", "Acertou um desafio", "✅"),
    ("Foco Total", "Concluiu três lições", "🔥"),
    ("Explorador C", "Acessou todos os módulos", "🏆"),
]


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_banco():
    os.makedirs("instance", exist_ok=True)
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
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
            concluida INTEGER DEFAULT 0,
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


def modulo_liberado(usuario_id, modulo_id):
    if modulo_id == 1:
        return True

    conn = conectar()
    modulo_anterior = next((m for m in MODULOS if m["id"] == modulo_id - 1), None)
    ids_licoes = [l["id"] for l in modulo_anterior["licoes"]]

    if not ids_licoes:
        conn.close()
        return False

    placeholders = ",".join("?" for _ in ids_licoes)
    params = [usuario_id] + ids_licoes
    concluidas = conn.execute(
        f"SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND licao_id IN ({placeholders}) AND concluida = 1",
        params
    ).fetchone()["total"]

    conn.close()
    return concluidas == len(ids_licoes)


def progresso_modulo(usuario_id, modulo):
    ids = [l["id"] for l in modulo["licoes"]]
    if not ids:
        return 0

    conn = conectar()
    placeholders = ",".join("?" for _ in ids)
    params = [usuario_id] + ids
    concluidas = conn.execute(
        f"SELECT COUNT(*) AS total FROM progresso WHERE usuario_id = ? AND licao_id IN ({placeholders}) AND concluida = 1",
        params
    ).fetchone()["total"]
    conn.close()

    return int((concluidas / len(ids)) * 100)


def encontrar_licao(licao_id):
    for modulo in MODULOS:
        for licao in modulo["licoes"]:
            if licao["id"] == licao_id:
                return modulo, licao
    return None, None


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
            (usuario_id, "Explorador C", "🏆")
        )

    conn.commit()
    conn.close()


@app.context_processor
def contexto():
    return {"usuario": usuario_logado(), "total_licoes": total_licoes()}


@app.route("/")
def index():
    if usuario_logado():
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = generate_password_hash(request.form["senha"])

        conn = conectar()
        try:
            cur = conn.execute(
                "INSERT INTO usuarios (nome, email, senha, ultimo_acesso) VALUES (?, ?, ?, ?)",
                (nome, email, senha, str(date.today()))
            )
            conn.commit()
            session["usuario_id"] = cur.lastrowid
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            return render_template("cadastro.html", erro="Este e-mail já está cadastrado.")
        finally:
            conn.close()

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        usuario = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

        if usuario and check_password_hash(usuario["senha"], senha):
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


@app.route("/estudar/<int:modulo_id>")
def estudar(modulo_id):
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    if not modulo_liberado(usuario["id"], modulo_id):
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
    concluidas = conn.execute(
        "SELECT licao_id FROM progresso WHERE usuario_id = ? AND modulo_id = ? AND concluida = 1",
        (usuario["id"], modulo_id)
    ).fetchall()
    conn.close()

    concluidas_ids = [c["licao_id"] for c in concluidas]

    return render_template(
        "estudar.html",
        modulo=modulo,
        licao=licao,
        concluidas_ids=concluidas_ids
    )


@app.route("/desafio-diario")
def desafio_diario():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))
    modulo, licao = encontrar_licao(3)
    return render_template("desafio_diario.html", modulo=modulo, licao=licao)


@app.route("/concluir/<int:licao_id>", methods=["POST"])
def concluir(licao_id):
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"erro": "Usuário não logado"}), 401

    modulo, licao = encontrar_licao(licao_id)
    if not licao:
        return jsonify({"erro": "Lição não encontrada"}), 404

    conn = conectar()
    ja_concluida = conn.execute(
        "SELECT * FROM progresso WHERE usuario_id = ? AND licao_id = ? AND concluida = 1",
        (usuario["id"], licao_id)
    ).fetchone()

    if not ja_concluida:
        conn.execute(
            "INSERT OR REPLACE INTO progresso (usuario_id, licao_id, modulo_id, concluida) VALUES (?, ?, ?, 1)",
            (usuario["id"], licao_id, modulo["id"])
        )
        conn.execute(
            "UPDATE usuarios SET xp = xp + 50 WHERE id = ?",
            (usuario["id"],)
        )
        conn.execute(
            "INSERT OR IGNORE INTO conquistas_usuario (usuario_id, nome, icone) VALUES (?, ?, ?)",
            (usuario["id"], "Código Correto", "✅")
        )

    conn.commit()
    conn.close()

    atualizar_nivel(usuario["id"])
    conceder_conquistas(usuario["id"])

    return jsonify({"ok": True, "mensagem": "Lição concluída! +50 XP"})


@app.route("/verificar", methods=["POST"])
def verificar():
    dados = request.get_json()
    licao_id = int(dados.get("licao_id"))
    resposta = dados.get("resposta", "")

    modulo, licao = encontrar_licao(licao_id)
    if not licao:
        return jsonify({"correta": False, "mensagem": "Lição não encontrada."})

    correta = resposta == licao["resposta"]
    return jsonify({
        "correta": correta,
        "mensagem": "Resposta correta! Agora você pode concluir a lição." if correta else "Resposta incorreta. Revise o conteúdo e tente novamente."
    })


@app.route("/certificado")
def certificado():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    concluidas = contar_concluidas(usuario["id"])
    if concluidas < total_licoes():
        return redirect(url_for("dashboard"))

    return render_template("certificado.html", concluidas=concluidas)


if __name__ == "__main__":
    iniciar_banco()
    app.run(debug=True)
