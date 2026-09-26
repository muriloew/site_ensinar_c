"""Exercícios de código de cada lição: lições só teóricas, versões simplificadas e testes ocultos."""

# O módulo 1 é conceitual: o aluno responde os desafios teóricos e ainda não programa.
LICOES_SO_TEORIA = {
    "O que é C": "Esta lição é apenas para entender a ideia geral da linguagem C. Responda o desafio teórico para avançar.",
    "Estrutura básica": "Nesta etapa, observe a estrutura de um programa pronto. A prática de escrita começa depois que a saída de dados for ensinada.",
    "Comentários": "Comentários servem para leitura do código. Por enquanto, responda o desafio teórico e avance.",
    "Compilação": "Esta lição explica o caminho do código até virar programa. A prática de compilação aparece novamente mais adiante.",
}

# Nas primeiras lições práticas o aluno ainda não conhece todos os tipos e operadores,
# então o exercício pedido é mais curto que o desafio completo do plano da lição.
EXERCICIOS_INICIANTES = {
    "printf": {
        "exercicio_codigo": 'Mostre exatamente a mensagem "Ola, C" usando printf.',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Use printf para mostrar a mensagem pedida. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["printf"], "saida_contem": ["Ola, C"]},
    },
    "scanf": {
        "exercicio_codigo": 'Leia um número inteiro digitado pelo usuário e mostre no formato "Numero: N".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    int numero;\n    /* Use scanf e depois mostre o valor lido. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["scanf", "&numero", "printf"], "testes": [{"entrada": "42\n", "saida_contem": ["Numero: 42"]}]},
    },
    "int": {
        "exercicio_codigo": 'Crie uma variável int chamada idade com valor 20 e mostre "Idade: 20".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Declare a variável idade aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["int", "idade", "printf"], "saida_contem": ["Idade: 20"]},
    },
    "float e double": {
        "exercicio_codigo": 'Crie uma variável double chamada nota com valor 9.5 e mostre "Nota: 9.5".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Declare a variável nota aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["double", "nota", "printf"], "saida_contem": ["Nota: 9.5"]},
    },
    "char": {
        "exercicio_codigo": 'Crie uma variável char chamada letra com valor C e mostre "Letra: C".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Declare a variável letra aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["char", "letra", "'C'", "printf"], "saida_contem": ["Letra: C"]},
    },
    "constantes": {
        "exercicio_codigo": 'Crie uma constante int chamada ANO com valor 2026 e mostre "Ano: 2026".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Declare a constante ANO aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["const int", "ANO", "printf"], "saida_contem": ["Ano: 2026"]},
    },
    "#define": {
        "exercicio_codigo": 'Crie um #define chamado ESCOLA com o texto "Ensinar C" e mostre esse texto.',
        "codigo_minimo": '#include <stdio.h>\n\n/* Crie o #define aqui. */\n\nint main(void) {\n    return 0;\n}',
        "correcao": {"codigo_contem": ["#define", "ESCOLA", "printf"], "saida_contem": ["Ensinar C"]},
    },
    "escopo": {
        "exercicio_codigo": 'Crie uma variável local chamada valor dentro da função main e mostre "Valor: 30".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Crie a variável valor aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["int valor", "printf"], "saida_contem": ["Valor: 30"]},
    },
    "divisão": {
        "exercicio_codigo": 'Divida 10.0 por 4.0 e mostre o resultado com duas casas decimais.',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Calcule a divisão aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["/", "%.2f", "printf"], "saida_contem": ["2.50"]},
    },
    "operadores lógicos": {
        "exercicio_codigo": 'Use && em uma expressão verdadeira e mostre "Resultado: 1".',
        "codigo_minimo": '#include <stdio.h>\n\nint main(void) {\n    /* Crie a expressão lógica aqui. */\n    return 0;\n}',
        "correcao": {"codigo_contem": ["&&", "printf"], "saida_contem": ["Resultado: 1"]},
    },
}

