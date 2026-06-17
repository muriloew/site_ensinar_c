from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import sqlite3
import os
import subprocess
import tempfile
import requests
import json
import re
import shutil
import unicodedata
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from flask_socketio import SocketIO, emit
import time
import signal
import threading
import select

try:
    import pty
except ImportError:
    pty = None

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-dev-ensinar-c")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

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


COMPLEMENTOS_LICOES = {
    1: {"correcao": {"codigo_contem": ["printf"], "saida_obrigatoria": True}},
    2: {"correcao": {"min_ocorrencias_codigo": {"printf": 2}, "min_linhas_saida": 2}},
    3: {"correcao": {"codigo_contem": ["int", "printf"], "saida_regex": [r"\d"]}},
    4: {"correcao": {"codigo_contem": ["scanf", "&", "printf"], "testes": [{"entrada": "42\n", "saida_contem": ["42"]}]}},
    5: {"correcao": {"codigo_contem": ["int", "+", "printf"], "saida_regex": [r"\d"]}},
    6: {"correcao": {"codigo_contem": ["float", "char", "printf"], "saida_obrigatoria": True}},
    7: {"correcao": {"codigo_contem": ["+", "-", "*", "printf"], "min_linhas_saida": 3}},
    8: {"correcao": {"codigo_contem": ["if", "printf"], "saida_regex": [r"positivo|negativo|zero|maior|menor"]}},
    9: {"correcao": {"codigo_contem": ["for", "printf"], "saida_contem": ["1", "10"]}}
}


MODULOS_COMPLEMENTARES = [
    {
        "id": 7,
        "titulo": "Arrays",
        "descricao": "Guarde vários valores em uma mesma estrutura e percorra listas com repetição.",
        "icone": "[]",
        "licoes": [
            {
                "id": 10,
                "titulo": "Vetores",
                "conteudo": "Um vetor armazena vários valores do mesmo tipo. Cada posição é acessada por um índice que começa em zero.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int valores[5] = {2, 4, 6, 8, 10};\n    printf("%d\\n", valores[2]);\n    return 0;\n}',
                "pergunta": "Qual é o primeiro índice de um vetor em C?",
                "alternativas": ["0", "1", "-1", "10"],
                "resposta": "0",
                "exercicio_codigo": "Crie um vetor com cinco números inteiros e mostre o terceiro valor na tela.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int valores[5] = {2, 4, 6, 8, 10};\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["[", "]", "printf"], "saida_contem": ["6"]}
            },
            {
                "id": 11,
                "titulo": "Percorrendo vetores",
                "conteudo": "Com for, podemos visitar todas as posições de um vetor e acumular resultados.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int numeros[3] = {1, 2, 3};\n    for (int i = 0; i < 3; i++) {\n        printf("%d\\n", numeros[i]);\n    }\n    return 0;\n}',
                "pergunta": "Qual estrutura combina bem com vetores para percorrer posições?",
                "alternativas": ["for", "return", "include", "char"],
                "resposta": "for",
                "exercicio_codigo": "Some os valores {1, 2, 3, 4, 5} usando um for e mostre o total.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int numeros[5] = {1, 2, 3, 4, 5};\n    int soma = 0;\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["for", "+", "printf"], "saida_contem": ["15"]}
            }
        ]
    },
    {
        "id": 8,
        "titulo": "Strings",
        "descricao": "Trabalhe com textos, vetores de caracteres e funções da biblioteca string.h.",
        "icone": "str",
        "licoes": [
            {
                "id": 12,
                "titulo": "Textos em char[]",
                "conteudo": "Em C, strings são vetores de char terminados pelo caractere nulo, representado por \\0.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    char linguagem[] = "C";\n    printf("Linguagem: %s\\n", linguagem);\n    return 0;\n}',
                "pergunta": "Qual especificador costuma imprimir uma string?",
                "alternativas": ["%s", "%d", "%f", "%c"],
                "resposta": "%s",
                "exercicio_codigo": "Crie uma string com o texto Programar em C e mostre esse texto na tela.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    char texto[] = \"Programar em C\";\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["char", "%s", "printf"], "saida_contem": ["programar", "c"]}
            },
            {
                "id": 13,
                "titulo": "strlen",
                "conteudo": "A função strlen, da biblioteca string.h, retorna a quantidade de caracteres de uma string.",
                "codigo": '#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char palavra[] = "codigo";\n    printf("%zu\\n", strlen(palavra));\n    return 0;\n}',
                "pergunta": "Qual biblioteca declara strlen?",
                "alternativas": ["string.h", "stdio.h", "math.h", "stdlib.h"],
                "resposta": "string.h",
                "exercicio_codigo": "Use strlen para mostrar o tamanho da palavra linguagem.",
                "codigo_minimo": "#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char palavra[] = \"linguagem\";\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["#include <string.h>", "strlen", "printf"], "saida_contem": ["9"]}
            }
        ]
    },
    {
        "id": 9,
        "titulo": "Funções",
        "descricao": "Divida programas em blocos reutilizáveis com parâmetros e retorno.",
        "icone": "fn",
        "licoes": [
            {
                "id": 14,
                "titulo": "Criando funções",
                "conteudo": "Funções evitam repetição e deixam o programa organizado. Elas podem receber valores e devolver um resultado.",
                "codigo": '#include <stdio.h>\n\nint dobro(int n) {\n    return n * 2;\n}\n\nint main() {\n    printf("%d\\n", dobro(5));\n    return 0;\n}',
                "pergunta": "Qual palavra devolve um valor de uma função?",
                "alternativas": ["return", "include", "scanf", "while"],
                "resposta": "return",
                "exercicio_codigo": "Crie uma função quadrado que receba 6 e mostre 36.",
                "codigo_minimo": "#include <stdio.h>\n\nint quadrado(int n) {\n    return 0;\n}\n\nint main() {\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["quadrado", "return", "*", "printf"], "saida_contem": ["36"]}
            },
            {
                "id": 15,
                "titulo": "Parâmetros e retorno",
                "conteudo": "Parâmetros permitem enviar dados para uma função. O retorno permite usar o resultado em outro ponto do programa.",
                "codigo": '#include <stdio.h>\n\nint maior(int a, int b) {\n    if (a > b) return a;\n    return b;\n}\n\nint main() {\n    printf("%d\\n", maior(7, 12));\n    return 0;\n}',
                "pergunta": "O que os parâmetros fazem?",
                "alternativas": ["Enviam valores para uma função", "Finalizam o programa", "Criam bibliotecas", "Apagam variáveis"],
                "resposta": "Enviam valores para uma função",
                "exercicio_codigo": "Crie uma função maior que receba 7 e 12 e mostre o maior valor.",
                "codigo_minimo": "#include <stdio.h>\n\nint maior(int a, int b) {\n    return 0;\n}\n\nint main() {\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["maior", "if", "return", "printf"], "saida_contem": ["12"]}
            }
        ]
    },
    {
        "id": 10,
        "titulo": "Ponteiros",
        "descricao": "Entenda endereços de memória, indireção e passagem por referência.",
        "icone": "*",
        "licoes": [
            {
                "id": 16,
                "titulo": "Endereços e valores",
                "conteudo": "Um ponteiro guarda o endereço de uma variável. Com * acessamos o valor apontado e com & pegamos o endereço.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    int valor = 10;\n    int *p = &valor;\n    printf("%d\\n", *p);\n    return 0;\n}',
                "pergunta": "Qual operador obtém o endereço de uma variável?",
                "alternativas": ["&", "*", "%", "#"],
                "resposta": "&",
                "exercicio_codigo": "Crie uma variável valor com 10, um ponteiro para ela e mostre o valor usando o ponteiro.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n    int valor = 10;\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["*", "&", "printf"], "saida_contem": ["10"]}
            },
            {
                "id": 17,
                "titulo": "Passagem por referência",
                "conteudo": "Ao passar o endereço de uma variável para uma função, a função pode alterar o valor original.",
                "codigo": '#include <stdio.h>\n\nvoid aumentar(int *n) {\n    *n = *n + 1;\n}\n\nint main() {\n    int valor = 5;\n    aumentar(&valor);\n    printf("%d\\n", valor);\n    return 0;\n}',
                "pergunta": "Por que passamos &valor para a função?",
                "alternativas": ["Para enviar o endereço", "Para multiplicar", "Para imprimir texto", "Para encerrar o programa"],
                "resposta": "Para enviar o endereço",
                "exercicio_codigo": "Crie uma função aumentar que receba um ponteiro, some 1 em valor 5 e mostre 6.",
                "codigo_minimo": "#include <stdio.h>\n\nvoid aumentar(int *n) {\n\n}\n\nint main() {\n    int valor = 5;\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["void aumentar", "*n", "&valor", "printf"], "saida_contem": ["6"]}
            }
        ]
    },
    {
        "id": 11,
        "titulo": "Structs",
        "descricao": "Agrupe dados relacionados em um tipo próprio.",
        "icone": "{}",
        "licoes": [
            {
                "id": 18,
                "titulo": "Criando uma struct",
                "conteudo": "Structs permitem juntar campos diferentes, como nome e nota, em uma única variável.",
                "codigo": '#include <stdio.h>\n\nstruct Aluno {\n    char nome[30];\n    float nota;\n};\n\nint main() {\n    struct Aluno aluno = {"Ana", 9.0};\n    printf("%s %.1f\\n", aluno.nome, aluno.nota);\n    return 0;\n}',
                "pergunta": "Qual palavra cria uma estrutura em C?",
                "alternativas": ["struct", "array", "scanf", "break"],
                "resposta": "struct",
                "exercicio_codigo": "Crie uma struct Aluno com nome Ana e nota 9.0 e mostre os dois valores.",
                "codigo_minimo": "#include <stdio.h>\n\nstruct Aluno {\n\n};\n\nint main() {\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["struct", "Aluno", "printf"], "saida_contem": ["ana", "9"]}
            },
            {
                "id": 19,
                "titulo": "Vetor de structs",
                "conteudo": "Também é possível criar vetores de structs para guardar vários registros.",
                "codigo": '#include <stdio.h>\n\nstruct Produto {\n    int preco;\n};\n\nint main() {\n    struct Produto produtos[2] = {{10}, {20}};\n    printf("%d\\n", produtos[0].preco + produtos[1].preco);\n    return 0;\n}',
                "pergunta": "Como acessamos um campo de uma struct comum?",
                "alternativas": [".", "->", "&", "#"],
                "resposta": ".",
                "exercicio_codigo": "Crie dois produtos em um vetor de structs, com preços 10 e 20, e mostre a soma 30.",
                "codigo_minimo": "#include <stdio.h>\n\nstruct Produto {\n    int preco;\n};\n\nint main() {\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["struct", "[", "]", ".preco", "printf"], "saida_contem": ["30"]}
            }
        ]
    },
    {
        "id": 12,
        "titulo": "Arquivos e memória",
        "descricao": "Conheça gravação em arquivo, alocação dinâmica e cuidados comuns.",
        "icone": "io",
        "licoes": [
            {
                "id": 20,
                "titulo": "Escrevendo arquivos",
                "conteudo": "fopen abre um arquivo, fprintf grava dados e fclose fecha o recurso quando terminamos.",
                "codigo": '#include <stdio.h>\n\nint main() {\n    FILE *arquivo = fopen("saida.txt", "w");\n    fprintf(arquivo, "Curso de C");\n    fclose(arquivo);\n    printf("Arquivo gravado\\n");\n    return 0;\n}',
                "pergunta": "Qual função abre um arquivo?",
                "alternativas": ["fopen", "printf", "strlen", "malloc"],
                "resposta": "fopen",
                "exercicio_codigo": "Abra um arquivo, grave uma mensagem, feche o arquivo e mostre Arquivo gravado.",
                "codigo_minimo": "#include <stdio.h>\n\nint main() {\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["FILE", "fopen", "fprintf", "fclose"], "saida_contem": ["arquivo", "gravado"]}
            },
            {
                "id": 21,
                "titulo": "Alocação dinâmica",
                "conteudo": "malloc reserva memória durante a execução. Depois do uso, free libera essa memória.",
                "codigo": '#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int *numero = malloc(sizeof(int));\n    *numero = 30;\n    printf("%d\\n", *numero);\n    free(numero);\n    return 0;\n}',
                "pergunta": "Qual função libera memória alocada com malloc?",
                "alternativas": ["free", "fclose", "return", "scanf"],
                "resposta": "free",
                "exercicio_codigo": "Use malloc para guardar o número 30, mostre o valor e libere a memória com free.",
                "codigo_minimo": "#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n\n    return 0;\n}",
                "correcao": {"codigo_contem": ["malloc", "free", "*"], "saida_contem": ["30"]}
            }
        ]
    }
]


