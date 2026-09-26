"""Catálogo dos desafios diários: problemas próprios, diferentes dos exercícios das lições.

Cada módulo a partir do 2 tem cinco desafios que usam apenas o que já foi ensinado até ele.
Um desafio traz enunciado, exemplo, código inicial, dicas, correção com testes e solução comentada.
Os testes do projeto garantem que cada solução compila sem avisos e passa na própria correção,
e que o código inicial ainda não passa (ou seja, há algo a fazer).
"""

FACIL, MEDIO, DESAFIADOR = "Fácil", "Médio", "Desafiador"

CATALOGO = []


def _desafio(modulo, numero, titulo, nivel, licao, enunciado, inicial, dicas, correcao, solucao,
             explicacao, exemplo=None):
    CATALOGO.append({
        "modulo_id": modulo,
        "numero_no_modulo": numero,
        "titulo": titulo,
        "nivel": nivel,
        "licao_id": licao,
        "enunciado": enunciado,
        "exemplo": exemplo,
        "codigo_inicial": inicial.strip("\n"),
        "dicas": dicas,
        "correcao": {"saida_obrigatoria": True, **correcao},
        "solucao": {"codigo": solucao.strip("\n"), "explicacao": explicacao},
    })


def _teste(entrada, *contem, nao_contem=(), regex=()):
    return {
        "entrada": entrada,
        "saida_contem": list(contem),
        "saida_nao_contem": list(nao_contem),
        "saida_regex": list(regex),
    }


# ---------------------------------------------------------------------------
# Módulo 2 · Conversando com o usuário (printf e scanf)
# ---------------------------------------------------------------------------

_desafio(
    2, 1, "Cartão de apresentação", FACIL, 5,
    'Use printf para mostrar um cartão com três linhas: "Nome: Ana", "Linguagem: C" e '
    '"Nivel: iniciante". Cada informação deve ficar em sua própria linha.',
    r'''
#include <stdio.h>

int main(void) {
    printf("Nome: Ana\n");
    /* complete com as outras duas linhas */
    return 0;
}
''',
    [
        "Cada printf pode mostrar uma linha; termine o texto com \\n para pular para a próxima.",
        "Você pode usar três printf ou um único printf com três \\n.",
        'A correção procura exatamente "Linguagem: C" e "Nivel: iniciante" (sem acento).',
    ],
    {
        "codigo_contem": ["printf"],
        "saida_contem": ["Nome: Ana", "Linguagem: C", "Nivel: iniciante"],
        "min_linhas_saida": 3,
    },
    r'''
#include <stdio.h>

int main(void) {
    printf("Nome: Ana\n");
    printf("Linguagem: C\n");
    printf("Nivel: iniciante\n");
    return 0;
}
''',
    "Cada printf termina com \\n, então cada informação aparece em uma linha diferente.",
    exemplo=("", "Nome: Ana\nLinguagem: C\nNivel: iniciante"),
)

