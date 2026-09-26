"""Solução de referência de cada exercício de código, mostrada depois que o aluno passa na correção.

Um teste automático garante que cada solução compila sem avisos e passa na correção da própria lição.
"""

SOLUCOES = {
    "printf": (
        r'''#include <stdio.h>

int main(void) {
    printf("Ola, C\n");  /* \n termina a linha */
    return 0;
}''',
        "printf mostra o texto entre aspas exatamente como está escrito; o \\n pula para a próxima linha.",
    ),
    "scanf": (
        r'''#include <stdio.h>

int main(void) {
    int numero;
    printf("Digite um numero: ");
    scanf("%d", &numero);            /* & entrega o endereço de numero */
    printf("Numero: %d\n", numero);
    return 0;
}''',
        "scanf precisa do endereço da variável (&numero) para gravar o valor digitado; depois o printf mostra esse valor.",
    ),
    "int": (
        r'''#include <stdio.h>

int main(void) {
    int idade = 20;
    printf("Idade: %d\n", idade);
    return 0;
}''',
        "A variável é declarada e inicializada na mesma linha; %d é o especificador de int.",
    ),
    "float e double": (
        r'''#include <stdio.h>

int main(void) {
    double nota = 9.5;
    printf("Nota: %.1f\n", nota);   /* .1 mostra uma casa decimal */
    return 0;
}''',
        "double guarda números com parte decimal; %.1f mostra uma casa depois da vírgula.",
    ),
    "char": (
        r'''#include <stdio.h>

int main(void) {
    char letra = 'C';               /* aspas simples: um caractere */
    printf("Letra: %c\n", letra);
    return 0;
}''',
        "Um char usa aspas simples e é mostrado com %c.",
    ),
    "constantes": (
        r'''#include <stdio.h>

int main(void) {
    const int ANO = 2026;           /* const impede mudar o valor depois */
    printf("Ano: %d\n", ANO);
    return 0;
}''',
        "const cria um valor que o programa não pode alterar; nomes em maiúsculas indicam constantes.",
    ),
    "#define": (
        r'''#include <stdio.h>

#define ESCOLA "Ensinar C"

int main(void) {
    printf("%s\n", ESCOLA);         /* o pré-processador troca ESCOLA pelo texto */
    return 0;
}''',
        "#define troca o nome ESCOLA pelo texto antes da compilação; %s mostra strings.",
    ),
    "escopo": (
        r'''#include <stdio.h>

int main(void) {
    int valor = 30;                 /* local: existe só dentro de main */
    printf("Valor: %d\n", valor);
    return 0;
}''',
        "Uma variável declarada dentro de main é local: só pode ser usada dentro dessa função.",
    ),
    "soma": (
        r'''#include <stdio.h>

int main(void) {
    int a = 18;
    int b = 24;
    int soma = a + b;
    printf("Soma: %d\n", soma);
    return 0;
}''',
        "O resultado de a + b é guardado em uma terceira variável antes de ser mostrado.",
    ),
    "subtração": (
        r'''#include <stdio.h>

int main(void) {
    int saldo = 100;
    int retirada = 58;
    saldo = saldo - retirada;
    printf("Saldo: %d\n", saldo);
    return 0;
}''',
        "O novo saldo é o antigo menos a retirada; a variável recebe o resultado da conta.",
    ),
    "multiplicação": (
        r'''#include <stdio.h>

int main(void) {
    int produto = 6 * 7;
    printf("Produto: %d\n", produto);
    return 0;
}''',
        "O operador * multiplica; o resultado é calculado e guardado em produto.",
    ),
    "divisão": (
        r'''#include <stdio.h>

int main(void) {
    double resultado = 10.0 / 4.0;  /* com .0 a divisão é real, não inteira */
    printf("%.2f\n", resultado);
    return 0;
}''',
        "Como os dois números são decimais, a divisão mantém a parte fracionária; %.2f mostra duas casas.",
    ),
    "operadores relacionais": (
        r'''#include <stdio.h>

int main(void) {
    int a = 42;
    int b = 30;
    printf("%d %d %d\n", a > b, a == b, a != b);  /* 1 = verdadeiro, 0 = falso */
    return 0;
}''',
        "Comparações em C valem 1 quando são verdadeiras e 0 quando são falsas.",
    ),
    "operadores lógicos": (
        r'''#include <stdio.h>

int main(void) {
    int resultado = (10 > 5) && (3 < 8);   /* as duas partes são verdadeiras */
    printf("Resultado: %d\n", resultado);
    return 0;
}''',
        "&& só dá 1 quando os dois lados são verdadeiros.",
    ),
    "incremento": (
        r'''#include <stdio.h>

int main(void) {
    int contador = 40;
    contador++;
    contador++;
    printf("Contador: %d\n", contador);
    return 0;
}''',
        "contador++ soma 1 ao valor atual; usado duas vezes, 40 vira 42.",
    ),
    "if": (
        r'''#include <stdio.h>

int main(void) {
    int numero;
    scanf("%d", &numero);
    if (numero > 0) {
        printf("Positivo\n");
    }
    return 0;
}''',
        "O bloco do if só executa quando a condição é verdadeira; para zero ou negativos nada é mostrado.",
    ),
    "else": (
        r'''#include <stdio.h>

int main(void) {
    int idade;
    scanf("%d", &idade);
    if (idade >= 18) {
        printf("Maior de idade\n");
    } else {
        printf("Menor de idade\n");
    }
    return 0;
}''',
        "O else cobre todos os casos em que a condição do if é falsa.",
    ),
    "else if": (
        r'''#include <stdio.h>

int main(void) {
    int nota;
    scanf("%d", &nota);
    if (nota >= 9) {
        printf("Conceito A\n");
    } else if (nota >= 7) {         /* só é testado se a nota for menor que 9 */
        printf("Conceito B\n");
    } else {
        printf("Conceito C\n");
    }
    return 0;
}''',
        "As condições são testadas em ordem; a primeira verdadeira escolhe o conceito e as outras são puladas.",
    ),
    "switch": (
        r'''#include <stdio.h>

int main(void) {
    int opcao;
    scanf("%d", &opcao);
    switch (opcao) {
        case 1:
            printf("Cadastrar\n");
            break;                  /* sem break, o próximo case também executaria */
        case 2:
            printf("Consultar\n");
            break;
        case 3:
            printf("Sair\n");
            break;
        default:
            printf("Opcao invalida\n");
    }
    return 0;
}''',
        "Cada case trata um valor e termina com break; default pega qualquer outra opção.",
    ),
    "ternário": (
        r'''#include <stdio.h>

int main(void) {
    int a = 17;
    int b = 42;
    int maior = a > b ? a : b;      /* condição ? se verdadeiro : se falso */
    printf("Maior: %d\n", maior);
    return 0;
}''',
        "O ternário escolhe entre dois valores em uma única expressão.",
    ),
    "while": (
        r'''#include <stdio.h>

int main(void) {
    int numero = 1;
    int soma = 0;
    while (numero <= 6) {
        soma += numero;
        numero++;
    }
    printf("Soma: %d\n", soma);
    return 0;
}''',
        "O laço repete enquanto numero for até 6, acumulando cada valor em soma.",
    ),
    "do while": (
        r'''#include <stdio.h>

int main(void) {
    int numero = 1;
    do {
        printf("%d\n", numero);
        numero++;
    } while (numero <= 3);          /* a condição é testada depois de cada volta */
    return 0;
}''',
        "O do while executa o bloco pelo menos uma vez e só depois confere a condição.",
    ),
    "for": (
        r'''#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 5; i++) {
        printf("%d ", i * i);
    }
    printf("\n");
    return 0;
}''',
        "O for reúne início, condição e passo; em cada volta é mostrado o quadrado de i.",
    ),
    "break": (
        r'''#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 10; i++) {
        if (i == 6) {
            break;                  /* sai do laço imediatamente */
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}''',
        "break encerra o laço assim que i chega a 6, então só 1 a 5 são mostrados.",
    ),
    "continue": (
        r'''#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 9; i++) {
        if (i % 3 == 0) {
            continue;               /* pula para a próxima volta */
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}''',
        "continue pula o restante da volta atual; os múltiplos de 3 não chegam ao printf.",
    ),
    "criando função": (
        r'''#include <stdio.h>

void exibirMensagem(void) {
    printf("Funcao chamada\n");
}

int main(void) {
    exibirMensagem();
    return 0;
}''',
        "A função é definida antes de main e chamada pelo nome; void indica que ela não retorna valor.",
    ),
    "parâmetros": (
        r'''#include <stdio.h>

int soma(int a, int b) {
    return a + b;
}

int main(void) {
    printf("%d\n", soma(19, 23));
    return 0;
}''',
        "Os valores 19 e 23 são copiados para os parâmetros a e b; o return devolve a soma para main.",
    ),
    "retorno": (
        r'''#include <stdio.h>

int quadrado(int n) {
    return n * n;
}

int main(void) {
    printf("%d\n", quadrado(7));
    return 0;
}''',
        "return devolve o resultado para quem chamou; quadrado(7) vale 49.",
    ),
    "protótipos": (
        r'''#include <stdio.h>

int dobro(int n);                   /* protótipo: avisa que a função existe */

int main(void) {
    printf("%d\n", dobro(21));
    return 0;
}

int dobro(int n) {
    return n * 2;
}''',
        "O protótipo antes de main permite chamar dobro mesmo que ela seja escrita depois.",
    ),
    "recursão": (
        r'''#include <stdio.h>

int fatorial(int n) {
    if (n <= 1) {
        return 1;                   /* caso de parada */
    }
    return n * fatorial(n - 1);
}

int main(void) {
    printf("%d\n", fatorial(5));
    return 0;
}''',
        "Cada chamada reduz n em 1 até chegar ao caso de parada; 5 * 4 * 3 * 2 * 1 = 120.",
    ),
    "arrays": (
        r'''#include <stdio.h>

int main(void) {
    int valores[6] = {4, 8, 15, 16, 23, 42};
    int soma = 0;
    for (int i = 0; i < 6; i++) {   /* índices vão de 0 a 5 */
        soma += valores[i];
    }
    printf("%d\n", soma);
    return 0;
}''',
        "O laço visita cada posição do vetor, do índice 0 ao 5, acumulando os valores.",
    ),
    "matrizes": (
        r'''#include <stdio.h>

int main(void) {
    int matriz[2][2] = {{10, 2}, {3, 32}};
    int diagonal = 0;
    for (int i = 0; i < 2; i++) {
        diagonal += matriz[i][i];   /* linha e coluna iguais */
    }
    printf("%d\n", diagonal);
    return 0;
}''',
        "Na diagonal principal a linha é igual à coluna, por isso basta matriz[i][i].",
    ),
    "strings": (
        r'''#include <stdio.h>

int main(void) {
    char texto[] = "Linguagem C";
    for (int i = 0; texto[i] != '\0'; i++) {   /* '\0' marca o fim do texto */
        printf("%c", texto[i]);
    }
    printf("\n");
    return 0;
}''',
        "Uma string termina no caractere '\\0'; o laço mostra cada letra até encontrá-lo.",
    ),
    "strlen": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const char palavra[] = "compilar";
    printf("%zu\n", strlen(palavra));   /* %zu é o formato de size_t */
    return 0;
}''',
        "strlen conta os caracteres antes do '\\0' e devolve um size_t, mostrado com %zu.",
    ),
    "strcpy": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char destino[20];
    strcpy(destino, "C seguro");    /* o destino tem espaço para o texto e o '\0' */
    printf("%s\n", destino);
    return 0;
}''',
        "strcpy copia o texto para o vetor; ele precisa ter espaço para as letras e o '\\0'.",
    ),
    "strcmp": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    const char a[] = "casa";
    const char b[] = "casa";
    if (strcmp(a, b) == 0) {        /* 0 significa textos iguais */
        printf("Iguais\n");
    }
    return 0;
}''',
        "Textos não se comparam com ==; strcmp devolve 0 quando as duas strings são iguais.",
    ),
    "strcat": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char destino[30] = "Curso ";
    strcat(destino, "de C");        /* acrescenta no fim do texto */
    printf("%s\n", destino);
    return 0;
}''',
        "strcat junta o segundo texto ao final do primeiro, que precisa ter espaço sobrando.",
    ),
    "fgets": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char nome[50];
    if (fgets(nome, sizeof(nome), stdin) != NULL) {
        nome[strcspn(nome, "\n")] = '\0';   /* remove o Enter lido pelo fgets */
        printf("Ola, %s\n", nome);
    }
    return 0;
}''',
        "fgets lê a linha inteira, com espaços, respeitando o tamanho do vetor; strcspn acha o Enter para removê-lo.",
    ),
    "memória": (
        r'''#include <stdio.h>