DESAFIOS_DIARIOS = [
    {
        "id": "media-simples",
        "titulo": "Desafio diário: média simples",
        "descricao": "Declare duas notas, calcule a média e mostre o resultado na tela.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    float nota1 = 8.0;\n    float nota2 = 7.0;\n\n    // calcule a média aqui\n\n    return 0;\n}',
        "dica": "Use uma variável media e divida a soma por 2.",
        "correcao": {"codigo_contem": ["float", "/", "printf"], "saida_regex": [r"7[,.]5|7\.50"]}
    },
    {
        "id": "soma-entrada",
        "titulo": "Desafio diário: soma com entrada",
        "descricao": "Leia dois números inteiros e mostre a soma deles.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int a, b;\n\n    // leia e some os valores\n\n    return 0;\n}',
        "dica": "Use scanf duas vezes ou leia os dois valores no mesmo scanf.",
        "correcao": {"codigo_contem": ["scanf", "+", "printf"], "testes": [{"entrada": "4\n6\n", "saida_contem": ["10"]}, {"entrada": "12\n5\n", "saida_contem": ["17"]}]}
    },
    {
        "id": "par-impar",
        "titulo": "Desafio diário: par ou ímpar",
        "descricao": "Leia um inteiro e informe se ele é par ou ímpar.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int numero;\n\n    // leia o número e teste o resto da divisão por 2\n\n    return 0;\n}',
        "dica": "Use numero % 2 para descobrir se o resto é zero.",
        "correcao": {"codigo_contem": ["scanf", "%", "if"], "testes": [{"entrada": "8\n", "saida_contem": ["par"]}, {"entrada": "7\n", "saida_contem": ["impar"]}]}
    },
    {
        "id": "maior-tres",
        "titulo": "Desafio diário: maior de três",
        "descricao": "Leia três números e mostre o maior.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int a, b, c, maior;\n\n    // leia os valores e encontre o maior\n\n    return 0;\n}',
        "dica": "Comece assumindo que a é o maior e compare com b e c.",
        "correcao": {"codigo_contem": ["scanf", "if", "printf"], "testes": [{"entrada": "3\n9\n4\n", "saida_contem": ["9"]}, {"entrada": "20\n5\n11\n", "saida_contem": ["20"]}]}
    },
    {
        "id": "tabuada",
        "titulo": "Desafio diário: tabuada",
        "descricao": "Leia um número e mostre a tabuada dele de 1 a 10.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int numero;\n\n    // leia o número e use for para a tabuada\n\n    return 0;\n}',
        "dica": "Um for de 1 até 10 resolve o desafio.",
        "correcao": {"codigo_contem": ["scanf", "for", "*"], "testes": [{"entrada": "5\n", "saida_contem": ["5", "25", "50"]}]}
    },
    {
        "id": "fatorial",
        "titulo": "Desafio diário: fatorial",
        "descricao": "Leia um número inteiro e mostre o fatorial dele.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int n;\n    int fatorial = 1;\n\n    // leia n e calcule o fatorial\n\n    return 0;\n}',
        "dica": "Multiplique os valores de 1 até n.",
        "correcao": {"codigo_contem": ["scanf", "for", "*"], "testes": [{"entrada": "5\n", "saida_contem": ["120"]}, {"entrada": "4\n", "saida_contem": ["24"]}]}
    },
    {
        "id": "positivos",
        "titulo": "Desafio diário: contador de positivos",
        "descricao": "Leia cinco inteiros e mostre quantos são positivos.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int numero;\n    int positivos = 0;\n\n    // leia 5 números e conte os positivos\n\n    return 0;\n}',
        "dica": "Use um for e incremente o contador quando numero > 0.",
        "correcao": {"codigo_contem": ["scanf", "for", "if"], "testes": [{"entrada": "1\n-2\n3\n0\n5\n", "saida_contem": ["3"]}]}
    },
    {
        "id": "strlen",
        "titulo": "Desafio diário: tamanho da palavra",
        "descricao": "Use strlen para mostrar o tamanho da palavra codigo.",
        "codigo_inicial": '#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char palavra[] = "codigo";\n\n    // mostre o tamanho da palavra\n\n    return 0;\n}',
        "dica": "strlen(palavra) retorna 6.",
        "correcao": {"codigo_contem": ["string.h", "strlen", "printf"], "saida_contem": ["6"]}
    },
    {
        "id": "soma-vetor",
        "titulo": "Desafio diário: soma do vetor",
        "descricao": "Some os valores do vetor {1, 2, 3, 4} e mostre o total.",
        "codigo_inicial": '#include <stdio.h>\n\nint main() {\n    int valores[4] = {1, 2, 3, 4};\n    int soma = 0;\n\n    // percorra o vetor e some\n\n    return 0;\n}',
        "dica": "Percorra o vetor com for e acumule em soma.",
        "correcao": {"codigo_contem": ["[", "]", "for", "+"], "saida_contem": ["10"]}
    },
    {
        "id": "funcao-quadrado",
        "titulo": "Desafio diário: função quadrado",
        "descricao": "Crie uma função que receba 6 e retorne o quadrado do número.",
        "codigo_inicial": '#include <stdio.h>\n\nint quadrado(int n) {\n    return 0;\n}\n\nint main() {\n    // mostre quadrado(6)\n\n    return 0;\n}',
        "dica": "O quadrado de n é n * n.",
        "correcao": {"codigo_contem": ["quadrado", "return", "*", "printf"], "saida_contem": ["36"]}
    }
]