_desafio(
    2, 2, "Ordem invertida", FACIL, 6,
    "Leia dois números inteiros e mostre-os na ordem contrária, no formato "
    '"Invertido: SEGUNDO PRIMEIRO".',
    r'''
#include <stdio.h>

int main(void) {
    int primeiro, segundo;
    /* leia os dois números com scanf */
    /* mostre: Invertido: segundo primeiro */
    return 0;
}
''',
    [
        'Um único scanf("%d %d", ...) lê os dois números de uma vez.',
        "Lembre do & antes de cada variável no scanf.",
        "No printf, basta passar as variáveis na ordem inversa: segundo, depois primeiro.",
    ],
    {
        "codigo_contem": ["scanf", "printf"],
        "testes": [
            _teste("3 8\n", "Invertido: 8 3"),
            _teste("10 2\n", "Invertido: 2 10"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int primeiro, segundo;
    scanf("%d %d", &primeiro, &segundo);
    printf("Invertido: %d %d\n", segundo, primeiro);
    return 0;
}
''',
    "O scanf guarda os valores nas variáveis; a ordem de saída é decidida só pela ordem dos argumentos do printf.",
    exemplo=("3 8", "Invertido: 8 3"),
)

_desafio(
    2, 3, "Data com dois dígitos", MEDIO, 6,
    "Leia dia, mês e ano (três inteiros) e mostre a data no formato \"Data: DD/MM/AAAA\", "
    "sempre com dois dígitos no dia e no mês.",
    r'''
#include <stdio.h>

int main(void) {
    int dia, mes, ano;
    /* leia os três números */
    /* mostre a data com dois dígitos no dia e no mês */
    return 0;
}
''',
    [
        'Leia os três valores com scanf("%d %d %d", &dia, &mes, &ano).',
        "O formato %02d mostra o número com pelo menos 2 dígitos, completando com zero à esquerda.",
        'A barra é texto comum dentro do printf: "Data: %02d/%02d/%d\\n".',
    ],
    {
        "codigo_contem": ["scanf"],
        "testes": [
            _teste("5 9 2026\n", "Data: 05/09/2026"),
            _teste("12 10 1999\n", "Data: 12/10/1999"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int dia, mes, ano;
    scanf("%d %d %d", &dia, &mes, &ano);
    printf("Data: %02d/%02d/%d\n", dia, mes, ano);  /* %02d completa com zero */
    return 0;
}
''',
    "O 0 em %02d pede zeros à esquerda e o 2 define a largura mínima; por isso 5 vira 05.",
    exemplo=("5 9 2026", "Data: 05/09/2026"),
)

_desafio(
    2, 4, "Caracteres especiais", MEDIO, 5,
    'Mostre as três linhas abaixo exatamente como estão: Ele disse "Oi" / Caminho: C:\\temp / '
    "Progresso: 100%",
    r'''
#include <stdio.h>

int main(void) {
    /* mostre: Ele disse "Oi" */
    /* mostre: Caminho: C:\temp */
    /* mostre: Progresso: 100% */
    return 0;
}
''',
    [
        'Aspas dentro do texto precisam de barra invertida: \\".',
        "Para mostrar uma barra invertida, escreva duas: \\\\.",
        "No printf, o símbolo de porcentagem é escrito como %%.",
    ],
    {
        "codigo_contem": ["printf"],
        "saida_contem": ['Ele disse "Oi"', "Caminho: C:\\temp", "Progresso: 100%"],
    },
    r'''
#include <stdio.h>

int main(void) {
    printf("Ele disse \"Oi\"\n");   /* \" coloca aspas no texto */
    printf("Caminho: C:\\temp\n");  /* \\ mostra uma barra invertida */
    printf("Progresso: 100%%\n");   /* %% mostra o símbolo de porcentagem */
    return 0;
}
''',
    "Aspas, barra invertida e porcentagem têm significado especial no printf, por isso usam sequências de escape.",
    exemplo=("", 'Ele disse "Oi"\nCaminho: C:\\temp\nProgresso: 100%'),
)

_desafio(
    2, 5, "Número alinhado", MEDIO, 5,
    "Leia um inteiro e mostre-o entre colchetes, alinhado à direita em um espaço de 5 caracteres. "
    'Exemplo: 42 vira "[   42]".',
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    printf("[%d]\n", numero);  /* ajuste a largura */
    return 0;
}
''',
    [
        "Um número entre o % e o d define a largura mínima do campo.",
        "%5d ocupa pelo menos 5 posições e completa com espaços à esquerda.",
        "Números com 5 dígitos ou mais aparecem inteiros, sem espaços.",
    ],
    {
        "codigo_contem": ["scanf"],
        "testes": [
            _teste("42\n", "[   42]"),
            _teste("7\n", "[    7]"),
            _teste("12345\n", "[12345]"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    printf("[%5d]\n", numero);  /* largura mínima 5, alinhado à direita */
    return 0;
}
''',
    "%5d reserva 5 posições; quando o número é menor, os espaços entram à esquerda.",
    exemplo=("42", "[   42]"),
)

# ---------------------------------------------------------------------------
# Módulo 3 · Guardando informações
# ---------------------------------------------------------------------------

_desafio(
    3, 1, "Ficha do produto", FACIL, 8,
    "Crie três variáveis: char categoria com 'B', int quantidade com 12 e double preco com 3.5. "
    'Mostre "Categoria: B", "Quantidade: 12" e "Preco: 3.50" (duas casas decimais).',
    r'''
#include <stdio.h>

int main(void) {
    char categoria = 'B';
    /* crie quantidade (int) e preco (double) */
    printf("Categoria: %c\n", categoria);
    return 0;
}
''',
    [
        "Cada tipo tem seu especificador: %c para char, %d para int e %f para double.",
        "%.2f mostra o double com exatamente duas casas decimais.",
        "Declare cada variável já com o valor pedido, por exemplo: int quantidade = 12;",
    ],
    {
        "codigo_contem": ["char", "int", "double"],
        "saida_contem": ["Categoria: B", "Quantidade: 12", "Preco: 3.50"],
    },
    r'''
#include <stdio.h>

int main(void) {
    char categoria = 'B';
    int quantidade = 12;
    double preco = 3.5;
    printf("Categoria: %c\n", categoria);
    printf("Quantidade: %d\n", quantidade);
    printf("Preco: %.2f\n", preco);  /* duas casas decimais */
    return 0;
}
''',
    "Cada tipo guarda um tipo de dado e usa o especificador certo no printf: %c, %d e %.2f.",
    exemplo=("", "Categoria: B\nQuantidade: 12\nPreco: 3.50"),
)

_desafio(
    3, 2, "Código da letra", MEDIO, 9,
    "Leia um caractere e mostre a letra e o seu código na tabela ASCII, no formato "
    '"Letra: A codigo: 65".',
    r'''
#include <stdio.h>

int main(void) {
    char letra;
    /* leia um caractere */
    /* mostre a letra e o seu código */
    return 0;
}
''',
    [
        'Leia com scanf(" %c", &letra); o espaço antes de %c ignora espaços e Enter.',
        "Um char é guardado como número: %c mostra a letra e %d mostra o código.",
        "Você pode passar a mesma variável duas vezes no printf.",
    ],
    {
        "codigo_contem": ["char", "scanf"],
        "testes": [
            _teste("A\n", "Letra: A", "codigo: 65"),
            _teste("z\n", "Letra: z", "codigo: 122"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    char letra;
    scanf(" %c", &letra);
    printf("Letra: %c codigo: %d\n", letra, letra);  /* mesma variável, dois formatos */
    return 0;
}
''',
    "O char guarda o código numérico da letra; %c mostra o símbolo e %d mostra esse número.",
    exemplo=("A", "Letra: A codigo: 65"),
)

_desafio(
    3, 3, "Altura com duas casas", FACIL, 8,
    'Leia uma altura como número real (double) e mostre "Altura: X.XX" com duas casas decimais.',
    r'''
#include <stdio.h>

int main(void) {
    double altura;
    /* leia a altura */
    /* mostre com duas casas decimais */
    return 0;
}
''',
    [
        "Para ler um double com scanf use %lf.",
        "Para mostrar use %.2f no printf.",
        "Um número inteiro como 2 também é lido corretamente e aparece como 2.00.",
    ],
    {
        "codigo_contem": ["double", "scanf"],
        "testes": [
            _teste("1.754\n", "Altura: 1.75"),
            _teste("2\n", "Altura: 2.00"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    double altura;
    scanf("%lf", &altura);          /* %lf lê double */
    printf("Altura: %.2f\n", altura); /* %.2f mostra duas casas */
    return 0;
}
''',
    "No scanf o double usa %lf; no printf, %.2f arredonda a exibição para duas casas.",
    exemplo=("1.754", "Altura: 1.75"),
)

_desafio(
    3, 4, "Constantes da escola", FACIL, 11,
    "Crie #define MAX_ALUNOS 30 e const int SALA = 12. Use as duas constantes no printf para "
    'mostrar "Sala 12 comporta 30 alunos".',
    r'''
#include <stdio.h>

/* crie o #define MAX_ALUNOS aqui */

int main(void) {
    /* crie a constante SALA */
    return 0;
}
''',
    [
        "#define fica fora do main e não leva ponto e vírgula: #define MAX_ALUNOS 30",
        "const int SALA = 12; cria uma variável que não pode ser alterada.",
        'printf("Sala %d comporta %d alunos\\n", SALA, MAX_ALUNOS);',
    ],
    {
        "codigo_contem": ["#define", "MAX_ALUNOS", "const", "SALA"],
        "saida_contem": ["Sala 12 comporta 30 alunos"],
    },
    r'''
#include <stdio.h>

#define MAX_ALUNOS 30

int main(void) {
    const int SALA = 12;
    printf("Sala %d comporta %d alunos\n", SALA, MAX_ALUNOS);
    return 0;
}
''',
    "#define troca o nome pelo valor antes da compilação; const cria uma variável somente leitura.",
    exemplo=("", "Sala 12 comporta 30 alunos"),
)

_desafio(
    3, 5, "Mesmo nome, outro escopo", MEDIO, 12,
    "Em main crie int x = 1. Depois abra um bloco { } e, dentro dele, crie outro int x = 2 e mostre "
    '"Dentro: 2". Após fechar o bloco mostre "Fora: 1".',
    r'''
#include <stdio.h>

int main(void) {
    int x = 1;
    /* abra um bloco e crie outro x aqui dentro */
    printf("Fora: %d\n", x);
    return 0;
}
''',
    [
        "Chaves { } criam um novo escopo, mesmo sem if ou laço.",
        "Uma variável declarada dentro do bloco esconde a de fora enquanto o bloco existir.",
        "Quando o bloco termina, o x de dentro deixa de existir e o de fora volta a valer.",
    ],
    {
        "min_ocorrencias_codigo": {"int x": 2},
        "saida_contem": ["Dentro: 2", "Fora: 1"],
    },
    r'''
#include <stdio.h>

int main(void) {
    int x = 1;
    {
        int x = 2;               /* esconde o x de fora */
        printf("Dentro: %d\n", x);
    }                            /* o x de dentro termina aqui */
    printf("Fora: %d\n", x);
    return 0;
}
''',
    "O x do bloco interno é outra variável; ao fechar a chave ela some e o x externo continua valendo 1.",
    exemplo=("", "Dentro: 2\nFora: 1"),
)

# ---------------------------------------------------------------------------
# Módulo 4 · Fazendo contas e comparações
# ---------------------------------------------------------------------------

_desafio(
    4, 1, "Troco da compra", FACIL, 14,
    'Leia o valor da compra e o valor pago (inteiros) e mostre "Troco: N".',
    r'''
#include <stdio.h>

int main(void) {
    int compra, pago;
    scanf("%d %d", &compra, &pago);
    /* calcule e mostre o troco */
    return 0;
}
''',
    [
        "O troco é o valor pago menos o valor da compra.",
        "Guarde o resultado em uma variável troco antes de mostrar.",
        'printf("Troco: %d\\n", troco);',
    ],
    {
        "codigo_contem": ["-"],
        "testes": [
            _teste("37 50\n", regex=[r"troco: 13\b"]),
            _teste("20 20\n", regex=[r"troco: 0\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int compra, pago;
    scanf("%d %d", &compra, &pago);
    int troco = pago - compra;
    printf("Troco: %d\n", troco);
    return 0;
}
''',
    "A subtração pago - compra dá o troco; guardar em uma variável deixa o código mais claro.",
    exemplo=("37 50", "Troco: 13"),
)

_desafio(
    4, 2, "Relógio digital", MEDIO, 16,
    "Leia um total de segundos e mostre no formato HH:MM:SS (sempre dois dígitos). "
    "Exemplo: 3725 vira 01:02:05.",
    r'''
#include <stdio.h>

int main(void) {
    int total;
    scanf("%d", &total);
    /* calcule horas, minutos e segundos */
    return 0;
}
''',
    [
        "Uma hora tem 3600 segundos: horas = total / 3600.",
        "O operador % dá o resto da divisão: (total % 3600) / 60 são os minutos e total % 60 os segundos.",
        'Use %02d para mostrar sempre dois dígitos: "%02d:%02d:%02d".',
    ],
    {
        "codigo_contem": ["scanf", "/"],
        "testes": [
            _teste("3725\n", "01:02:05"),
            _teste("59\n", "00:00:59"),
            _teste("86399\n", "23:59:59"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int total;
    scanf("%d", &total);
    int horas = total / 3600;
    int minutos = (total % 3600) / 60;  /* o que sobrou das horas, em minutos */
    int segundos = total % 60;
    printf("%02d:%02d:%02d\n", horas, minutos, segundos);
    return 0;
}
''',
    "A divisão inteira separa as unidades maiores e o resto (%) guarda o que sobrou para a unidade seguinte.",
    exemplo=("3725", "01:02:05"),
)

_desafio(
    4, 3, "Média ponderada", MEDIO, 16,
    "Leia três notas (double). A primeira vale peso 2, a segunda peso 3 e a terceira peso 5. "
    'Mostre "Media: X.XX".',
    r'''
#include <stdio.h>

int main(void) {
    double n1, n2, n3;
    scanf("%lf %lf %lf", &n1, &n2, &n3);
    /* calcule a média ponderada */
    return 0;
}
''',
    [
        "Multiplique cada nota pelo seu peso e some tudo.",
        "Divida a soma pela soma dos pesos: 2 + 3 + 5 = 10.",
        'Mostre com printf("Media: %.2f\\n", media);',
    ],
    {
        "codigo_contem": ["*", "/"],
        "testes": [
            _teste("6 7 8\n", "Media: 7.30"),
            _teste("10 10 10\n", "Media: 10.00"),
            _teste("0 5 10\n", "Media: 6.50"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    double n1, n2, n3;
    scanf("%lf %lf %lf", &n1, &n2, &n3);
    double media = (n1 * 2 + n2 * 3 + n3 * 5) / 10;  /* 10 = soma dos pesos */
    printf("Media: %.2f\n", media);
    return 0;
}
''',
    "Os parênteses garantem que a soma inteira seja feita antes da divisão pelo total dos pesos.",
    exemplo=("6 7 8", "Media: 7.30"),
)

_desafio(
    4, 4, "Par sem if", MEDIO, 17,
    'Leia um inteiro e mostre "Par: 1" se ele for par ou "Par: 0" se for ímpar, usando apenas '
    "uma comparação (sem if).",
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    /* mostre o resultado da comparação */
    return 0;
}
''',
    [
        "Um número é par quando o resto da divisão por 2 é zero.",
        "Uma comparação em C vale 1 quando é verdadeira e 0 quando é falsa.",
        'printf("Par: %d\\n", numero % 2 == 0);',
    ],
    {
        "codigo_contem": ["=="],
        "testes": [
            _teste("8\n", "Par: 1"),
            _teste("7\n", "Par: 0"),
            _teste("-4\n", "Par: 1"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    printf("Par: %d\n", numero % 2 == 0);  /* a comparação já vale 1 ou 0 */
    return 0;
}
''',
    "Operadores relacionais produzem um int: 1 para verdadeiro e 0 para falso, então dá para mostrar direto.",
    exemplo=("8", "Par: 1"),
)

_desafio(
    4, 5, "Dentro do intervalo", MEDIO, 18,
    'Leia um inteiro e mostre "Dentro: 1" se ele estiver entre 10 e 20 (incluindo os dois) '
    'ou "Dentro: 0" caso contrário. Use o operador &&.',
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    /* combine duas comparações com && */
    return 0;
}
''',
    [
        "Você precisa de duas condições: numero >= 10 e numero <= 20.",
        "&& só vale 1 quando as duas condições são verdadeiras.",
        'printf("Dentro: %d\\n", numero >= 10 && numero <= 20);',
    ],
    {
        "codigo_contem": ["&&"],
        "testes": [
            _teste("15\n", "Dentro: 1"),
            _teste("10\n", "Dentro: 1"),
            _teste("20\n", "Dentro: 1"),
            _teste("21\n", "Dentro: 0"),
            _teste("5\n", "Dentro: 0"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    printf("Dentro: %d\n", numero >= 10 && numero <= 20);
    return 0;
}
''',
    "Com >= e <= os extremos 10 e 20 contam como dentro; && exige que as duas comparações sejam verdadeiras.",
    exemplo=("15", "Dentro: 1"),
)

# ---------------------------------------------------------------------------
# Módulo 5 · Tomando decisões
# ---------------------------------------------------------------------------

_desafio(
    5, 1, "Maior de três", FACIL, 22,
    'Leia três inteiros e mostre "Maior: N" com o maior deles.',
    r'''
#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    /* descubra o maior */
    return 0;
}
''',
    [
        "Comece supondo que o maior é a: int maior = a;",
        "Depois compare com b e com c, trocando o valor de maior quando achar alguém maior.",
        "Teste com números negativos e com números repetidos.",
    ],
    {
        "codigo_contem": ["if"],
        "testes": [
            _teste("3 9 5\n", regex=[r"maior: 9\b"]),
            _teste("-1 -7 -3\n", regex=[r"maior: -1\b"]),
            _teste("4 4 2\n", regex=[r"maior: 4\b"]),
            _teste("1 2 8\n", regex=[r"maior: 8\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    int maior = a;          /* suposição inicial */
    if (b > maior) {
        maior = b;
    }
    if (c > maior) {
        maior = c;
    }
    printf("Maior: %d\n", maior);
    return 0;
}
''',
    "Guardar o maior até agora e comparar com cada valor funciona para qualquer quantidade de números.",
    exemplo=("3 9 5", "Maior: 9"),
)

_desafio(
    5, 2, "Ano bissexto", DESAFIADOR, 22,
    'Leia um ano e mostre "Bissexto" ou "Comum". Regra: é bissexto se for divisível por 4 e não por 100, '
    "ou se for divisível por 400.",
    r'''
#include <stdio.h>

int main(void) {
    int ano;
    scanf("%d", &ano);
    /* aplique a regra do ano bissexto */
    return 0;
}
''',
    [
        "Divisível por 4 significa ano % 4 == 0.",
        "Monte a condição com && e ||: (ano % 4 == 0 && ano % 100 != 0) || ano % 400 == 0",
        "Teste 1900 (comum) e 2000 (bissexto): são os casos que mais pegam.",
    ],
    {
        "codigo_contem": ["if", "%"],
        "testes": [
            _teste("2024\n", "Bissexto", nao_contem=["Comum"]),
            _teste("1900\n", "Comum", nao_contem=["Bissexto"]),
            _teste("2000\n", "Bissexto", nao_contem=["Comum"]),
            _teste("2023\n", "Comum", nao_contem=["Bissexto"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int ano;
    scanf("%d", &ano);
    if ((ano % 4 == 0 && ano % 100 != 0) || ano % 400 == 0) {
        printf("Bissexto\n");
    } else {
        printf("Comum\n");
    }
    return 0;
}
''',
    "Os parênteses agrupam a primeira regra; o || aceita também os anos divisíveis por 400, como 2000.",
    exemplo=("2024", "Bissexto"),
)

_desafio(
    5, 3, "Calculadora com switch", MEDIO, 23,
    'Leia uma conta no formato "7 * 6" (inteiro, operador, inteiro). Trate +, -, * e / com switch e '
    'mostre "Resultado: N". Na divisão por zero mostre "Erro: divisao por zero" e para outro operador '
    '"Operador invalido".',
    r'''
#include <stdio.h>

int main(void) {
    int a, b;
    char operador;
    scanf("%d %c %d", &a, &operador, &b);
    /* use switch (operador) */
    return 0;
}
''',
    [
        "Cada case compara com um caractere: case '+':",
        "Não esqueça o break no fim de cada case.",
        "Dentro do case '/' verifique se b é zero antes de dividir; use default para o operador inválido.",
    ],
    {
        "codigo_contem": ["switch", "case", "break"],
        "testes": [
            _teste("7 * 6\n", regex=[r"resultado: 42\b"]),
            _teste("10 - 25\n", regex=[r"resultado: -15\b"]),
            _teste("9 / 0\n", "Erro: divisao por zero"),
            _teste("3 ^ 2\n", "Operador invalido"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int a, b;
    char operador;
    scanf("%d %c %d", &a, &operador, &b);
    switch (operador) {
        case '+':
            printf("Resultado: %d\n", a + b);
            break;
        case '-':
            printf("Resultado: %d\n", a - b);
            break;
        case '*':
            printf("Resultado: %d\n", a * b);
            break;
        case '/':
            if (b == 0) {
                printf("Erro: divisao por zero\n");
            } else {
                printf("Resultado: %d\n", a / b);
            }
            break;
        default:
            printf("Operador invalido\n");
    }
    return 0;
}
''',
    "O switch escolhe o case pelo caractere lido; o default cobre qualquer operador não previsto.",
    exemplo=("7 * 6", "Resultado: 42"),
)

_desafio(
    5, 4, "Tipo de triângulo", DESAFIADOR, 22,
    "Leia três lados inteiros. Se não formarem triângulo (um lado maior ou igual à soma dos outros dois), "
    'mostre "Nao forma triangulo". Senão mostre "Equilatero", "Isosceles" ou "Escaleno".',
    r'''
#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    /* primeiro verifique se forma triângulo */
    return 0;
}
''',
    [
        "Não forma triângulo se a >= b + c, ou b >= a + c, ou c >= a + b.",
        "Equilátero: três lados iguais. Isósceles: exatamente dois iguais. Escaleno: todos diferentes.",
        "Use uma cadeia if / else if / else para que só uma mensagem apareça.",
    ],
    {
        "codigo_contem": ["if", "else"],
        "testes": [
            _teste("3 3 3\n", "Equilatero", nao_contem=["Isosceles", "Escaleno"]),
            _teste("3 3 5\n", "Isosceles", nao_contem=["Equilatero", "Escaleno"]),
            _teste("3 4 5\n", "Escaleno", nao_contem=["Equilatero", "Isosceles"]),
            _teste("1 2 10\n", "Nao forma triangulo", nao_contem=["Escaleno"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    if (a >= b + c || b >= a + c || c >= a + b) {
        printf("Nao forma triangulo\n");
    } else if (a == b && b == c) {
        printf("Equilatero\n");
    } else if (a == b || b == c || a == c) {
        printf("Isosceles\n");
    } else {
        printf("Escaleno\n");
    }
    return 0;
}
''',
    "A ordem importa: primeiro descarta o caso inválido, depois testa o mais restrito (três iguais) antes de dois iguais.",
    exemplo=("3 4 5", "Escaleno"),
)

_desafio(
    5, 5, "Par ou ímpar com ternário", FACIL, 24,
    'Leia um inteiro e mostre "N e par" ou "N e impar" usando o operador ternário (?:).',
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    /* use condição ? "par" : "impar" */
    return 0;
}
''',
    [
        "O ternário tem a forma condição ? valor_se_verdadeiro : valor_se_falso.",
        "Ele pode escolher um texto: numero % 2 == 0 ? \"par\" : \"impar\"",
        'Mostre o texto com %s: printf("%d e %s\\n", numero, ...);',
    ],
    {
        "codigo_contem": ["?", ":"],
        "testes": [
            _teste("4\n", "4 e par", nao_contem=["impar"]),
            _teste("7\n", "7 e impar"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    printf("%d e %s\n", numero, numero % 2 == 0 ? "par" : "impar");
    return 0;
}
''',
    "O ternário escolhe entre os dois textos e o %s mostra o texto escolhido.",
    exemplo=("7", "7 e impar"),
)

# ---------------------------------------------------------------------------
# Módulo 6 · Repetindo tarefas
# ---------------------------------------------------------------------------

_desafio(
    6, 1, "Tabuada completa", FACIL, 27,
    'Leia um número N e mostre a tabuada de 1 a 10, uma linha por vez, no formato "N x 1 = N".',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* use um for de 1 a 10 */
    return 0;
}
''',
    [
        "for (int i = 1; i <= 10; i++) repete exatamente 10 vezes.",
        "Dentro do laço calcule n * i.",
        'printf("%d x %d = %d\\n", n, i, n * i);',
    ],
    {
        "codigo_contem": ["for"],
        "testes": [
            _teste("7\n", "7 x 1 = 7", "7 x 5 = 35", "7 x 10 = 70"),
            _teste("3\n", "3 x 1 = 3", "3 x 10 = 30", nao_contem=["3 x 11"]),
        ],
        "min_linhas_saida": 10,
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 1; i <= 10; i++) {
        printf("%d x %d = %d\n", n, i, n * i);
    }
    return 0;
}
''',
    "O for controla o multiplicador i de 1 a 10 e cada volta mostra uma linha da tabuada.",
    exemplo=("7", "7 x 1 = 7\n7 x 2 = 14\n...\n7 x 10 = 70"),
)

_desafio(
    6, 2, "Soma dos dígitos", MEDIO, 25,
    'Leia um inteiro positivo e mostre "Soma dos digitos: S". Exemplo: 1234 dá 10.',
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    int soma = 0;
    /* use while para separar os dígitos */
    printf("Soma dos digitos: %d\n", soma);
    return 0;
}
''',
    [
        "numero % 10 dá o último dígito.",
        "numero / 10 remove o último dígito.",
        "Repita enquanto numero > 0, somando o último dígito a cada volta.",
    ],
    {
        "codigo_contem": ["while"],
        "testes": [
            _teste("1234\n", regex=[r"soma dos digitos: 10\b"]),
            _teste("9\n", regex=[r"soma dos digitos: 9\b"]),
            _teste("1005\n", regex=[r"soma dos digitos: 6\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    int soma = 0;
    while (numero > 0) {
        soma += numero % 10;  /* último dígito */
        numero /= 10;         /* remove o último dígito */
    }
    printf("Soma dos digitos: %d\n", soma);
    return 0;
}
''',
    "Resto por 10 pega o último dígito e a divisão por 10 o descarta, até o número chegar a zero.",
    exemplo=("1234", "Soma dos digitos: 10"),
)

_desafio(
    6, 3, "Contagem regressiva", FACIL, 27,
    'Leia N e mostre a contagem de N até 1, um número por linha, e depois "Fogo!".',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* conte de n até 1 */
    printf("Fogo!\n");
    return 0;
}
''',
    [
        "Um for também pode contar para trás: for (int i = n; i >= 1; i--)",
        "Mostre i com \\n para cada número ficar em uma linha.",
        '"Fogo!" aparece uma única vez, depois do laço.',
    ],
    {
        "codigo_contem": ["for"],
        "testes": [
            _teste("3\n", regex=[r"3\s+2\s+1\s+fogo!"]),
            _teste("5\n", regex=[r"5\s+4\s+3\s+2\s+1\s+fogo!"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = n; i >= 1; i--) {  /* i-- diminui a cada volta */
        printf("%d\n", i);
    }
    printf("Fogo!\n");
    return 0;
}
''',
    "O laço começa em n e usa i-- para descer até 1; a mensagem final fica fora do laço.",
    exemplo=("3", "3\n2\n1\nFogo!"),
)

_desafio(
    6, 4, "Soma até o zero", MEDIO, 26,
    "Leia números inteiros até o usuário digitar 0. No fim mostre \"Soma: S\" e \"Quantidade: Q\" "
    "(o zero não entra na conta). Use do while.",
    r'''
#include <stdio.h>

int main(void) {
    int numero, soma = 0, quantidade = 0;
    /* use do { ... } while (numero != 0); */
    printf("Soma: %d\n", soma);
    printf("Quantidade: %d\n", quantidade);
    return 0;
}
''',
    [
        "O do while executa o bloco pelo menos uma vez e testa a condição no final.",
        "Dentro do bloco leia o número e só some quando ele for diferente de 0.",
        "A condição de parada é while (numero != 0);",
    ],
    {
        "codigo_contem": ["do", "while"],
        "testes": [
            _teste("5 3 2 0\n", regex=[r"soma: 10\b", r"quantidade: 3\b"]),
            _teste("0\n", regex=[r"soma: 0\b", r"quantidade: 0\b"]),
            _teste("-4 10 0\n", regex=[r"soma: 6\b", r"quantidade: 2\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero, soma = 0, quantidade = 0;
    do {
        if (scanf("%d", &numero) != 1) {
            numero = 0;              /* entrada acabou: encerra */
        }
        if (numero != 0) {
            soma += numero;
            quantidade++;
        }
    } while (numero != 0);
    printf("Soma: %d\n", soma);
    printf("Quantidade: %d\n", quantidade);
    return 0;
}
''',
    "O do while garante a primeira leitura; o if evita contar o zero, que só serve para parar.",
    exemplo=("5 3 2 0", "Soma: 10\nQuantidade: 3"),
)

_desafio(
    6, 5, "Número primo", DESAFIADOR, 28,
    'Leia um inteiro N e mostre "Primo" ou "Nao primo". Use break para parar assim que achar um divisor.',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int primo = 1;
    /* procure divisores de 2 até n - 1 */
    return 0;
}
''',
    [
        "Números menores que 2 não são primos.",
        "Se n % d == 0 para algum d entre 2 e n - 1, n não é primo.",
        "Basta testar d enquanto d * d <= n; ao achar um divisor, marque primo = 0 e use break.",
    ],
    {
        "codigo_contem": ["break"],
        "testes": [
            _teste("7\n", "Primo", nao_contem=["Nao primo"]),
            _teste("9\n", "Nao primo"),
            _teste("1\n", "Nao primo"),
            _teste("2\n", "Primo", nao_contem=["Nao primo"]),
            _teste("97\n", "Primo", nao_contem=["Nao primo"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int primo = n >= 2;              /* 0 e 1 não são primos */
    for (int d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            primo = 0;
            break;                   /* já sabemos a resposta */
        }
    }
    printf("%s\n", primo ? "Primo" : "Nao primo");
    return 0;
}
''',
    "Se existe divisor, algum deles é no máximo a raiz de n; o break encerra o laço no primeiro encontrado.",
    exemplo=("7", "Primo"),
)

# ---------------------------------------------------------------------------
# Módulo 7 · Organizando o código
# ---------------------------------------------------------------------------

_desafio(
    7, 1, "Função maior", FACIL, 32,
    "Crie a função int maior(int a, int b) que devolve o maior dos dois valores. Em main leia dois "
    'inteiros e mostre "Maior: N" usando a função.',
    r'''
#include <stdio.h>

/* crie aqui a função int maior(int a, int b) */

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    /* mostre Maior: usando a função */
    return 0;
}
''',
    [
        "A função recebe dois int e devolve um int: int maior(int a, int b) { ... }",
        "Dentro dela, use if para decidir qual valor retornar com return.",
        'Em main chame a função dentro do printf: printf("Maior: %d\\n", maior(a, b));',
    ],
    {
        "min_ocorrencias_codigo": {"maior(": 2},
        "codigo_contem": ["return"],
        "testes": [
            _teste("4 9\n", regex=[r"maior: 9\b"]),
            _teste("-3 -8\n", regex=[r"maior: -3\b"]),
            _teste("5 5\n", regex=[r"maior: 5\b"]),
        ],
    },
    r'''
#include <stdio.h>

int maior(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("Maior: %d\n", maior(a, b));
    return 0;
}
''',
    "A função concentra a regra de comparação; main só lê os dados e mostra o valor retornado.",
    exemplo=("4 9", "Maior: 9"),
)

_desafio(
    7, 2, "Pares até N", FACIL, 32,
    "Crie int ehPar(int n) que devolve 1 para par e 0 para ímpar. Leia N e mostre, na mesma linha e "
    "separados por espaço, todos os pares de 1 até N usando a função.",
    r'''
#include <stdio.h>

/* crie int ehPar(int n) */

int main(void) {
    int n;
    scanf("%d", &n);
    /* percorra de 1 até n e mostre só os pares */
    printf("\n");
    return 0;
}
''',
    [
        "ehPar pode ser uma linha só: return n % 2 == 0;",
        "Em main use for (int i = 1; i <= n; i++) e chame ehPar(i) dentro de um if.",
        'Mostre cada par com printf("%d ", i); e pule a linha só no final.',
    ],
    {
        "min_ocorrencias_codigo": {"ehpar(": 2},
        "codigo_contem": ["return"],
        "testes": [
            _teste("10\n", "2 4 6 8 10"),
            _teste("5\n", "2 4", nao_contem=["6"]),
        ],
    },
    r'''
#include <stdio.h>

int ehPar(int n) {
    return n % 2 == 0;  /* a comparação já é 1 ou 0 */
}

int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        if (ehPar(i)) {
            printf("%d ", i);
        }
    }
    printf("\n");
    return 0;
}
''',
    "A função devolve o resultado da comparação e o if de main usa esse 1 ou 0 como verdadeiro ou falso.",
    exemplo=("10", "2 4 6 8 10"),
)

_desafio(
    7, 3, "Potência recursiva", MEDIO, 34,
    "Crie a função recursiva int potencia(int base, int expoente), sem usar pow. Leia base e expoente "
    '(expoente >= 0) e mostre "Resultado: N".',
    r'''
#include <stdio.h>

/* crie int potencia(int base, int expoente) usando recursão */

int main(void) {
    int base, expoente;
    scanf("%d %d", &base, &expoente);
    /* mostre o resultado */
    return 0;
}
''',
    [
        "Caso base: qualquer número elevado a 0 é 1.",
        "Passo recursivo: base elevado a e é base * potencia(base, e - 1).",
        "Cada chamada diminui o expoente, então a recursão sempre chega ao caso base.",
    ],
    {
        "min_ocorrencias_codigo": {"potencia(": 3},
        "codigo_nao_contem": ["pow("],
        "testes": [
            _teste("2 10\n", regex=[r"resultado: 1024\b"]),
            _teste("5 0\n", regex=[r"resultado: 1\b"]),
            _teste("3 4\n", regex=[r"resultado: 81\b"]),
        ],
    },
    r'''
#include <stdio.h>

int potencia(int base, int expoente) {
    if (expoente == 0) {
        return 1;                                /* caso base */
    }
    return base * potencia(base, expoente - 1);  /* passo recursivo */
}

int main(void) {
    int base, expoente;
    scanf("%d %d", &base, &expoente);
    printf("Resultado: %d\n", potencia(base, expoente));
    return 0;
}
''',
    "A recursão reduz o expoente em 1 a cada chamada até chegar a 0, quando devolve 1 e as multiplicações voltam.",
    exemplo=("2 10", "Resultado: 1024"),
)

_desafio(
    7, 4, "Conversor com protótipo", FACIL, 33,
    "Declare o protótipo double celsiusParaFahrenheit(double c) antes de main e implemente a função "
    'depois de main. Leia a temperatura em Celsius e mostre "Fahrenheit: X.X" com uma casa decimal.',
    r'''
#include <stdio.h>

/* declare o protótipo aqui */

int main(void) {
    double celsius;
    scanf("%lf", &celsius);
    /* mostre a conversão */
    return 0;
}

/* implemente a função aqui */
''',
    [
        "O protótipo é a primeira linha da função terminada em ponto e vírgula.",
        "A fórmula é F = C * 9 / 5 + 32.",
        'Mostre com printf("Fahrenheit: %.1f\\n", ...);',
    ],
    {
        "min_ocorrencias_codigo": {"celsiusparafahrenheit(": 3},
        "testes": [
            _teste("100\n", "Fahrenheit: 212.0"),
            _teste("-40\n", "Fahrenheit: -40.0"),
            _teste("36.5\n", "Fahrenheit: 97.7"),
        ],
    },
    r'''
#include <stdio.h>

double celsiusParaFahrenheit(double c);  /* protótipo */

int main(void) {
    double celsius;
    scanf("%lf", &celsius);
    printf("Fahrenheit: %.1f\n", celsiusParaFahrenheit(celsius));
    return 0;
}

double celsiusParaFahrenheit(double c) {
    return c * 9 / 5 + 32;
}
''',
    "O protótipo avisa o compilador sobre a função antes do uso, então a implementação pode ficar depois de main.",
    exemplo=("100", "Fahrenheit: 212.0"),
)

_desafio(
    7, 5, "MDC de Euclides", DESAFIADOR, 34,
    "Crie a função recursiva int mdc(int a, int b) usando o algoritmo de Euclides: mdc(a, 0) = a e "
    'mdc(a, b) = mdc(b, a % b). Leia dois inteiros positivos e mostre "MDC: N".',
    r'''
#include <stdio.h>

/* crie int mdc(int a, int b) */

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    /* mostre o MDC */
    return 0;
}
''',
    [
        "O caso base é b == 0: aí a resposta é a.",
        "Senão, chame mdc(b, a % b).",
        "Teste de cabeça: mdc(48, 18) → mdc(18, 12) → mdc(12, 6) → mdc(6, 0) = 6.",
    ],
    {
        "min_ocorrencias_codigo": {"mdc(": 3},
        "testes": [
            _teste("48 18\n", regex=[r"mdc: 6\b"]),
            _teste("17 5\n", regex=[r"mdc: 1\b"]),
            _teste("100 75\n", regex=[r"mdc: 25\b"]),
        ],
    },
    r'''
#include <stdio.h>

int mdc(int a, int b) {
    if (b == 0) {
        return a;           /* caso base */
    }
    return mdc(b, a % b);   /* o resto fica cada vez menor */
}

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("MDC: %d\n", mdc(a, b));
    return 0;
}
''',
    "Os divisores comuns de a e b são os mesmos de b e a % b; como o resto diminui, a recursão termina.",
    exemplo=("48 18", "MDC: 6"),
)

# ---------------------------------------------------------------------------
# Módulo 8 · Listas e textos
# ---------------------------------------------------------------------------

_desafio(
    8, 1, "Maior e menor do vetor", FACIL, 35,
    'Leia 5 inteiros em um vetor int v[5] e mostre "Maior: X" e "Menor: Y".',
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    /* encontre o maior e o menor */
    return 0;
}
''',
    [
        "Comece com maior = v[0] e menor = v[0].",
        "Percorra o vetor a partir do índice 1 comparando cada elemento.",
        "Não comece com 0: se todos forem negativos, o maior estaria errado.",
    ],
    {
        "codigo_contem": ["[5]", "for"],
        "testes": [
            _teste("4 9 1 7 3\n", regex=[r"maior: 9\b", r"menor: 1\b"]),
            _teste("-2 -8 -5 -1 -9\n", regex=[r"maior: -1\b", r"menor: -9\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    int maior = v[0], menor = v[0];  /* começa pelo primeiro elemento */
    for (int i = 1; i < 5; i++) {
        if (v[i] > maior) {
            maior = v[i];
        }
        if (v[i] < menor) {
            menor = v[i];
        }
    }
    printf("Maior: %d\n", maior);
    printf("Menor: %d\n", menor);
    return 0;
}
''',
    "Iniciar com o primeiro elemento funciona para qualquer vetor, inclusive só com negativos.",
    exemplo=("4 9 1 7 3", "Maior: 9\nMenor: 1"),
)

_desafio(
    8, 2, "Vetor ao contrário", FACIL, 35,
    "Leia 5 inteiros em um vetor e mostre-os na ordem inversa, na mesma linha, separados por espaço.",
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    /* leia os 5 valores */
    /* mostre do último para o primeiro */
    return 0;
}
''',
    [
        "Primeiro leia todos os valores com um for de 0 a 4.",
        "Depois use outro for começando em 4 e descendo até 0.",
        'Mostre cada valor com printf("%d ", v[i]);',
    ],
    {
        "codigo_contem": ["for", "["],
        "testes": [
            _teste("1 2 3 4 5\n", "5 4 3 2 1"),
            _teste("10 20 30 40 50\n", "50 40 30 20 10"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    for (int i = 4; i >= 0; i--) {  /* último índice é 4 */
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}
''',
    "O vetor guarda todos os valores; o segundo laço só percorre os índices de trás para frente.",
    exemplo=("1 2 3 4 5", "5 4 3 2 1"),
)

_desafio(
    8, 3, "Contador de vogais", MEDIO, 42,
    'Leia uma frase com fgets e mostre "Vogais: N", contando a, e, i, o, u maiúsculas e minúsculas.',
    r'''
#include <stdio.h>

int main(void) {
    char frase[100];
    fgets(frase, sizeof frase, stdin);
    int vogais = 0;
    /* percorra a frase até o '\0' */
    printf("Vogais: %d\n", vogais);
    return 0;
}
''',
    [
        "Percorra com for (int i = 0; frase[i] != '\\0'; i++).",
        "Compare frase[i] com cada vogal, maiúscula e minúscula, usando ||.",
        "Um switch com vários case seguidos também funciona bem aqui.",
    ],
    {
        "codigo_contem": ["fgets"],
        "testes": [
            _teste("Programar em C\n", regex=[r"vogais: 4\b"]),
            _teste("AEIOU xyz\n", regex=[r"vogais: 5\b"]),
            _teste("rtz\n", regex=[r"vogais: 0\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    char frase[100];
    fgets(frase, sizeof frase, stdin);
    int vogais = 0;
    for (int i = 0; frase[i] != '\0'; i++) {
        switch (frase[i]) {
            case 'a': case 'e': case 'i': case 'o': case 'u':
            case 'A': case 'E': case 'I': case 'O': case 'U':
                vogais++;
                break;
            default:
                break;
        }
    }
    printf("Vogais: %d\n", vogais);
    return 0;
}
''',
    "A string termina no '\\0'; vários case seguidos compartilham o mesmo bloco de contagem.",
    exemplo=("Programar em C", "Vogais: 4"),
)

_desafio(
    8, 4, "Palíndromo", MEDIO, 38,
    'Leia uma palavra (sem espaços) e mostre "Palindromo" se ela for igual de trás para frente, '
    'ou "Nao e palindromo" caso contrário.',
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    /* compare as letras das pontas indo para o meio */
    return 0;
}
''',
    [
        "Use strlen para saber o tamanho da palavra.",
        "Compare palavra[i] com palavra[tamanho - 1 - i] até a metade.",
        "Uma variável int eh = 1 que vira 0 na primeira diferença resolve a decisão final.",
    ],
    {
        "codigo_contem": ["strlen"],
        "testes": [
            _teste("arara\n", "Palindromo", nao_contem=["Nao e"]),
            _teste("casa\n", "Nao e palindromo"),
            _teste("a\n", "Palindromo", nao_contem=["Nao e"]),
            _teste("abba\n", "Palindromo", nao_contem=["Nao e"]),
        ],
    },
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    size_t tamanho = strlen(palavra);
    int eh = 1;
    for (size_t i = 0; i < tamanho / 2; i++) {
        if (palavra[i] != palavra[tamanho - 1 - i]) {  /* letras das pontas */
            eh = 0;
            break;
        }
    }
    printf("%s\n", eh ? "Palindromo" : "Nao e palindromo");
    return 0;
}
''',
    "Basta comparar até a metade: cada letra é comparada com a que está na posição espelhada.",
    exemplo=("arara", "Palindromo"),
)

_desafio(
    8, 5, "Soma das linhas da matriz", MEDIO, 36,
    'Leia uma matriz 3x3 de inteiros (linha por linha) e mostre a soma de cada linha: "Linha 1: S".',
    r'''
#include <stdio.h>

int main(void) {
    int m[3][3];
    /* leia a matriz com dois for */
    /* some cada linha */
    return 0;
}
''',
    [
        "Dois for aninhados leem a matriz: o de fora é a linha, o de dentro a coluna.",
        "Para cada linha, zere a soma antes de percorrer as colunas.",
        'Mostre com printf("Linha %d: %d\\n", i + 1, soma);',
    ],
    {
        "codigo_contem": ["[3][3]"],
        "testes": [
            _teste("1 2 3\n4 5 6\n7 8 9\n", regex=[r"linha 1: 6\b", r"linha 2: 15\b", r"linha 3: 24\b"]),
            _teste("0 0 1\n2 2 2\n-1 0 1\n", regex=[r"linha 1: 1\b", r"linha 2: 6\b", r"linha 3: 0\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int m[3][3];
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            scanf("%d", &m[i][j]);
        }
    }
    for (int i = 0; i < 3; i++) {
        int soma = 0;              /* recomeça em cada linha */
        for (int j = 0; j < 3; j++) {
            soma += m[i][j];
        }
        printf("Linha %d: %d\n", i + 1, soma);
    }
    return 0;
}
''',
    "O primeiro índice escolhe a linha; zerar a soma dentro do laço externo separa o total de cada linha.",
    exemplo=("1 2 3 4 5 6 7 8 9", "Linha 1: 6\nLinha 2: 15\nLinha 3: 24"),
)

# ---------------------------------------------------------------------------
# Módulo 9 · Como a memória funciona
# ---------------------------------------------------------------------------

_desafio(
    9, 1, "Quociente e resto por ponteiro", MEDIO, 45,
    "Crie void dividir(int a, int b, int *quociente, int *resto), que grava os dois resultados pelos "
    'ponteiros. Leia a e b e mostre "Quociente: Q" e "Resto: R".',
    r'''
#include <stdio.h>

/* crie void dividir(int a, int b, int *quociente, int *resto) */

int main(void) {
    int a, b, q, r;
    scanf("%d %d", &a, &b);
    /* chame dividir passando &q e &r */
    return 0;
}
''',
    [
        "Uma função só retorna um valor, mas pode gravar vários por ponteiros.",
        "Dentro da função use *quociente = a / b; e *resto = a % b;",
        "Na chamada passe os endereços: dividir(a, b, &q, &r);",
    ],
    {
        "min_ocorrencias_codigo": {"dividir(": 2},
        "codigo_contem": ["*", "&"],
        "testes": [
            _teste("17 5\n", regex=[r"quociente: 3\b", r"resto: 2\b"]),
            _teste("20 4\n", regex=[r"quociente: 5\b", r"resto: 0\b"]),
        ],
    },
    r'''
#include <stdio.h>

void dividir(int a, int b, int *quociente, int *resto) {
    *quociente = a / b;  /* grava no endereço recebido */
    *resto = a % b;
}

int main(void) {
    int a, b, q, r;
    scanf("%d %d", &a, &b);
    dividir(a, b, &q, &r);
    printf("Quociente: %d\n", q);
    printf("Resto: %d\n", r);
    return 0;
}
''',
    "Ao receber os endereços de q e r, a função consegue alterar as variáveis de main.",
    exemplo=("17 5", "Quociente: 3\nResto: 2"),
)

_desafio(
    9, 2, "Dobrar o vetor", FACIL, 46,
    "Crie void dobrar(int *v, int n) que multiplica por 2 cada elemento do vetor. Leia 4 inteiros, "
    "chame a função e mostre o vetor alterado na mesma linha.",
    r'''
#include <stdio.h>

/* crie void dobrar(int *v, int n) */

int main(void) {
    int v[4];
    for (int i = 0; i < 4; i++) {
        scanf("%d", &v[i]);
    }
    /* chame dobrar e mostre o vetor */
    return 0;
}
''',
    [
        "Um vetor passado para função vira um ponteiro para o primeiro elemento.",
        "Dentro da função, v[i] *= 2; altera o vetor original.",
        "Passe também o tamanho, porque o ponteiro não sabe quantos elementos existem.",
    ],
    {
        "min_ocorrencias_codigo": {"dobrar(": 2},
        "codigo_contem": ["*"],
        "testes": [
            _teste("1 2 3 4\n", "2 4 6 8"),
            _teste("-1 0 5 10\n", "-2 0 10 20"),
        ],
    },
    r'''
#include <stdio.h>

void dobrar(int *v, int n) {
    for (int i = 0; i < n; i++) {
        v[i] *= 2;          /* altera o vetor de main */
    }
}

int main(void) {
    int v[4];
    for (int i = 0; i < 4; i++) {
        scanf("%d", &v[i]);
    }
    dobrar(v, 4);
    for (int i = 0; i < 4; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}
''',
    "O nome do vetor já é o endereço do primeiro elemento, então a função altera os valores originais.",
    exemplo=("1 2 3 4", "2 4 6 8"),
)

_desafio(
    9, 3, "Tamanho sem strlen", MEDIO, 46,
    'Leia uma palavra e mostre "Tamanho: N" contando os caracteres com um ponteiro char *p que anda '
    "até o '\\0'. Não use strlen.",
    r'''
#include <stdio.h>

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    int tamanho = 0;
    /* use char *p = palavra; e avance até o '\0' */
    printf("Tamanho: %d\n", tamanho);
    return 0;
}
''',
    [
        "char *p = palavra; faz p apontar para a primeira letra.",
        "Enquanto *p != '\\0', some 1 ao tamanho e avance com p++.",
        "O '\\0' marca o fim de toda string em C.",
    ],
    {
        "codigo_contem": ["*p"],
        "codigo_nao_contem": ["strlen"],
        "testes": [
            _teste("computador\n", regex=[r"tamanho: 10\b"]),
            _teste("C\n", regex=[r"tamanho: 1\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    int tamanho = 0;
    for (char *p = palavra; *p != '\0'; p++) {  /* anda uma letra por vez */
        tamanho++;
    }
    printf("Tamanho: %d\n", tamanho);
    return 0;
}
''',
    "É assim que strlen funciona por dentro: anda pela memória até achar o terminador '\\0'.",
    exemplo=("computador", "Tamanho: 10"),
)

_desafio(
    9, 4, "Ordenar três com ponteiros", DESAFIADOR, 45,
    "Crie void ordenar(int *a, int *b) que troca os valores quando *a > *b. Leia três inteiros e, "
    'usando apenas chamadas a ordenar, mostre "Ordenados: X Y Z" em ordem crescente.',
    r'''
#include <stdio.h>

/* crie void ordenar(int *a, int *b) */

int main(void) {
    int x, y, z;
    scanf("%d %d %d", &x, &y, &z);
    /* chame ordenar algumas vezes */
    printf("Ordenados: %d %d %d\n", x, y, z);
    return 0;
}
''',
    [
        "Para trocar use uma variável auxiliar: int temp = *a; *a = *b; *b = temp;",
        "Três chamadas bastam: (x, y), depois (y, z) e de novo (x, y).",
        "Passe os endereços: ordenar(&x, &y);",
    ],
    {
        "min_ocorrencias_codigo": {"ordenar(": 3},
        "testes": [
            _teste("3 1 2\n", "Ordenados: 1 2 3"),
            _teste("9 5 1\n", "Ordenados: 1 5 9"),
            _teste("2 2 1\n", "Ordenados: 1 2 2"),
        ],
    },
    r'''
#include <stdio.h>

void ordenar(int *a, int *b) {
    if (*a > *b) {
        int temp = *a;
        *a = *b;
        *b = temp;
    }
}

int main(void) {
    int x, y, z;
    scanf("%d %d %d", &x, &y, &z);
    ordenar(&x, &y);
    ordenar(&y, &z);  /* agora o maior está em z */
    ordenar(&x, &y);  /* arruma os dois primeiros */
    printf("Ordenados: %d %d %d\n", x, y, z);
    return 0;
}
''',
    "A segunda chamada leva o maior para z; a terceira corrige a ordem entre x e y.",
    exemplo=("3 1 2", "Ordenados: 1 2 3"),
)

_desafio(
    9, 5, "Trocar ponteiros", DESAFIADOR, 47,
    "Crie int x = 10, y = 20, int *p = &x e int *q = &y. Escreva void trocarPonteiros(int **a, int **b) "
    'que faz p apontar para y e q para x. Mostre "*p = 20, *q = 10" e depois "x = 10, y = 20".',
    r'''
#include <stdio.h>

/* crie void trocarPonteiros(int **a, int **b) */

int main(void) {
    int x = 10, y = 20;
    int *p = &x;
    int *q = &y;
    /* troque para onde p e q apontam */
    printf("*p = %d, *q = %d\n", *p, *q);
    printf("x = %d, y = %d\n", x, y);
    return 0;
}
''',
    [
        "Para mudar um ponteiro dentro da função é preciso o endereço dele: int **.",
        "Dentro da função troque *a e *b usando um int *temp.",
        "Os valores de x e y não mudam; só muda para onde p e q apontam.",
    ],
    {
        "codigo_contem": ["**"],
        "min_ocorrencias_codigo": {"trocarponteiros(": 2},
        "saida_contem": ["*p = 20, *q = 10", "x = 10, y = 20"],
    },
    r'''
#include <stdio.h>

void trocarPonteiros(int **a, int **b) {
    int *temp = *a;  /* *a é o próprio ponteiro p */
    *a = *b;
    *b = temp;
}

int main(void) {
    int x = 10, y = 20;
    int *p = &x;
    int *q = &y;
    trocarPonteiros(&p, &q);
    printf("*p = %d, *q = %d\n", *p, *q);
    printf("x = %d, y = %d\n", x, y);
    return 0;
}
''',
    "Com int ** a função recebe o endereço dos ponteiros e troca os endereços guardados, sem mexer em x e y.",
    exemplo=("", "*p = 20, *q = 10\nx = 10, y = 20"),
)

# ---------------------------------------------------------------------------
# Módulo 10 · Usando memória quando precisar
# ---------------------------------------------------------------------------

_desafio(
    10, 1, "Média com vetor dinâmico", FACIL, 48,
    "Leia N e depois N inteiros guardando-os em um vetor criado com malloc. Mostre \"Media: X.XX\" "
    "e libere a memória.",
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* aloque o vetor com malloc e verifique se deu certo */
    return 0;
}
''',
    [
        "int *v = malloc(n * sizeof(int)); reserva espaço para n inteiros.",
        "Se malloc devolver NULL, mostre um erro e encerre.",
        "Some em double para a média ter casas decimais e chame free(v) no final.",
    ],
    {
        "codigo_contem": ["malloc", "free"],
        "testes": [
            _teste("4\n10 20 30 40\n", "Media: 25.00"),
            _teste("3\n1 2 2\n", "Media: 1.67"),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int *v = malloc(n * sizeof(int));
    if (v == NULL) {
        printf("Sem memoria\n");
        return 1;
    }
    double soma = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d", &v[i]);
        soma += v[i];
    }
    printf("Media: %.2f\n", soma / n);
    free(v);  /* devolve a memória */
    return 0;
}
''',
    "O tamanho só é conhecido durante a execução, por isso o vetor é alocado com malloc e liberado com free.",
    exemplo=("4\n10 20 30 40", "Media: 25.00"),
)

_desafio(
    10, 2, "Frequência com calloc", MEDIO, 49,
    "Leia N e depois N dígitos (0 a 9). Use calloc para criar um contador zerado para cada dígito e mostre "
    'apenas os dígitos que apareceram, em ordem, no formato "D: vezes".',
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* crie int *contagem com calloc(10, sizeof(int)) */
    return 0;
}
''',
    [
        "calloc(10, sizeof(int)) cria 10 contadores já valendo zero.",
        "Para cada dígito lido faça contagem[digito]++.",
        "Na hora de mostrar, pule os dígitos com contagem zero e lembre do free.",
    ],
    {
        "codigo_contem": ["calloc", "free"],
        "testes": [
            _teste("6\n1 3 3 7 1 3\n", "1: 2", "3: 3", "7: 1", nao_contem=["2: 0", "0: 0"]),
            _teste("3\n0 0 9\n", "0: 2", "9: 1", nao_contem=["1: 0"]),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int *contagem = calloc(10, sizeof(int));  /* 10 contadores zerados */
    if (contagem == NULL) {
        printf("Sem memoria\n");
        return 1;
    }
    for (int i = 0; i < n; i++) {
        int digito;
        scanf("%d", &digito);
        if (digito >= 0 && digito <= 9) {
            contagem[digito]++;
        }
    }
    for (int d = 0; d < 10; d++) {
        if (contagem[d] > 0) {
            printf("%d: %d\n", d, contagem[d]);
        }
    }
    free(contagem);
    return 0;
}
''',
    "calloc já entrega a memória zerada, ideal para contadores; o dígito lido serve de índice.",
    exemplo=("6\n1 3 3 7 1 3", "1: 2\n3: 3\n7: 1"),
)

_desafio(
    10, 3, "Lista que cresce com realloc", DESAFIADOR, 50,
    "Leia inteiros até aparecer 0 (sem saber quantos virão). Guarde-os em um vetor que cresce com "
    "realloc e, no fim, mostre-os na ordem inversa na mesma linha.",
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int capacidade = 2, quantidade = 0;
    int *v = malloc(capacidade * sizeof(int));
    if (v == NULL) {
        return 1;
    }
    /* leia até o 0, aumentando o vetor com realloc quando encher */
    free(v);
    return 0;
}
''',
    [
        "Quando quantidade == capacidade, dobre a capacidade.",
        "Use um ponteiro temporário: int *novo = realloc(v, ...); se for NULL, o v antigo continua válido.",
        "No final, percorra de quantidade - 1 até 0 e não esqueça do free.",
    ],
    {
        "codigo_contem": ["realloc", "free"],
        "testes": [
            _teste("4 8 15 0\n", "15 8 4"),
            _teste("7 0\n", "7"),
            _teste("1 2 3 4 5 6 0\n", "6 5 4 3 2 1"),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int capacidade = 2, quantidade = 0;
    int *v = malloc(capacidade * sizeof(int));
    if (v == NULL) {
        return 1;
    }
    int numero;
    while (scanf("%d", &numero) == 1 && numero != 0) {
        if (quantidade == capacidade) {
            capacidade *= 2;
            int *novo = realloc(v, capacidade * sizeof(int));
            if (novo == NULL) {   /* v continua válido */
                free(v);
                return 1;
            }
            v = novo;
        }
        v[quantidade++] = numero;
    }
    for (int i = quantidade - 1; i >= 0; i--) {
        printf("%d ", v[i]);
    }
    printf("\n");
    free(v);
    return 0;
}
''',
    "Dobrar a capacidade evita chamar realloc a cada número; o ponteiro temporário protege contra falha.",
    exemplo=("4 8 15 0", "15 8 4"),
)

_desafio(
    10, 4, "Duplicar texto", MEDIO, 48,
    "Crie char *duplicar(const char *s) que aloca exatamente o espaço necessário, copia o texto e "
    'devolve a cópia. Leia uma palavra e mostre "Copia: PALAVRA" e "Bytes: N" (tamanho alocado).',
    r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* crie char *duplicar(const char *s) */

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    /* duplique, mostre e libere */
    return 0;
}
''',
    [
        "O espaço necessário é strlen(s) + 1: o +1 guarda o '\\0'.",
        "Depois do malloc, use strcpy para copiar o texto.",
        "Quem recebe a cópia é responsável pelo free.",
    ],
    {
        "codigo_contem": ["malloc", "strlen", "free"],
        "min_ocorrencias_codigo": {"duplicar(": 2},
        "testes": [
            _teste("memoria\n", "Copia: memoria", "Bytes: 8"),
            _teste("C\n", "Copia: C", "Bytes: 2"),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *duplicar(const char *s) {
    char *copia = malloc(strlen(s) + 1);  /* +1 para o '\0' */
    if (copia != NULL) {
        strcpy(copia, s);
    }
    return copia;
}

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    char *copia = duplicar(palavra);
    if (copia == NULL) {
        return 1;
    }
    printf("Copia: %s\n", copia);
    printf("Bytes: %zu\n", strlen(copia) + 1);
    free(copia);
    return 0;
}
''',
    "A memória do malloc continua existindo depois que a função retorna, por isso main precisa liberá-la.",
    exemplo=("memoria", "Copia: memoria\nBytes: 8"),
)

_desafio(
    10, 5, "Sequência sem vazamento", MEDIO, 52,
    "Crie int *criarSequencia(int n) que aloca um vetor com os valores 1, 2, ..., n e o devolve. Em main "
    'leia N, some os valores do vetor, mostre "Soma: S" e libere a memória.',
    r'''
#include <stdio.h>
#include <stdlib.h>

/* crie int *criarSequencia(int n) */

int main(void) {
    int n;
    scanf("%d", &n);
    /* use a sequência e libere */
    return 0;
}
''',
    [
        "Dentro da função: int *v = malloc(n * sizeof(int)); e preencha v[i] = i + 1.",
        "Devolva o ponteiro com return v;",
        "Em main, depois de somar, chame free para não haver vazamento de memória.",
    ],
    {
        "codigo_contem": ["malloc", "free", "return"],
        "min_ocorrencias_codigo": {"criarsequencia(": 2},
        "testes": [
            _teste("5\n", regex=[r"soma: 15\b"]),
            _teste("10\n", regex=[r"soma: 55\b"]),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

int *criarSequencia(int n) {
    int *v = malloc(n * sizeof(int));
    if (v == NULL) {
        return NULL;
    }
    for (int i = 0; i < n; i++) {
        v[i] = i + 1;
    }
    return v;
}

int main(void) {
    int n;
    scanf("%d", &n);
    int *sequencia = criarSequencia(n);
    if (sequencia == NULL) {
        return 1;
    }
    int soma = 0;
    for (int i = 0; i < n; i++) {
        soma += sequencia[i];
    }
    printf("Soma: %d\n", soma);
    free(sequencia);  /* quem usa por último libera */
    return 0;
}
''',
    "A função cria a memória e main, que é a última a usar, faz o free: assim nada vaza.",
    exemplo=("5", "Soma: 15"),
)

# ---------------------------------------------------------------------------
# Módulo 11 · Agrupando informações
# ---------------------------------------------------------------------------

_desafio(
    11, 1, "Boletim do aluno", FACIL, 54,
    "Crie typedef struct Aluno com nome (texto), nota1 e nota2 (double). Leia nome e duas notas e mostre "
    '"NOME: MEDIA SITUACAO", com média de duas casas e situação Aprovado (média >= 7) ou Reprovado.',
    r'''
#include <stdio.h>

/* crie typedef struct { ... } Aluno; */

int main(void) {
    /* leia os dados em uma variável Aluno */
    return 0;
}
''',
    [
        "typedef struct { char nome[30]; double nota1; double nota2; } Aluno;",
        'Leia com scanf("%29s %lf %lf", a.nome, &a.nota1, &a.nota2); (nome não leva &).',
        "Calcule a média e use o ternário ou if para escolher a situação.",
    ],
    {
        "codigo_contem": ["typedef", "struct"],
        "testes": [
            _teste("Ana 7 9\n", "Ana: 8.00", "Aprovado", nao_contem=["Reprovado"]),
            _teste("Beto 4 6\n", "Beto: 5.00", "Reprovado"),
        ],
    },
    r'''
#include <stdio.h>

typedef struct {
    char nome[30];
    double nota1;
    double nota2;
} Aluno;

int main(void) {
    Aluno a;
    scanf("%29s %lf %lf", a.nome, &a.nota1, &a.nota2);
    double media = (a.nota1 + a.nota2) / 2;
    printf("%s: %.2f %s\n", a.nome, media, media >= 7 ? "Aprovado" : "Reprovado");
    return 0;
}
''',
    "A struct agrupa os dados do aluno e o ponto (a.nota1) acessa cada campo.",
    exemplo=("Ana 7 9", "Ana: 8.00 Aprovado"),
)

_desafio(
    11, 2, "Produto mais barato", MEDIO, 53,
    "Crie struct Produto com nome e preco. Leia 3 produtos (nome e preço) em um vetor de structs e "
    'mostre "Mais barato: NOME (PRECO)" com o preço em duas casas.',
    r'''
#include <stdio.h>

struct Produto {
    char nome[30];
    double preco;
};

int main(void) {
    struct Produto itens[3];
    /* leia os 3 produtos e ache o mais barato */
    return 0;
}
''',
    [
        'Leia cada item com scanf("%29s %lf", itens[i].nome, &itens[i].preco);',
        "Guarde o índice do mais barato (comece com 0) em vez de copiar a struct.",
        'printf("Mais barato: %s (%.2f)\\n", itens[m].nome, itens[m].preco);',
    ],
    {
        "codigo_contem": ["struct", "[3]"],
        "testes": [
            _teste("Arroz 5.5\nFeijao 7.2\nSal 2.1\n", "Mais barato: Sal (2.10)"),
            _teste("Cafe 12\nLeite 4.5\nPao 9\n", "Mais barato: Leite (4.50)"),
        ],
    },
    r'''
#include <stdio.h>

struct Produto {
    char nome[30];
    double preco;
};

int main(void) {
    struct Produto itens[3];
    for (int i = 0; i < 3; i++) {
        scanf("%29s %lf", itens[i].nome, &itens[i].preco);
    }
    int m = 0;                      /* índice do mais barato */
    for (int i = 1; i < 3; i++) {
        if (itens[i].preco < itens[m].preco) {
            m = i;
        }
    }
    printf("Mais barato: %s (%.2f)\n", itens[m].nome, itens[m].preco);
    return 0;
}
''',
    "Um vetor de structs guarda vários registros; itens[i].preco acessa o campo de cada um.",
    exemplo=("Arroz 5.5 Feijao 7.2 Sal 2.1", "Mais barato: Sal (2.10)"),
)

_desafio(
    11, 3, "Dia da semana com enum", MEDIO, 56,
    "Crie enum DiaSemana com DOMINGO = 1 até SABADO. Leia um número e, com switch sobre o enum, mostre o "
    'nome do dia (Domingo, Segunda, Terca, Quarta, Quinta, Sexta, Sabado) ou "Invalido".',
    r'''
#include <stdio.h>

/* crie enum DiaSemana { DOMINGO = 1, ... }; */

int main(void) {
    int numero;
    scanf("%d", &numero);
    /* use switch com os nomes do enum */
    return 0;
}
''',
    [
        "Se DOMINGO = 1, os próximos nomes recebem 2, 3, ... automaticamente.",
        "Nos case use os nomes do enum: case DOMINGO:",
        "O default cobre números fora de 1 a 7.",
    ],
    {
        "codigo_contem": ["enum", "switch", "DOMINGO"],
        "testes": [
            _teste("1\n", "Domingo"),
            _teste("7\n", "Sabado"),
            _teste("4\n", "Quarta"),
            _teste("9\n", "Invalido"),
        ],
    },
    r'''
#include <stdio.h>

enum DiaSemana { DOMINGO = 1, SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO };

int main(void) {
    int numero;
    scanf("%d", &numero);
    switch (numero) {
        case DOMINGO: printf("Domingo\n"); break;
        case SEGUNDA: printf("Segunda\n"); break;
        case TERCA:   printf("Terca\n");   break;
        case QUARTA:  printf("Quarta\n");  break;
        case QUINTA:  printf("Quinta\n");  break;
        case SEXTA:   printf("Sexta\n");   break;
        case SABADO:  printf("Sabado\n");  break;
        default:      printf("Invalido\n");
    }
    return 0;
}
''',
    "O enum dá nomes aos números 1 a 7, deixando os case muito mais fáceis de ler.",
    exemplo=("4", "Quarta"),
)

_desafio(
    11, 4, "Retângulo com funções", FACIL, 54,
    "Crie typedef struct Retangulo com largura e altura (int) e as funções int area(Retangulo r) e "
    'int perimetro(Retangulo r). Leia largura e altura e mostre "Area: A" e "Perimetro: P".',
    r'''
#include <stdio.h>

/* crie o typedef struct Retangulo e as funções area e perimetro */

int main(void) {
    /* leia largura e altura */
    return 0;
}
''',
    [
        "typedef struct { int largura; int altura; } Retangulo;",
        "A área é largura * altura e o perímetro é 2 * (largura + altura).",
        "Passe a struct inteira para a função: area(r).",
    ],
    {
        "codigo_contem": ["typedef", "struct"],
        "min_ocorrencias_codigo": {"area(": 2, "perimetro(": 2},
        "testes": [
            _teste("4 5\n", regex=[r"area: 20\b", r"perimetro: 18\b"]),
            _teste("7 7\n", regex=[r"area: 49\b", r"perimetro: 28\b"]),
        ],
    },
    r'''
#include <stdio.h>

typedef struct {
    int largura;
    int altura;
} Retangulo;

int area(Retangulo r) {
    return r.largura * r.altura;
}

int perimetro(Retangulo r) {
    return 2 * (r.largura + r.altura);
}

int main(void) {
    Retangulo r;
    scanf("%d %d", &r.largura, &r.altura);
    printf("Area: %d\n", area(r));
    printf("Perimetro: %d\n", perimetro(r));
    return 0;
}
''',
    "A struct viaja inteira para as funções, que só precisam ler os campos para calcular.",
    exemplo=("4 5", "Area: 20\nPerimetro: 18"),
)

_desafio(
    11, 5, "Struct dentro de struct", MEDIO, 53,
    "Crie struct Data (dia, mes, ano) e struct Pessoa com nome e um campo struct Data nascimento. Leia "
    'nome, dia, mês e ano e mostre "NOME nasceu em DD/MM/AAAA".',
    r'''
#include <stdio.h>

/* crie struct Data e struct Pessoa (com o campo nascimento) */

int main(void) {
    /* leia os dados em uma struct Pessoa */
    return 0;
}
''',
    [
        "Declare struct Data antes de struct Pessoa, porque Pessoa usa Data.",
        "Acesse campos aninhados com dois pontos: p.nascimento.dia",
        'Use %02d para dia e mês: "%s nasceu em %02d/%02d/%d\\n".',
    ],
    {
        "codigo_contem": ["nascimento."],
        "min_ocorrencias_codigo": {"struct": 3},
        "testes": [
            _teste("Ana 5 9 2001\n", "Ana nasceu em 05/09/2001"),
            _teste("Rui 23 11 1998\n", "Rui nasceu em 23/11/1998"),
        ],
    },
    r'''
#include <stdio.h>

struct Data {
    int dia;
    int mes;
    int ano;
};

struct Pessoa {
    char nome[30];
    struct Data nascimento;  /* uma struct dentro da outra */
};

int main(void) {
    struct Pessoa p;
    scanf("%29s %d %d %d", p.nome, &p.nascimento.dia, &p.nascimento.mes, &p.nascimento.ano);
    printf("%s nasceu em %02d/%02d/%d\n",
           p.nome, p.nascimento.dia, p.nascimento.mes, p.nascimento.ano);
    return 0;
}
''',
    "Structs podem conter outras structs; cada ponto desce um nível até o campo desejado.",
    exemplo=("Ana 5 9 2001", "Ana nasceu em 05/09/2001"),
)

# ---------------------------------------------------------------------------
# Módulo 12 · Salvando dados
# ---------------------------------------------------------------------------

_desafio(
    12, 1, "Somar pelo arquivo", FACIL, 60,
    'Leia três inteiros, grave-os em "numeros.txt" com fprintf e feche o arquivo. Depois reabra para '
    'leitura, leia os números com fscanf e mostre "Soma: S".',
    r'''
#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    /* 1) grave em numeros.txt  2) feche  3) reabra e leia com fscanf */
    return 0;
}
''',
    [
        'Abra para escrita com fopen("numeros.txt", "w") e verifique se voltou NULL.',
        'fprintf(arquivo, "%d %d %d\\n", a, b, c); grava os números; depois fclose.',
        'Reabra com "r", leia com fscanf(arquivo, "%d %d %d", &x, &y, &z) e feche de novo.',
    ],
    {
        "codigo_contem": ["fopen", "fprintf", "fscanf", "fclose"],
        "testes": [
            _teste("4 5 6\n", regex=[r"soma: 15\b"]),
            _teste("10 -3 7\n", regex=[r"soma: 14\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);

    FILE *arquivo = fopen("numeros.txt", "w");
    if (arquivo == NULL) {
        printf("Erro ao criar o arquivo\n");
        return 1;
    }
    fprintf(arquivo, "%d %d %d\n", a, b, c);
    fclose(arquivo);                         /* garante a gravação */

    arquivo = fopen("numeros.txt", "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo\n");
        return 1;
    }
    int x, y, z;
    if (fscanf(arquivo, "%d %d %d", &x, &y, &z) == 3) {
        printf("Soma: %d\n", x + y + z);
    }
    fclose(arquivo);
    return 0;
}
''',
    "Fechar depois de gravar garante que os dados estão no arquivo antes de reabri-lo para leitura.",
    exemplo=("4 5 6", "Soma: 15"),
)

_desafio(
    12, 2, "Contar linhas do arquivo", MEDIO, 59,
    'Leia N e depois N palavras. Grave cada palavra em uma linha de "palavras.txt". Reabra o arquivo, '
    'conte as linhas lendo com fgets e mostre "Linhas: N".',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* grave as palavras, uma por linha */
    /* reabra e conte as linhas com fgets */
    return 0;
}
''',
    [
        'Leia cada palavra com scanf("%49s", palavra) e grave com fprintf(arquivo, "%s\\n", palavra).',
        "Para contar, repita while (fgets(linha, sizeof linha, arquivo) != NULL).",
        "Cada fgets bem-sucedido lê uma linha: some 1 a cada volta.",
    ],
    {
        "codigo_contem": ["fopen", "fgets", "fclose"],
        "testes": [
            _teste("3\nsol\nlua\nmar\n", regex=[r"linhas: 3\b"]),
            _teste("1\nC\n", regex=[r"linhas: 1\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    FILE *arquivo = fopen("palavras.txt", "w");
    if (arquivo == NULL) {
        return 1;
    }
    char palavra[50];
    for (int i = 0; i < n; i++) {
        scanf("%49s", palavra);
        fprintf(arquivo, "%s\n", palavra);
    }
    fclose(arquivo);

    arquivo = fopen("palavras.txt", "r");
    if (arquivo == NULL) {
        return 1;
    }
    char linha[100];
    int linhas = 0;
    while (fgets(linha, sizeof linha, arquivo) != NULL) {  /* NULL = fim do arquivo */
        linhas++;
    }
    fclose(arquivo);
    printf("Linhas: %d\n", linhas);
    return 0;
}
''',
    "fgets devolve NULL quando o arquivo acaba, o que torna o laço de leitura simples e seguro.",
    exemplo=("3\nsol\nlua\nmar", "Linhas: 3"),
)

_desafio(
    12, 3, "Configuração padrão", FACIL, 57,
    'Tente abrir "config.txt" para leitura. Se não existir (fopen devolve NULL), crie-o com o texto '
    '"volume 7". Depois leia o nome e o valor do arquivo e mostre "volume = 7".',
    r'''
#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("config.txt", "r");
    /* se for NULL, crie o arquivo com "volume 7" */
    /* depois leia e mostre: volume = 7 */
    return 0;
}
''',
    [
        'Se arquivo == NULL, abra com "w", grave "volume 7\\n", feche e abra de novo com "r".',
        'Leia com fscanf(arquivo, "%19s %d", nome, &valor).',
        "Sempre feche o arquivo com fclose no final.",
    ],
    {
        "codigo_contem": ["NULL", "fscanf", "fclose"],
        "saida_contem": ["volume = 7"],
    },
    r'''
#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("config.txt", "r");
    if (arquivo == NULL) {                   /* não existe: cria o padrão */
        arquivo = fopen("config.txt", "w");
        if (arquivo == NULL) {
            return 1;
        }
        fprintf(arquivo, "volume 7\n");
        fclose(arquivo);
        arquivo = fopen("config.txt", "r");
        if (arquivo == NULL) {
            return 1;
        }
    }
    char nome[20];
    int valor;
    if (fscanf(arquivo, "%19s %d", nome, &valor) == 2) {
        printf("%s = %d\n", nome, valor);
    }
    fclose(arquivo);
    return 0;
}
''',
    "Testar o NULL evita usar um arquivo inexistente e permite criar um padrão na primeira execução.",
    exemplo=("", "volume = 7"),
)

_desafio(
    12, 4, "Diário com modo de acréscimo", MEDIO, 59,
    'Crie "log.txt" com a linha "inicio". Depois reabra no modo "a" e acrescente uma palavra lida do '
    'teclado. Por fim leia o arquivo e mostre cada linha numerada: "1: inicio", "2: PALAVRA".',
    r'''
#include <stdio.h>

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);
    /* 1) "w" com inicio  2) "a" com a palavra  3) "r" mostrando as linhas numeradas */
    return 0;
}
''',
    [
        'O modo "w" apaga o arquivo; o modo "a" escreve no final sem apagar o que já existe.',
        "Leia as linhas com fgets e remova o \\n com linha[strcspn(linha, \"\\n\")] = '\\0';",
        "Use um contador para numerar as linhas ao mostrar.",
    ],
    {
        "codigo_contem": ['"a"', "fgets", "fclose"],
        "testes": [
            _teste("fim\n", "1: inicio", "2: fim"),
            _teste("teste\n", "1: inicio", "2: teste", nao_contem=["3:"]),
        ],
    },
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char palavra[50];
    scanf("%49s", palavra);

    FILE *arquivo = fopen("log.txt", "w");      /* começa do zero */
    if (arquivo == NULL) {
        return 1;
    }
    fprintf(arquivo, "inicio\n");
    fclose(arquivo);

    arquivo = fopen("log.txt", "a");            /* acrescenta no final */
    if (arquivo == NULL) {
        return 1;
    }
    fprintf(arquivo, "%s\n", palavra);
    fclose(arquivo);

    arquivo = fopen("log.txt", "r");
    if (arquivo == NULL) {
        return 1;
    }
    char linha[100];
    int numero = 1;
    while (fgets(linha, sizeof linha, arquivo) != NULL) {
        linha[strcspn(linha, "\n")] = '\0';
        printf("%d: %s\n", numero++, linha);
    }
    fclose(arquivo);
    return 0;
}
''',
    'O modo "a" preserva o conteúdo e grava no fim; é o modo usado em arquivos de registro (log).',
    exemplo=("fim", "1: inicio\n2: fim"),
)

_desafio(
    12, 5, "Maior valor do arquivo", MEDIO, 60,
    'Leia N e N inteiros e grave-os em "valores.txt". Reabra e leia com while (fscanf(...) == 1) até o fim, '
    'mostrando "Maior no arquivo: X".',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* grave os n valores e depois procure o maior lendo o arquivo */
    return 0;
}
''',
    [
        "fscanf devolve quantos valores conseguiu ler; no fim do arquivo ele não devolve 1.",
        "Use uma variável achou = 0 para saber se já leu o primeiro valor.",
        "O primeiro valor lido vira o maior inicial; os próximos são comparados com ele.",
    ],
    {
        "codigo_contem": ["fprintf", "fscanf", "while"],
        "testes": [
            _teste("5\n3 9 2 7 1\n", regex=[r"maior no arquivo: 9\b"]),
            _teste("3\n-4 -1 -8\n", regex=[r"maior no arquivo: -1\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    FILE *arquivo = fopen("valores.txt", "w");
    if (arquivo == NULL) {
        return 1;
    }
    for (int i = 0; i < n; i++) {
        int valor;
        scanf("%d", &valor);
        fprintf(arquivo, "%d\n", valor);
    }
    fclose(arquivo);

    arquivo = fopen("valores.txt", "r");
    if (arquivo == NULL) {
        return 1;
    }
    int valor, maior = 0, achou = 0;
    while (fscanf(arquivo, "%d", &valor) == 1) {  /* para no fim do arquivo */
        if (!achou || valor > maior) {
            maior = valor;
            achou = 1;
        }
    }
    fclose(arquivo);
    if (achou) {
        printf("Maior no arquivo: %d\n", maior);
    }
    return 0;
}
''',
    "Comparar o retorno do fscanf com 1 lê o arquivo inteiro sem precisar saber quantos números existem.",
    exemplo=("5\n3 9 2 7 1", "Maior no arquivo: 9"),
)

# ---------------------------------------------------------------------------
# Módulo 13 · Dividindo o programa em partes
# ---------------------------------------------------------------------------

_desafio(
    13, 1, "Biblioteca de áreas", FACIL, 61,
    "Simule um .h no topo do arquivo: declare os protótipos int areaQuadrado(int lado) e "
    "int areaRetangulo(int base, int altura) antes de main e implemente as funções depois de main. "
    'Leia lado, base e altura e mostre "Quadrado: A" e "Retangulo: B".',
    r'''
#include <stdio.h>

/* ---- "geometria.h": protótipos ---- */

int main(void) {
    int lado, base, altura;
    scanf("%d %d %d", &lado, &base, &altura);
    /* use as funções */
    return 0;
}

/* ---- "geometria.c": implementações ---- */
''',
    [
        "Um protótipo é a assinatura da função seguida de ponto e vírgula.",
        "Com os protótipos no topo, main pode chamar funções que só aparecem depois.",
        "areaQuadrado devolve lado * lado; areaRetangulo devolve base * altura.",
    ],
    {
        "min_ocorrencias_codigo": {"areaquadrado(": 3, "arearetangulo(": 3},
        "testes": [
            _teste("3 4 5\n", regex=[r"quadrado: 9\b", r"retangulo: 20\b"]),
            _teste("10 2 7\n", regex=[r"quadrado: 100\b", r"retangulo: 14\b"]),
        ],
    },
    r'''
#include <stdio.h>

/* ---- "geometria.h": protótipos ---- */
int areaQuadrado(int lado);
int areaRetangulo(int base, int altura);

int main(void) {
    int lado, base, altura;
    scanf("%d %d %d", &lado, &base, &altura);
    printf("Quadrado: %d\n", areaQuadrado(lado));
    printf("Retangulo: %d\n", areaRetangulo(base, altura));
    return 0;
}

/* ---- "geometria.c": implementações ---- */
int areaQuadrado(int lado) {
    return lado * lado;
}

int areaRetangulo(int base, int altura) {
    return base * altura;
}
''',
    "Os protótipos fazem o papel do .h: dizem o que existe, e as implementações podem vir em outro lugar.",
    exemplo=("3 4 5", "Quadrado: 9\nRetangulo: 20"),
)

_desafio(
    13, 2, "Guarda de inclusão", MEDIO, 63,
    "Crie uma seção de cabeçalho protegida por #ifndef CONVERSOR_H / #define CONVERSOR_H / #endif com o "
    "protótipo void mostrarHoras(int minutos). Leia um total de minutos e mostre no formato \"2h15min\".",
    r'''
#include <stdio.h>

/* crie a guarda CONVERSOR_H com o protótipo aqui */

int main(void) {
    int minutos;
    scanf("%d", &minutos);
    /* chame mostrarHoras */
    return 0;
}
''',
    [
        "A guarda começa com #ifndef CONVERSOR_H e #define CONVERSOR_H e termina com #endif.",
        "Horas são minutos / 60 e o que sobra é minutos % 60.",
        'printf("%dh%02dmin\\n", horas, resto);',
    ],
    {
        "codigo_contem": ["#ifndef CONVERSOR_H", "#define CONVERSOR_H", "#endif"],
        "min_ocorrencias_codigo": {"mostrarhoras(": 3},
        "testes": [
            _teste("135\n", "2h15min"),
            _teste("59\n", "0h59min"),
            _teste("120\n", "2h00min"),
        ],
    },
    r'''
#include <stdio.h>

#ifndef CONVERSOR_H
#define CONVERSOR_H
void mostrarHoras(int minutos);
#endif /* CONVERSOR_H */

int main(void) {
    int minutos;
    scanf("%d", &minutos);
    mostrarHoras(minutos);
    return 0;
}

void mostrarHoras(int minutos) {
    printf("%dh%02dmin\n", minutos / 60, minutos % 60);
}
''',
    "A guarda impede que o mesmo cabeçalho seja processado duas vezes quando é incluído por vários arquivos.",
    exemplo=("135", "2h15min"),
)

_desafio(
    13, 3, "Gerador de IDs com static", MEDIO, 62,
    "Crie int proximoId(void) que guarda um contador static e devolve 1, 2, 3... a cada chamada. "
    'Leia N e mostre "ID 1" até "ID N", um por linha, sempre chamando a função.',
    r'''
#include <stdio.h>

/* crie int proximoId(void) com um contador static */

int main(void) {
    int n;
    scanf("%d", &n);
    /* chame proximoId n vezes */
    return 0;
}
''',
    [
        "Uma variável static dentro da função mantém o valor entre as chamadas.",
        "static int contador = 0; só é inicializada uma vez.",
        "Faça contador++ e devolva o novo valor.",
    ],
    {
        "codigo_contem": ["static"],
        "min_ocorrencias_codigo": {"proximoid(": 2},
        "testes": [
            _teste("3\n", "ID 1", "ID 2", "ID 3", nao_contem=["ID 4"]),
            _teste("1\n", "ID 1", nao_contem=["ID 2"]),
        ],
    },
    r'''
#include <stdio.h>

int proximoId(void) {
    static int contador = 0;  /* mantém o valor entre as chamadas */
    contador++;
    return contador;
}

int main(void) {
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("ID %d\n", proximoId());
    }
    return 0;
}
''',
    "static faz a variável viver o programa inteiro, mas ela continua visível só dentro da função.",
    exemplo=("3", "ID 1\nID 2\nID 3"),
)

_desafio(
    13, 4, "Validador de notas", FACIL, 62,
    "Declare o protótipo int notaValida(double nota) antes de main e implemente depois. Leia 4 notas e "
    'mostre "Validas: N", contando as que estão entre 0 e 10.',
    r'''
#include <stdio.h>

/* protótipo de notaValida */

int main(void) {
    int validas = 0;
    /* leia 4 notas e conte as válidas */
    printf("Validas: %d\n", validas);
    return 0;
}

/* implementação de notaValida */
''',
    [
        "A função pode ser uma linha: return nota >= 0 && nota <= 10;",
        "Leia as notas em um for com scanf(\"%lf\", &nota).",
        "Some 1 em validas quando notaValida(nota) for verdadeiro.",
    ],
    {
        "min_ocorrencias_codigo": {"notavalida(": 3},
        "testes": [
            _teste("8 11 -1 7\n", regex=[r"validas: 2\b"]),
            _teste("10 0 5.5 9\n", regex=[r"validas: 4\b"]),
        ],
    },
    r'''
#include <stdio.h>

int notaValida(double nota);

int main(void) {
    int validas = 0;
    for (int i = 0; i < 4; i++) {
        double nota;
        scanf("%lf", &nota);
        if (notaValida(nota)) {
            validas++;
        }
    }
    printf("Validas: %d\n", validas);
    return 0;
}

int notaValida(double nota) {
    return nota >= 0 && nota <= 10;
}
''',
    "Separar a regra em uma função com protótipo deixa main curto e a regra fácil de reutilizar.",
    exemplo=("8 11 -1 7", "Validas: 2"),
)

_desafio(
    13, 5, "Somar minutos ao horário", DESAFIADOR, 62,
    "No topo declare typedef struct Horario (hora, minuto) e o protótipo Horario somarMinutos(Horario h, "
    "int minutos); implemente depois de main. Leia hora, minuto e quantos minutos somar e mostre o novo "
    "horário como HH:MM (depois de 23:59 volta para 00:00).",
    r'''
#include <stdio.h>

/* typedef struct Horario e protótipo de somarMinutos */

int main(void) {
    int hora, minuto, somar;
    scanf("%d %d %d", &hora, &minuto, &somar);
    /* monte o Horario, chame somarMinutos e mostre HH:MM */
    return 0;
}
''',
    [
        "Converta tudo para minutos: total = h.hora * 60 + h.minuto + minutos.",
        "Um dia tem 1440 minutos; total % 1440 faz o horário dar a volta.",
        "Depois separe de novo: hora = total / 60, minuto = total % 60, e mostre com %02d.",
    ],
    {
        "codigo_contem": ["typedef", "struct"],
        "min_ocorrencias_codigo": {"somarminutos(": 3},
        "testes": [
            _teste("10 50 25\n", "11:15"),
            _teste("23 30 45\n", "00:15"),
            _teste("8 0 0\n", "08:00"),
        ],
    },
    r'''
#include <stdio.h>

typedef struct {
    int hora;
    int minuto;
} Horario;

Horario somarMinutos(Horario h, int minutos);

int main(void) {
    int hora, minuto, somar;
    scanf("%d %d %d", &hora, &minuto, &somar);
    Horario inicio = {hora, minuto};
    Horario fim = somarMinutos(inicio, somar);
    printf("%02d:%02d\n", fim.hora, fim.minuto);
    return 0;
}

Horario somarMinutos(Horario h, int minutos) {
    int total = (h.hora * 60 + h.minuto + minutos) % 1440;  /* 1440 = minutos do dia */
    Horario resultado = {total / 60, total % 60};
    return resultado;
}
''',
    "Trabalhar tudo em minutos simplifica a conta; o resto por 1440 cuida da virada da meia-noite.",
    exemplo=("10 50 25", "11:15"),
)

# ---------------------------------------------------------------------------
# Módulo 14 · Usando recursos prontos
# ---------------------------------------------------------------------------

_desafio(
    14, 1, "Hipotenusa", FACIL, 67,
    'Leia os dois catetos (double) e mostre "Hipotenusa: X.XX" usando sqrt da math.h.',
    r'''
#include <stdio.h>

int main(void) {
    double a, b;
    scanf("%lf %lf", &a, &b);
    /* calcule a hipotenusa */
    return 0;
}
''',
    [
        "Inclua #include <math.h> para usar sqrt.",
        "A hipotenusa é a raiz de a * a + b * b.",
        'Mostre com printf("Hipotenusa: %.2f\\n", h);',
    ],
    {
        "codigo_contem": ["math.h", "sqrt"],
        "testes": [
            _teste("3 4\n", "Hipotenusa: 5.00"),
            _teste("5 12\n", "Hipotenusa: 13.00"),
            _teste("1 1\n", "Hipotenusa: 1.41"),
        ],
    },
    r'''
#include <stdio.h>
#include <math.h>

int main(void) {
    double a, b;
    scanf("%lf %lf", &a, &b);
    double h = sqrt(a * a + b * b);  /* Pitágoras */
    printf("Hipotenusa: %.2f\n", h);
    return 0;
}
''',
    "sqrt vem da biblioteca matemática; o compilador precisa de -lm para ligá-la, o que o site já faz.",
    exemplo=("3 4", "Hipotenusa: 5.00"),
)

_desafio(
    14, 2, "Número validado com strtol", MEDIO, 65,
    'Leia uma linha com fgets e converta com strtol. Se a linha for um número inteiro completo, mostre '
    '"Numero: N"; se tiver letras ou estiver vazia, mostre "Entrada invalida".',
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char linha[64];
    if (fgets(linha, sizeof linha, stdin) == NULL) {
        return 0;
    }
    /* use strtol(linha, &fim, 10) e confira onde a leitura parou */
    return 0;
}
''',
    [
        "strtol recebe o endereço de um char *fim e o faz apontar para onde a conversão parou.",
        "Se fim == linha, nenhum dígito foi lido.",
        "Depois do número só pode vir '\\n' ou '\\0'; qualquer outra coisa torna a entrada inválida.",
    ],
    {
        "codigo_contem": ["strtol"],
        "testes": [
            _teste("123\n", "Numero: 123", nao_contem=["invalida"]),
            _teste("-7\n", "Numero: -7", nao_contem=["invalida"]),
            _teste("12abc\n", "Entrada invalida"),
            _teste("abc\n", "Entrada invalida"),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char linha[64];
    if (fgets(linha, sizeof linha, stdin) == NULL) {
        return 0;
    }
    char *fim;
    long numero = strtol(linha, &fim, 10);
    if (fim == linha || (*fim != '\n' && *fim != '\0')) {  /* nada lido ou sobrou texto */
        printf("Entrada invalida\n");
    } else {
        printf("Numero: %ld\n", numero);
    }
    return 0;
}
''',
    "O ponteiro fim mostra até onde strtol conseguiu converter; sobras indicam que a entrada não era só um número.",
    exemplo=("12abc", "Entrada invalida"),
)

_desafio(
    14, 3, "Piso, teto e arredondado", FACIL, 67,
    'Leia um número real e mostre "Piso: X", "Teto: Y" e "Arredondado: Z" usando floor, ceil e round, '
    "sem casas decimais.",
    r'''
#include <stdio.h>
#include <math.h>

int main(void) {
    double x;
    scanf("%lf", &x);
    /* use floor, ceil e round */
    return 0;
}
''',
    [
        "floor arredonda para baixo, ceil para cima e round para o inteiro mais próximo.",
        "As três funções devolvem double; mostre com %.0f para não aparecer casa decimal.",
        "Cuidado com negativos: floor(-1.2) é -2.",
    ],
    {
        "codigo_contem": ["floor", "ceil", "round"],
        "testes": [
            _teste("2.5\n", regex=[r"piso: 2\b", r"teto: 3\b", r"arredondado: 3\b"]),
            _teste("-1.2\n", regex=[r"piso: -2\b", r"teto: -1\b", r"arredondado: -1\b"]),
            _teste("7\n", regex=[r"piso: 7\b", r"teto: 7\b", r"arredondado: 7\b"]),
        ],
    },
    r'''
#include <stdio.h>
#include <math.h>

int main(void) {
    double x;
    scanf("%lf", &x);
    printf("Piso: %.0f\n", floor(x));        /* para baixo */
    printf("Teto: %.0f\n", ceil(x));         /* para cima */
    printf("Arredondado: %.0f\n", round(x)); /* mais próximo */
    return 0;
}
''',
    "Cada função arredonda em uma direção; com negativos, 'para baixo' significa mais longe do zero.",
    exemplo=("2.5", "Piso: 2\nTeto: 3\nArredondado: 3"),
)

_desafio(
    14, 4, "Ordenar com qsort", DESAFIADOR, 65,
    "Leia N e N inteiros e ordene-os em ordem crescente com qsort da stdlib.h, escrevendo a função de "
    "comparação. Mostre os valores ordenados na mesma linha.",
    r'''
#include <stdio.h>
#include <stdlib.h>

/* crie int comparar(const void *a, const void *b) */

int main(void) {
    int n;
    scanf("%d", &n);
    int v[100];
    for (int i = 0; i < n && i < 100; i++) {
        scanf("%d", &v[i]);
    }
    /* chame qsort(v, n, sizeof v[0], comparar) */
    return 0;
}
''',
    [
        "A comparação recebe ponteiros genéricos: converta com *(const int *)a.",
        "Devolva negativo se a vem antes, positivo se vem depois e zero se forem iguais.",
        "(x > y) - (x < y) devolve -1, 0 ou 1 sem risco de estouro.",
    ],
    {
        "codigo_contem": ["qsort", "const void"],
        "testes": [
            _teste("5\n42 7 19 3 8\n", "3 7 8 19 42"),
            _teste("4\n-1 -5 10 0\n", "-5 -1 0 10"),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

int comparar(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return (x > y) - (x < y);  /* -1, 0 ou 1 */
}

int main(void) {
    int n;
    scanf("%d", &n);
    if (n > 100) {
        n = 100;
    }
    int v[100];
    for (int i = 0; i < n; i++) {
        scanf("%d", &v[i]);
    }
    qsort(v, n, sizeof v[0], comparar);
    for (int i = 0; i < n; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}
''',
    "qsort ordena qualquer tipo de vetor; ele só precisa saber o tamanho de cada item e como comparar dois.",
    exemplo=("5\n42 7 19 3 8", "3 7 8 19 42"),
)

_desafio(
    14, 5, "Procurar palavra na frase", MEDIO, 66,
    "Leia uma frase (primeira linha) e uma palavra (segunda linha) com fgets. Use strstr para procurar a "
    'palavra e mostre "Encontrado na posicao N" (contando do 0) ou "Nao encontrado".',
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char frase[100], palavra[30];
    fgets(frase, sizeof frase, stdin);
    fgets(palavra, sizeof palavra, stdin);
    /* remova os \n e use strstr */
    return 0;
}
''',
    [
        "Remova o Enter de cada texto com texto[strcspn(texto, \"\\n\")] = '\\0';",
        "strstr(frase, palavra) devolve um ponteiro para o começo do trecho ou NULL.",
        "A posição é a diferença entre ponteiros: achou - frase.",
    ],
    {
        "codigo_contem": ["strstr"],
        "testes": [
            _teste("aprender C e divertido\nC\n", "Encontrado na posicao 9"),
            _teste("gosto de ponteiros\nvetor\n", "Nao encontrado"),
            _teste("ola mundo\nola\n", "Encontrado na posicao 0"),
        ],
    },
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char frase[100], palavra[30];
    if (fgets(frase, sizeof frase, stdin) == NULL || fgets(palavra, sizeof palavra, stdin) == NULL) {
        return 0;
    }
    frase[strcspn(frase, "\n")] = '\0';
    palavra[strcspn(palavra, "\n")] = '\0';

    char *achou = strstr(frase, palavra);
    if (achou != NULL) {
        printf("Encontrado na posicao %d\n", (int)(achou - frase));  /* distância do início */
    } else {
        printf("Nao encontrado\n");
    }
    return 0;
}
''',
    "strstr devolve o endereço do trecho encontrado; subtrair o início da frase dá o índice.",
    exemplo=("aprender C e divertido\nC", "Encontrado na posicao 9"),
)

# ---------------------------------------------------------------------------
# Módulo 15 · Como o computador guarda informações
# ---------------------------------------------------------------------------

_desafio(
    15, 1, "Par pelo último bit", FACIL, 68,
    'Leia um inteiro e mostre "Par" ou "Impar" olhando apenas o último bit com o operador & (sem usar %).',
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    /* teste numero & 1 */
    return 0;
}
''',
    [
        "Números ímpares sempre têm o último bit (o bit 0) igual a 1.",
        "numero & 1 vale 1 para ímpar e 0 para par.",
        "Use o resultado dentro de um if ou de um ternário.",
    ],
    {
        "codigo_contem": ["& 1"],
        "testes": [
            _teste("6\n", "Par", nao_contem=["Impar"]),
            _teste("9\n", "Impar"),
            _teste("0\n", "Par", nao_contem=["Impar"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    if (numero & 1) {        /* bit 0 ligado = ímpar */
        printf("Impar\n");
    } else {
        printf("Par\n");
    }
    return 0;
}
''',
    "Em binário o bit 0 vale 1; só os ímpares o têm ligado, e & 1 isola exatamente esse bit.",
    exemplo=("9", "Impar"),
)

_desafio(
    15, 2, "Contar bits ligados", MEDIO, 68,
    'Leia um inteiro sem sinal e mostre "Bits ligados: N", contando quantos bits valem 1.',
    r'''
#include <stdio.h>

int main(void) {
    unsigned int numero;
    scanf("%u", &numero);
    int ligados = 0;
    /* olhe o último bit e desloque para a direita até zerar */
    printf("Bits ligados: %d\n", ligados);
    return 0;
}
''',
    [
        "numero & 1u diz se o último bit está ligado.",
        "numero >>= 1 descarta o último bit e traz o próximo para o lugar dele.",
        "Repita enquanto numero != 0.",
    ],
    {
        "codigo_contem": [">>"],
        "testes": [
            _teste("13\n", regex=[r"bits ligados: 3\b"]),
            _teste("255\n", regex=[r"bits ligados: 8\b"]),
            _teste("0\n", regex=[r"bits ligados: 0\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    unsigned int numero;
    scanf("%u", &numero);
    int ligados = 0;
    while (numero != 0) {
        ligados += numero & 1u;  /* soma o bit atual */
        numero >>= 1;            /* passa para o próximo */
    }
    printf("Bits ligados: %d\n", ligados);
    return 0;
}
''',
    "Cada deslocamento traz um novo bit para a posição 0, onde & 1u consegue lê-lo.",
    exemplo=("13", "Bits ligados: 3"),
)

_desafio(
    15, 3, "Binário de 8 bits", MEDIO, 68,
    'Leia um número de 0 a 255 e mostre "Binario: " seguido dos 8 bits, do mais alto para o mais baixo.',
    r'''
#include <stdio.h>

int main(void) {
    unsigned int numero;
    scanf("%u", &numero);
    printf("Binario: ");
    /* mostre os bits 7, 6, ..., 0 */
    printf("\n");
    return 0;
}
''',
    [
        "O bit i pode ser lido com (numero >> i) & 1u.",
        "Percorra i de 7 até 0 para mostrar do bit mais alto para o mais baixo.",
        'Mostre cada bit com printf("%u", ...).',
    ],
    {
        "codigo_contem": [">>"],
        "testes": [
            _teste("5\n", "Binario: 00000101"),
            _teste("200\n", "Binario: 11001000"),
            _teste("255\n", "Binario: 11111111"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    unsigned int numero;
    scanf("%u", &numero);
    printf("Binario: ");
    for (int i = 7; i >= 0; i--) {
        printf("%u", (numero >> i) & 1u);  /* traz o bit i para a posição 0 */
    }
    printf("\n");
    return 0;
}
''',
    "Deslocar i posições para a direita e aplicar & 1u lê um bit por vez, na ordem escolhida.",
    exemplo=("5", "Binario: 00000101"),
)

_desafio(
    15, 4, "Permissões rwx", MEDIO, 69,
    "Defina LER = 4, ESCREVER = 2 e EXECUTAR = 1 com #define. Leia um número de 0 a 7 e mostre "
    '"Permissoes: " com r, w e x para os bits ligados e - para os desligados (ex.: 5 vira r-x).',
    r'''
#include <stdio.h>

/* crie #define LER, ESCREVER e EXECUTAR */

int main(void) {
    unsigned int permissoes;
    scanf("%u", &permissoes);
    printf("Permissoes: ");
    /* teste cada máscara com & */
    printf("\n");
    return 0;
}
''',
    [
        "(permissoes & LER) é diferente de zero quando o bit de leitura está ligado.",
        "Para cada máscara mostre a letra ou '-' com um ternário.",
        "A ordem é sempre r, depois w, depois x.",
    ],
    {
        "codigo_contem": ["#define", "LER", "ESCREVER", "EXECUTAR"],
        "testes": [
            _teste("5\n", "Permissoes: r-x"),
            _teste("7\n", "Permissoes: rwx"),
            _teste("0\n", "Permissoes: ---"),
            _teste("6\n", "Permissoes: rw-"),
        ],
    },
    r'''
#include <stdio.h>

#define LER      4u
#define ESCREVER 2u
#define EXECUTAR 1u

int main(void) {
    unsigned int permissoes;
    scanf("%u", &permissoes);
    printf("Permissoes: ");
    printf("%c", (permissoes & LER) ? 'r' : '-');
    printf("%c", (permissoes & ESCREVER) ? 'w' : '-');
    printf("%c", (permissoes & EXECUTAR) ? 'x' : '-');
    printf("\n");
    return 0;
}
''',
    "Cada permissão ocupa um bit; & com a máscara diz se aquele bit está ligado. É assim que o chmod funciona.",
    exemplo=("5", "Permissoes: r-x"),
)

_desafio(
    15, 5, "Potência de 2", DESAFIADOR, 68,
    'Leia um inteiro e mostre "Potencia de 2" ou "Nao e potencia de 2", usando a propriedade de bits: '
    "uma potência de 2 tem exatamente um bit ligado.",
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* use n & (n - 1) */
    return 0;
}
''',
    [
        "Subtrair 1 de uma potência de 2 liga todos os bits abaixo do único bit ligado (8 = 1000, 7 = 0111).",
        "Por isso n & (n - 1) é zero exatamente para as potências de 2.",
        "Não esqueça que n precisa ser maior que zero.",
    ],
    {
        "codigo_contem": ["&"],
        "testes": [
            _teste("64\n", "Potencia de 2", nao_contem=["Nao e"]),
            _teste("12\n", "Nao e potencia de 2"),
            _teste("1\n", "Potencia de 2", nao_contem=["Nao e"]),
            _teste("0\n", "Nao e potencia de 2"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    if (n > 0 && (n & (n - 1)) == 0) {  /* só um bit ligado */
        printf("Potencia de 2\n");
    } else {
        printf("Nao e potencia de 2\n");
    }
    return 0;
}
''',
    "n - 1 inverte o bit mais baixo ligado e todos abaixo dele; se sobrar zero no &, havia apenas um bit.",
    exemplo=("64", "Potencia de 2"),
)

# ---------------------------------------------------------------------------
# Módulo 16 · Encontrando e corrigindo erros
# ---------------------------------------------------------------------------

_desafio(
    16, 1, "Conserte a compilação", FACIL, 70,
    "O código inicial tem dois erros de sintaxe e não compila. Leia a mensagem do compilador, corrija os "
    'erros e faça o programa mostrar "Total: 15".',
    r'''
#include <stdio.h>

int main(void) {
    int total = 0
    for (int i = 1; i <= 5; i++) {
        total += i;
    }
    printf("Total: %d\n", total)
    return 0;
}
''',
    [
        "Compile e leia a primeira mensagem de erro: ela indica a linha e o que era esperado.",
        "O compilador costuma apontar a linha seguinte ao erro real.",
        "Procure instruções que terminam sem ponto e vírgula.",
    ],
    {
        "codigo_contem": ["for"],
        "saida_contem": ["Total: 15"],
    },
    r'''
#include <stdio.h>

int main(void) {
    int total = 0;                  /* faltava ; */
    for (int i = 1; i <= 5; i++) {
        total += i;
    }
    printf("Total: %d\n", total);   /* faltava ; */
    return 0;
}
''',
    "Os dois erros eram pontos e vírgulas faltando; o gcc mostra 'expected ;' perto da linha com problema.",
    exemplo=("", "Total: 15"),
)

_desafio(
    16, 2, "O laço que para cedo", MEDIO, 71,
    'O programa deveria somar de 1 até N e mostrar "Soma de 1 a N: S", mas sempre dá um valor menor. '
    "Encontre o erro de lógica e corrija.",
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int soma = 0;
    for (int i = 1; i < n; i++) {
        soma += i;
    }
    printf("Soma de 1 a %d: %d\n", n, soma);
    return 0;
}
''',
    [
        "Teste com N = 3 de cabeça: quais valores de i entram no laço?",
        "O último valor somado deveria ser o próprio N.",
        "Esse tipo de erro se chama 'erro por um' (off-by-one) e aparece muito em condições de laço.",
    ],
    {
        "codigo_contem": ["for"],
        "testes": [
            _teste("5\n", "Soma de 1 a 5: 15"),
            _teste("1\n", "Soma de 1 a 1: 1"),
            _teste("10\n", "Soma de 1 a 10: 55"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int soma = 0;
    for (int i = 1; i <= n; i++) {  /* <= inclui o próprio n */
        soma += i;
    }
    printf("Soma de 1 a %d: %d\n", n, soma);
    return 0;
}
''',
    "Com i < n o laço parava antes de somar n; trocar para <= inclui o último valor.",
    exemplo=("5", "Soma de 1 a 5: 15"),
)

_desafio(
    16, 3, "A média sem casas", MEDIO, 71,
    'O programa lê dois inteiros e mostra "Media: X.XX", mas para 7 e 8 mostra 7.00 em vez de 7.50. '
    "Descubra por que e corrija.",
    r'''
#include <stdio.h>

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    double media = (a + b) / 2;
    printf("Media: %.2f\n", media);
    return 0;
}
''',
    [
        "Guardar em double não basta: o problema acontece antes, na própria divisão.",
        "Quando os dois lados da divisão são int, o resultado é int e a parte decimal some.",
        "Divida por 2.0 ou converta a soma com (double).",
    ],
    {
        "testes": [
            _teste("7 8\n", "Media: 7.50"),
            _teste("3 4\n", "Media: 3.50"),
            _teste("10 20\n", "Media: 15.00"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int a, b;
    scanf("%d %d", &a, &b);
    double media = (a + b) / 2.0;  /* 2.0 força a divisão real */
    printf("Media: %.2f\n", media);
    return 0;
}
''',
    "Com 2.0 a divisão passa a ser entre double, então a parte decimal é preservada.",
    exemplo=("7 8", "Media: 7.50"),
)

_desafio(
    16, 4, "A senha que sempre entra", MEDIO, 70,
    'O programa deveria mostrar "Acesso liberado" só para a senha 1234 e "Acesso negado" para as outras, '
    "mas libera qualquer senha. Corrija o erro.",
    r'''
#include <stdio.h>

int main(void) {
    int senha;
    scanf("%d", &senha);
    if (senha = 1234) {
        printf("Acesso liberado\n");
    } else {
        printf("Acesso negado\n");
    }
    return 0;
}
''',
    [
        "Leia os avisos (warnings) do compilador: eles apontam a linha do if.",
        "Um único = é atribuição; ele troca o valor de senha e o resultado 1234 conta como verdadeiro.",
        "Para comparar use ==.",
    ],
    {
        "codigo_contem": ["=="],
        "testes": [
            _teste("1111\n", "Acesso negado", nao_contem=["liberado"]),
            _teste("1234\n", "Acesso liberado", nao_contem=["negado"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int senha;
    scanf("%d", &senha);
    if (senha == 1234) {  /* == compara; = atribuiria */
        printf("Acesso liberado\n");
    } else {
        printf("Acesso negado\n");
    }
    return 0;
}
''',
    "senha = 1234 grava 1234 e vale verdadeiro; == apenas compara. O -Wall do gcc avisa sobre esse erro.",
    exemplo=("1111", "Acesso negado"),
)

_desafio(
    16, 5, "O maior que começa errado", MEDIO, 72,
    'O programa lê 4 inteiros e mostra "Maior: X", mas erra quando todos são negativos. Use a depuração '
    "(mostrar valores intermediários ajuda) para achar o erro e corrija.",
    r'''
#include <stdio.h>

int main(void) {
    int v[4];
    for (int i = 0; i < 4; i++) {
        scanf("%d", &v[i]);
    }
    int maior = 0;
    for (int i = 0; i < 4; i++) {
        if (v[i] > maior) {
            maior = v[i];
        }
    }
    printf("Maior: %d\n", maior);
    return 0;
}
''',
    [
        "Teste com -5 -2 -9 -3: algum desses valores é maior que o valor inicial de maior?",
        "O valor inicial precisa ser um dos elementos do vetor.",
        "Comece com maior = v[0].",
    ],
    {
        "codigo_contem": ["for"],
        "testes": [
            _teste("-5 -2 -9 -3\n", regex=[r"maior: -2\b"]),
            _teste("3 8 1 5\n", regex=[r"maior: 8\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int v[4];
    for (int i = 0; i < 4; i++) {
        scanf("%d", &v[i]);
    }
    int maior = v[0];  /* começa com um valor que existe no vetor */
    for (int i = 1; i < 4; i++) {
        if (v[i] > maior) {
            maior = v[i];
        }
    }
    printf("Maior: %d\n", maior);
    return 0;
}
''',
    "Começar em 0 inventa um valor que não está no vetor; com todos negativos, nenhum elemento o superava.",
    exemplo=("-5 -2 -9 -3", "Maior: -2"),
)

# ---------------------------------------------------------------------------
# Módulo 17 · Transformando código em programa
# ---------------------------------------------------------------------------

_desafio(
    17, 1, "Qual padrão de C?", FACIL, 73,
    "O gcc do site compila com -std=c11. Mostre o valor da macro __STDC_VERSION__ no formato "
    '"Padrao: N" e, se ele for pelo menos 201112, mostre também "Compilado como C11".',
    r'''
#include <stdio.h>

int main(void) {
    printf("Padrao: ?\n");  /* troque o ? pelo valor de __STDC_VERSION__ */
    return 0;
}
''',
    [
        "__STDC_VERSION__ é uma macro que o próprio compilador define; ela é um long.",
        'Mostre com printf("Padrao: %ld\\n", __STDC_VERSION__);',
        "Use #if __STDC_VERSION__ >= 201112L para decidir no pré-processador.",
    ],
    {
        "codigo_contem": ["__STDC_VERSION__"],
        "saida_contem": ["Padrao: 201112", "Compilado como C11"],
    },
    r'''
#include <stdio.h>

int main(void) {
    printf("Padrao: %ld\n", __STDC_VERSION__);  /* definido pelo compilador */
#if __STDC_VERSION__ >= 201112L
    printf("Compilado como C11\n");
#endif
    return 0;
}
''',
    "A opção -std=c11 faz o gcc definir __STDC_VERSION__ como 201112L; o #if decide antes da compilação.",
    exemplo=("", "Padrao: 201112\nCompilado como C11"),
)

_desafio(
    17, 2, "Variável de outra unidade", MEDIO, 74,
    "Simule duas unidades de compilação no mesmo arquivo: antes de main declare extern int contador; e o "
    "protótipo void incrementar(void). Chame incrementar três vezes e mostre \"Contador: 3\". Defina "
    "contador e incrementar depois de main.",
    r'''
#include <stdio.h>

/* declarações (o que o "outro arquivo" oferece) */

int main(void) {
    /* chame incrementar três vezes */
    return 0;
}

/* definições (o "outro arquivo") */
''',
    [
        "extern int contador; avisa que a variável existe, mas é definida em outro lugar.",
        "A definição de verdade é int contador = 0; depois de main.",
        "Quem junta declaração e definição é o linker, na etapa final do build.",
    ],
    {
        "codigo_contem": ["extern"],
        "min_ocorrencias_codigo": {"incrementar(": 3},
        "saida_contem": ["Contador: 3"],
    },
    r'''
#include <stdio.h>

/* declarações (o que o "outro arquivo" oferece) */
extern int contador;
void incrementar(void);

int main(void) {
    incrementar();
    incrementar();
    incrementar();
    printf("Contador: %d\n", contador);
    return 0;
}

/* definições (o "outro arquivo") */
int contador = 0;

void incrementar(void) {
    contador++;
}
''',
    "extern só declara; a definição reserva a memória. Em projetos reais elas ficam no .h e no .c.",
    exemplo=("", "Contador: 3"),
)

_desafio(
    17, 3, "Modo debug", MEDIO, 75,
    "Crie #define DEBUG 1. Leia um inteiro N; quando DEBUG estiver ligado, mostre \"[debug] lido: N\" "
    '(use #if DEBUG ... #endif). Sempre mostre "Quadrado: Q".',
    r'''
#include <stdio.h>

/* crie #define DEBUG 1 */

int main(void) {
    int n;
    scanf("%d", &n);
    /* mensagem de depuração só quando DEBUG for 1 */
    return 0;
}
''',
    [
        "#if DEBUG é decidido pelo pré-processador, antes do compilador ver o código.",
        "Coloque o printf de depuração entre #if DEBUG e #endif.",
        "Com #define DEBUG 0 a mensagem some do programa sem apagar nenhuma linha.",
    ],
    {
        "codigo_contem": ["#define DEBUG", "#if", "#endif"],
        "testes": [
            _teste("5\n", "[debug] lido: 5", "Quadrado: 25"),
            _teste("-3\n", "[debug] lido: -3", "Quadrado: 9"),
        ],
    },
    r'''
#include <stdio.h>

#define DEBUG 1

int main(void) {
    int n;
    scanf("%d", &n);
#if DEBUG
    printf("[debug] lido: %d\n", n);  /* some com DEBUG 0 */
#endif
    printf("Quadrado: %d\n", n * n);
    return 0;
}
''',
    "A compilação condicional liga e desliga trechos inteiros; em Makefiles isso vira a opção -DDEBUG=1.",
    exemplo=("5", "[debug] lido: 5\nQuadrado: 25"),
)

_desafio(
    17, 4, "Sistema detectado", FACIL, 73,
    "Use as macros que o compilador define para descobrir o sistema: com __linux__ mostre "
    '"Sistema: Linux", com _WIN32 mostre "Sistema: Windows" e nos outros casos "Sistema: outro".',
    r'''
#include <stdio.h>

int main(void) {
    /* use #ifdef __linux__ / #elif defined(_WIN32) / #else / #endif */
    return 0;
}
''',
    [
        "#ifdef NOME é verdadeiro quando a macro NOME existe.",
        "#elif defined(_WIN32) testa outra macro na mesma cadeia.",
        "O compilador do site roda em Linux, então a resposta aqui será Linux.",
    ],
    {
        "codigo_contem": ["#ifdef", "__linux__", "#endif"],
        "saida_contem": ["Sistema: Linux"],
    },
    r'''
#include <stdio.h>

int main(void) {
#ifdef __linux__
    printf("Sistema: Linux\n");
#elif defined(_WIN32)
    printf("Sistema: Windows\n");
#else
    printf("Sistema: outro\n");
#endif
    return 0;
}
''',
    "Cada compilador define macros do sistema; só um dos ramos chega a ser compilado.",
    exemplo=("", "Sistema: Linux"),
)

_desafio(
    17, 5, "A macro traiçoeira", DESAFIADOR, 75,
    "O código usa a macro QUADRADO(x) para calcular (n + 1) ao quadrado, mas para n = 3 mostra 7 em vez de "
    '16. Corrija a macro para mostrar "Resultado: 16".',
    r'''
#include <stdio.h>

#define QUADRADO(x) x * x

int main(void) {
    int n;
    scanf("%d", &n);
    printf("Resultado: %d\n", QUADRADO(n + 1));
    return 0;
}
''',
    [
        "A macro troca texto: QUADRADO(n + 1) vira n + 1 * n + 1.",
        "Por causa da precedência, a multiplicação acontece antes das somas.",
        "Coloque parênteses em cada uso do parâmetro e no resultado todo: ((x) * (x)).",
    ],
    {
        "codigo_contem": ["#define QUADRADO"],
        "testes": [
            _teste("3\n", regex=[r"resultado: 16\b"]),
            _teste("4\n", regex=[r"resultado: 25\b"]),
        ],
    },
    r'''
#include <stdio.h>

#define QUADRADO(x) ((x) * (x))  /* parênteses protegem a expressão */

int main(void) {
    int n;
    scanf("%d", &n);
    printf("Resultado: %d\n", QUADRADO(n + 1));
    return 0;
}
''',
    "Macros não calculam, só substituem texto; os parênteses mantêm n + 1 junto antes da multiplicação.",
    exemplo=("3", "Resultado: 16"),
)

# ---------------------------------------------------------------------------
# Módulo 18 · Escrevendo programas seguros
# ---------------------------------------------------------------------------

_desafio(
    18, 1, "Nome cortado com segurança", FACIL, 76,
    'Leia um nome com fgets para char nome[8] usando sizeof, remova o Enter e mostre "Nome: X". Nomes '
    "longos devem ser cortados em 7 letras, sem estourar o vetor.",
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char nome[8] = "";
    /* leia com fgets(nome, sizeof nome, stdin) e remova o \n */
    printf("Nome: %s\n", nome);
    return 0;
}
''',
    [
        "fgets nunca grava mais que sizeof nome - 1 caracteres, e sempre coloca o '\\0'.",
        "Remova o Enter com nome[strcspn(nome, \"\\n\")] = '\\0';",
        "scanf(\"%s\") sem largura poderia gravar fora do vetor: é o buffer overflow.",
    ],
    {
        "codigo_contem": ["fgets", "sizeof"],
        "testes": [
            _teste("Ana\n", "Nome: Ana"),
            _teste("Maximiliano\n", "Nome: Maximil", nao_contem=["Maximili"]),
        ],
    },
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char nome[8] = "";
    if (fgets(nome, sizeof nome, stdin) != NULL) {  /* no máximo 7 letras + '\0' */
        nome[strcspn(nome, "\n")] = '\0';
    }
    printf("Nome: %s\n", nome);
    return 0;
}
''',
    "Passar sizeof nome para o fgets limita a leitura ao espaço que existe, e o texto extra é descartado.",
    exemplo=("Maximiliano", "Nome: Maximil"),
)

_desafio(
    18, 2, "Conferir o retorno do scanf", FACIL, 77,
    'Leia um inteiro. Se o scanf não conseguir ler (por exemplo, a pessoa digitou letras), mostre '
    '"Entrada invalida". Senão mostre "Dobro: D".',
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    printf("Dobro: %d\n", numero * 2);
    return 0;
}
''',
    [
        "scanf devolve quantos valores conseguiu ler.",
        "Se o retorno for diferente de 1, o número não foi lido e numero tem lixo.",
        "Coloque o scanf dentro do if: if (scanf(\"%d\", &numero) != 1) { ... }",
    ],
    {
        "codigo_contem": ["scanf", "if"],
        "testes": [
            _teste("abc\n", "Entrada invalida", nao_contem=["Dobro"]),
            _teste("21\n", "Dobro: 42"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int numero;
    if (scanf("%d", &numero) != 1) {  /* não leu um inteiro */
        printf("Entrada invalida\n");
        return 0;
    }
    printf("Dobro: %d\n", numero * 2);
    return 0;
}
''',
    "Testar o retorno do scanf evita usar uma variável que nunca recebeu valor.",
    exemplo=("abc", "Entrada invalida"),
)

_desafio(
    18, 3, "Insistir até ser válido", MEDIO, 77,
    "Leia notas até aparecer uma entre 0 e 10. Depois mostre \"Tentativas invalidas: N\" e "
    '"Nota aceita: X" (sem casas decimais se for inteira, use %g).',
    r'''
#include <stdio.h>

int main(void) {
    double nota;
    int invalidas = 0;
    /* repita a leitura enquanto a nota estiver fora de 0 a 10 */
    return 0;
}
''',
    [
        "Um while (1) com break quando a nota for válida é uma forma simples de repetir.",
        "Se o scanf falhar (fim da entrada), pare também para não entrar em laço infinito.",
        "%g mostra 8 como 8 e 7.5 como 7.5.",
    ],
    {
        "codigo_contem": ["while"],
        "testes": [
            _teste("15\n-2\n8\n", regex=[r"tentativas invalidas: 2\b", r"nota aceita: 8\b"]),
            _teste("7.5\n", regex=[r"tentativas invalidas: 0\b", r"nota aceita: 7\.5\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    double nota;
    int invalidas = 0;
    while (1) {
        if (scanf("%lf", &nota) != 1) {
            printf("Entrada encerrada\n");
            return 0;
        }
        if (nota >= 0 && nota <= 10) {
            break;               /* nota válida: sai do laço */
        }
        invalidas++;
    }
    printf("Tentativas invalidas: %d\n", invalidas);
    printf("Nota aceita: %g\n", nota);
    return 0;
}
''',
    "O laço só termina com um valor aceito, e o teste do scanf protege contra o fim da entrada.",
    exemplo=("15\n-2\n8", "Tentativas invalidas: 2\nNota aceita: 8"),
)

_desafio(
    18, 4, "Índice seguro", FACIL, 76,
    "O vetor int v[5] = {10, 20, 30, 40, 50} já existe. Leia um índice e mostre \"Valor: X\" apenas se "
    'ele for válido; senão mostre "Indice fora do limite".',
    r'''
#include <stdio.h>

int main(void) {
    int v[5] = {10, 20, 30, 40, 50};
    int indice;
    scanf("%d", &indice);
    printf("Valor: %d\n", v[indice]);  /* e se o índice for 5 ou -1? */
    return 0;
}
''',
    [
        "Os índices válidos de um vetor de 5 posições vão de 0 a 4.",
        "Confira indice >= 0 && indice < 5 antes de acessar v[indice].",
        "Acessar fora do vetor não dá erro de compilação: lê memória de outra coisa.",
    ],
    {
        "codigo_contem": ["if"],
        "testes": [
            _teste("2\n", regex=[r"valor: 30\b"]),
            _teste("5\n", "Indice fora do limite", nao_contem=["Valor"]),
            _teste("-1\n", "Indice fora do limite", nao_contem=["Valor"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int v[5] = {10, 20, 30, 40, 50};
    int indice;
    scanf("%d", &indice);
    if (indice >= 0 && indice < 5) {  /* só acessa dentro do vetor */
        printf("Valor: %d\n", v[indice]);
    } else {
        printf("Indice fora do limite\n");
    }
    return 0;
}
''',
    "C não confere limites sozinho; a verificação antes do acesso evita ler memória que não é do vetor.",
    exemplo=("5", "Indice fora do limite"),
)

_desafio(
    18, 5, "Concatenação que cabe", MEDIO, 76,
    "Leia duas palavras. Junte-as em char destino[10] somente se couberem (contando o '\\0'); nesse caso "
    'mostre "Resultado: AB". Se não couberem, mostre "Nao cabe" e não chame strcat.',
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[30], b[30], destino[10];
    scanf("%29s %29s", a, b);
    /* verifique o espaço antes de juntar */
    return 0;
}
''',
    [
        "O espaço necessário é strlen(a) + strlen(b) + 1.",
        "Compare com sizeof destino antes de copiar qualquer coisa.",
        "Se couber: strcpy(destino, a); strcat(destino, b);",
    ],
    {
        "codigo_contem": ["strlen", "strcat", "sizeof"],
        "testes": [
            _teste("sol lua\n", "Resultado: sollua"),
            _teste("paralelepipedo x\n", "Nao cabe", nao_contem=["Resultado"]),
            _teste("abcd efghi\n", "Resultado: abcdefghi"),
        ],
    },
    r'''
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[30], b[30], destino[10];
    scanf("%29s %29s", a, b);
    if (strlen(a) + strlen(b) + 1 > sizeof destino) {  /* +1 para o '\0' */
        printf("Nao cabe\n");
    } else {
        strcpy(destino, a);
        strcat(destino, b);
        printf("Resultado: %s\n", destino);
    }
    return 0;
}
''',
    "strcat não confere o tamanho do destino; a conta antes da cópia é o que impede o estouro.",
    exemplo=("sol lua", "Resultado: sollua"),
)

# ---------------------------------------------------------------------------
# Módulo 19 · Organizando muitos dados
# ---------------------------------------------------------------------------

_desafio(
    19, 1, "Lista ligada ao contrário", MEDIO, 78,
    "Leia inteiros até aparecer 0. Insira cada um no início de uma lista ligada (struct No com valor e "
    "proximo). Depois percorra a lista mostrando os valores na mesma linha e libere todos os nós.",
    r'''
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No *proximo;
} No;

int main(void) {
    No *inicio = NULL;
    /* leia até 0 inserindo no início; depois mostre e libere */
    return 0;
}
''',
    [
        "Para inserir no início: novo->proximo = inicio; inicio = novo;",
        "Percorra com for (No *p = inicio; p != NULL; p = p->proximo).",
        "Para liberar, guarde o próximo antes do free: No *seguinte = inicio->proximo;",
    ],
    {
        "codigo_contem": ["malloc", "free", "->"],
        "testes": [
            _teste("1 2 3 0\n", "3 2 1"),
            _teste("42 0\n", "42"),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No *proximo;
} No;

int main(void) {
    No *inicio = NULL;
    int numero;
    while (scanf("%d", &numero) == 1 && numero != 0) {
        No *novo = malloc(sizeof(No));
        if (novo == NULL) {
            break;
        }
        novo->valor = numero;
        novo->proximo = inicio;  /* o novo aponta para o antigo primeiro */
        inicio = novo;
    }
    for (No *p = inicio; p != NULL; p = p->proximo) {
        printf("%d ", p->valor);
    }
    printf("\n");
    while (inicio != NULL) {
        No *seguinte = inicio->proximo;  /* guarda antes de liberar */
        free(inicio);
        inicio = seguinte;
    }
    return 0;
}
''',
    "Inserir no início é O(1) e inverte a ordem naturalmente; liberar exige guardar o próximo antes do free.",
    exemplo=("1 2 3 0", "3 2 1"),
)

_desafio(
    19, 2, "Inverter palavra com pilha", FACIL, 79,
    "Implemente uma pilha de caracteres com as funções push e pop. Leia uma palavra, empilhe todas as "
    'letras e desempilhe mostrando "Invertida: PALAVRA_AO_CONTRARIO".',
    r'''
#include <stdio.h>

char pilha[100];
int topo = 0;

/* crie void push(char c) e char pop(void) */

int main(void) {
    char palavra[100];
    scanf("%99s", palavra);
    /* empilhe e desempilhe */
    return 0;
}
''',
    [
        "push grava em pilha[topo] e aumenta topo; pop diminui topo e devolve pilha[topo].",
        "A última letra empilhada é a primeira a sair: é isso que inverte a palavra.",
        "Desempilhe enquanto topo > 0.",
    ],
    {
        "min_ocorrencias_codigo": {"push(": 2, "pop(": 2},
        "testes": [
            _teste("pilha\n", "Invertida: ahlip"),
            _teste("C11\n", "Invertida: 11C"),
        ],
    },
    r'''
#include <stdio.h>

char pilha[100];
int topo = 0;

void push(char c) {
    if (topo < 100) {
        pilha[topo++] = c;
    }
}

char pop(void) {
    return pilha[--topo];  /* o último que entrou sai primeiro */
}

int main(void) {
    char palavra[100];
    scanf("%99s", palavra);
    for (int i = 0; palavra[i] != '\0'; i++) {
        push(palavra[i]);
    }
    printf("Invertida: ");
    while (topo > 0) {
        printf("%c", pop());
    }
    printf("\n");
    return 0;
}
''',
    "A pilha segue a regra LIFO (último a entrar, primeiro a sair), então as letras saem na ordem inversa.",
    exemplo=("pilha", "Invertida: ahlip"),
)

_desafio(
    19, 3, "Parênteses balanceados", DESAFIADOR, 79,
    "Leia uma linha e verifique com uma pilha se (), [] e {} estão balanceados: cada abertura precisa ser "
    'fechada pelo símbolo certo e na ordem certa. Mostre "Balanceado" ou "Desbalanceado".',
    r'''
#include <stdio.h>

int main(void) {
    char linha[200];
    if (fgets(linha, sizeof linha, stdin) == NULL) {
        return 0;
    }
    char pilha[200];
    int topo = 0;
    /* empilhe aberturas; em cada fechamento confira o topo */
    return 0;
}
''',
    [
        "Ao ver (, [ ou { empilhe o símbolo.",
        "Ao ver ), ] ou }, a pilha não pode estar vazia e o topo precisa ser a abertura correspondente.",
        "No final, a pilha precisa estar vazia para a linha ser balanceada.",
    ],
    {
        "codigo_contem": ["fgets"],
        "testes": [
            _teste("(a[b]{c})\n", "Balanceado", nao_contem=["Desbalanceado"]),
            _teste("(]\n", "Desbalanceado"),
            _teste("((\n", "Desbalanceado"),
            _teste("x + y\n", "Balanceado", nao_contem=["Desbalanceado"]),
            _teste("())\n", "Desbalanceado"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    char linha[200];
    if (fgets(linha, sizeof linha, stdin) == NULL) {
        return 0;
    }
    char pilha[200];
    int topo = 0, ok = 1;
    for (int i = 0; linha[i] != '\0' && ok; i++) {
        char c = linha[i];
        if (c == '(' || c == '[' || c == '{') {
            pilha[topo++] = c;                   /* abre: empilha */
        } else if (c == ')' || c == ']' || c == '}') {
            char esperado = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (topo == 0 || pilha[topo - 1] != esperado) {
                ok = 0;                          /* fechou errado ou sem abrir */
            } else {
                topo--;
            }
        }
    }
    if (topo != 0) {
        ok = 0;                                  /* sobrou algo aberto */
    }
    printf("%s\n", ok ? "Balanceado" : "Desbalanceado");
    return 0;
}
''',
    "A pilha lembra a abertura mais recente, que é exatamente a que deve ser fechada primeiro.",
    exemplo=("(a[b]{c})", "Balanceado"),
)

_desafio(
    19, 4, "Fila de atendimento", MEDIO, 80,
    "Implemente uma fila de nomes com as funções enfileirar e desenfileirar. Leia N e N nomes, enfileire "
    'todos e depois atenda na ordem de chegada mostrando "Atendendo: NOME".',
    r'''
#include <stdio.h>
#include <string.h>

char fila[20][30];
int inicio = 0, fim = 0;

/* crie void enfileirar(const char *nome) e const char *desenfileirar(void) */

int main(void) {
    int n;
    scanf("%d", &n);
    /* leia, enfileire e atenda */
    return 0;
}
''',
    [
        "enfileirar copia o nome para fila[fim] e aumenta fim.",
        "desenfileirar devolve fila[inicio] e aumenta inicio.",
        "A fila está vazia quando inicio == fim.",
    ],
    {
        "min_ocorrencias_codigo": {"enfileirar(": 2, "desenfileirar(": 2},
        "testes": [
            _teste("3\nAna\nBeto\nCaio\n", regex=[r"atendendo: ana\s+atendendo: beto\s+atendendo: caio"]),
            _teste("1\nZe\n", "Atendendo: Ze"),
        ],
    },
    r'''
#include <stdio.h>
#include <string.h>

char fila[20][30];
int inicio = 0, fim = 0;

void enfileirar(const char *nome) {
    if (fim < 20) {
        strcpy(fila[fim++], nome);  /* entra no fim */
    }
}

const char *desenfileirar(void) {
    return fila[inicio++];          /* sai do começo */
}

int main(void) {
    int n;
    scanf("%d", &n);
    char nome[30];
    for (int i = 0; i < n; i++) {
        scanf("%29s", nome);
        enfileirar(nome);
    }
    while (inicio < fim) {
        printf("Atendendo: %s\n", desenfileirar());
    }
    return 0;
}
''',
    "Na fila (FIFO) quem chega primeiro sai primeiro: entra-se pelo fim e sai-se pelo início.",
    exemplo=("3\nAna\nBeto\nCaio", "Atendendo: Ana\nAtendendo: Beto\nAtendendo: Caio"),
)

_desafio(
    19, 5, "Árvore de busca", DESAFIADOR, 81,
    "Leia inteiros até aparecer 0 e insira-os em uma árvore binária de busca com a função inserir. Mostre os "
    'valores em ordem (percurso em ordem), depois "Altura: H", e libere a árvore.',
    r'''
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No *esquerda;
    struct No *direita;
} No;

/* crie inserir, emOrdem, altura e liberar */

int main(void) {
    No *raiz = NULL;
    /* leia até 0 */
    return 0;
}
''',
    [
        "inserir(raiz, valor): se raiz for NULL cria o nó; menores vão para a esquerda, maiores para a direita.",
        "Em ordem: esquerda, valor, direita. Isso mostra os números ordenados.",
        "altura(NULL) é 0; senão é 1 + o maior entre a altura da esquerda e a da direita.",
    ],
    {
        "codigo_contem": ["malloc", "free"],
        "min_ocorrencias_codigo": {"inserir(": 2},
        "testes": [
            _teste("50 30 70 20 40 0\n", "20 30 40 50 70", regex=[r"altura: 3\b"]),
            _teste("5 4 3 0\n", "3 4 5", regex=[r"altura: 3\b"]),
            _teste("8 0\n", regex=[r"\b8\b", r"altura: 1\b"]),
        ],
    },
    r'''
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No *esquerda;
    struct No *direita;
} No;

No *inserir(No *raiz, int valor) {
    if (raiz == NULL) {
        No *novo = malloc(sizeof(No));
        if (novo != NULL) {
            novo->valor = valor;
            novo->esquerda = novo->direita = NULL;
        }
        return novo;
    }
    if (valor < raiz->valor) {
        raiz->esquerda = inserir(raiz->esquerda, valor);
    } else {
        raiz->direita = inserir(raiz->direita, valor);
    }
    return raiz;
}

void emOrdem(const No *raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esquerda);
        printf("%d ", raiz->valor);
        emOrdem(raiz->direita);
    }
}

int altura(const No *raiz) {
    if (raiz == NULL) {
        return 0;
    }
    int e = altura(raiz->esquerda), d = altura(raiz->direita);
    return 1 + (e > d ? e : d);
}

void liberar(No *raiz) {
    if (raiz != NULL) {
        liberar(raiz->esquerda);
        liberar(raiz->direita);
        free(raiz);  /* filhos primeiro, depois o nó */
    }
}

int main(void) {
    No *raiz = NULL;
    int numero;
    while (scanf("%d", &numero) == 1 && numero != 0) {
        raiz = inserir(raiz, numero);
    }
    emOrdem(raiz);
    printf("\n");
    printf("Altura: %d\n", altura(raiz));
    liberar(raiz);
    return 0;
}
''',
    "A regra 'menor à esquerda, maior à direita' faz o percurso em ordem sair ordenado; tudo é recursivo.",
    exemplo=("50 30 70 20 40 0", "20 30 40 50 70\nAltura: 3"),
)

# ---------------------------------------------------------------------------
# Módulo 20 · Resolvendo problemas melhor
# ---------------------------------------------------------------------------

_desafio(
    20, 1, "Quantas vezes aparece", FACIL, 82,
    'Leia N, depois N inteiros e por fim um valor procurado. Mostre "Aparece K vezes" percorrendo o vetor '
    "com busca linear.",
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int v[100];
    for (int i = 0; i < n && i < 100; i++) {
        scanf("%d", &v[i]);
    }
    int alvo;
    scanf("%d", &alvo);
    /* conte as ocorrências */
    return 0;
}
''',
    [
        "A busca linear olha cada posição, do começo ao fim.",
        "Em vez de parar no primeiro encontrado, some 1 a cada igualdade.",
        'printf("Aparece %d vezes\\n", contador);',
    ],
    {
        "codigo_contem": ["for", "=="],
        "testes": [
            _teste("5\n1 3 1 2 1\n1\n", regex=[r"aparece 3 vezes"]),
            _teste("3\n4 5 6\n9\n", regex=[r"aparece 0 vezes"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    if (n > 100) {
        n = 100;
    }
    int v[100];
    for (int i = 0; i < n; i++) {
        scanf("%d", &v[i]);
    }
    int alvo;
    scanf("%d", &alvo);
    int contador = 0;
    for (int i = 0; i < n; i++) {
        if (v[i] == alvo) {  /* não para: conta todas */
            contador++;
        }
    }
    printf("Aparece %d vezes\n", contador);
    return 0;
}
''',
    "Contar ocorrências exige olhar o vetor inteiro, então a busca linear sem break é a escolha natural.",
    exemplo=("5\n1 3 1 2 1\n1", "Aparece 3 vezes"),
)

_desafio(
    20, 2, "Bubble sort decrescente", FACIL, 83,
    "Leia 5 inteiros e ordene-os do maior para o menor com bubble sort (sem qsort). Mostre na mesma linha.",
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    /* bubble sort decrescente */
    for (int i = 0; i < 5; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}
''',
    [
        "O bubble sort compara vizinhos e troca quando estão fora de ordem.",
        "Para ordem decrescente, troque quando v[j] < v[j + 1].",
        "Dois for: o de fora repete as passadas, o de dentro percorre os pares vizinhos.",
    ],
    {
        "codigo_contem": ["for"],
        "codigo_nao_contem": ["qsort"],
        "testes": [
            _teste("3 9 1 7 5\n", "9 7 5 3 1"),
            _teste("-1 4 4 0 2\n", "4 4 2 0 -1"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4 - i; j++) {
            if (v[j] < v[j + 1]) {  /* < deixa o maior na frente */
                int temp = v[j];
                v[j] = v[j + 1];
                v[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < 5; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}
''',
    "Trocar o sinal da comparação inverte a ordem; o resto do algoritmo continua igual.",
    exemplo=("3 9 1 7 5", "9 7 5 3 1"),
)

_desafio(
    20, 3, "Busca binária", MEDIO, 84,
    "Leia N, N inteiros já em ordem crescente e um valor procurado. Use busca binária (variáveis inicio, fim "
    'e meio) e mostre "Posicao: P" (contando do 0) ou "Nao encontrado".',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int v[100];
    for (int i = 0; i < n && i < 100; i++) {
        scanf("%d", &v[i]);
    }
    int alvo;
    scanf("%d", &alvo);
    /* busca binária com inicio, fim e meio */
    return 0;
}
''',
    [
        "Comece com inicio = 0 e fim = n - 1; repita enquanto inicio <= fim.",
        "meio = inicio + (fim - inicio) / 2; se v[meio] for o alvo, achou.",
        "Se o alvo for maior, descarte a metade esquerda (inicio = meio + 1); senão a direita (fim = meio - 1).",
    ],
    {
        "codigo_contem": ["meio", "while"],
        "testes": [
            _teste("7\n1 3 5 7 9 11 13\n11\n", regex=[r"posicao: 5\b"]),
            _teste("7\n1 3 5 7 9 11 13\n4\n", "Nao encontrado"),
            _teste("1\n8\n8\n", regex=[r"posicao: 0\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    if (n > 100) {
        n = 100;
    }
    int v[100];
    for (int i = 0; i < n; i++) {
        scanf("%d", &v[i]);
    }
    int alvo;
    scanf("%d", &alvo);

    int inicio = 0, fim = n - 1, posicao = -1;
    while (inicio <= fim) {
        int meio = inicio + (fim - inicio) / 2;
        if (v[meio] == alvo) {
            posicao = meio;
            break;
        } else if (v[meio] < alvo) {
            inicio = meio + 1;  /* alvo está à direita */
        } else {
            fim = meio - 1;     /* alvo está à esquerda */
        }
    }
    if (posicao >= 0) {
        printf("Posicao: %d\n", posicao);
    } else {
        printf("Nao encontrado\n");
    }
    return 0;
}
''',
    "Cada comparação descarta metade do vetor, por isso a busca binária precisa de poucos passos (O(log n)).",
    exemplo=("7\n1 3 5 7 9 11 13\n11", "Posicao: 5"),
)

_desafio(
    20, 4, "Contando trocas", MEDIO, 83,
    'Ordene 5 inteiros em ordem crescente com bubble sort e mostre os valores e depois "Trocas: T", '
    "o número de trocas feitas.",
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    int trocas = 0;
    /* ordene contando as trocas */
    printf("Trocas: %d\n", trocas);
    return 0;
}
''',
    [
        "Some 1 em trocas toda vez que dois vizinhos forem trocados.",
        "Um vetor já ordenado não precisa de nenhuma troca.",
        "O pior caso (ordem inversa) com 5 elementos faz 10 trocas.",
    ],
    {
        "codigo_contem": ["for"],
        "testes": [
            _teste("5 4 3 2 1\n", "1 2 3 4 5", regex=[r"trocas: 10\b"]),
            _teste("1 2 3 4 5\n", "1 2 3 4 5", regex=[r"trocas: 0\b"]),
            _teste("2 1 3 5 4\n", "1 2 3 4 5", regex=[r"trocas: 2\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int v[5];
    for (int i = 0; i < 5; i++) {
        scanf("%d", &v[i]);
    }
    int trocas = 0;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4 - i; j++) {
            if (v[j] > v[j + 1]) {
                int temp = v[j];
                v[j] = v[j + 1];
                v[j + 1] = temp;
                trocas++;          /* mede o trabalho feito */
            }
        }
    }
    for (int i = 0; i < 5; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
    printf("Trocas: %d\n", trocas);
    return 0;
}
''',
    "Contar trocas mostra como o esforço do bubble sort depende de quão desordenado o vetor está.",
    exemplo=("5 4 3 2 1", "1 2 3 4 5\nTrocas: 10"),
)

_desafio(
    20, 5, "Segundo maior em uma passada", DESAFIADOR, 84,
    'Leia N e N inteiros e mostre "Segundo maior: X" (o maior valor diferente do maior de todos) '
    'percorrendo o vetor uma única vez, sem ordenar. Se não existir, mostre "Nao existe".',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* guarde o maior e o segundo maior enquanto lê */
    return 0;
}
''',
    [
        "Mantenha duas variáveis: maior e segundo, e marque quando cada uma já recebeu um valor.",
        "Se o novo valor for maior que maior, o antigo maior passa a ser o segundo.",
        "Valores iguais ao maior não contam como segundo maior.",
    ],
    {
        "codigo_nao_contem": ["qsort"],
        "testes": [
            _teste("5\n4 9 2 9 7\n", regex=[r"segundo maior: 7\b"]),
            _teste("3\n5 5 5\n", "Nao existe"),
            _teste("4\n-1 -5 -3 -2\n", regex=[r"segundo maior: -2\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    int maior = 0, segundo = 0, temMaior = 0, temSegundo = 0;
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        if (!temMaior || x > maior) {
            if (temMaior) {             /* o antigo maior desce */
                segundo = maior;
                temSegundo = 1;
            }
            maior = x;
            temMaior = 1;
        } else if (x != maior && (!temSegundo || x > segundo)) {
            segundo = x;
            temSegundo = 1;
        }
    }
    if (temSegundo) {
        printf("Segundo maior: %d\n", segundo);
    } else {
        printf("Nao existe\n");
    }
    return 0;
}
''',
    "Uma passada com duas variáveis resolve em O(n), mais rápido que ordenar o vetor inteiro (O(n log n)).",
    exemplo=("5\n4 9 2 9 7", "Segundo maior: 7"),
)

# ---------------------------------------------------------------------------
# Módulo 21 · Criando programas completos
# ---------------------------------------------------------------------------

_desafio(
    21, 1, "Caixa eletrônico", MEDIO, 85,
    "Leia um valor de saque. Se não for positivo e múltiplo de 10, mostre \"Valor invalido\". Senão mostre "
    'a menor quantidade de notas de 100, 50, 20 e 10, só as que forem usadas: "Notas de 100: 3".',
    r'''
#include <stdio.h>

int main(void) {
    int valor;
    scanf("%d", &valor);
    int notas[] = {100, 50, 20, 10};
    /* valide e distribua as notas da maior para a menor */
    return 0;
}
''',
    [
        "Valide antes: valor > 0 && valor % 10 == 0.",
        "Para cada nota, quantidade = valor / nota e o que sobra é valor % nota.",
        "Mostre a linha só quando quantidade > 0.",
    ],
    {
        "codigo_contem": ["%", "/"],
        "testes": [
            _teste("380\n", "Notas de 100: 3", "Notas de 50: 1", "Notas de 20: 1", "Notas de 10: 1"),
            _teste("70\n", "Notas de 50: 1", "Notas de 20: 1", nao_contem=["Notas de 100", "Notas de 10:"]),
            _teste("35\n", "Valor invalido", nao_contem=["Notas"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int valor;
    scanf("%d", &valor);
    if (valor <= 0 || valor % 10 != 0) {
        printf("Valor invalido\n");
        return 0;
    }
    int notas[] = {100, 50, 20, 10};
    for (int i = 0; i < 4; i++) {
        int quantidade = valor / notas[i];  /* quantas notas cabem */
        valor %= notas[i];                  /* o que falta pagar */
        if (quantidade > 0) {
            printf("Notas de %d: %d\n", notas[i], quantidade);
        }
    }
    return 0;
}
''',
    "Começar pela maior nota (estratégia gulosa) dá o menor número de notas para esses valores.",
    exemplo=("380", "Notas de 100: 3\nNotas de 50: 1\nNotas de 20: 1\nNotas de 10: 1"),
)

_desafio(
    21, 2, "Boletim da turma", MEDIO, 91,
    "Leia N e, para cada aluno, nome e duas notas. Guarde em um vetor de structs e mostre \"NOME: MEDIA "
    'SITUACAO" (Aprovado com média >= 7). No fim mostre "Aprovados: A de N".',
    r'''
#include <stdio.h>

typedef struct {
    char nome[30];
    double media;
} Aluno;

int main(void) {
    int n;
    scanf("%d", &n);
    Aluno turma[50];
    /* leia, calcule, mostre e conte os aprovados */
    return 0;
}
''',
    [
        "Leia as duas notas e guarde só a média na struct.",
        "Conte os aprovados em uma variável enquanto mostra cada aluno.",
        "Limite N a 50, o tamanho do vetor.",
    ],
    {
        "codigo_contem": ["struct"],
        "testes": [
            _teste(
                "3\nAna 8 9\nBia 5 6\nCaio 7 7\n",
                "Ana: 8.50 Aprovado", "Bia: 5.50 Reprovado", "Caio: 7.00 Aprovado", "Aprovados: 2 de 3",
            ),
            _teste("1\nDeco 2 3\n", "Deco: 2.50 Reprovado", "Aprovados: 0 de 1"),
        ],
    },
    r'''
#include <stdio.h>

typedef struct {
    char nome[30];
    double media;
} Aluno;

int main(void) {
    int n;
    scanf("%d", &n);
    if (n > 50) {
        n = 50;
    }
    Aluno turma[50];
    int aprovados = 0;
    for (int i = 0; i < n; i++) {
        double n1, n2;
        scanf("%29s %lf %lf", turma[i].nome, &n1, &n2);
        turma[i].media = (n1 + n2) / 2;
    }
    for (int i = 0; i < n; i++) {
        int passou = turma[i].media >= 7;
        aprovados += passou;
        printf("%s: %.2f %s\n", turma[i].nome, turma[i].media, passou ? "Aprovado" : "Reprovado");
    }
    printf("Aprovados: %d de %d\n", aprovados, n);
    return 0;
}
''',
    "Separar leitura e relatório em dois laços deixa cada parte simples; a struct mantém nome e média juntos.",
    exemplo=("3\nAna 8 9\nBia 5 6\nCaio 7 7", "Ana: 8.50 Aprovado\nBia: 5.50 Reprovado\nCaio: 7.00 Aprovado\nAprovados: 2 de 3"),
)

_desafio(
    21, 3, "Conversor com menu", MEDIO, 85,
    "Faça um menu que repete até a opção 0: a opção 1 lê quilômetros e mostra \"X.XX m\"; a opção 2 lê "
    'metros e mostra "X.XX cm"; outra opção mostra "Opcao invalida". Ao sair mostre "Fim".',
    r'''
#include <stdio.h>

int main(void) {
    int opcao;
    /* repita: leia a opção e use switch */
    printf("Fim\n");
    return 0;
}
''',
    [
        "Um do { ... } while (opcao != 0); repete o menu até o 0.",
        "Dentro, um switch trata as opções 1, 2, 0 e o default.",
        "Proteja-se do fim da entrada: se o scanf da opção falhar, trate como 0.",
    ],
    {
        "codigo_contem": ["switch", "while"],
        "testes": [
            _teste("1\n2.5\n2\n3\n0\n", "2500.00 m", "300.00 cm", "Fim"),
            _teste("9\n0\n", "Opcao invalida", "Fim"),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int opcao;
    do {
        printf("1) km para m  2) m para cm  0) sair\n");
        if (scanf("%d", &opcao) != 1) {
            opcao = 0;                       /* entrada acabou */
        }
        double valor;
        switch (opcao) {
            case 1:
                if (scanf("%lf", &valor) == 1) {
                    printf("%.2f m\n", valor * 1000);
                }
                break;
            case 2:
                if (scanf("%lf", &valor) == 1) {
                    printf("%.2f cm\n", valor * 100);
                }
                break;
            case 0:
                break;
            default:
                printf("Opcao invalida\n");
        }
    } while (opcao != 0);
    printf("Fim\n");
    return 0;
}
''',
    "O do while mostra o menu pelo menos uma vez e o switch separa cada opção de forma organizada.",
    exemplo=("1\n2.5\n2\n3\n0", "2500.00 m\n300.00 cm\nFim"),
)

_desafio(
    21, 4, "Estoque em arquivo", DESAFIADOR, 86,
    'Leia N produtos (nome, quantidade e preço) e grave-os em "estoque.txt". Depois reabra o arquivo, leia '
    'tudo de volta e mostre "Itens: Q" (soma das quantidades) e "Valor total: V" (quantidade x preço).',
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    /* grave em estoque.txt e depois leia de volta somando */
    return 0;
}
''',
    [
        'Grave cada produto em uma linha: fprintf(arquivo, "%s %d %.2f\\n", nome, qtd, preco);',
        'Na leitura use while (fscanf(arquivo, "%29s %d %lf", nome, &qtd, &preco) == 3).',
        "Some qtd em itens e qtd * preco em valor total.",
    ],
    {
        "codigo_contem": ["fprintf", "fscanf", "fclose"],
        "testes": [
            _teste("2\nCaneta 3 2.50\nCaderno 2 10.00\n", regex=[r"itens: 5\b", r"valor total: 27\.50\b"]),
            _teste("1\nLapis 10 0.75\n", regex=[r"itens: 10\b", r"valor total: 7\.50\b"]),
        ],
    },
    r'''
#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);

    FILE *arquivo = fopen("estoque.txt", "w");
    if (arquivo == NULL) {
        return 1;
    }
    char nome[30];
    int quantidade;
    double preco;
    for (int i = 0; i < n; i++) {
        scanf("%29s %d %lf", nome, &quantidade, &preco);
        fprintf(arquivo, "%s %d %.2f\n", nome, quantidade, preco);
    }
    fclose(arquivo);

    arquivo = fopen("estoque.txt", "r");
    if (arquivo == NULL) {
        return 1;
    }
    int itens = 0;
    double total = 0;
    while (fscanf(arquivo, "%29s %d %lf", nome, &quantidade, &preco) == 3) {
        itens += quantidade;
        total += quantidade * preco;
    }
    fclose(arquivo);
    printf("Itens: %d\n", itens);
    printf("Valor total: %.2f\n", total);
    return 0;
}
''',
    "Os dados sobrevivem no arquivo entre a gravação e a leitura; fscanf == 3 confirma cada linha completa.",
    exemplo=("2\nCaneta 3 2.50\nCaderno 2 10.00", "Itens: 5\nValor total: 27.50"),
)

_desafio(
    21, 5, "Jogo da velha: quem venceu?", DESAFIADOR, 88,
    "Leia um tabuleiro de jogo da velha em 3 linhas de 3 caracteres (X, O ou . para vazio). Verifique "
    'linhas, colunas e diagonais e mostre "Vencedor: X", "Vencedor: O" ou "Sem vencedor".',
    r'''
#include <stdio.h>

int main(void) {
    char t[3][4];
    for (int i = 0; i < 3; i++) {
        scanf("%3s", t[i]);
    }
    /* verifique linhas, colunas e diagonais */
    return 0;
}
''',
    [
        "Uma linha vence quando t[i][0] == t[i][1] == t[i][2] e não é '.'.",
        "Faça o mesmo para colunas (t[0][j], t[1][j], t[2][j]) e para as duas diagonais.",
        "Uma função char tres(char a, char b, char c) que devolve o vencedor ou '.' evita repetição.",
    ],
    {
        "codigo_contem": ["[3]"],
        "testes": [
            _teste("XXX\nOO.\n...\n", "Vencedor: X"),
            _teste("OX.\nOX.\nO.X\n", "Vencedor: O"),
            _teste("XOX\nXOO\nOXX\n", "Sem vencedor", nao_contem=["Vencedor:"]),
            _teste("X.O\n.XO\n..X\n", "Vencedor: X"),
        ],
    },
    r'''
#include <stdio.h>

char tres(char a, char b, char c) {
    return (a != '.' && a == b && b == c) ? a : '.';  /* '.' = ninguém */
}

int main(void) {
    char t[3][4];
    for (int i = 0; i < 3; i++) {
        scanf("%3s", t[i]);
    }
    char vencedor = '.';
    for (int i = 0; i < 3 && vencedor == '.'; i++) {
        vencedor = tres(t[i][0], t[i][1], t[i][2]);          /* linha i */
        if (vencedor == '.') {
            vencedor = tres(t[0][i], t[1][i], t[2][i]);      /* coluna i */
        }
    }
    if (vencedor == '.') {
        vencedor = tres(t[0][0], t[1][1], t[2][2]);
    }
    if (vencedor == '.') {
        vencedor = tres(t[0][2], t[1][1], t[2][0]);
    }
    if (vencedor == '.') {
        printf("Sem vencedor\n");
    } else {
        printf("Vencedor: %c\n", vencedor);
    }
    return 0;
}
''',
    "A função tres concentra a regra de vitória; o programa só aplica essa regra às 8 combinações possíveis.",
    exemplo=("XXX\nOO.\n...", "Vencedor: X"),
)
