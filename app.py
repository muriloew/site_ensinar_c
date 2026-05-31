from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

MODULOS = [
    {
        "id": 1,
        "titulo": "Introdução ao C",
        "descricao": "Entenda o que é a linguagem C, sua importância e a estrutura básica de um programa.",
        "licoes": [
            {
                "id": "1-1",
                "titulo": "O que é a linguagem C?",
                "teoria": "A linguagem C é uma linguagem compilada, muito utilizada por sua eficiência, desempenho e controle de memória. Ela é usada em sistemas embarcados, sistemas operacionais, microcontroladores e aplicações que exigem bom desempenho.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Olá, mundo!");\n    return 0;\n}',
                "explicacao": "Esse programa mostra uma mensagem na tela. A função main é o ponto inicial do programa e o printf exibe o texto.",
                "desafio": {
                    "pergunta": "Qual função é o ponto inicial de execução de um programa em C?",
                    "alternativas": ["printf", "scanf", "main", "include"],
                    "resposta": "main"
                }
            },
            {
                "id": "1-2",
                "titulo": "Estrutura básica de um programa",
                "teoria": "Um programa em C normalmente possui bibliotecas, a função main, comandos dentro de chaves e um retorno indicando o final da execução.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    printf("Meu primeiro programa em C");\n    return 0;\n}',
                "explicacao": "A linha #include <stdio.h> permite usar funções de entrada e saída. O return 0 indica que o programa terminou corretamente.",
                "desafio": {
                    "pergunta": "Qual biblioteca permite usar printf e scanf?",
                    "alternativas": ["stdio.h", "math.h", "string.h", "time.h"],
                    "resposta": "stdio.h"
                }
            }
        ]
    },
    {
        "id": 2,
        "titulo": "printf e scanf",
        "descricao": "Aprenda a exibir informações na tela e ler dados digitados pelo usuário.",
        "licoes": [
            {
                "id": "2-1",
                "titulo": "Saída de dados com printf",
                "teoria": "A função printf é usada para mostrar mensagens, valores de variáveis e resultados na tela.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    printf("Idade: %d", idade);\n    return 0;\n}',
                "explicacao": "O %d é um especificador de formato usado para exibir números inteiros.",
                "desafio": {
                    "pergunta": "Qual especificador é usado para mostrar números inteiros?",
                    "alternativas": ["%f", "%c", "%d", "%s"],
                    "resposta": "%d"
                }
            },
            {
                "id": "2-2",
                "titulo": "Entrada de dados com scanf",
                "teoria": "A função scanf permite ler dados digitados pelo usuário e armazená-los em variáveis.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade;\n    scanf("%d", &idade);\n    printf("Idade digitada: %d", idade);\n    return 0;\n}',
                "explicacao": "No scanf, o operador & indica o endereço da variável onde o valor digitado será armazenado.",
                "desafio": {
                    "pergunta": "Por que usamos o operador & no scanf?",
                    "alternativas": ["Para imprimir texto", "Para indicar o endereço da variável", "Para somar valores", "Para finalizar o programa"],
                    "resposta": "Para indicar o endereço da variável"
                }
            }
        ]
    },
    {
        "id": 3,
        "titulo": "Variáveis e tipos de dados",
        "descricao": "Conheça os principais tipos usados para armazenar informações em C.",
        "licoes": [
            {
                "id": "3-1",
                "titulo": "Tipo int",
                "teoria": "O tipo int é usado para armazenar números inteiros, como 1, 10, -5 e 250.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int numero = 10;\n    printf("%d", numero);\n    return 0;\n}',
                "explicacao": "A variável numero armazena o valor inteiro 10.",
                "desafio": {
                    "pergunta": "Qual tipo armazena números inteiros?",
                    "alternativas": ["float", "char", "int", "double"],
                    "resposta": "int"
                }
            },
            {
                "id": "3-2",
                "titulo": "float, double e char",
                "teoria": "float e double armazenam valores com casas decimais. char armazena um único caractere.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    float nota = 8.5;\n    char conceito = \'A\';\n    printf("Nota: %.1f - Conceito: %c", nota, conceito);\n    return 0;\n}',
                "explicacao": "O %.1f mostra uma casa decimal e o %c mostra um caractere.",
                "desafio": {
                    "pergunta": "Qual tipo armazena um caractere?",
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
                "teoria": "Os operadores matemáticos permitem realizar soma, subtração, multiplicação, divisão e resto da divisão.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int a = 10;\n    int b = 3;\n    printf("Soma: %d", a + b);\n    return 0;\n}',
                "explicacao": "O operador + realiza a soma entre dois valores.",
                "desafio": {
                    "pergunta": "Qual operador realiza multiplicação em C?",
                    "alternativas": ["+", "-", "*", "/"],
                    "resposta": "*"
                }
            },
            {
                "id": "4-2",
                "titulo": "Operadores relacionais",
                "teoria": "Operadores relacionais comparam valores e retornam verdadeiro ou falso.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    printf("%d", idade >= 18);\n    return 0;\n}',
                "explicacao": "A expressão idade >= 18 verifica se idade é maior ou igual a 18.",
                "desafio": {
                    "pergunta": "Qual operador significa maior ou igual?",
                    "alternativas": [">", "<", ">=", "=="],
                    "resposta": ">="
                }
            }
        ]
    },
    {
        "id": 5,
        "titulo": "Estruturas de decisão",
        "descricao": "Controle o fluxo do programa usando if, else, else if e switch.",
        "licoes": [
            {
                "id": "5-1",
                "titulo": "if e else",
                "teoria": "O if executa um bloco quando uma condição é verdadeira. O else executa outro bloco quando a condição é falsa.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n\n    if (idade >= 18) {\n        printf("Maior de idade");\n    } else {\n        printf("Menor de idade");\n    }\n\n    return 0;\n}',
                "explicacao": "A condição idade >= 18 define qual mensagem será exibida.",
                "desafio": {
                    "pergunta": "Qual comando é usado para testar uma condição?",
                    "alternativas": ["for", "if", "scanf", "return"],
                    "resposta": "if"
                }
            },
            {
                "id": "5-2",
                "titulo": "switch case",
                "teoria": "O switch é usado para comparar uma variável com vários valores possíveis.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int opcao = 1;\n\n    switch (opcao) {\n        case 1:\n            printf("Opção 1");\n            break;\n        default:\n            printf("Opção inválida");\n    }\n\n    return 0;\n}',
                "explicacao": "O case representa uma possibilidade e o break evita que o programa continue executando outros casos.",
                "desafio": {
                    "pergunta": "Qual comando interrompe um case no switch?",
                    "alternativas": ["stop", "break", "return", "end"],
                    "resposta": "break"
                }
            }
        ]
    },
    {
        "id": 6,
        "titulo": "Estruturas de repetição",
        "descricao": "Aprenda while, do while e for.",
        "licoes": [
            {
                "id": "6-1",
                "titulo": "Laço for",
                "teoria": "O for é usado quando sabemos quantas vezes queremos repetir um comando.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    for (int i = 1; i <= 5; i++) {\n        printf("%d\\n", i);\n    }\n    return 0;\n}',
                "explicacao": "A variável i começa em 1, repete enquanto i <= 5 e aumenta de 1 em 1.",
                "desafio": {
                    "pergunta": "Qual estrutura é indicada para repetição com contador?",
                    "alternativas": ["if", "else", "for", "switch"],
                    "resposta": "for"
                }
            },
            {
                "id": "6-2",
                "titulo": "Laço while",
                "teoria": "O while repete um bloco enquanto uma condição for verdadeira.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int contador = 1;\n\n    while (contador <= 5) {\n        printf("%d\\n", contador);\n        contador++;\n    }\n\n    return 0;\n}',
                "explicacao": "O contador precisa ser atualizado dentro do while para evitar repetição infinita.",
                "desafio": {
                    "pergunta": "O que acontece se a condição do while nunca ficar falsa?",
                    "alternativas": ["O programa fecha sozinho", "Ocorre um loop infinito", "O printf para", "O código não compila"],
                    "resposta": "Ocorre um loop infinito"
                }
            }
        ]
    }
]


@app.context_processor
def contexto_global():
    total_licoes = sum(len(modulo["licoes"]) for modulo in MODULOS)
    return {"total_licoes": total_licoes}


@app.route("/")
def index():
    return render_template("index.html", modulos=MODULOS)


@app.route("/modulos")
def modulos():
    return render_template("modulos.html", modulos=MODULOS)


@app.route("/modulo/<int:modulo_id>")
def modulo(modulo_id):
    modulo_encontrado = next((m for m in MODULOS if m["id"] == modulo_id), None)

    if modulo_encontrado is None:
        return render_template("erro.html", mensagem="Módulo não encontrado."), 404

    return render_template("modulo.html", modulo=modulo_encontrado)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


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