def aplicar_conteudo_expandido():
    for modulo in MODULOS:
        for licao in modulo["licoes"]:
            extra = COMPLEMENTOS_LICOES.get(licao["id"])
            if extra:
                licao.update(extra)

    ids_existentes = {modulo["id"] for modulo in MODULOS}
    for modulo in MODULOS_COMPLEMENTARES:
        if modulo["id"] not in ids_existentes:
            MODULOS.append(modulo)


aplicar_conteudo_expandido()


TRILHA_COMPLETA_C = [
    {
        "id": 1,
        "titulo": "Introdução ao C",
        "descricao": "Primeiros conceitos da linguagem C, estrutura de programas e processo de compilação.",
        "icone": "C",
        "conteudos": ["O que é C", "Estrutura básica", "Comentários", "Compilação"],
        "topicos": [
            "linguagem compilada", "sintaxe básica", "estrutura de programas", "eficiência",
            "desempenho", "gerenciamento de memória", "comandos básicos", "bibliotecas",
            "pré-processador", "função main()", "comentários", "compilação e execução",
            "erros de compilação", "mensagens do compilador"
        ]
    },
    {
        "id": 2,
        "titulo": "printf e scanf",
        "descricao": "Saída formatada e entrada de dados pelo teclado.",
        "icone": "io",
        "conteudos": ["printf", "scanf"],
        "topicos": [
            "saída de dados", "formatação", "%d", "%f", "%c", "%s", "entrada de dados",
            "leitura do teclado", "operador &", "armazenamento de entrada", "validação básica"
        ]
    },
    {
        "id": 3,
        "titulo": "Variáveis",
        "descricao": "Tipos, constantes, macros e escopo de variáveis.",
        "icone": "var",
        "conteudos": ["int", "float e double", "char", "constantes", "#define", "escopo"],
        "topicos": [
            "declaração", "inicialização", "memória", "precisão", "ASCII", "constantes",
            "macros", "variáveis locais e globais"
        ]
    },
    {
        "id": 4,
        "titulo": "Operadores",
        "descricao": "Operações matemáticas, comparação, lógica e incremento.",
        "icone": "+-",
        "conteudos": [
            "soma", "subtração", "multiplicação", "divisão",
            "operadores relacionais", "operadores lógicos", "incremento"
        ],
        "topicos": [
            "operadores matemáticos", "comparação", "expressões booleanas",
            "incremento e decremento", "operações condicionais"
        ]
    },
    {
        "id": 5,
        "titulo": "Decisão",
        "descricao": "Controle de fluxo com decisões simples e múltiplas.",
        "icone": "if",
        "conteudos": ["if", "else", "else if", "switch", "ternário"],
        "topicos": ["condições", "execução condicional", "múltiplas decisões", "switch case", "operador ternário"]
    },
    {
        "id": 6,
        "titulo": "Repetição",
        "descricao": "Laços de repetição e controle de execução.",
        "icone": "for",
        "conteudos": ["while", "do while", "for", "break", "continue"],
        "topicos": ["loops", "repetição", "controle de execução", "interrupção de laços"]
    },
    {
        "id": 7,
        "titulo": "Funções",
        "descricao": "Criação de funções, parâmetros, retorno, protótipos e recursão.",
        "icone": "fn",
        "conteudos": ["criando função", "parâmetros", "retorno", "protótipos", "recursão"],
        "topicos": [
            "modularização", "reutilização", "passagem de parâmetros",
            "retorno de valores", "chamadas recursivas"
        ]
    },
    {
        "id": 8,
        "titulo": "Arrays e strings",
        "descricao": "Vetores, matrizes e manipulação de textos em C.",
        "icone": "[]",
        "conteudos": ["arrays", "matrizes", "strings", "strlen", "strcpy", "strcmp", "strcat", "fgets"],
        "topicos": ["vetores", "matrizes", "manipulação textual", "entrada segura", "funções da biblioteca string"]
    },
    {
        "id": 9,
        "titulo": "Ponteiros",
        "descricao": "Endereços de memória, desreferenciamento e ponteiros em funções e arrays.",
        "icone": "*",
        "conteudos": ["memória", "operador &", "ponteiros + funções", "ponteiros + arrays", "ponteiro para ponteiro"],
        "topicos": ["endereços de memória", "desreferenciamento", "aritmética de ponteiros", "passagem por referência"]
    },
    {
        "id": 10,
        "titulo": "Alocação dinâmica",
        "descricao": "Uso da heap e gerenciamento manual de memória.",
        "icone": "mem",
        "conteudos": ["malloc", "calloc", "realloc", "free", "memory leak"],
        "topicos": ["alocação dinâmica", "heap", "gerenciamento de memória", "vazamento de memória"]
    },
    {
        "id": 11,
        "titulo": "Structs",
        "descricao": "Tipos compostos com struct, typedef, unions e enum.",
        "icone": "{}",
        "conteudos": ["structs", "typedef", "unions", "enum"],
        "topicos": ["agrupamento de dados", "tipos personalizados", "compartilhamento de memória", "conjuntos nomeados"]
    },
    {
        "id": 12,
        "titulo": "Arquivos",
        "descricao": "Leitura e escrita de arquivos usando a biblioteca padrão.",
        "icone": "file",
        "conteudos": ["fopen", "fclose", "fprintf", "fscanf"],
        "topicos": ["abertura de arquivos", "fechamento de arquivos", "gravação", "leitura formatada"]
    },
    {
        "id": 13,
        "titulo": "Modularização",
        "descricao": "Separação de código em arquivos .h e .c com proteção de inclusão.",
        "icone": ".h",
        "conteudos": [".h", ".c", "include guards"],
        "topicos": ["cabeçalhos", "arquivos fonte", "organização de projetos", "proteção contra inclusão duplicada"]
    },
    {
        "id": 14,
        "titulo": "Bibliotecas",
        "descricao": "Principais bibliotecas padrão usadas em programas C.",
        "icone": "lib",
        "conteudos": ["stdio", "stdlib", "string", "math"],
        "topicos": ["entrada e saída", "utilidades gerais", "manipulação de strings", "funções matemáticas"]
    },
    {
        "id": 15,
        "titulo": "Bits",
        "descricao": "Operadores bitwise e criação de máscaras.",
        "icone": "01",
        "conteudos": ["bitwise", "máscaras"],
        "topicos": ["operações bit a bit", "AND", "OR", "XOR", "deslocamento", "máscaras de bits"]
    },
    {
        "id": 16,
        "titulo": "Debug",
        "descricao": "Identificação de erros de sintaxe, erros lógicos e técnicas de depuração.",
        "icone": "bug",
        "conteudos": ["erros de sintaxe", "erros lógicos", "debug"],
        "topicos": ["mensagens de erro", "teste de hipóteses", "rastreamento de valores", "correção de falhas"]
    },
    {
        "id": 17,
        "titulo": "GCC e build",
        "descricao": "Compilação pela linha de comando, linking e automação com Makefile.",
        "icone": "gcc",
        "conteudos": ["gcc", "linking", "makefile"],
        "topicos": ["compilador GCC", "etapas de build", "ligação de objetos", "automação de compilação"]
    },
    {
        "id": 18,
        "titulo": "Segurança",
        "descricao": "Cuidados com buffer overflow e validação de entrada.",
        "icone": "sec",
        "conteudos": ["buffer overflow", "validação"],
        "topicos": ["limites de buffers", "entrada insegura", "validação de dados", "boas práticas"]
    },
    {
        "id": 19,
        "titulo": "Estruturas de dados",
        "descricao": "Listas, pilhas, filas e árvores.",
        "icone": "ds",
        "conteudos": ["listas", "pilhas", "filas", "árvores"],
        "topicos": ["organização de dados", "inserção", "remoção", "percurso", "uso de ponteiros"]
    },
    {
        "id": 20,
        "titulo": "Algoritmos",
        "descricao": "Busca, ordenação e noções de eficiência.",
        "icone": "alg",
        "conteudos": ["busca linear", "bubble sort", "eficiência"],
        "topicos": ["busca sequencial", "ordenação simples", "complexidade", "comparação de desempenho"]
    },
    {
        "id": 21,
        "titulo": "Projetos",
        "descricao": "Projetos práticos para consolidar a linguagem C.",
        "icone": "app",
        "conteudos": [
            "calculadora", "cadastro", "agenda", "jogo terminal",
            "sistema biblioteca", "editor texto", "projeto final"
        ],
        "topicos": ["integração de conteúdos", "organização", "entrada e saída", "persistência", "projeto completo"]
    }
]