int main(void) {
    printf("int: %zu bytes\n", sizeof(int));
    printf("double: %zu bytes\n", sizeof(double));
    return 0;
}''',
        "sizeof informa quantos bytes um tipo ocupa na memória desta máquina.",
    ),
    "operador &": (
        r'''#include <stdio.h>

int main(void) {
    int valor = 42;
    int *ponteiro = &valor;         /* ponteiro guarda o endereço de valor */
    printf("%d\n", *ponteiro);      /* * acessa o valor nesse endereço */
    return 0;
}''',
        "& obtém o endereço de valor; *ponteiro lê o conteúdo guardado naquele endereço.",
    ),
    "ponteiros + funções": (
        r'''#include <stdio.h>

void trocar(int *a, int *b) {
    int temporario = *a;
    *a = *b;
    *b = temporario;
}

int main(void) {
    int x = 10;
    int y = 42;
    trocar(&x, &y);                 /* passa os endereços para a função alterar x e y */
    printf("%d %d\n", x, y);
    return 0;
}''',
        "Recebendo endereços, a função altera as variáveis originais de main, e não cópias.",
    ),
    "ponteiros + arrays": (
        r'''#include <stdio.h>

int main(void) {
    int valores[3] = {10, 20, 12};
    int *p = valores;               /* o nome do vetor é o endereço do primeiro elemento */
    int soma = 0;
    for (int i = 0; i < 3; i++) {
        soma += *(p + i);           /* p + i avança i posições de int */
    }
    printf("%d\n", soma);
    return 0;
}''',
        "p aponta para o primeiro elemento; *(p + i) lê o elemento i, igual a valores[i].",
    ),
    "ponteiro para ponteiro": (
        r'''#include <stdio.h>