# Casos extras rodados na correção automática; impedem que o aluno escreva a saída "decorada".
TESTES_OCULTOS = {
    "scanf": [
        {"entrada": "7\n", "saida_contem": ["Numero: 7"]},
    ],
    "if": [
        {
            "entrada": "-3\n",
            "saida_obrigatoria": False,
            "saida_nao_contem": ["Positivo"],
        },
    ],
    "else": [
        {"entrada": "18\n", "saida_contem": ["Maior de idade"]},
    ],
    "else if": [
        {"entrada": "9\n", "saida_regex": [r"\bA\b"]},
        {"entrada": "5\n", "saida_regex": [r"\bC\b"]},
    ],
    "switch": [
        {"entrada": "1\n", "saida_contem": ["Cadastrar"]},
        {"entrada": "3\n", "saida_contem": ["Sair"]},
        {"entrada": "9\n", "saida_contem": ["invalida"]},
    ],
    "fgets": [
        {"entrada": "Joao da Silva\n", "saida_contem": ["Ola, Joao da Silva"]},
    ],
    "stdio": [
        {"entrada": "-4\n", "saida_contem": ["-8"]},
    ],
    "buffer overflow": [
        {"entrada": "123456789abcdef\n", "saida_contem": ["123456789"]},
    ],
    "validação": [
        {"entrada": "150\n", "saida_contem": ["Entrada invalida"]},
        {"entrada": "-1\n", "saida_contem": ["Entrada invalida"]},
    ],
    "calculadora": [
        {"entrada": "10 - 3\n", "saida_contem": ["Resultado: 7.00"]},
    ],
    "cadastro": [
        {"entrada": "Bia 18\n", "saida_contem": ["Bia tem 18 anos"]},
    ],
    "jogo terminal": [
        {"entrada": "42\n", "saida_contem": ["Acertou"]},
    ],
    "projeto final": [
        {"entrada": "6 6 9\n", "saida_contem": ["Media: 7.00"]},
    ],
}


def regra_correcao(conteudo, plano):
    simplificado = EXERCICIOS_INICIANTES.get(conteudo)
    regra = dict(simplificado["correcao"] if simplificado else plano["correcao"])
    testes = [dict(teste) for teste in regra.get("testes", [])]
    testes += [dict(teste) for teste in TESTES_OCULTOS.get(conteudo, [])]
    if testes:
        regra["testes"] = testes
    return regra


def codigo_inicial(conteudo):
    simplificado = EXERCICIOS_INICIANTES.get(conteudo)
    if simplificado:
        return simplificado["codigo_minimo"]

    chave = conteudo.lower()
    cabecalhos = ["#include <stdio.h>"]
    if any(item in chave for item in ["string", "strlen", "strcpy", "strcmp", "strcat", "fgets", "agenda", "editor texto"]):
        cabecalhos.append("#include <string.h>")
    if any(item in chave for item in ["malloc", "calloc", "realloc", "free", "memory leak", "stdlib", "listas"]):
        cabecalhos.append("#include <stdlib.h>")
    if chave == "math":
        cabecalhos.append("#include <math.h>")

    return (
        "\n".join(cabecalhos)
        + "\n\nint main(void) {\n"
        + f"    /* TODO: resolva o desafio sobre {conteudo}. */\n"
        + "    return 0;\n"
        + "}"
    )


def montar_dicas(plano, regra):
    """Três dicas da mais geral à mais direta; o aluno vê uma nova a cada tentativa errada."""
    termos = regra.get("codigo_contem", [])
    recursos = (
        "O código precisa usar: " + ", ".join(termos) + "."
        if termos
        else "Releia o objetivo e confira se usou todos os comandos pedidos."
    )

    teste = (regra.get("testes") or [None])[0]
    esperado = (teste or regra).get("saida_contem", [])
    if teste and esperado:
        entrada = teste.get("entrada", "").strip()
        saida = f'Teste: digitando "{entrada}", a saída deve mostrar "{" / ".join(esperado)}".'
    elif esperado:
        saida = f'A saída deve mostrar exatamente: "{" / ".join(esperado)}".'
    else:
        saida = "Execute o programa e compare a saída, letra por letra, com o que o objetivo pede."

    return [f"Cuidado comum: {plano['cuidado']}", recursos, saida]


def enunciado_exercicio(conteudo, plano):
    if conteudo in LICOES_SO_TEORIA:
        return LICOES_SO_TEORIA[conteudo]
    simplificado = EXERCICIOS_INICIANTES.get(conteudo)
    return simplificado["exercicio_codigo"] if simplificado else plano["desafio"]