def codigo_exemplo_para_conteudo(conteudo):
    chave = conteudo.lower()

    if "scanf" in chave or "entrada" in chave or "validação" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int numero;\n    printf("Digite um numero: ");\n    scanf("%d", &numero);\n    printf("Valor informado: %d\\n", numero);\n    return 0;\n}'
    if "if" in chave or "else" in chave or "ternário" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int idade = 18;\n    if (idade >= 18) {\n        printf("Maior de idade\\n");\n    } else {\n        printf("Menor de idade\\n");\n    }\n    return 0;\n}'
    if "switch" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int opcao = 2;\n    switch (opcao) {\n        case 1: printf("Cadastrar\\n"); break;\n        case 2: printf("Consultar\\n"); break;\n        default: printf("Opcao invalida\\n");\n    }\n    return 0;\n}'
    if "while" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int contador = 1;\n    while (contador <= 3) {\n        printf("%d\\n", contador);\n        contador++;\n    }\n    return 0;\n}'
    if "do while" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int contador = 1;\n    do {\n        printf("%d\\n", contador);\n        contador++;\n    } while (contador <= 3);\n    return 0;\n}'
    if "for" in chave or "break" in chave or "continue" in chave:
        return '#include <stdio.h>\n\nint main() {\n    for (int i = 1; i <= 5; i++) {\n        if (i == 3) continue;\n        printf("%d\\n", i);\n    }\n    return 0;\n}'
    if "função" in chave or "parâmetro" in chave or "retorno" in chave or "protótipo" in chave:
        return '#include <stdio.h>\n\nint dobro(int n) {\n    return n * 2;\n}\n\nint main() {\n    printf("%d\\n", dobro(5));\n    return 0;\n}'
    if "recurs" in chave:
        return '#include <stdio.h>\n\nint fatorial(int n) {\n    if (n <= 1) return 1;\n    return n * fatorial(n - 1);\n}\n\nint main() {\n    printf("%d\\n", fatorial(5));\n    return 0;\n}'
    if "array" in chave or "vetor" in chave or "matriz" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int valores[3] = {10, 20, 30};\n    for (int i = 0; i < 3; i++) {\n        printf("%d\\n", valores[i]);\n    }\n    return 0;\n}'
    if "string" in chave or "strlen" in chave or "strcpy" in chave or "strcmp" in chave or "strcat" in chave or "fgets" in chave:
        return '#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char palavra[] = "codigo";\n    printf("Tamanho: %zu\\n", strlen(palavra));\n    return 0;\n}'
    if "ponteiro" in chave or "memória" in chave or "operador &" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int valor = 10;\n    int *p = &valor;\n    printf("%d\\n", *p);\n    return 0;\n}'
    if "malloc" in chave or "calloc" in chave or "realloc" in chave or "free" in chave or "memory leak" in chave:
        return '#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    int *numero = malloc(sizeof(int));\n    *numero = 30;\n    printf("%d\\n", *numero);\n    free(numero);\n    return 0;\n}'
    if "struct" in chave or "typedef" in chave:
        return '#include <stdio.h>\n\ntypedef struct {\n    char nome[30];\n    int idade;\n} Pessoa;\n\nint main() {\n    Pessoa pessoa = {"Ana", 20};\n    printf("%s %d\\n", pessoa.nome, pessoa.idade);\n    return 0;\n}'
    if "union" in chave:
        return '#include <stdio.h>\n\nunion Valor {\n    int inteiro;\n    float decimal;\n};\n\nint main() {\n    union Valor v;\n    v.inteiro = 10;\n    printf("%d\\n", v.inteiro);\n    return 0;\n}'
    if "enum" in chave:
        return '#include <stdio.h>\n\nenum Status {ABERTO, FECHADO};\n\nint main() {\n    enum Status atual = ABERTO;\n    printf("%d\\n", atual);\n    return 0;\n}'
    if "fopen" in chave or "fclose" in chave or "fprintf" in chave or "fscanf" in chave or "arquivo" in chave:
        return '#include <stdio.h>\n\nint main() {\n    FILE *arquivo = fopen("saida.txt", "w");\n    fprintf(arquivo, "Curso de C");\n    fclose(arquivo);\n    printf("Arquivo gravado\\n");\n    return 0;\n}'
    if "math" in chave:
        return '#include <stdio.h>\n#include <math.h>\n\nint main() {\n    printf("%.0f\\n", sqrt(25));\n    return 0;\n}'
    if "bit" in chave or "máscara" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int permissoes = 6;\n    int leitura = 2;\n    printf("%d\\n", permissoes & leitura);\n    return 0;\n}'
    if "busca" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int valores[4] = {4, 8, 15, 16};\n    int alvo = 15;\n    for (int i = 0; i < 4; i++) {\n        if (valores[i] == alvo) printf("Encontrado\\n");\n    }\n    return 0;\n}'
    if "bubble" in chave or "sort" in chave:
        return '#include <stdio.h>\n\nint main() {\n    int v[3] = {3, 1, 2};\n    for (int i = 0; i < 2; i++) {\n        for (int j = 0; j < 2 - i; j++) {\n            if (v[j] > v[j + 1]) {\n                int temp = v[j];\n                v[j] = v[j + 1];\n                v[j + 1] = temp;\n            }\n        }\n    }\n    printf("%d %d %d\\n", v[0], v[1], v[2]);\n    return 0;\n}'

    return f'#include <stdio.h>\n\nint main() {{\n    printf("Estudo de {conteudo} em C\\\\n");\n    return 0;\n}}'


