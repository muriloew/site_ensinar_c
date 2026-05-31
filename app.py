from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

MODULOS = [
    {
        "id": 1,
        "titulo": "Introdução ao C",
        "descricao": "Entenda o que é a linguagem C, sua estrutura básica e como um programa é executado.",
        "licoes": [
            {
                "id": "1-1",
                "titulo": "O que é a linguagem C?",
                "teoria": "A linguagem C é uma linguagem compilada, muito usada por sua eficiência, desempenho e controle de memória. Ela é base para várias outras linguagens e aparece em sistemas embarcados, sistemas operacionais e aplicações de baixo nível.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Olá, mundo!");\n    return 0;\n}',
                "explicacao": "O comando printf mostra uma mensagem na tela. A função main é o ponto de entrada do programa.",
                "desafio": {
                    "pergunta": "Qual função é usada como ponto inicial de execução em um programa C?",
                    "alternativas": ["printf", "scanf", "main", "include"],
                    "resposta": "main"
                }
            },
            {
                "id": "1-2",
                "titulo": "Estrutura básica",
                "teoria": "Um programa em C normalmente possui bibliotecas, a função main, comandos e o retorno da execução.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Meu primeiro programa em C");\n    return 0;\n}',
                "explicacao": "A biblioteca stdio.h permite usar printf. O return 0 indica que o programa terminou corretamente.",
                "desafio": {
                    "pergunta": "Qual biblioteca permite utilizar printf e scanf?",
                    "alternativas": ["math.h", "stdio.h", "string.h", "stdlib.h"],
                    "resposta": "stdio.h"
                }
            }
        ]
    },
    {
        "id": 2,
        "titulo": "printf e scanf",
        "descricao": "Aprenda saída e entrada de dados em C.",
        "licoes": [
            {
                "id": "2-1",
                "titulo": "Usando printf",
                "teoria": "A função printf é usada para exibir mensagens, valores de variáveis e resultados na tela.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    printf("Idade: %d", idade);\n    return 0;\n}',
                "explicacao": "O %d é usado para mostrar valores inteiros.",
                "desafio": {
                    "pergunta": "Qual especificador é usado para imprimir números inteiros?",
                    "alternativas": ["%f", "%c", "%d", "%s"],
                    "resposta": "%d"
                }
            },
            {
                "id": "2-2",
                "titulo": "Usando scanf",
                "teoria": "A função scanf é usada para ler dados digitados pelo usuário e armazenar em variáveis.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade;\n    scanf("%d", &idade);\n    printf("Idade digitada: %d", idade);\n    return 0;\n}',
                "explicacao": "O operador & indica o endereço da variável onde o valor será armazenado.",
                "desafio": {
                    "pergunta": "Por que usamos &idade no scanf?",
                    "alternativas": ["Para somar valores", "Para indicar o endereço da variável", "Para imprimir texto", "Para encerrar o programa"],
                    "resposta": "Para indicar o endereço da variável"
                }
            }
        ]
    },
    {
        "id": 3,
        "titulo": "Variáveis",
        "descricao": "Conheça tipos de dados, declaração e armazenamento de informações.",
        "licoes": [
            {
                "id": "3-1",
                "titulo": "Tipo int",
                "teoria": "O tipo int armazena números inteiros, como 1, 10, -5 e 200.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int numero = 10;\n    printf("%d", numero);\n    return 0;\n}',
                "explicacao": "A variável numero guarda um valor inteiro.",
                "desafio": {
                    "pergunta": "Qual tipo é usado para armazenar números inteiros?",
                    "alternativas": ["float", "char", "int", "double"],
                    "resposta": "int"
                }
            },
            {
                "id": "3-2",
                "titulo": "float, double e char",
                "teoria": "float e double armazenam números com casas decimais. char armazena um caractere.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    float nota = 8.5;\n    char letra = \'A\';\n    printf("Nota: %.1f - Letra: %c", nota, letra);\n    return 0;\n}',
                "explicacao": "%.1f mostra uma casa decimal. %c mostra um caractere.",
                "desafio": {
                    "pergunta": "Qual tipo armazena apenas um caractere?",
                    "alternativas": ["int", "float", "char", "double"],
                    "resposta": "char"
                }
            }
        ]
    },
    {
        "id": 4,
        "titulo": "Operadores",
        "descricao": "Use operadores matemáticos, relacionais e lógicos.",
        "licoes": [
            {
                "id": "4-1",
                "titulo": "Operadores matemáticos",
                "teoria": "Em C, podemos usar operadores para soma, subtração, multiplicação, divisão e resto.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int a = 10;\n    int b = 3;\n    printf("Soma: %d", a + b);\n    return 0;\n}',
                "explicacao": "O operador + realiza soma entre dois valores.",
                "desafio": {
                    "pergunta": "Qual operador realiza multiplicação em C?",
                    "alternativas": ["+", "-", "*", "/"],
                    "resposta": "*"
                }
            }
        ]
    },
    {
        "id": 5,
        "titulo": "Decisão",
        "descricao": "Controle o fluxo do programa usando if, else e switch.",
        "licoes": [
            {
                "id": "5-1",
                "titulo": "if e else",
                "teoria": "O if permite executar um bloco de código somente se uma condição for verdadeira. O else executa outro bloco quando a condição é falsa.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n\n    if (idade >= 18) {\n        printf("Maior de idade");\n    } else {\n        printf("Menor de idade");\n    }\n\n    return 0;\n}',
                "explicacao": "A condição idade >= 18 verifica se a idade é maior ou igual a 18.",
                "desafio": {
                    "pergunta": "Qual comando é usado para testar uma condição?",
                    "alternativas": ["for", "if", "scanf", "return"],
                    "resposta": "if"
                }
            }
        ]
    },
    {
        "id": 6,
        "titulo": "Repetição",
        "descricao": "Aprenda while, do while e for.",
        "licoes": [
            {
                "id": "6-1",
                "titulo": "Laço for",
                "teoria": "O for é usado quando sabemos quantas vezes queremos repetir um comando.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    for (int i = 1; i <= 5; i++) {\n        printf("%d\\n", i);\n    }\n    return 0;\n}',
                "explicacao": "O contador i começa em 1, repete enquanto i <= 5 e aumenta de 1 em 1.",
                "desafio": {
                    "pergunta": "Qual estrutura é indicada para repetir algo com contador?",
                    "alternativas": ["if", "else", "for", "switch"],
                    "resposta": "for"
                }
            }
        ]
    }
]


@app.route("/")
def index():
    total_licoes = sum(len(modulo["licoes"]) for modulo in MODULOS)
    return render_template("index.html", modulos=MODULOS, total_licoes=total_licoes)


@app.route("/modulos")
def modulos():
    return render_template("modulos.html", modulos=MODULOS)


@app.route("/modulo/<int:modulo_id>")
def modulo(modulo_id):
    modulo_encontrado = next((m for m in MODULOS if m["id"] == modulo_id), None)

    if modulo_encontrado is None:
        return render_template("erro.html", mensagem="Módulo não encontrado."), 404

    return render_template("modulo.html", modulo=modulo_encontrado)


@app.route("/api/modulos")
def api_modulos():
    return jsonify(MODULOS)


@app.route("/api/verificar", methods=["POST"])
def verificar():
    dados = request.get_json()
    resposta_usuario = dados.get("resposta", "").strip()
    resposta_correta = dados.get("resposta_correta", "").strip()

    acertou = resposta_usuario == resposta_correta

    return jsonify({
        "acertou": acertou,
        "mensagem": "Resposta correta!" if acertou else "Resposta incorreta. Revise a explicação e tente novamente."
    })


if __name__ == "__main__":
    app.run(debug=True)