int main(void) {
    int valor = 10;
    int *p = &valor;
    int **pp = &p;                  /* pp guarda o endereço de p */
    **pp = 42;                      /* dois * chegam até valor */
    printf("%d\n", valor);
    return 0;
}''',
        "*pp é o ponteiro p e **pp é o próprio valor; por isso a atribuição muda valor.",
    ),
    "malloc": (
        r'''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *valores = malloc(3 * sizeof(int));
    if (valores == NULL) {          /* malloc devolve NULL quando falta memória */
        return 1;
    }
    valores[0] = 10;
    valores[1] = 20;
    valores[2] = 12;
    printf("%d\n", valores[0] + valores[1] + valores[2]);
    free(valores);
    return 0;
}''',
        "malloc reserva espaço para três int; o programa confere NULL, usa a memória e a libera com free.",
    ),
    "calloc": (
        r'''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *valores = calloc(4, sizeof(int));   /* calloc já zera a memória */
    if (valores == NULL) {
        return 1;
    }
    valores[3] += 42;
    for (int i = 0; i < 4; i++) {
        printf("%d ", valores[i]);
    }
    printf("\n");
    free(valores);
    return 0;
}''',
        "Diferente de malloc, calloc entrega a memória zerada; só a última posição recebe 42.",
    ),
    "realloc": (
        r'''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *valores = malloc(2 * sizeof(int));
    if (valores == NULL) {
        return 1;
    }
    valores[0] = 10;
    valores[1] = 20;

    int *temporario = realloc(valores, 3 * sizeof(int));
    if (temporario == NULL) {       /* em caso de falha, o bloco antigo continua válido */
        free(valores);
        return 1;
    }
    valores = temporario;
    valores[2] = 12;

    printf("%d\n", valores[0] + valores[1] + valores[2]);
    free(valores);
    return 0;
}''',
        "O resultado do realloc vai para um ponteiro temporário: se falhar, o bloco original não se perde.",
    ),
    "free": (
        r'''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *valor = malloc(sizeof(int));
    if (valor == NULL) {
        return 1;
    }
    *valor = 42;
    printf("%d\n", *valor);
    free(valor);
    valor = NULL;                   /* evita usar o endereço já liberado */
    return 0;
}''',
        "Depois do free, atribuir NULL evita usar por engano a memória que já foi devolvida.",
    ),
    "memory leak": (
        r'''#include <stdio.h>