def regra_correcao_para_conteudo(conteudo):
    chave = conteudo.lower()
    termos = ["printf"]

    if "scanf" in chave:
        termos = ["scanf", "&", "printf"]
    elif any(item in chave for item in ["if", "else", "ternário"]):
        termos = ["if", "printf"]
    elif "switch" in chave:
        termos = ["switch", "case", "printf"]
    elif "while" in chave:
        termos = ["while", "printf"]
    elif "do while" in chave:
        termos = ["do", "while", "printf"]
    elif "for" in chave:
        termos = ["for", "printf"]
    elif "break" in chave:
        termos = ["break", "printf"]
    elif "continue" in chave:
        termos = ["continue", "printf"]
    elif "função" in chave or "parâmetro" in chave or "retorno" in chave or "protótipo" in chave:
        termos = ["(", ")", "return", "printf"]
    elif "recurs" in chave:
        termos = ["return", "printf"]
    elif any(item in chave for item in ["array", "matriz", "lista", "pilha", "fila", "árvore"]):
        termos = ["[", "]", "printf"]
    elif any(item in chave for item in ["string", "strlen", "strcpy", "strcmp", "strcat", "fgets"]):
        termos = ["char", "printf"]
    elif any(item in chave for item in ["ponteiro", "memória", "operador &"]):
        termos = ["*", "&", "printf"]
    elif any(item in chave for item in ["malloc", "calloc", "realloc", "free", "memory leak"]):
        termos = ["stdlib.h", "free", "printf"]
    elif any(item in chave for item in ["struct", "typedef"]):
        termos = ["struct", "printf"]
    elif "union" in chave:
        termos = ["union", "printf"]
    elif "enum" in chave:
        termos = ["enum", "printf"]
    elif any(item in chave for item in ["fopen", "fclose", "fprintf", "fscanf"]):
        termos = ["FILE", "fopen", "fclose", "printf"]
    elif any(item in chave for item in ["bitwise", "máscara"]):
        termos = ["&", "printf"]

    return {"codigo_contem": termos, "saida_obrigatoria": True}


def criar_alternativas(conteudos_modulo, resposta):
    alternativas = [resposta]
    for item in conteudos_modulo:
        if item != resposta and item not in alternativas:
            alternativas.append(item)
        if len(alternativas) == 4:
            break

    for item in ["printf", "scanf", "main", "for", "struct"]:
        if len(alternativas) == 4:
            break
        if item not in alternativas:
            alternativas.append(item)

    return alternativas[:4]


def gerar_trilha_completa_c():
    licoes = []
    proximo_id = 1
    trilha = []

    for modulo in TRILHA_COMPLETA_C:
        modulo_licoes = []
        topicos = "; ".join(modulo["topicos"])

        for conteudo in modulo["conteudos"]:
            codigo = codigo_exemplo_para_conteudo(conteudo)
            modulo_licoes.append({
                "id": proximo_id,
                "titulo": conteudo,
                "conteudo": (
                    f"{conteudo} faz parte do módulo {modulo['titulo']}. "
                    f"Nesta lição você estuda: {topicos}."
                ),
                "codigo": codigo,
                "pergunta": f"Qual conteúdo é o foco desta lição do módulo {modulo['titulo']}?",
                "alternativas": criar_alternativas(modulo["conteudos"], conteudo),
                "resposta": conteudo,
                "exercicio_codigo": f"Faça um programa em C que demonstre {conteudo} e mostre uma saída no terminal.",
                "codigo_minimo": codigo,
                "correcao": regra_correcao_para_conteudo(conteudo)
            })
            proximo_id += 1

        trilha.append({
            "id": modulo["id"],
            "titulo": modulo["titulo"],
            "descricao": modulo["descricao"],
            "icone": modulo["icone"],
            "licoes": modulo_licoes
        })

    return trilha


