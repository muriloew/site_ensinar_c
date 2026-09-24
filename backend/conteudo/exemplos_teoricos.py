"""Exemplos de estudo independentes dos enunciados e da correcao automatica."""


def exemplo(codigo, saida, entrada="", casos=()):
    return {
        "codigo": codigo.strip(),
        "entrada": entrada,
        "saida": saida,
        "casos": [{"entrada": entrada, "saida": saida, "retorno": 0}, *casos],
    }


EXEMPLOS = {
    "scanf": exemplo(r'''
#include <stdio.h>

int main(void) {
    int numero;
    printf("Digite um numero: ");
    fflush(stdout);
    if (scanf("%d", &numero) != 1) {
        printf("Entrada invalida\n");
        return 1;
    }
    printf("Numero: %d\n", numero);
    return 0;
}
''', "Digite um numero: Numero: 12\n", "12\n", (
        {"entrada": "abc\n", "saida": "Digite um numero: Entrada invalida\n", "retorno": 1},
        {"entrada": "", "saida": "Digite um numero: Entrada invalida\n", "retorno": 1},
    )),
    "if": exemplo(r'''
#include <stdio.h>

int main(void) {
    int numero = 7;
    if (numero > 0) {
        printf("Positivo\n");
    }
    return 0;
}
''', "Positivo\n"),
    "for": exemplo(r'''
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 5; i++) {
        printf("%d\n", i);
    }
    return 0;
}
''', "1\n2\n3\n4\n5\n"),
    "protótipos": exemplo(r'''
#include <stdio.h>

int dobro(int n);

int main(void) {
    printf("%d\n", dobro(5));
    return 0;
}

int dobro(int n) {
    return n * 2;
}
''', "10\n"),
    "malloc": exemplo(r'''
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *numero = malloc(sizeof *numero);
    if (numero == NULL) {
        printf("Falha de alocacao\n");
        return 1;
    }
    *numero = 30;
    printf("%d\n", *numero);
    free(numero);
    return 0;
}
''', "30\n"),
    "fopen": exemplo(r'''
#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("dados.txt", "w");
    if (arquivo == NULL) {
        printf("Falha ao abrir\n");
        return 1;
    }
    printf("Arquivo aberto\n");
    if (fclose(arquivo) != 0) return 1;
    return 0;
}
''', "Arquivo aberto\n"),
    "fclose": exemplo(r'''
#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("dados.txt", "w");
    if (arquivo == NULL) return 1;
    int escrita = fprintf(arquivo, "%d\n", 42);
    int fechamento = fclose(arquivo);
    if (escrita < 0 || fechamento != 0) {
        printf("Falha ao salvar\n");
        return 1;
    }
    printf("Arquivo fechado\n");
    return 0;
}
''', "Arquivo fechado\n"),
    "fprintf": exemplo(r'''
#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("resultado.txt", "w");
    if (arquivo == NULL) return 1;
    int escrita = fprintf(arquivo, "Resposta: %d\n", 42);
    int fechamento = fclose(arquivo);
    if (escrita < 0 || fechamento != 0) {
        printf("Falha ao gravar\n");
        return 1;
    }
    printf("Gravado\n");
    return 0;
}
''', "Gravado\n"),
    "fscanf": exemplo(r'''
#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("numeros.txt", "w");
    if (arquivo == NULL) return 1;
    int escrita = fprintf(arquivo, "19 23\n");
    int fechamento = fclose(arquivo);
    if (escrita < 0 || fechamento != 0) return 1;

    arquivo = fopen("numeros.txt", "r");
    if (arquivo == NULL) return 1;
    int a, b;
    int lidos = fscanf(arquivo, "%d %d", &a, &b);
    fechamento = fclose(arquivo);
    if (lidos != 2 || fechamento != 0) return 1;
    printf("%d\n", a + b);
    return 0;
}
''', "42\n"),
    "stdlib": exemplo(r'''
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int main(void) {
    const char texto[] = "42";
    char *fim;
    errno = 0;
    long valor = strtol(texto, &fim, 10);
    if (fim == texto || *fim != '\0' || errno == ERANGE ||
        valor < INT_MIN || valor > INT_MAX) {
        printf("Inteiro invalido\n");
        return 1;
    }
    int numero = (int) valor;
    printf("%d\n", numero);
    return 0;
}
''', "42\n"),
    "validação": exemplo(r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

int main(void) {
    char linha[64];
    printf("Idade (0 a 120): ");
    fflush(stdout);
    if (fgets(linha, sizeof linha, stdin) == NULL) return 1;
    if (strchr(linha, '\n') == NULL && !feof(stdin)) {
        printf("Linha longa demais\n");
        return 1;
    }

    char *fim;
    errno = 0;
    long idade = strtol(linha, &fim, 10);
    int houve_digitos = fim != linha;
    while (isspace((unsigned char) *fim)) fim++;
    if (!houve_digitos || *fim != '\0' || errno == ERANGE ||
        idade < 0 || idade > 120) {
        printf("Idade invalida\n");
        return 1;
    }
    printf("Idade aceita: %ld\n", idade);
    return 0;
}
''', "Idade (0 a 120): Idade aceita: 18\n", "18\n", tuple(
        {"entrada": entrada, "saida": "Idade (0 a 120): Idade invalida\n", "retorno": 1}
        for entrada in ("abc\n", "18abc\n", "-1\n", "121\n", "\n", "999999999999999999999999\n")
    ) + (
        {"entrada": "0\n", "saida": "Idade (0 a 120): Idade aceita: 0\n", "retorno": 0},
        {"entrada": "120\n", "saida": "Idade (0 a 120): Idade aceita: 120\n", "retorno": 0},
        {"entrada": " 18 \n", "saida": "Idade (0 a 120): Idade aceita: 18\n", "retorno": 0},
        {"entrada": "1" * 70 + "\n", "saida": "Idade (0 a 120): Linha longa demais\n", "retorno": 1},
        {"entrada": "", "saida": "Idade (0 a 120): ", "retorno": 1},
    )),
    "listas": exemplo(r'''
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No *proximo;
} No;

void liberar(No *atual) {
    while (atual != NULL) {
        No *proximo = atual->proximo;
        free(atual);
        atual = proximo;
    }
}

int main(void) {
    No *inicio = NULL;
    const int valores[] = {12, 20, 10};
    for (int i = 0; i < 3; i++) {
        No *novo = malloc(sizeof *novo);
        if (novo == NULL) {
            liberar(inicio);
            return 1;
        }
        novo->valor = valores[i];
        novo->proximo = inicio;
        inicio = novo;
    }
    int total = 0;
    for (No *p = inicio; p != NULL; p = p->proximo) {
        total += p->valor;
    }
    printf("Soma: %d\n", total);
    liberar(inicio);
    return 0;
}
''', "Soma: 42\n"),
    "pilhas": exemplo(r'''
#include <stdio.h>
#define CAPACIDADE 2

typedef struct {
    int dados[CAPACIDADE];
    int quantidade;
} Pilha;

int push(Pilha *pilha, int valor) {
    if (pilha->quantidade == CAPACIDADE) return 0;
    pilha->dados[pilha->quantidade++] = valor;
    return 1;
}

int pop(Pilha *pilha, int *valor) {
    if (pilha->quantidade == 0) return 0;
    *valor = pilha->dados[--pilha->quantidade];
    return 1;
}

int main(void) {
    Pilha pilha = {{0}, 0};
    if (!push(&pilha, 10) || !push(&pilha, 20)) return 1;
    if (!push(&pilha, 30)) printf("Pilha cheia\n");
    int valor;
    while (pop(&pilha, &valor)) printf("Pop: %d\n", valor);
    if (!pop(&pilha, &valor)) printf("Pilha vazia\n");
    return 0;
}
''', "Pilha cheia\nPop: 20\nPop: 10\nPilha vazia\n"),
    "filas": exemplo(r'''
#include <stdio.h>
#define CAPACIDADE 2

typedef struct {
    int dados[CAPACIDADE];
    int inicio;
    int quantidade;
} Fila;

int inserir(Fila *fila, int valor) {
    if (fila->quantidade == CAPACIDADE) return 0;
    int fim = (fila->inicio + fila->quantidade) % CAPACIDADE;
    fila->dados[fim] = valor;
    fila->quantidade++;
    return 1;
}

int remover(Fila *fila, int *valor) {
    if (fila->quantidade == 0) return 0;
    *valor = fila->dados[fila->inicio];
    fila->inicio = (fila->inicio + 1) % CAPACIDADE;
    fila->quantidade--;
    return 1;
}

int main(void) {
    Fila fila = {{0}, 0, 0};
    if (!inserir(&fila, 10) || !inserir(&fila, 20)) return 1;
    if (!inserir(&fila, 30)) printf("Fila cheia\n");
    int valor;
    if (remover(&fila, &valor)) printf("Saiu: %d\n", valor);
    if (!inserir(&fila, 30)) return 1;
    while (remover(&fila, &valor)) printf("Saiu: %d\n", valor);
    if (!remover(&fila, &valor)) printf("Fila vazia\n");
    return 0;
}
''', "Fila cheia\nSaiu: 10\nSaiu: 20\nSaiu: 30\nFila vazia\n"),
    "busca linear": exemplo(r'''
#include <stdio.h>

int buscar(const int valores[], int quantidade, int alvo) {
    for (int i = 0; i < quantidade; i++) {
        if (valores[i] == alvo) return i;
    }
    return -1;
}

int main(void) {
    const int valores[] = {4, 8, 15, 16};
    int posicao = buscar(valores, 4, 15);
    if (posicao >= 0) printf("Encontrado no indice %d\n", posicao);
    if (buscar(valores, 4, 99) == -1) printf("Nao encontrado\n");
    return 0;
}
''', "Encontrado no indice 2\nNao encontrado\n"),
    "calculadora": exemplo(r'''
#include <stdio.h>
#include <math.h>

int calcular(double a, double b, char operador, double *resultado) {
    switch (operador) {
        case '+': *resultado = a + b; break;
        case '-': *resultado = a - b; break;
        case '*': *resultado = a * b; break;
        case '/':
            if (b == 0.0) return 0;
            *resultado = a / b;
            break;
        default: return 0;
    }
    return isfinite(*resultado);
}

int main(void) {
    double a, b, resultado;
    char operador;
    printf("Conta (ex.: 8 / 2): ");
    fflush(stdout);
    if (scanf("%lf %c %lf", &a, &operador, &b) != 3 ||
        !isfinite(a) || !isfinite(b)) {
        printf("Entrada invalida\n");
        return 1;
    }
    if (!calcular(a, b, operador, &resultado)) {
        printf("Operacao invalida\n");
        return 1;
    }
    printf("Resultado: %.2f\n", resultado);
    return 0;
}
''', "Conta (ex.: 8 / 2): Resultado: 4.00\n", "8 / 2\n", (
        {"entrada": "8 / 0\n", "saida": "Conta (ex.: 8 / 2): Operacao invalida\n", "retorno": 1},
        {"entrada": "8 ? 2\n", "saida": "Conta (ex.: 8 / 2): Operacao invalida\n", "retorno": 1},
        {"entrada": "abc\n", "saida": "Conta (ex.: 8 / 2): Entrada invalida\n", "retorno": 1},
        {"entrada": "1.5 + 2\n", "saida": "Conta (ex.: 8 / 2): Resultado: 3.50\n", "retorno": 0},
        {"entrada": "3 - 8\n", "saida": "Conta (ex.: 8 / 2): Resultado: -5.00\n", "retorno": 0},
        {"entrada": "3 * 8\n", "saida": "Conta (ex.: 8 / 2): Resultado: 24.00\n", "retorno": 0},
    )),
    "cadastro": exemplo(r'''
#include <stdio.h>
#include <string.h>
#define CAPACIDADE 2

typedef struct { char nome[30]; int idade; } Pessoa;

int adicionar(Pessoa pessoas[], int *quantidade, const char *nome, int idade) {
    if (*quantidade >= CAPACIDADE || nome[0] == '\0' ||
        strlen(nome) >= sizeof pessoas[0].nome || idade < 0 || idade > 120) {
        return 0;
    }
    Pessoa nova;
    strcpy(nova.nome, nome);
    nova.idade = idade;
    pessoas[*quantidade] = nova;
    (*quantidade)++;
    return 1;
}

int main(void) {
    Pessoa pessoas[CAPACIDADE];
    int quantidade = 0;
    if (!adicionar(pessoas, &quantidade, "Lia", 21)) return 1;
    if (!adicionar(pessoas, &quantidade, "Rui", 35)) return 1;
    if (!adicionar(pessoas, &quantidade, "Eva", 19)) printf("Cadastro cheio\n");
    for (int i = 0; i < quantidade; i++) {
        printf("%s: %d anos\n", pessoas[i].nome, pessoas[i].idade);
    }
    return 0;
}
''', "Cadastro cheio\nLia: 21 anos\nRui: 35 anos\n"),
    "agenda": exemplo(r'''
#include <stdio.h>
#include <string.h>

typedef struct { char nome[30]; char telefone[20]; } Contato;

int buscar(const Contato contatos[], int quantidade, const char *nome) {
    for (int i = 0; i < quantidade; i++) {
        if (strcmp(contatos[i].nome, nome) == 0) return i;
    }
    return -1;
}

int main(void) {
    const Contato contatos[] = {{"Lia", "0123-4567"}, {"Rui", "9876-5432"}};
    int posicao = buscar(contatos, 2, "Lia");
    if (posicao >= 0) printf("%s\n", contatos[posicao].telefone);
    if (buscar(contatos, 2, "Eva") == -1) printf("Contato nao encontrado\n");
    return 0;
}
''', "0123-4567\nContato nao encontrado\n"),
    "jogo terminal": exemplo(r'''
#include <stdio.h>

int main(void) {
    const int segredo = 17;
    int tentativa;
    for (;;) {
        printf("Palpite (1 a 20): ");
        fflush(stdout);
        if (scanf("%d", &tentativa) != 1) {
            printf("Entrada encerrada ou invalida\n");
            return 1;
        }
        if (tentativa < 1 || tentativa > 20) {
            printf("Fora do intervalo\n");
            continue;
        }
        if (tentativa < segredo) printf("Maior\n");
        else if (tentativa > segredo) printf("Menor\n");
        else {
            printf("Acertou\n");
            break;
        }
    }
    return 0;
}
''', "Palpite (1 a 20): Maior\nPalpite (1 a 20): Menor\nPalpite (1 a 20): Acertou\n", "10\n20\n17\n", (
        {"entrada": "0\n17\n", "saida": "Palpite (1 a 20): Fora do intervalo\nPalpite (1 a 20): Acertou\n", "retorno": 0},
        {"entrada": "abc\n", "saida": "Palpite (1 a 20): Entrada encerrada ou invalida\n", "retorno": 1},
        {"entrada": "", "saida": "Palpite (1 a 20): Entrada encerrada ou invalida\n", "retorno": 1},
    )),
    "sistema biblioteca": exemplo(r'''
#include <stdio.h>

typedef enum { DISPONIVEL, EMPRESTADO } Estado;
typedef struct { int id; char titulo[40]; Estado estado; } Livro;

int emprestar(Livro *livro) {
    if (livro == NULL || livro->estado != DISPONIVEL) return 0;
    livro->estado = EMPRESTADO;
    return 1;
}

int devolver(Livro *livro) {
    if (livro == NULL || livro->estado != EMPRESTADO) return 0;
    livro->estado = DISPONIVEL;
    return 1;
}

int main(void) {
    Livro livro = {1, "Estudando C", DISPONIVEL};
    if (emprestar(&livro)) printf("Emprestimo confirmado\n");
    if (!emprestar(&livro)) printf("Livro indisponivel\n");
    if (devolver(&livro)) printf("Devolucao confirmada\n");
    if (!devolver(&livro)) printf("Livro ja disponivel\n");
    return 0;
}
''', "Emprestimo confirmado\nLivro indisponivel\nDevolucao confirmada\nLivro ja disponivel\n"),
    "projeto final": exemplo(r'''
#include <stdio.h>

int calcular_media(const double notas[], int quantidade, double *resultado) {
    if (quantidade <= 0) return 0;
    double total = 0.0;
    for (int i = 0; i < quantidade; i++) total += notas[i];
    *resultado = total / quantidade;
    return 1;
}

int main(void) {
    const double notas[] = {7.0, 8.0, 9.0};
    double media;
    if (calcular_media(notas, 3, &media)) printf("Media: %.2f\n", media);
    if (!calcular_media(notas, 0, &media)) printf("Sem notas para calcular\n");
    return 0;
}
''', "Media: 8.00\nSem notas para calcular\n"),
}


# Uma aplicacao de varios arquivos para leitura nas licoes de modularizacao/build.
ARQUIVOS_BUILD = [
    {"nome": "calculos.h", "codigo": "#ifndef ENSINAR_C_CALCULOS_H\n#define ENSINAR_C_CALCULOS_H\n\nint dobro(int valor);\n\n#endif\n"},
    {"nome": "calculos.c", "codigo": '#include "calculos.h"\n\nint dobro(int valor) {\n    return valor * 2;\n}\n'},
    {"nome": "main.c", "codigo": '#include <stdio.h>\n#include "calculos.h"\n\nint main(void) {\n    printf("%d\\n", dobro(21));\n    return 0;\n}\n'},
    {"nome": "Makefile", "codigo": "CC = gcc\nCFLAGS = -std=c11 -Wall -Wextra -pedantic\n\nprograma: main.o calculos.o\n\t$(CC) main.o calculos.o -o programa\n\nmain.o: main.c calculos.h\n\t$(CC) $(CFLAGS) -c main.c -o main.o\n\ncalculos.o: calculos.c calculos.h\n\t$(CC) $(CFLAGS) -c calculos.c -o calculos.o\n"},
]