#include <stdlib.h>

static int usarValor(void) {
    int *valor = malloc(sizeof(int));
    if (valor == NULL) {
        return 0;
    }
    *valor = 42;
    int resultado = *valor;
    free(valor);                    /* libera antes de sair da função */
    return resultado;
}

int main(void) {
    printf("%d\n", usarValor());
    return 0;
}''',
        "O valor é copiado para uma variável comum e a memória é liberada antes do return, sem vazamento.",
    ),
    "structs": (
        r'''#include <stdio.h>

struct Produto {
    char nome[20];
    double preco;
};

int main(void) {
    struct Produto produto = {"Livro", 42.0};
    printf("%s: %.2f\n", produto.nome, produto.preco);
    return 0;
}''',
        "A struct agrupa nome e preço; cada campo é acessado com o ponto (produto.nome).",
    ),
    "typedef": (
        r'''#include <stdio.h>

typedef struct {
    int x;
    int y;
} Ponto;

int main(void) {
    Ponto ponto = {19, 23};         /* com typedef não é preciso escrever struct */
    printf("%d\n", ponto.x + ponto.y);
    return 0;
}''',
        "typedef dá o nome Ponto ao tipo, deixando as declarações mais curtas.",
    ),
    "unions": (
        r'''#include <stdio.h>