MODULOS = gerar_trilha_completa_c()


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
            codigo_validado INTEGER DEFAULT 0,
            feedback_codigo TEXT,
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
            desafio_id TEXT,
            codigo_usuario TEXT,
            saida_codigo TEXT,
            entrada_codigo TEXT,
            codigo_validado INTEGER DEFAULT 0,
            feedback_codigo TEXT,
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS backups_progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            caminho TEXT,
            dados_json TEXT,
            criado_em TEXT
        )
    """)

    # Migração para bancos antigos já criados antes das novas funções.
    adicionar_coluna(conn, "progresso", "quiz_correto", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "progresso", "codigo_enviado", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "progresso", "codigo_usuario", "TEXT")
    adicionar_coluna(conn, "progresso", "saida_codigo", "TEXT")
    adicionar_coluna(conn, "progresso", "entrada_codigo", "TEXT")
    adicionar_coluna(conn, "progresso", "codigo_validado", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "progresso", "feedback_codigo", "TEXT")
    adicionar_coluna(conn, "progresso", "atualizado_em", "TEXT")

    adicionar_coluna(conn, "usuarios", "xp", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "usuarios", "nivel", "INTEGER DEFAULT 1")
    adicionar_coluna(conn, "usuarios", "sequencia", "INTEGER DEFAULT 1")
    adicionar_coluna(conn, "usuarios", "ultimo_acesso", "TEXT")
    adicionar_coluna(conn, "desafios_diarios", "desafio_id", "TEXT")
    adicionar_coluna(conn, "desafios_diarios", "entrada_codigo", "TEXT")
    adicionar_coluna(conn, "desafios_diarios", "codigo_validado", "INTEGER DEFAULT 0")
    adicionar_coluna(conn, "desafios_diarios", "feedback_codigo", "TEXT")

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


def desafio_por_id(desafio_id):
    return next((desafio for desafio in DESAFIOS_DIARIOS if desafio["id"] == desafio_id), DESAFIOS_DIARIOS[0])


def desafio_do_dia(data_texto=None):
    data_base = date.fromisoformat(data_texto) if data_texto else date.today()
    indice = data_base.toordinal() % len(DESAFIOS_DIARIOS)
    return DESAFIOS_DIARIOS[indice]


def linhas_para_dicts(linhas):
    return [dict(linha) for linha in linhas]


def criar_backup_progresso(usuario_id):
    try:
        conn = conectar()
        usuario = conn.execute(
            "SELECT id, nome, email, xp, nivel, sequencia, ultimo_acesso FROM usuarios WHERE id = ?",
            (usuario_id,)
        ).fetchone()

        if not usuario:
            conn.close()
            return None

        dados = {
            "gerado_em": datetime.now().isoformat(timespec="seconds"),
            "usuario": dict(usuario),
            "progresso": linhas_para_dicts(conn.execute(
                "SELECT * FROM progresso WHERE usuario_id = ? ORDER BY modulo_id, licao_id",
                (usuario_id,)
            ).fetchall()),
            "desafios_diarios": linhas_para_dicts(conn.execute(
                "SELECT * FROM desafios_diarios WHERE usuario_id = ? ORDER BY data DESC",
                (usuario_id,)
            ).fetchall()),
            "conquistas": linhas_para_dicts(conn.execute(
                "SELECT * FROM conquistas_usuario WHERE usuario_id = ? ORDER BY id",
                (usuario_id,)
            ).fetchall())
        }

        pasta_backup = os.path.join(os.path.dirname(DB_PATH) or ".", "backups")
        os.makedirs(pasta_backup, exist_ok=True)
        caminho = os.path.join(pasta_backup, f"progresso_usuario_{usuario_id}.json")

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

        dados_json = json.dumps(dados, ensure_ascii=False)
        conn.execute(
            "INSERT INTO backups_progresso (usuario_id, caminho, dados_json, criado_em) VALUES (?, ?, ?, ?)",
            (usuario_id, caminho, dados_json, dados["gerado_em"])
        )
        conn.commit()
        conn.close()
        return {"caminho": caminho, "criado_em": dados["gerado_em"]}
    except Exception:
        return None


def backup_mais_recente(usuario_id):
    conn = conectar()
    backup = conn.execute(
        "SELECT * FROM backups_progresso WHERE usuario_id = ? ORDER BY id DESC LIMIT 1",
        (usuario_id,)
    ).fetchone()
    conn.close()
    return backup


def montar_terminal_unificado(saida, entrada="", codigo_retorno=0):
    saida_final = saida or "Programa executado sem saída na tela."
    if "Process returned" not in saida_final:
        saida_final = saida_final.rstrip() + f"\n\nProcess returned {codigo_retorno}."
    return saida_final


def detectar_prompt_entrada(codigo):
    achou = re.search(r'printf\s*\(\s*"([^"]*)"\s*\)\s*;\s*scanf', codigo or "", re.S)
    if achou:
        return achou.group(1).replace("\\n", "\n").replace("\\t", "\t")
    if "scanf" in (codigo or ""):
        return "Entrada:"
    return ""



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
        "saida": montar_terminal_unificado(saida, entrada, run_out.get("code", 0)),
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


def normalizar_texto(texto):
    texto = (texto or "").lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(char for char in texto if unicodedata.category(char) != "Mn")
    return texto


def limpar_saida_para_correcao(saida):
    linhas = []
    for linha in (saida or "").splitlines():
        normalizada = normalizar_texto(linha).strip()
        if normalizada.startswith("process returned"):
            continue
        if normalizada.startswith("press any key"):
            continue
        if normalizada.startswith("origem:"):
            continue
        linhas.append(linha)
    return "\n".join(linhas).strip()


def validar_regras_estaticas(codigo, regra):
    falhas = []
    codigo_normalizado = normalizar_texto(codigo)

    for termo in regra.get("codigo_contem", []):
        if normalizar_texto(termo) not in codigo_normalizado:
            falhas.append(f"O código precisa usar: {termo}.")

    for termo in regra.get("codigo_nao_contem", []):
        if normalizar_texto(termo) in codigo_normalizado:
            falhas.append(f"Remova o uso de: {termo}.")

    for termo, minimo in regra.get("min_ocorrencias_codigo", {}).items():
        if codigo_normalizado.count(normalizar_texto(termo)) < minimo:
            falhas.append(f"Use {termo} pelo menos {minimo} vezes.")

    return falhas


def validar_saida(saida, regra):
    falhas = []
    saida_limpa = limpar_saida_para_correcao(saida)
    saida_normalizada = normalizar_texto(saida_limpa)

    if regra.get("saida_obrigatoria") and not saida_limpa:
        falhas.append("O programa precisa mostrar alguma saída na tela.")

    for termo in regra.get("saida_contem", []):
        if normalizar_texto(termo) not in saida_normalizada:
            falhas.append(f"A saída precisa conter: {termo}.")

    for expressao in regra.get("saida_regex", []):
        if not re.search(expressao, saida_normalizada, re.I):
            falhas.append("A saída ainda não bate com o resultado esperado.")

    minimo_linhas = regra.get("min_linhas_saida")
    if minimo_linhas:
        linhas = [linha for linha in saida_limpa.splitlines() if linha.strip()]
        if len(linhas) < minimo_linhas:
            falhas.append(f"A saída precisa ter pelo menos {minimo_linhas} linhas.")

    return falhas


def avaliar_codigo_automaticamente(codigo, resultado_execucao, regra):
    if not resultado_execucao.get("ok", False):
        return {
            "ok": False,
            "mensagem": "Corrija os erros de compilação ou execução antes de concluir."
        }

    regra = regra or {"saida_obrigatoria": True}
    falhas = validar_regras_estaticas(codigo, regra)

    testes = regra.get("testes", [])
    if testes:
        for indice, teste in enumerate(testes, start=1):
            resultado_teste = executar_compilador_online(codigo, teste.get("entrada", ""))
            if not resultado_teste.get("ok", False):
                falhas.append(f"O teste automático {indice} não executou corretamente.")
                continue

            regra_saida_teste = {
                "saida_contem": teste.get("saida_contem", []),
                "saida_regex": teste.get("saida_regex", []),
                "saida_obrigatoria": True
            }
            falhas.extend(validar_saida(resultado_teste.get("saida", ""), regra_saida_teste))
    else:
        falhas.extend(validar_saida(resultado_execucao.get("saida", ""), regra))

    if falhas:
        return {
            "ok": False,
            "mensagem": " ".join(falhas[:3])
        }

    return {
        "ok": True,
        "mensagem": "Correção automática aprovada. Você pode concluir."
    }


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
                saida = f"Process returned {execucao.returncode}.\nO programa executou, mas não mostrou nenhuma saída."

            return {
                "ok": execucao.returncode == 0,
                "build": "Build finished successfully.\n0 errors, 0 warnings.",
                "saida": saida + f"\n\nProcess returned {execucao.returncode}."
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
        novo_usuario_id = cur.lastrowid

        conn.close()
        criar_backup_progresso(novo_usuario_id)
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
    backup_recente = conn.execute(
        "SELECT * FROM backups_progresso WHERE usuario_id = ? ORDER BY id DESC LIMIT 1",
        (usuario["id"],)
    ).fetchone()
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
        ranking=ranking,
        backup_recente=backup_recente
    )


@app.route("/backup-progresso")
def baixar_backup_progresso():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    backup = criar_backup_progresso(usuario["id"])
    if not backup or not os.path.exists(backup["caminho"]):
        return render_template("erro.html", mensagem="Não foi possível gerar o backup agora.")

    nome_arquivo = f"backup_progresso_{usuario['id']}_{date.today()}.json"
    return send_file(backup["caminho"], as_attachment=True, download_name=nome_arquivo)


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
    quiz_correto = registro_licao["quiz_correto"] if registro_licao and "quiz_correto" in registro_licao.keys() else 0

    return render_template(
        "estudar.html",
        modulo=modulo,
        licao=licao,
        concluidas_ids=concluidas_ids,
        codigo_salvo=codigo_salvo,
        saida_salva=saida_salva,
        resposta_teorica="",
        quiz_correto=quiz_correto
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
    codigo_validado = registro["codigo_validado"] if registro and "codigo_validado" in registro.keys() else 0
    feedback_codigo = registro["feedback_codigo"] if registro and "feedback_codigo" in registro.keys() and registro["feedback_codigo"] else ""
    return render_template(
        "exercicio.html",
        modulo=modulo,
        licao=licao,
        codigo_salvo=codigo_salvo,
        saida_salva=saida_salva,
        entrada_salva=entrada_salva,
        codigo_validado=codigo_validado,
        feedback_codigo=feedback_codigo
    )




@app.route("/api/exercicio/preparar-terminal", methods=["POST"])
def api_exercicio_preparar_terminal():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "build": "Usuário não logado.", "prompt": ""}), 401

    dados = request.get_json()
    codigo = dados.get("codigo", "")

    resultado_build = compilar_codigo_c(codigo)
    prompt = detectar_prompt_entrada(codigo)

    return jsonify({
        "ok": resultado_build.get("ok", False),
        "build": resultado_build.get("build", ""),
        "prompt": prompt
    })


@app.route("/api/exercicio/compilar", methods=["POST"])
def api_exercicio_compilar():
    usuario = usuario_logado()
    if not usuario:
        return jsonify({"ok": False, "build": "Usuário não logado.", "saida": ""}), 401

    dados = request.get_json()
    licao_id = int(dados.get("licao_id"))
    codigo = dados.get("codigo", "")
    entrada = dados.get("entrada", "")

    modulo, licao = encontrar_licao(licao_id)
    if not licao:
        return jsonify({"ok": False, "build": "Lição não encontrada.", "saida": ""}), 404

    resultado = executar_compilador_online(codigo, entrada)
    validacao = avaliar_codigo_automaticamente(codigo, resultado, licao.get("correcao"))
    resultado["correcao"] = validacao
    resultado["codigo_validado"] = 1 if validacao["ok"] else 0

    conn = conectar()
    conn.execute(
        """
        INSERT INTO progresso (usuario_id, licao_id, modulo_id, codigo_usuario, saida_codigo, entrada_codigo, codigo_enviado, codigo_validado, feedback_codigo, atualizado_em)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
        ON CONFLICT(usuario_id, licao_id)
        DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                      saida_codigo = excluded.saida_codigo,
                      entrada_codigo = excluded.entrada_codigo,
                      codigo_enviado = 1,
                      codigo_validado = excluded.codigo_validado,
                      feedback_codigo = excluded.feedback_codigo,
                      atualizado_em = excluded.atualizado_em
        """,
        (usuario["id"], licao_id, modulo["id"], codigo, resultado.get("saida", ""), entrada, resultado["codigo_validado"], validacao["mensagem"], str(date.today()))
    )
    conn.commit()
    conn.close()
    criar_backup_progresso(usuario["id"])

    return jsonify(resultado)


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

    desafio = desafio_por_id(registro["desafio_id"]) if registro and "desafio_id" in registro.keys() and registro["desafio_id"] else desafio_do_dia(hoje)
    codigo = registro["codigo_usuario"] if registro and registro["codigo_usuario"] else desafio["codigo_inicial"]
    saida = registro["saida_codigo"] if registro and registro["saida_codigo"] else "A saída do desafio aparecerá aqui."
    entrada = registro["entrada_codigo"] if registro and "entrada_codigo" in registro.keys() and registro["entrada_codigo"] else ""
    concluido = registro["concluido"] if registro else 0
    codigo_validado = registro["codigo_validado"] if registro and "codigo_validado" in registro.keys() else 0
    feedback_codigo = registro["feedback_codigo"] if registro and "feedback_codigo" in registro.keys() and registro["feedback_codigo"] else ""
    return render_template(
        "desafio_diario.html",
        desafio=desafio,
        codigo=codigo,
        saida=saida,
        entrada=entrada,
        concluido=concluido,
        codigo_validado=codigo_validado,
        feedback_codigo=feedback_codigo
    )


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
            criar_backup_progresso(usuario_logado()["id"])
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

    resultado = executar_compilador_online(codigo, entrada)

    if tipo == "licao" and licao_id:
        modulo, licao = encontrar_licao(int(licao_id))
        if modulo:
            validacao = avaliar_codigo_automaticamente(codigo, resultado, licao.get("correcao"))
            resultado["correcao"] = validacao
            resultado["codigo_validado"] = 1 if validacao["ok"] else 0
            try:
                conn = conectar()
                conn.execute(
                    """
                    INSERT INTO progresso (usuario_id, licao_id, modulo_id, codigo_usuario, saida_codigo, entrada_codigo, codigo_enviado, codigo_validado, feedback_codigo, atualizado_em)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
                    ON CONFLICT(usuario_id, licao_id)
                    DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                                  saida_codigo = excluded.saida_codigo,
                                  entrada_codigo = excluded.entrada_codigo,
                                  codigo_enviado = 1,
                                  codigo_validado = excluded.codigo_validado,
                                  feedback_codigo = excluded.feedback_codigo,
                                  atualizado_em = excluded.atualizado_em
                    """,
                    (usuario["id"], int(licao_id), modulo["id"], codigo, resultado["saida"], entrada, resultado["codigo_validado"], validacao["mensagem"], str(date.today()))
                )
                conn.commit()
                conn.close()
                criar_backup_progresso(usuario["id"])
            except Exception as erro:
                return jsonify({
                    "ok": False,
                    "saida": f"Erro ao salvar código no banco: {erro}"
                }), 500

    if tipo == "diario":
        hoje = str(date.today())
        desafio = desafio_do_dia(hoje)
        validacao = avaliar_codigo_automaticamente(codigo, resultado, desafio.get("correcao"))
        resultado["correcao"] = validacao
        resultado["codigo_validado"] = 1 if validacao["ok"] else 0
        conn = conectar()
        conn.execute(
            """
            INSERT INTO desafios_diarios (usuario_id, data, desafio_id, codigo_usuario, saida_codigo, entrada_codigo, codigo_validado, feedback_codigo, concluido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(usuario_id, data)
            DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                          saida_codigo = excluded.saida_codigo,
                          entrada_codigo = excluded.entrada_codigo,
                          desafio_id = excluded.desafio_id,
                          codigo_validado = excluded.codigo_validado,
                          feedback_codigo = excluded.feedback_codigo
            """,
            (usuario["id"], hoje, desafio["id"], codigo, resultado["saida"], entrada, resultado["codigo_validado"], validacao["mensagem"])
        )
        conn.commit()
        conn.close()
        criar_backup_progresso(usuario["id"])

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

    if "codigo_validado" in registro.keys() and registro["codigo_validado"] != 1:
        mensagem = registro["feedback_codigo"] or "Execute o código e passe na correção automática antes de concluir."
        conn.close()
        return jsonify({"ok": False, "mensagem": mensagem})

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
    criar_backup_progresso(usuario["id"])

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

    if "codigo_validado" in registro.keys() and registro["codigo_validado"] != 1:
        mensagem = registro["feedback_codigo"] or "Passe na correção automática antes de concluir o desafio diário."
        conn.close()
        return jsonify({"ok": False, "mensagem": mensagem})

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
    criar_backup_progresso(usuario["id"])

    return jsonify({"ok": True, "mensagem": "Desafio diário concluído! +30 XP"})



# -------------------------------
# COMPILADOR REAL INTERATIVO
# -------------------------------

PROCESSOS_TERMINAL = {}


def salvar_codigo_execucao(usuario_id, licao_id, codigo, entrada, saida):
    modulo, licao = encontrar_licao(int(licao_id))
    if not modulo:
        return {"ok": False, "mensagem": "Lição não encontrada."}

    validacao = avaliar_codigo_automaticamente(
        codigo,
        {"ok": True, "saida": saida, "build": "Build finished successfully."},
        licao.get("correcao")
    )

    conn = conectar()
    conn.execute(
        """
        INSERT INTO progresso (usuario_id, licao_id, modulo_id, codigo_usuario, saida_codigo, entrada_codigo, codigo_enviado, codigo_validado, feedback_codigo, atualizado_em)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
        ON CONFLICT(usuario_id, licao_id)
        DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                      saida_codigo = excluded.saida_codigo,
                      entrada_codigo = excluded.entrada_codigo,
                      codigo_enviado = 1,
                      codigo_validado = excluded.codigo_validado,
                      feedback_codigo = excluded.feedback_codigo,
                      atualizado_em = excluded.atualizado_em
        """,
        (usuario_id, int(licao_id), modulo["id"], codigo, saida, entrada, 1 if validacao["ok"] else 0, validacao["mensagem"], str(date.today()))
    )
    conn.commit()
    conn.close()
    criar_backup_progresso(usuario_id)
    return validacao


def salvar_desafio_diario_execucao(usuario_id, codigo, entrada, saida):
    hoje = str(date.today())
    desafio = desafio_do_dia(hoje)
    validacao = avaliar_codigo_automaticamente(
        codigo,
        {"ok": True, "saida": saida, "build": "Build finished successfully."},
        desafio.get("correcao")
    )

    conn = conectar()
    conn.execute(
        """
        INSERT INTO desafios_diarios (usuario_id, data, desafio_id, codigo_usuario, saida_codigo, entrada_codigo, codigo_validado, feedback_codigo, concluido)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        ON CONFLICT(usuario_id, data)
        DO UPDATE SET desafio_id = excluded.desafio_id,
                      codigo_usuario = excluded.codigo_usuario,
                      saida_codigo = excluded.saida_codigo,
                      entrada_codigo = excluded.entrada_codigo,
                      codigo_validado = excluded.codigo_validado,
                      feedback_codigo = excluded.feedback_codigo
        """,
        (usuario_id, hoje, desafio["id"], codigo, saida, entrada, 1 if validacao["ok"] else 0, validacao["mensagem"])
    )
    conn.commit()
    conn.close()
    criar_backup_progresso(usuario_id)
    return validacao


def encerrar_processo_socket(sid):
    dados = PROCESSOS_TERMINAL.pop(sid, None)
    if not dados:
        return

    proc = dados.get("proc")
    fd = dados.get("fd")
    temp_dir = dados.get("temp_dir")

    try:
        if proc and proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except Exception:
        pass

    try:
        if fd:
            os.close(fd)
    except Exception:
        pass

    try:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass


def leitor_terminal(sid):
    dados = PROCESSOS_TERMINAL.get(sid)
    if not dados:
        return

    proc = dados["proc"]
    fd = dados["fd"]
    saida_total = ""

    inicio = time.time()
    limite_segundos = 20

    while True:
        if time.time() - inicio > limite_segundos:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception:
                pass
            socketio.emit("terminal_saida", {"texto": "\n\nTempo limite excedido.\n"}, to=sid)
            break

        if proc.poll() is not None:
            break

        try:
            pronto, _, _ = select.select([fd], [], [], 0.2)
            if fd in pronto:
                dados_lidos = os.read(fd, 4096)
                if not dados_lidos:
                    break

                texto = dados_lidos.decode("utf-8", errors="replace")
                saida_total += texto
                socketio.emit("terminal_saida", {"texto": texto}, to=sid)
        except OSError:
            break
        except Exception as erro:
            socketio.emit("terminal_saida", {"texto": f"\nErro no terminal: {erro}\n"}, to=sid)
            break

    codigo_saida = proc.poll()
    if codigo_saida is None:
        codigo_saida = proc.wait()

    fim = "\n\nProcess returned 0 (0x0)\nPress any key to continue.\n" if codigo_saida == 0 else f"\n\nProcess returned {codigo_saida}\nPress any key to continue.\n"
    saida_total += fim
    socketio.emit("terminal_saida", {"texto": fim}, to=sid)
    socketio.emit("terminal_finalizado", {"codigo": codigo_saida}, to=sid)

    usuario_id = dados.get("usuario_id")
    licao_id = dados.get("licao_id")
    tipo = dados.get("tipo", "licao")
    codigo = dados.get("codigo", "")
    entrada = dados.get("entrada", "")

    validacao = None
    if usuario_id and tipo == "diario":
        validacao = salvar_desafio_diario_execucao(usuario_id, codigo, entrada, saida_total)
    elif usuario_id and licao_id:
        validacao = salvar_codigo_execucao(usuario_id, licao_id, codigo, entrada, saida_total)

    if validacao:
        socketio.emit("correcao_resultado", validacao, to=sid)

    encerrar_processo_socket(sid)


@socketio.on("compilar_real")
def compilar_real(dados):
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        emit("build_log", {"ok": False, "texto": "Usuário não logado."})
        return

    sid = request.sid
    encerrar_processo_socket(sid)

    codigo = dados.get("codigo", "")
    licao_id = dados.get("licao_id")
    tipo = dados.get("tipo", "licao")

    temp_dir = tempfile.mkdtemp(prefix="ensinar_c_")
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
            shutil.rmtree(temp_dir, ignore_errors=True)
            emit("build_log", {
                "ok": False,
                "texto": "Build failed.\n\n" + compilacao.stderr
            })
            return

        if pty is None or os.name == "nt":
            shutil.rmtree(temp_dir, ignore_errors=True)
            emit("build_log", {
                "ok": False,
                "texto": "Terminal interativo real disponível no ambiente Linux/Docker. Para Windows local, use o Dockerfile do projeto ou publique no Render."
            })
            return

        emit("build_log", {
            "ok": True,
            "texto": "Build finished successfully.\n0 errors, 0 warnings."
        })

        master_fd, slave_fd = pty.openpty()

        proc = subprocess.Popen(
            [arquivo_saida],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            text=False,
            close_fds=True,
            preexec_fn=os.setsid
        )

        os.close(slave_fd)

        PROCESSOS_TERMINAL[sid] = {
            "proc": proc,
            "fd": master_fd,
            "temp_dir": temp_dir,
            "usuario_id": usuario_id,
            "licao_id": licao_id,
            "tipo": tipo,
            "codigo": codigo,
            "entrada": ""
        }

        socketio.start_background_task(leitor_terminal, sid)

    except FileNotFoundError:
        shutil.rmtree(temp_dir, ignore_errors=True)
        emit("build_log", {
            "ok": False,
            "texto": "GCC não está instalado no servidor. Use o Dockerfile desta versão para publicar com GCC."
        })
    except subprocess.TimeoutExpired:
        shutil.rmtree(temp_dir, ignore_errors=True)
        emit("build_log", {
            "ok": False,
            "texto": "Tempo de compilação excedido."
        })
    except Exception as erro:
        shutil.rmtree(temp_dir, ignore_errors=True)
        emit("build_log", {
            "ok": False,
            "texto": f"Erro ao compilar: {erro}"
        })


@socketio.on("terminal_entrada")
def terminal_entrada(dados):
    sid = request.sid
    texto = dados.get("texto", "")

    proc_data = PROCESSOS_TERMINAL.get(sid)
    if not proc_data:
        return

    proc_data["entrada"] += texto

    try:
        os.write(proc_data["fd"], texto.encode("utf-8"))
    except Exception:
        pass


@socketio.on("disconnect")
def desconectar_terminal():
    encerrar_processo_socket(request.sid)


# Importante para Render/Gunicorn: cria o banco ao importar o app.
iniciar_banco()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