union Numero {
    int inteiro;
    double decimal;
};

int main(void) {
    union Numero numero;
    numero.inteiro = 42;            /* só o último membro gravado é válido */
    printf("%d\n", numero.inteiro);
    return 0;
}''',
        "Os membros de uma union dividem a mesma memória; lê-se o membro que foi gravado por último.",
    ),
    "enum": (
        r'''#include <stdio.h>

enum Status { PENDENTE, ATIVO, CONCLUIDO };

int main(void) {
    enum Status status = ATIVO;
    switch (status) {
        case PENDENTE:
            printf("Pendente\n");
            break;
        case ATIVO:
            printf("Ativo\n");
            break;
        case CONCLUIDO:
            printf("Concluido\n");
            break;
    }
    return 0;
}''',
        "O enum dá nomes a valores inteiros; o switch escolhe o texto de acordo com o status.",
    ),
    "fopen": (
        r'''#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("dados.txt", "w");
    if (arquivo == NULL) {          /* a abertura pode falhar */
        return 1;
    }
    printf("Arquivo aberto\n");
    fclose(arquivo);
    return 0;
}''',
        "fopen devolve NULL quando não consegue abrir; o arquivo aberto sempre precisa de fclose.",
    ),
    "fclose": (
        r'''#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("dados.txt", "w");
    if (arquivo == NULL) {
        return 1;
    }
    fprintf(arquivo, "%d\n", 42);
    if (fclose(arquivo) == 0) {     /* 0 indica que tudo foi gravado */
        printf("Arquivo fechado\n");
    }
    return 0;
}''',
        "fclose grava o que estava pendente e devolve 0 quando dá certo.",
    ),
    "fprintf": (
        r'''#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("resultado.txt", "w");
    if (arquivo == NULL) {
        return 1;
    }
    fprintf(arquivo, "Resposta: %d\n", 42);   /* igual ao printf, mas no arquivo */
    fclose(arquivo);
    printf("Gravado\n");
    return 0;
}''',
        "fprintf funciona como o printf, só que escreve no arquivo indicado.",
    ),
    "fscanf": (
        r'''#include <stdio.h>

int main(void) {
    FILE *arquivo = fopen("numeros.txt", "w");
    if (arquivo == NULL) {
        return 1;
    }
    fprintf(arquivo, "19 23\n");
    fclose(arquivo);

    arquivo = fopen("numeros.txt", "r");
    if (arquivo == NULL) {
        return 1;
    }
    int a;
    int b;
    if (fscanf(arquivo, "%d %d", &a, &b) == 2) {   /* confere se leu os dois */
        printf("%d\n", a + b);
    }
    fclose(arquivo);
    return 0;
}''',
        "O arquivo é gravado, fechado e reaberto para leitura; fscanf devolve quantos valores leu.",
    ),
    ".h": (
        r'''#include <stdio.h>

/* Seção que ficaria em um arquivo .h */
int somar(int a, int b);

int main(void) {
    printf("%d\n", somar(19, 23));
    return 0;
}

/* Implementação que ficaria em um arquivo .c */
int somar(int a, int b) {
    return a + b;
}''',
        "O protótipo faz o papel do .h (a interface) e a definição depois de main faz o papel do .c.",
    ),
    ".c": (
        r'''#include <stdio.h>

/* Protótipos */
int triplo(int n);

/* Programa principal */
int main(void) {
    printf("%d\n", triplo(14));
    return 0;
}

/* Implementação */
int triplo(int n) {
    return n * 3;
}''',
        "Separar protótipos, main e implementação imita a organização de um projeto em vários arquivos.",
    ),
    "include guards": (
        r'''#include <stdio.h>

#ifndef MATEMATICA_H
#define MATEMATICA_H
int dobro(int n);
#endif

int main(void) {
    printf("%d\n", dobro(21));
    return 0;
}

int dobro(int n) {
    return n * 2;
}''',
        "#ifndef/#define/#endif impedem que o mesmo cabeçalho seja incluído duas vezes.",
    ),
    "stdio": (
        r'''#include <stdio.h>

int main(void) {
    int numero;
    if (scanf("%d", &numero) == 1) {
        printf("%d\n", numero * 2);
    }
    return 0;
}''',
        "scanf e printf vêm de stdio.h; conferir o retorno do scanf garante que um número foi lido.",
    ),
    "stdlib": (
        r'''#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const char texto[] = "42";
    char *fim;
    long numero = strtol(texto, &fim, 10);   /* base 10 */
    if (*fim == '\0') {             /* o texto inteiro era um número */
        printf("%ld\n", numero);
    }
    return 0;
}''',
        "strtol converte o texto e indica em fim onde parou; se parou no '\\0', a conversão foi completa.",
    ),
    "string": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char texto[10];
    strcpy(texto, "C");
    strcat(texto, "11");
    if (strcmp(texto, "C11") == 0) {
        printf("%s: correto\n", texto);
    }
    return 0;
}''',
        "strcpy começa o texto, strcat acrescenta e strcmp confirma o resultado.",
    ),
    "math": (
        r'''#include <stdio.h>
#include <math.h>

int main(void) {
    printf("%.0f\n", sqrt(1764.0));   /* %.0f: sem casas decimais */
    return 0;
}''',
        "sqrt devolve um double; %.0f mostra o número sem casas decimais.",
    ),
    "bitwise": (
        r'''#include <stdio.h>

int main(void) {
    unsigned valor = 21u;
    printf("%u\n", valor << 1);    /* deslocar 1 bit à esquerda multiplica por 2 */
    return 0;
}''',
        "Deslocar os bits uma posição para a esquerda dobra o valor: 21 vira 42.",
    ),
    "máscaras": (
        r'''#include <stdio.h>

#define LER      (1u << 0)
#define ESCREVER (1u << 1)
#define EXECUTAR (1u << 2)

int main(void) {
    unsigned permissoes = LER | EXECUTAR;   /* | liga os bits */
    if ((permissoes & EXECUTAR) != 0u) {    /* & testa um bit */
        printf("Pode executar\n");
    }
    return 0;
}''',
        "Cada permissão ocupa um bit; | liga bits e & verifica se um bit específico está ligado.",
    ),
    "erros de sintaxe": (
        r'''#include <stdio.h>

int main(void) {
    int resposta = 42;
    printf("%d\n", resposta);
    return 0;
}''',
        "Todas as instruções terminam com ponto e vírgula e cada { tem o seu }.",
    ),
    "erros lógicos": (
        r'''#include <stdio.h>

int main(void) {
    double media = (8.0 + 10.0 + 12.0) / 3.0;   /* parênteses: soma antes de dividir */
    printf("%.2f\n", media);
    return 0;
}''',
        "Sem os parênteses só o 12.0 seria dividido por 3; o erro não aparece na compilação, só no resultado.",
    ),
    "debug": (
        r'''#include <stdio.h>

int main(void) {
    int valores[3] = {10, 20, 12};
    int total = 0;
    for (int i = 0; i < 3; i++) {
        total += valores[i];
        printf("Indice %d: %d\n", i, valores[i]);   /* rastreia cada passo */
    }
    printf("Total: %d\n", total);
    return 0;
}''',
        "Mostrar o índice e o valor em cada volta ajuda a localizar onde um cálculo sai errado.",
    ),
    "gcc": (
        r'''#include <stdio.h>

int main(void) {
    printf("GCC OK\n");
    return 0;
}''',
        "Um programa simples, sem variáveis sobrando, compila sem avisos com -Wall -Wextra.",
    ),
    "linking": (
        r'''#include <stdio.h>

int resposta(void);                 /* declaração: o ligador procura a definição */

int main(void) {
    printf("%d\n", resposta());
    return 0;
}

int resposta(void) {                /* definição */
    return 42;
}''',
        "A declaração permite compilar main; a definição é quem o ligador conecta à chamada.",
    ),
    "makefile": (
        r'''#include <stdio.h>

#define CC "gcc"
#define CFLAGS "-std=c11 -Wall"

int main(void) {
    printf("%s %s main.c\n", CC, CFLAGS);
    return 0;
}''',
        "Em um Makefile, CC guarda o compilador e CFLAGS as opções; aqui elas montam o comando de build.",
    ),
    "buffer overflow": (
        r'''#include <stdio.h>

int main(void) {
    char nome[10];
    if (scanf("%9s", nome) == 1) {  /* no máximo 9 letras + o '\0' */
        printf("%s\n", nome);
    }
    return 0;
}''',
        "A largura %9s impede que o scanf escreva além das 10 posições do vetor.",
    ),
    "validação": (
        r'''#include <stdio.h>

int main(void) {
    int idade;
    if (scanf("%d", &idade) == 1 && idade >= 0 && idade <= 120) {
        printf("Idade valida\n");
    } else {
        printf("Entrada invalida\n");
    }
    return 0;
}''',
        "Primeiro confere se um número foi lido e depois se ele está na faixa aceita.",
    ),
    "listas": (
        r'''#include <stdio.h>
#include <stdlib.h>

struct No {
    int valor;
    struct No *proximo;
};

int main(void) {
    int dados[3] = {10, 20, 12};
    struct No *inicio = NULL;

    for (int i = 2; i >= 0; i--) {  /* insere no começo, do último para o primeiro */
        struct No *novo = malloc(sizeof(struct No));
        if (novo == NULL) {
            return 1;
        }
        novo->valor = dados[i];
        novo->proximo = inicio;
        inicio = novo;
    }

    int soma = 0;
    struct No *atual = inicio;
    while (atual != NULL) {
        soma += atual->valor;
        atual = atual->proximo;
    }
    printf("%d\n", soma);

    while (inicio != NULL) {        /* libera nó por nó */
        struct No *seguinte = inicio->proximo;
        free(inicio);
        inicio = seguinte;
    }
    return 0;
}''',
        "Cada nó aponta para o próximo; a lista é percorrida até NULL e os nós são liberados um a um.",
    ),
    "pilhas": (
        r'''#include <stdio.h>

int pilha[10];
int topo = 0;

void push(int valor) {
    if (topo < 10) {
        pilha[topo++] = valor;
    }
}

int pop(void) {
    return pilha[--topo];           /* o último que entrou é o primeiro que sai */
}

int main(void) {
    push(10);
    push(42);
    printf("%d\n", pop());
    return 0;
}''',
        "A pilha retira sempre o último elemento colocado (LIFO); por isso o primeiro pop devolve 42.",
    ),
    "filas": (
        r'''#include <stdio.h>

int fila[10];
int inicio = 0;
int fim = 0;

void enfileirar(int valor) {
    if (fim < 10) {
        fila[fim++] = valor;
    }
}

int desenfileirar(void) {
    return fila[inicio++];          /* o primeiro que entrou é o primeiro que sai */
}

int main(void) {
    enfileirar(42);
    enfileirar(10);
    printf("%d\n", desenfileirar());
    return 0;
}''',
        "A fila atende na ordem de chegada (FIFO); o primeiro removido é o 42.",
    ),
    "árvores": (
        r'''#include <stdio.h>

struct No {
    int valor;
    struct No *esquerda;
    struct No *direita;
};

void emOrdem(const struct No *no) {
    if (no == NULL) {
        return;
    }
    emOrdem(no->esquerda);          /* primeiro os menores */
    printf("%d ", no->valor);
    emOrdem(no->direita);           /* depois os maiores */
}

int main(void) {
    struct No menor = {10, NULL, NULL};
    struct No maior = {42, NULL, NULL};
    struct No raiz = {20, &menor, &maior};
    emOrdem(&raiz);
    printf("\n");
    return 0;
}''',
        "O percurso em ordem visita esquerda, raiz e direita, mostrando os valores em ordem crescente.",
    ),
    "busca linear": (
        r'''#include <stdio.h>

int main(void) {
    int valores[4] = {5, 12, 42, 9};
    int alvo = 42;
    int posicao = -1;
    for (int i = 0; i < 4; i++) {
        if (valores[i] == alvo) {
            posicao = i;
            break;                  /* achou: não precisa continuar */
        }
    }
    printf("Posicao: %d\n", posicao);
    return 0;
}''',
        "A busca linear confere um elemento de cada vez e para no primeiro que for igual ao alvo.",
    ),
    "bubble sort": (
        r'''#include <stdio.h>

int main(void) {
    int v[4] = {42, 7, 19, 3};
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3 - i; j++) {
            if (v[j] > v[j + 1]) {  /* vizinhos fora de ordem trocam de lugar */
                int troca = v[j];
                v[j] = v[j + 1];
                v[j + 1] = troca;
            }
        }
    }
    for (int i = 0; i < 4; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}''',
        "A cada passada o maior valor restante vai para o fim; após três passadas o vetor está ordenado.",
    ),
    "eficiência": (
        r'''#include <stdio.h>

int main(void) {
    int valores[5] = {2, 5, 8, 11, 42};
    int contador = 0;
    for (int i = 0; i < 5; i++) {   /* uma única passada pelo vetor */
        if (valores[i] % 2 == 0) {
            contador++;
        }
    }
    printf("%d\n", contador);
    return 0;
}''',
        "Um único laço resolve o problema visitando cada elemento uma vez só.",
    ),
    "calculadora": (
        r'''#include <stdio.h>

int main(void) {
    double a;
    double b;
    char operador;
    if (scanf("%lf %c %lf", &a, &operador, &b) != 3) {
        printf("Entrada invalida\n");
        return 0;
    }
    switch (operador) {
        case '+':
            printf("Resultado: %.2f\n", a + b);
            break;
        case '-':
            printf("Resultado: %.2f\n", a - b);
            break;
        case '*':
            printf("Resultado: %.2f\n", a * b);
            break;
        case '/':
            if (b == 0.0) {
                printf("Divisao por zero\n");
            } else {
                printf("Resultado: %.2f\n", a / b);
            }
            break;
        default:
            printf("Operador invalido\n");
    }
    return 0;
}''',
        "O scanf lê número, operador e número; o switch escolhe a conta e a divisão por zero é tratada.",
    ),
    "cadastro": (
        r'''#include <stdio.h>

struct Pessoa {
    char nome[30];
    int idade;
};

int main(void) {
    struct Pessoa pessoa;
    if (scanf("%29s", pessoa.nome) != 1 || scanf("%d", &pessoa.idade) != 1) {
        printf("Entrada invalida\n");
        return 0;
    }
    printf("%s tem %d anos\n", pessoa.nome, pessoa.idade);
    return 0;
}''',
        "Os dados lidos vão direto para os campos da struct; %29s protege o vetor de 30 posições.",
    ),
    "agenda": (
        r'''#include <stdio.h>
#include <string.h>

struct Contato {
    char nome[30];
    char telefone[20];
};

int main(void) {
    struct Contato agenda[2] = {
        {"Bia", "1234-5678"},
        {"Ana", "4242-4242"},
    };
    for (int i = 0; i < 2; i++) {
        if (strcmp(agenda[i].nome, "Ana") == 0) {
            printf("%s\n", agenda[i].telefone);
        }
    }
    return 0;
}''',
        "Um vetor de structs guarda os contatos; strcmp encontra o nome procurado.",
    ),
    "jogo terminal": (
        r'''#include <stdio.h>

int main(void) {
    int alvo = 42;
    int tentativa;
    printf("Adivinhe o numero: ");
    while (scanf("%d", &tentativa) == 1) {   /* para se a entrada acabar */
        if (tentativa == alvo) {
            printf("Acertou\n");
            break;
        }
        printf(tentativa < alvo ? "Maior. Tente de novo: " : "Menor. Tente de novo: ");
    }
    return 0;
}''',
        "O laço lê palpites até acertar; conferir o retorno do scanf evita repetir para sempre se a entrada acabar.",
    ),
    "sistema biblioteca": (
        r'''#include <stdio.h>

struct Livro {
    char titulo[30];
    int disponivel;
};

int emprestar(struct Livro *livro) {
    if (livro->disponivel) {
        livro->disponivel = 0;      /* marca como emprestado */
        return 1;
    }
    return 0;
}

int main(void) {
    struct Livro livro = {"C na pratica", 1};
    for (int pedido = 0; pedido < 2; pedido++) {
        printf(emprestar(&livro) ? "Emprestado\n" : "Indisponivel\n");
    }
    return 0;
}''',
        "A função recebe o endereço do livro para alterar o campo disponivel; o segundo pedido é recusado.",
    ),
    "editor texto": (
        r'''#include <stdio.h>
#include <string.h>

int main(void) {
    char texto[50] = "Aprender ";
    const char acrescimo[] = "C";
    if (strlen(texto) + strlen(acrescimo) + 1 <= sizeof(texto)) {   /* cabe com o '\0'? */
        strcat(texto, acrescimo);
    }
    printf("%s\n", texto);
    return 0;
}''',
        "Antes do strcat, a conta confere se o texto final e o '\\0' cabem no vetor.",
    ),
    "projeto final": (
        r'''#include <stdio.h>

double calcularMedia(double a, double b, double c) {
    return (a + b + c) / 3.0;
}

int main(void) {
    double nota1;
    double nota2;
    double nota3;
    if (scanf("%lf %lf %lf", &nota1, &nota2, &nota3) == 3) {
        printf("Media: %.2f\n", calcularMedia(nota1, nota2, nota3));
    } else {
        printf("Entrada invalida\n");
    }
    return 0;
}''',
        "O programa valida a leitura das três notas e delega o cálculo a uma função reutilizável.",
    ),
}
