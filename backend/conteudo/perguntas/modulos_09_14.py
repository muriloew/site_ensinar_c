"""Perguntas dos módulos 9 a 14: memória, ponteiros, alocação, structs, arquivos e bibliotecas."""

from backend.conteudo.perguntas.base import conceito, erro, lacuna, saida

PERGUNTAS = {
    # ------------------------------------------------------------------ Módulo 9
    "memória": [
        saida(
            r'''printf("%zu\n", sizeof(char));''',
            "1",
            ["0", "8", "2"],
            "Por definição, sizeof(char) é sempre 1. Os outros tipos são medidos em múltiplos de char.",
        ),
        saida(
            r'''
            int v[10];
            printf("%zu\n", sizeof(v) / sizeof(v[0]));
            ''',
            "10",
            ["40", "4", "1"],
            "sizeof(v) é o tamanho do vetor inteiro em bytes, e sizeof(v[0]) o de um elemento. A divisão dá a "
            "quantidade de elementos, em qualquer computador.",
        ),
        conceito(
            "Em `int x = 5;`, o que o tipo int informa ao compilador?",
            "Quantos bytes reservar para x e como interpretar esses bits.",
            [
                "Em qual endereço da memória x deve ficar enquanto o programa estiver rodando.",
                "Por quanto tempo o programa vai rodar.",
                "Que x só pode guardar números positivos.",
            ],
            "O tipo define o tamanho e a interpretação. O endereço é escolhido pelo compilador e pelo sistema.",
        ),
        conceito(
            "Por que escrever sizeof(int) em vez de simplesmente 4?",
            "Porque o tamanho de int pode mudar entre computadores e compiladores.",
            [
                "Porque sizeof é calculado mais rápido que o número 4 durante a execução do programa.",
                "Porque o número 4 não pode ser usado em contas com memória.",
                "Porque sizeof(int) vale sempre 8 nos computadores modernos.",
            ],
            "Usar sizeof deixa o programa portátil: o valor certo é calculado pelo compilador de cada máquina.",
        ),
    ],
    "operador &": [
        saida(
            r'''
            int x = 10;
            int *p = &x;
            *p = 25;
            printf("%d\n", x);
            ''',
            "25",
            ["10", "35", "0"],
            "p guarda o endereço de x, então *p = 25 escreve diretamente em x.",
        ),
        conceito(
            "Qual especificador do printf mostra um endereço de memória?",
            "%p",
            ["%d", "%a", "%e"],
            "Endereços não são int. O formato certo é printf(\"%p\", (void *) &x).",
        ),
        erro(
            r'''
            #include <stdio.h>

            int *criar(void) {
                int valor = 42;
                return &valor;
            }

            int main(void) {
                int *p = criar();
                printf("%d\n", *p);
                return 0;
            }
            ''',
            "valor deixa de existir quando criar termina; p aponta para uma memória que não vale mais.",
            [
                "Funções não podem devolver ponteiros.",
                "Falta um * antes de criar() em main.",
                "valor deveria ser declarado como double.",
            ],
            "Variáveis locais acabam quando a função termina. Devolver o endereço delas cria um ponteiro pendente.",
        ),
        conceito(
            "Depois de `int x; int *p = &x;`, o que p guarda?",
            "O endereço de x.",
            ["Uma cópia do valor de x.", "O tamanho de x em bytes.", "O nome x, como texto."],
            "& obtém o endereço. Para chegar ao valor guardado nesse endereço, usa-se *p.",
        ),
    ],
    "ponteiros + funções": [
        saida(
            r'''
            #include <stdio.h>

            void dobrar(int *x) {
                *x = *x * 2;
            }

            int main(void) {
                int n = 5;
                dobrar(&n);
                printf("%d\n", n);
                return 0;
            }
            ''',
            "10",
            ["5", "25", "0"],
            "A função recebeu o endereço de n. Assim, *x = ... altera o próprio n, e não uma cópia.",
        ),
        saida(
            r'''
            #include <stdio.h>

            void trocar(int a, int b) {
                int t = a;
                a = b;
                b = t;
            }

            int main(void) {
                int x = 1, y = 2;
                trocar(x, y);
                printf("%d %d\n", x, y);
                return 0;
            }
            ''',
            "1 2",
            ["2 1", "2 2", "1 1"],
            "a e b são cópias, então a troca acontece só dentro da função. Para trocar x e y, a função deve "
            "receber int *.",
        ),
        erro(
            r'''
            #include <stdio.h>

            void zerar(int *p) {
                *p = 0;
            }

            int main(void) {
                int *p = NULL;
                zerar(p);
                printf("Zerado\n");
                return 0;
            }
            ''',
            "p é NULL, e zerar escreve em *p sem verificar: isso é um acesso inválido.",
            [
                "zerar deveria receber int em vez de int *.",
                "printf não pode vir depois da chamada de uma função void.",
                "Nada: NULL vale 0, então *p = 0 não muda nada.",
            ],
            "Desreferenciar NULL derruba o programa. Uma função que recebe ponteiro deve testar if (p != NULL).",
        ),
        lacuna(
            r'''
            #include <stdio.h>

            void incrementar(int *p) {
                ____;
            }

            int main(void) {
                int n = 41;
                incrementar(&n);
                printf("%d\n", n);
                return 0;
            }
            ''',
            "(*p)++",
            ["*p++", "p++", "p = p + 1"],
            "42",
            "(*p)++ aumenta o valor apontado. Sem parênteses, *p++ avança o ponteiro, e p++ também só muda o "
            "endereço.",
        ),
    ],
    "ponteiros + arrays": [
        saida(
            r'''
            int v[] = {10, 20, 30};
            int *p = v;
            printf("%d %d\n", *(p + 1), *p + 1);
            ''',
            "20 11",
            ["11 20", "20 20", "11 11"],
            "*(p + 1) é o elemento seguinte (v[1]). *p + 1 pega v[0] e soma 1.",
        ),
        conceito(
            "Em `int v[5]; int *p = v;`, o que é p + 2?",
            "O endereço de v[2].",
            [
                "O endereço 2 bytes depois de v[0].",
                "O valor de v[0] mais 2.",
                "O valor guardado em v[2].",
            ],
            "Somar 2 a um ponteiro avança dois elementos do tipo apontado. *(p + 2) seria o valor de v[2].",
        ),
        saida(
            r'''
            int v[] = {5, 10, 15, 20};
            int *p = v + 3;
            printf("%d %d\n", *p, p[-1]);
            ''',
            "20 15",
            ["15 10", "20 19", "15 20"],
            "p aponta para v[3] (20), e p[-1] é o elemento anterior, v[2] (15).",
        ),
        erro(
            r'''
            int v[3] = {1, 2, 3};
            int soma = 0;
            for (int *p = v; p <= v + 3; p++) {
                soma = soma + *p;
            }
            printf("%d\n", soma);
            ''',
            "Com p <= v + 3, o laço lê *p quando p já aponta para depois do último elemento.",
            [
                "Ponteiros não podem ser usados como variável de controle de um for.",
                "v + 3 não compila, porque v é um vetor.",
                "soma também deveria ser um ponteiro.",
            ],
            "v + 3 é a posição logo depois do fim. Ela pode ser usada em comparações, mas não pode ser lida. A "
            "condição certa é p < v + 3.",
        ),
    ],
    "ponteiro para ponteiro": [
        saida(
            r'''
            int a = 1, b = 2;
            int *p = &a;
            int **pp = &p;
            *pp = &b;
            *p = 9;
            printf("%d %d\n", a, b);
            ''',
            "1 9",
            ["9 2", "9 9", "1 2"],
            "*pp = &b muda o próprio p, que passa a apontar para b. Por isso *p = 9 altera b.",
        ),
        conceito(
            "Se pp foi declarado como `int **pp`, qual é o tipo de *pp?",
            "int *",
            ["int", "int **", "void"],
            "Cada * remove um nível: **pp é um int, e *pp é o ponteiro intermediário.",
        ),
        saida(
            r'''
            #include <stdio.h>

            int primeiro = 1;
            int segundo = 2;

            void apontar_para_segundo(int **pp) {
                *pp = &segundo;
            }

            int main(void) {
                int *p = &primeiro;
                apontar_para_segundo(&p);
                printf("%d\n", *p);
                return 0;
            }
            ''',
            "2",
            ["1", "0", "3"],
            "A função recebeu o endereço de p e mudou para onde ele aponta. Esse é o uso típico de int **.",
        ),
        conceito(
            "Para que uma função mude para onde aponta o ponteiro `int *p` de main, o que ela deve receber?",
            "Um int **, que é o endereço do ponteiro.",
            [
                "Um int *, que é o próprio ponteiro que está em main.",
                "Um int, que é o valor apontado.",
                "Nada, pois ponteiros são globais.",
            ],
            "Assim como int * permite alterar um int, int ** permite alterar um int *.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 10
    "malloc": [
        conceito(
            "O que malloc devolve quando não consegue reservar a memória pedida?",
            "NULL",
            [
                "Um ponteiro para uma área menor que a pedida.",
                "Um bloco com todos os bytes zerados.",
                "Nada: o programa é encerrado com uma mensagem.",
            ],
            "Por isso o retorno sempre deve ser testado antes do uso: if (v == NULL) { ... }.",
        ),
        conceito(
            "Qual chamada reserva espaço para 5 int?",
            "`malloc(5 * sizeof(int))`",
            ["`malloc(5)`", "`malloc(sizeof(5))`", "`malloc(sizeof(int) + sizeof(5))`"],
            "malloc recebe bytes. malloc(5) reservaria só 5 bytes, o que não basta para 5 int.",
        ),
        erro(
            r'''
            int *v = malloc(3 * sizeof(int));
            if (v == NULL) {
                return 1;
            }
            printf("%d\n", v[0] + v[1] + v[2]);
            free(v);
            ''',
            "Os valores de v são lidos sem terem sido inicializados: malloc não zera a memória.",
            [
                "Falta converter o retorno de malloc com (int *).",
                "v[0] não existe, porque a memória alocada começa em v[1].",
                "free(v) deveria vir antes do printf.",
            ],
            "malloc entrega memória com conteúdo indefinido. Grave valores antes de ler, ou use calloc. Em C, a "
            "conversão de void * é automática.",
            inclui=("stdlib.h",),
        ),
        saida(
            r'''
            int *p = malloc(sizeof(int));
            if (p == NULL) {
                return 1;
            }
            *p = 7;
            int *q = p;
            *q = *q + 1;
            printf("%d\n", *p);
            free(p);
            ''',
            "8",
            ["7", "1", "14"],
            "q = p copia o endereço, e não o bloco. Os dois apontam para o mesmo int.",
            inclui=("stdlib.h",),
        ),
    ],
    "calloc": [
        saida(
            r'''
            int *v = calloc(4, sizeof(int));
            if (v == NULL) {
                return 1;
            }
            v[1] = 5;
            printf("%d %d %d %d\n", v[0], v[1], v[2], v[3]);
            free(v);
            ''',
            "0 5 0 0",
            ["5 5 5 5", "5 0 0 0", "1 5 1 1"],
            "calloc zera todos os bytes, então só a posição 1 tem um valor diferente de 0.",
            inclui=("stdlib.h",),
        ),
        conceito(
            "Qual a diferença entre `malloc(4 * sizeof(int))` e `calloc(4, sizeof(int))`?",
            "calloc zera todos os bytes; malloc deixa o conteúdo indefinido.",
            [
                "malloc zera os bytes; calloc não.",
                "calloc não precisa de free.",
                "calloc reserva quatro vezes mais memória que malloc para o mesmo pedido.",
            ],
            "As duas reservam o mesmo espaço. calloc também recebe quantidade e tamanho separados e confere a "
            "multiplicação.",
        ),
        conceito(
            "calloc já zera a memória. Ainda é preciso verificar se o retorno é NULL?",
            "Sim: calloc também pode falhar e devolver NULL.",
            [
                "Não: calloc nunca falha.",
                "Não: quando falha, calloc devolve memória zerada mesmo assim.",
                "Só quando a quantidade pedida passa de 1000.",
            ],
            "Toda alocação pode falhar. Zerar a memória não muda isso.",
        ),
        saida(
            r'''
            char *texto = calloc(10, sizeof(char));
            if (texto == NULL) {
                return 1;
            }
            printf("[%s] %zu\n", texto, strlen(texto));
            free(texto);
            ''',
            "[] 0",
            ["[] 10", "[0000000000] 10", "[ ] 1"],
            "Com todos os bytes em 0, o primeiro caractere já é '\\0': a string está vazia.",
            inclui=("stdlib.h", "string.h"),
        ),
    ],
    "realloc": [
        conceito(
            "Por que escrever `int *tmp = realloc(v, novo);` em vez de `v = realloc(v, novo);`?",
            "Se realloc falhar e devolver NULL, v ainda guarda o bloco original.",
            [
                "Porque realloc não pode receber e devolver a mesma variável.",
                "Porque usando tmp a cópia dos dados para o novo bloco fica mais rápida.",
                "Porque realloc libera v toda vez que é chamada.",
            ],
            "Com v = realloc(...), uma falha sobrescreve v com NULL e o bloco antigo fica sem dono (vazamento).",
        ),
        saida(
            r'''
            int *v = malloc(2 * sizeof(int));
            if (v == NULL) {
                return 1;
            }
            v[0] = 10;
            v[1] = 20;
            int *tmp = realloc(v, 3 * sizeof(int));
            if (tmp == NULL) {
                free(v);
                return 1;
            }
            v = tmp;
            v[2] = 12;
            printf("%d %d %d\n", v[0], v[1], v[2]);
            free(v);
            ''',
            "10 20 12",
            ["0 0 12", "10 20 0", "12 10 20"],
            "realloc preserva o conteúdo antigo, mesmo quando move o bloco. A posição nova recebeu 12.",
            inclui=("stdlib.h",),
        ),
        conceito(
            "Depois de um realloc que aumentou o bloco, o que se sabe sobre as posições novas?",
            "Não foram inicializadas: precisam de valores antes de ser lidas.",
            [
                "Elas começam com 0.",
                "Elas repetem o último valor que estava no bloco antigo, até serem alteradas.",
                "Elas ficam inacessíveis até o próximo realloc.",
            ],
            "Como no malloc, o espaço acrescentado tem conteúdo indefinido.",
        ),
        conceito(
            "Depois de `tmp = realloc(v, maior)` dar certo, o endereço em tmp é igual ao de v?",
            "Não necessariamente: realloc pode mover o bloco inteiro para outro lugar da memória.",
            [
                "Sim, realloc nunca move o bloco.",
                "Sim, sempre que o tamanho aumenta.",
                "Não: o endereço muda sempre, e por isso os valores antigos se perdem.",
            ],
            "Se não houver espaço logo depois do bloco, realloc copia os dados para outro lugar e libera o antigo. "
            "Por isso use sempre o ponteiro devolvido.",
        ),
    ],
    "free": [
        erro(
            r'''
            int *p = malloc(sizeof(int));
            if (p == NULL) {
                return 1;
            }
            *p = 42;
            free(p);
            printf("%d\n", *p);
            ''',
            "p é usado depois do free: o bloco já foi devolvido e não pode mais ser lido.",
            [
                "Nada: free zera *p, então o printf mostra 0 com segurança.",
                "O certo seria free(&p).",
                "malloc deveria receber o valor 42 como argumento.",
            ],
            "Depois do free, o ponteiro ainda guarda o endereço antigo, mas usá-lo é comportamento indefinido.",
            inclui=("stdlib.h",),
        ),
        conceito(
            "Qual destes usos de free é permitido?",
            "`free(NULL);`",
            [
                "Chamar free duas vezes no mesmo ponteiro.",
                "Chamar free em um vetor declarado como `int v[10];`.",
                "Chamar free no endereço de uma variável local.",
            ],
            "free(NULL) não faz nada e é seguro. free só pode receber o que veio de malloc, calloc ou realloc, e "
            "uma única vez.",
        ),
        conceito(
            "Por que atribuir NULL ao ponteiro logo depois do free?",
            "Para um uso acidental posterior ser fácil de detectar com um teste de NULL.",
            [
                "Porque free só libera a memória depois dessa atribuição.",
                "Para devolver a memória ao sistema mais rápido.",
                "Porque sem isso o programa não compila.",
            ],
            "Um ponteiro NULL é fácil de testar, e free(NULL) é inofensivo. Já o endereço antigo parece válido e "
            "engana.",
        ),
        erro(
            r'''
            int *a = malloc(sizeof(int));
            int *b = a;
            free(a);
            free(b);
            ''',
            "a e b apontam para o mesmo bloco, que acaba sendo liberado duas vezes.",
            [
                "b nunca foi alocado com malloc, então free(b) não faz nada.",
                "free precisa receber também o tamanho do bloco.",
                "Faltou comparar a e b com strcmp antes de liberar.",
            ],
            "Copiar um ponteiro não copia o bloco. Cada bloco deve ter um dono que o libera uma única vez.",
            inclui=("stdlib.h",),
        ),
    ],
    "memory leak": [
        erro(
            r'''
            int *p = malloc(10 * sizeof(int));
            p = malloc(20 * sizeof(int));
            free(p);
            ''',
            "O primeiro bloco fica sem nenhum ponteiro e nunca é liberado.",
            [
                "O segundo malloc apenas aumenta o primeiro bloco para 20 int.",
                "free(p) libera os dois blocos de uma vez.",
                "Não se pode chamar malloc duas vezes com o mesmo ponteiro.",
            ],
            "Ao sobrescrever p, o endereço do primeiro bloco se perde. Libere antes de reaproveitar o ponteiro.",
            inclui=("stdlib.h",),
        ),
        conceito(
            "Em qual destes programas um vazamento de memória causa mais problemas?",
            "Um servidor que fica dias rodando e vaza um pouco a cada pedido.",
            [
                "Um programa que roda por um segundo e termina.",
                "Um programa que nunca usa malloc.",
                "Um programa que aloca bastante, mas libera todos os blocos antes de terminar.",
            ],
            "Pequenos vazamentos se somam. Em processos longos, a memória acaba e o programa falha.",
        ),
        erro(
            r'''
            #include <stdio.h>
            #include <stdlib.h>

            int processar(int n) {
                int *dados = malloc(n * sizeof(int));
                if (dados == NULL) {
                    return -1;
                }
                if (n > 100) {
                    return -1;
                }
                free(dados);
                return 0;
            }

            int main(void) {
                printf("%d\n", processar(200));
                return 0;
            }
            ''',
            "Quando n passa de 100, a função retorna sem liberar dados.",
            [
                "Quando malloc falha, falta chamar free(dados).",
                "free precisa ser chamado antes do malloc.",
                "A função vaza memória em todos os casos.",
            ],
            "Todo caminho que sai da função depois da alocação precisa liberar o bloco. Se malloc falhou, não há "
            "nada a liberar.",
        ),
        conceito(
            "O que mais ajuda a evitar vazamentos de memória?",
            "Definir quem é dono de cada bloco e responsável pelo free.",
            [
                "Usar sempre calloc em vez de malloc.",
                "Alocar um único bloco grande no início do programa e nunca liberar.",
                "Atribuir NULL ao ponteiro em vez de chamar free.",
            ],
            "Quando cada alocação tem um dono claro, fica fácil conferir que todo malloc tem um free.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 11
    "structs": [
        saida(
            r'''
            #include <stdio.h>

            struct Ponto {
                int x;
                int y;
            };

            int main(void) {
                struct Ponto a = {1, 2};
                struct Ponto b = a;
                b.x = 10;
                printf("%d %d\n", a.x, b.x);
                return 0;
            }
            ''',
            "1 10",
            ["10 10", "1 1", "10 1"],
            "Atribuir uma struct copia todos os campos. Depois disso, a e b são independentes.",
        ),
        conceito(
            "Se `struct Produto *p` aponta para um produto, como se lê o campo preco?",
            "`p->preco`",
            ["`p.preco`", "`*p.preco`", "`p[preco]`"],
            "-> acessa um campo por meio de um ponteiro, e equivale a (*p).preco. *p.preco seria lido como "
            "*(p.preco).",
        ),
        saida(
            r'''
            #include <stdio.h>

            struct Aluno {
                char nome[20];
                double nota;
            };

            int main(void) {
                struct Aluno turma[2] = {{"Ana", 8.5}, {"Bia", 9.0}};
                printf("%s %.1f\n", turma[1].nome, turma[0].nota);
                return 0;
            }
            ''',
            "Bia 8.5",
            ["Ana 9.0", "Bia 9.0", "Ana 8.5"],
            "turma[1] é o segundo aluno (Bia), e turma[0].nota é a nota da primeira (8.5).",
        ),
        saida(
            r'''
            #include <stdio.h>

            struct Lista {
                int *dados;
            };

            int main(void) {
                int numeros[2] = {1, 2};
                struct Lista a = {numeros};
                struct Lista b = a;
                b.dados[0] = 99;
                printf("%d\n", a.dados[0]);
                return 0;
            }
            ''',
            "99",
            ["1", "2", "0"],
            "A cópia levou o ponteiro, mas não os dados apontados. a.dados e b.dados apontam para o mesmo vetor.",
        ),
    ],
    "typedef": [
        conceito(
            "O que `typedef struct { int x; int y; } Ponto;` permite fazer?",
            "Declarar variáveis como `Ponto p;`, sem escrever struct.",
            [
                "Somar dois pontos diretamente, como em p1 + p2, sem escrever função.",
                "Declarar Ponto como uma variável global.",
                "Impedir que os campos x e y sejam alterados.",
            ],
            "typedef só dá um apelido ao tipo. Ele não cria operações novas.",
        ),
        saida(
            r'''
            #include <stdio.h>

            typedef int Pontos;

            int main(void) {
                Pontos a = 7;
                int b = a + 3;
                printf("%d\n", b);
                return 0;
            }
            ''',
            "10",
            ["7", "3", "73"],
            "Pontos é só outro nome para int, então a + 3 é uma soma de int comum.",
        ),
        erro(
            r'''
            #include <stdio.h>

            struct Ponto {
                int x;
                int y;
            };

            int main(void) {
                Ponto p = {1, 2};
                printf("%d\n", p.x + p.y);
                return 0;
            }
            ''',
            "Sem typedef, o tipo se chama struct Ponto; Ponto sozinho não existe.",
            [
                "Faltou indicar o nome dos campos na inicialização.",
                "printf não aceita campos de struct.",
                "Os campos x e y deveriam ser double.",
            ],
            "Escreva struct Ponto p = {1, 2}; ou crie o apelido com typedef struct Ponto Ponto;.",
            compila=False,
        ),
        conceito(
            "Por que esconder um ponteiro em um typedef, como `typedef int *Lista;`, pode atrapalhar?",
            "Esconde que a variável é um ponteiro e quem deve liberá-la.",
            [
                "Porque typedef não aceita ponteiros.",
                "Porque o programa fica mais lento a cada acesso feito por meio do apelido.",
                "Porque Lista passa a ocupar o dobro de memória.",
            ],
            "Quem lê Lista l; não vê o *. Isso esconde cuidados como testar NULL e chamar free.",
        ),
    ],
    "unions": [
        conceito(
            "Qual a principal diferença entre struct e union?",
            "Na union, todos os membros dividem a mesma memória.",
            [
                "A union só aceita membros do tipo int.",
                "A struct não pode ter campos de tipos diferentes.",
                "A union guarda o valor de todos os membros ao mesmo tempo.",
            ],
            "Por dividir a memória, a union guarda um membro de cada vez.",
        ),
        conceito(
            "Uma union tem um int (4 bytes) e um double (8 bytes). Qual o tamanho mínimo dela?",
            "8 bytes, o tamanho do maior membro.",
            [
                "12 bytes, a soma dos dois.",
                "4 bytes, o tamanho do menor.",
                "16 bytes, o dobro do maior membro, para caber os dois.",
            ],
            "Os membros ocupam o mesmo lugar, então a union precisa caber o maior deles.",
        ),
        conceito(
            "Depois de `n.real = 2.5;` e, em seguida, `n.inteiro = 42;` em uma union, qual membro é válido ler?",
            "Só n.inteiro, que foi escrito por último.",
            [
                "Só n.real, que foi escrito primeiro.",
                "Os dois: n.real continua 2.5 e n.inteiro vale 42.",
                "Nenhum, porque unions não podem ser lidas.",
            ],
            "Gravar n.inteiro sobrescreveu os bytes que guardavam n.real. Só o último membro escrito está ativo.",
        ),
        saida(
            r'''
            #include <stdio.h>

            enum Tipo { INTEIRO, REAL };

            struct Valor {
                enum Tipo tipo;
                union {
                    int i;
                    double d;
                } dado;
            };

            int main(void) {
                struct Valor v;
                v.tipo = REAL;
                v.dado.d = 2.5;
                if (v.tipo == INTEIRO) {
                    printf("%d\n", v.dado.i);
                } else {
                    printf("%.1f\n", v.dado.d);
                }
                return 0;
            }
            ''',
            "2.5",
            ["2", "0", "2.500000"],
            "A enum tipo registra qual membro da union foi gravado. Assim o programa lê o membro certo, d, com %.1f.",
        ),
    ],
    "enum": [
        saida(
            r'''
            #include <stdio.h>

            enum Cor { VERMELHO, VERDE, AZUL };

            int main(void) {
                printf("%d %d\n", VERDE, AZUL);
                return 0;
            }
            ''',
            "1 2",
            ["2 3", "0 1", "1 3"],
            "Sem valores explícitos, a enum começa em 0: VERMELHO = 0, VERDE = 1 e AZUL = 2.",
        ),
        saida(
            r'''
            #include <stdio.h>

            enum Nivel { BAIXO = 1, MEDIO, ALTO = 10, MAXIMO };

            int main(void) {
                printf("%d %d\n", MEDIO, MAXIMO);
                return 0;
            }
            ''',
            "2 11",
            ["1 10", "2 3", "3 11"],
            "Cada nome sem valor é o anterior mais 1: MEDIO vem depois de BAIXO (1) e MAXIMO depois de ALTO (10).",
        ),
        conceito(
            "Uma variável `enum Status s;` pode receber o valor 7?",
            "Pode: o compilador aceita o 7, então o próprio programa precisa validar o valor.",
            [
                "Não: o compilador recusa qualquer valor que não esteja na lista da enum.",
                "Não: o programa trava no momento da atribuição.",
                "Pode, e o 7 vira automaticamente o último valor da enum.",
            ],
            "Em C, uma enum é um inteiro. Nada impede valores fora da lista, por isso valide antes de usar.",
        ),
        conceito(
            "Por que usar enum em vez de números soltos, como 0, 1 e 2, para representar estados?",
            "Os nomes deixam claro o significado de cada estado ao ler o código.",
            [
                "Porque enum ocupa menos memória que int.",
                "Porque o compilador passa a impedir qualquer erro de lógica com esses estados.",
                "Porque o switch só funciona com enum.",
            ],
            "case ATIVO: se explica sozinho. Já case 1: obriga quem lê a lembrar o que o 1 significa.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 12
    "fopen": [
        conceito(
            "Qual modo de fopen apaga o conteúdo do arquivo, se ele já existir?",
            "\"w\"",
            ["\"a\"", "\"r\"", "\"r+\""],
            "\"w\" cria o arquivo ou o recria vazio. \"a\" acrescenta no fim, e \"r\" só lê.",
        ),
        conceito(
            "Um arquivo já tem texto. O que acontece ao abri-lo com \"a\" e gravar algo?",
            "O texto novo é acrescentado no fim, sem apagar o antigo.",
            [
                "O texto antigo é apagado antes de gravar.",
                "O texto novo é gravado no início, empurrando o antigo para baixo.",
                "Dá erro, porque o modo \"a\" é só para leitura.",
            ],
            "\"a\" vem de append (acrescentar). Ele é útil para registros que vão crescendo, como um log.",
        ),
        erro(
            r'''
            FILE *arq = fopen("notas.txt", "r");
            int nota;
            fscanf(arq, "%d", &nota);
            printf("%d\n", nota);
            fclose(arq);
            ''',
            "Se notas.txt não existir, fopen devolve NULL, e o fscanf usa um ponteiro inválido.",
            [
                "O modo \"r\" cria o arquivo quando ele não existe.",
                "fclose deveria vir antes do fscanf.",
                "fopen exige o caminho completo do arquivo, com a letra do disco.",
            ],
            "Sempre teste if (arq == NULL) antes de ler ou gravar. O arquivo pode não existir ou faltar permissão.",
        ),
        saida(
            r'''
            FILE *arq = fopen("arquivo_que_nao_existe.txt", "r");
            if (arq == NULL) {
                printf("Nao abriu\n");
            } else {
                printf("Abriu\n");
                fclose(arq);
            }
            ''',
            "Nao abriu",
            ["Abriu", "Abriu\nNao abriu", "NULL"],
            "Abrir para leitura um arquivo que não existe falha, e fopen devolve NULL.",
        ),
    ],
    "fclose": [
        conceito(
            "O que fclose faz além de fechar o arquivo?",
            "Grava no disco o que ainda estava no buffer e libera o arquivo.",
            [
                "Apaga o arquivo do disco.",
                "Volta para o início do arquivo, deixando-o pronto para a próxima leitura.",
                "Transforma o FILE * em NULL automaticamente.",
            ],
            "As gravações ficam guardadas na memória até o buffer encher ou o arquivo ser fechado.",
        ),
        erro(
            r'''
            FILE *arq = fopen("dados.txt", "w");
            if (arq == NULL) {
                return 1;
            }
            fclose(arq);
            fprintf(arq, "42\n");
            ''',
            "O arquivo é usado depois de fechado: aquele FILE * não pode mais ser usado.",
            [
                "fprintf só funciona com arquivos abertos no modo \"a\".",
                "O nome do arquivo deveria terminar com \\n.",
                "fclose deveria receber o nome do arquivo, e não o ponteiro.",
            ],
            "Depois de fclose, o ponteiro não vale mais. Grave tudo antes de fechar.",
        ),
        conceito(
            "Por que verificar o valor devolvido por fclose?",
            "Porque erros ao gravar o buffer, como disco cheio, aparecem nesse momento.",
            [
                "Porque fclose devolve o conteúdo do arquivo.",
                "Porque fclose devolve quantas linhas foram gravadas, para conferir se não faltou nada.",
                "Não há motivo: fclose nunca falha.",
            ],
            "fclose devolve 0 quando dá certo e EOF quando dá erro. Em gravações importantes, confira.",
        ),
        saida(
            r'''
            FILE *arq = fopen("teste_fclose.txt", "w");
            if (arq == NULL) {
                return 1;
            }
            fprintf(arq, "%d", 42);
            fclose(arq);

            arq = fopen("teste_fclose.txt", "r");
            if (arq == NULL) {
                return 1;
            }
            int n = 0;
            fscanf(arq, "%d", &n);
            fclose(arq);
            printf("%d\n", n);
            ''',
            "42",
            ["0", "4", "-1"],
            "O fclose gravou o 42 no disco. Ao reabrir para leitura, o fscanf o encontra.",
        ),
    ],
    "fprintf": [
        conceito(
            "Qual a diferença entre printf e fprintf?",
            "fprintf recebe como primeiro argumento o FILE * de destino.",
            [
                "fprintf só consegue escrever números.",
                "fprintf só escreve na tela, e printf é a versão usada para gravar arquivos.",
                "fprintf não aceita especificadores como %d.",
            ],
            "printf(...) é o mesmo que fprintf(stdout, ...). Os formatos são os mesmos.",
        ),
        saida(
            r'''fprintf(stdout, "%d-%d\n", 4, 2);''',
            "4-2",
            ["42", "4 2", "stdout 4-2"],
            "stdout é a saída padrão (a tela), então fprintf(stdout, ...) se comporta como printf.",
        ),
        saida(
            r'''
            int n = fprintf(stdout, "Ola\n");
            printf("%d\n", n);
            ''',
            "Ola\n4",
            ["Ola\n3", "Ola\n1", "4\nOla"],
            "fprintf devolve quantos caracteres escreveu. São 3 letras mais o \\n.",
        ),
        conceito(
            "Como gravar a linha `Nota: 9` no arquivo aberto em `arq`?",
            r'`fprintf(arq, "Nota: %d\n", 9);`',
            [
                r'`printf(arq, "Nota: %d\n", 9);`',
                r'`fprintf("Nota: %d\n", 9, arq);`',
                r'`fprintf("arq", "Nota: %d\n", 9);`',
            ],
            "O FILE * vem primeiro, depois o formato e os valores. printf não recebe arquivo.",
        ),
    ],
    "fscanf": [
        conceito(
            "O que `fscanf(arq, \"%d\", &n)` devolve quando já chegou ao fim do arquivo?",
            "EOF",
            ["0, e n passa a valer 0", "O último número lido, de novo", "NULL"],
            "No fim do arquivo, fscanf devolve EOF (um valor negativo). Já 0 indica que havia dados, mas no formato "
            "errado.",
        ),
        erro(
            r'''
            FILE *arq = fopen("numeros.txt", "r");
            if (arq == NULL) {
                return 1;
            }
            int n, soma = 0;
            while (!feof(arq)) {
                fscanf(arq, "%d", &n);
                soma = soma + n;
            }
            printf("%d\n", soma);
            fclose(arq);
            ''',
            "feof só fica verdadeiro depois que uma leitura falha; na última volta, o n antigo é somado de novo.",
            [
                "feof deveria ser testado depois do fclose.",
                "fscanf não lê números de arquivos, só de teclado.",
                "O laço nunca executa, porque o arquivo começa no fim.",
            ],
            "Teste o retorno da leitura: while (fscanf(arq, \"%d\", &n) == 1).",
        ),
        saida(
            r'''
            FILE *arq = fopen("numeros_teste.txt", "w");
            if (arq == NULL) {
                return 1;
            }
            fprintf(arq, "5 10 15\n");
            fclose(arq);

            arq = fopen("numeros_teste.txt", "r");
            if (arq == NULL) {
                return 1;
            }
            int n, soma = 0;
            while (fscanf(arq, "%d", &n) == 1) {
                soma = soma + n;
            }
            fclose(arq);
            printf("%d\n", soma);
            ''',
            "30",
            ["45", "15", "5"],
            "O laço para quando fscanf deixa de ler um número. Soma 5 + 10 + 15, sem repetir o último.",
        ),
        conceito(
            "Qual condição de laço é a correta para ler todos os inteiros de um arquivo?",
            "`while (fscanf(arq, \"%d\", &n) == 1)`",
            [
                "`while (!feof(arq))`",
                "`while (arq != NULL)`",
                "`while (fscanf(arq, \"%d\", &n) != 0)`",
            ],
            "== 1 confirma que um número foi lido. != 0 continuaria com EOF (-1) e entraria em laço infinito.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 13
    ".h": [
        conceito(
            "O que normalmente fica em um arquivo .h?",
            "Protótipos, tipos e constantes compartilhados.",
            [
                "A função main do programa.",
                "A implementação completa de todas as funções do projeto.",
                "Os dados digitados pelo usuário.",
            ],
            "O .h é a interface: diz o que existe. As implementações ficam nos arquivos .c.",
        ),
        conceito(
            "Qual a diferença entre `#include <stdio.h>` e `#include \"matematica.h\"`?",
            "< > procura nos cabeçalhos do sistema; aspas, primeiro na pasta do projeto.",
            [
                "Nenhuma: as duas formas são equivalentes.",
                "Com aspas, o arquivo só é incluído se alguma função dele for usada no programa.",
                "< > é para arquivos .h e as aspas são para arquivos .c.",
            ],
            "Use < > para a biblioteca padrão e aspas para os cabeçalhos do seu projeto.",
        ),
        conceito(
            "O que acontece se `int contador = 0;` ficar em util.h, incluído por dois arquivos .c?",
            "Cada .c ganha uma definição de contador, e a ligação falha por definição múltipla.",
            [
                "Os dois arquivos compartilham a mesma variável sem problemas.",
                "O compilador percebe e cria uma única cópia automaticamente.",
                "contador vale 0 em um arquivo e 1 no outro.",
            ],
            "No .h fica só a declaração (extern int contador;). A definição fica em um único .c.",
        ),
        erro(
            r'''
            #include <stdio.h>

            /* trecho que veio de util.h */
            int dobro(int n) {
                return n * 2;
            }

            /* util.h incluído de novo */
            int dobro(int n) {
                return n * 2;
            }

            int main(void) {
                printf("%d\n", dobro(21));
                return 0;
            }
            ''',
            "dobro passa a ter duas definições; o .h deveria ter só o protótipo.",
            [
                "Funções não podem ser escritas antes de main, só depois dela.",
                "Comentários com o nome de um arquivo .h não são permitidos em C.",
                "O printf não pode receber diretamente o valor devolvido por uma função.",
            ],
            "#include copia o texto do cabeçalho. Se ele tiver a implementação, cada inclusão repete a função. Por "
            "isso o .h leva só int dobro(int n); e o corpo fica no .c.",
            pergunta="Este arquivo simula um util.h com a função inteira, incluído duas vezes. Por que não compila?",
            compila=False,
        ),
    ],
    ".c": [
        saida(
            r'''
            #include <stdio.h>

            /* parte de util.h: o protótipo */
            int triplo(int n);

            /* parte de main.c */
            int main(void) {
                printf("%d\n", triplo(14));
                return 0;
            }

            /* parte de util.c: a implementação */
            int triplo(int n) {
                return n * 3;
            }
            ''',
            "42",
            ["14", "17", "0"],
            "Em um projeto real, cada parte ficaria em seu arquivo. O protótipo permite chamar triplo antes da "
            "implementação, que é ligada ao programa depois.",
            pergunta="Este arquivo simula a divisão em util.h, main.c e util.c. O que o programa mostra?",
        ),
        conceito(
            "Por que não escrever `#include \"util.c\"` em main.c quando util.c também é compilado?",
            "As funções de util.c seriam definidas duas vezes na ligação.",
            [
                "Porque #include só aceita arquivos da biblioteca padrão.",
                "Porque o compilador não consegue ler arquivos .c incluídos com #include.",
                "Porque o programa ficaria mais lento ao executar.",
            ],
            "Inclua o util.h, com os protótipos, e compile util.c separadamente.",
        ),
        conceito(
            "Qual comando compila main.c e util.c e gera o programa app?",
            "`gcc main.c util.c -o app`",
            ["`gcc main.c -o app util.h`", "`gcc util.h main.h -o app`", "`gcc main.c -o util.c`"],
            "Todos os .c entram no comando, e -o dá nome ao executável. Os .h não são compilados diretamente.",
        ),
        conceito(
            "Em um projeto grande, depois de mudar só util.c, o que precisa ser feito?",
            "Compilar de novo util.c e ligar o programa outra vez.",
            [
                "Recompilar sempre todos os arquivos .c do projeto, um por um.",
                "Recompilar só os arquivos .h.",
                "Nada: a ligação percebe a mudança sozinha.",
            ],
            "Compilar cada .c separadamente permite refazer só o que mudou. É o que o make automatiza.",
        ),
    ],
    "include guards": [
        conceito(
            "Para que servem #ifndef, #define e #endif no início de um arquivo .h?",
            "Para o conteúdo ser processado uma só vez, mesmo incluído várias vezes.",
            [
                "Para impedir que o arquivo seja usado em outro projeto.",
                "Para que as funções declaradas no cabeçalho sejam executadas uma única vez.",
                "Para esconder o código de outras pessoas.",
            ],
            "Sem a guarda, incluir o mesmo .h duas vezes repetiria tipos e declarações e causaria erros.",
        ),
        saida(
            r'''
            #include <stdio.h>

            #ifndef CONFIG_H
            #define CONFIG_H
            #define VERSAO 1
            #endif

            #ifndef CONFIG_H
            #define VERSAO 2
            #endif

            int main(void) {
                printf("%d\n", VERSAO);
                return 0;
            }
            ''',
            "1",
            ["2", "12", "0"],
            "Na segunda vez, CONFIG_H já está definido, então o #ifndef pula o bloco. É assim que a guarda "
            "evita a repetição.",
        ),
        conceito(
            "Dois cabeçalhos diferentes usam a mesma guarda, #ifndef UTIL_H. O que pode acontecer?",
            "O segundo a ser incluído é ignorado, e as declarações dele somem.",
            [
                "O compilador junta os dois arquivos automaticamente.",
                "Nada, porque a guarda vale para cada arquivo separadamente.",
                "Os dois passam a ser incluídos duas vezes, e as declarações se repetem.",
            ],
            "A guarda depende do nome da macro. Por isso cada cabeçalho precisa de um nome único.",
        ),
        conceito(
            "Qual é a ordem correta de uma guarda de inclusão?",
            "#ifndef NOME_H, #define NOME_H, conteúdo, #endif",
            [
                "#define NOME_H, #ifndef NOME_H, conteúdo, #endif",
                "#ifdef NOME_H, #define NOME_H, conteúdo, #endif",
                "#endif, conteúdo, #ifndef NOME_H, #define NOME_H",
            ],
            "Primeiro se testa se o nome ainda não existe, depois ele é definido. Definir antes de testar faria o "
            "conteúdo nunca entrar.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 14
    "stdio": [
        conceito(
            "Para que servem stdout e stderr?",
            "stdout é a saída normal; stderr, a saída para mensagens de erro.",
            [
                "stdout é para números e stderr para textos.",
                "stderr grava os erros em um arquivo de log automaticamente, sem aparecer na tela.",
                "São dois nomes para a mesma coisa.",
            ],
            "Separar os dois permite, por exemplo, mandar a saída para um arquivo e ainda ver os erros na tela.",
        ),
        conceito(
            "Qual cabeçalho declara printf, scanf, fopen e fgets?",
            "<stdio.h>",
            ["<stdlib.h>", "<string.h>", "<math.h>"],
            "stdio significa standard input/output: entrada e saída padrão, inclusive de arquivos.",
        ),
        saida(
            r'''printf("%5d|\n", 42);''',
            "   42|",
            ["42   |", "42|", "00042|"],
            "%5d reserva 5 posições e alinha o número à direita, completando com espaços.",
        ),
        saida(
            r'''printf("%-5s|\n", "C");''',
            "C    |",
            ["    C|", "C|", "-5C|"],
            "O - alinha à esquerda: o texto ocupa 5 posições e os espaços ficam depois.",
        ),
    ],
    "stdlib": [
        saida(
            r'''printf("%d %d\n", atoi("42abc"), atoi("abc"));''',
            "42 0",
            ["0 0", "42 -1", "-1 -1"],
            "atoi converte o começo numérico e devolve 0 quando não há número. O resultado 0 não diferencia "
            "\"abc\" de \"0\".",
            inclui=("stdlib.h",),
        ),
        saida(
            r'''
            char *fim;
            long n = strtol("123xyz", &fim, 10);
            printf("%ld %s\n", n, fim);
            ''',
            "123 xyz",
            ["123 123xyz", "0 xyz", "123"],
            "strtol converte o que consegue e deixa fim apontando para o primeiro caractere que não é número.",
            inclui=("stdlib.h",),
        ),
        conceito(
            "Por que strtol é melhor que atoi para converter um texto digitado?",
            "O ponteiro de fim mostra se o texto inteiro era um número válido.",
            [
                "Porque strtol também converte números decimais para double.",
                "Porque atoi não existe mais no C moderno.",
                "Porque strtol nunca falha.",
            ],
            "Se *fim não for '\\0', sobrou texto que não é número, e a entrada pode ser recusada.",
        ),
        conceito(
            "O que `return EXIT_FAILURE;` em main indica?",
            "Que o programa terminou com erro, para quem o executou.",
            [
                "Que o programa deve ser reiniciado.",
                "Que a memória do programa não foi liberada antes de ele terminar.",
                "Que o compilador encontrou um erro.",
            ],
            "O sistema e os scripts podem conferir esse código de saída. EXIT_SUCCESS indica sucesso.",
        ),
    ],
    "string": [
        saida(
            r'''
            char s[6] = "abcde";
            memset(s, '*', 3);
            printf("%s\n", s);
            ''',
            "***de",
            ["***", "abc**", "*****"],
            "memset preencheu os 3 primeiros bytes com '*'. O resto e o '\\0' continuam lá.",
            inclui=("string.h",),
        ),
        saida(
            r'''
            int a[3] = {1, 2, 3};
            int b[3] = {0, 0, 0};
            memcpy(b, a, 2 * sizeof(int));
            printf("%d %d %d\n", b[0], b[1], b[2]);
            ''',
            "1 2 0",
            ["1 2 3", "1 0 0", "2 3 0"],
            "memcpy copia bytes. Foram pedidos os bytes de 2 int, então só os dois primeiros foram copiados.",
            inclui=("string.h",),
        ),
        conceito(
            "strcpy e strcat sabem o tamanho real do vetor de destino?",
            "Não: elas confiam que quem chama reservou espaço suficiente.",
            [
                "Sim: elas leem o tamanho declarado entre colchetes.",
                "Sim, mas só quando o vetor foi declarado como global, fora das funções.",
                "Não, mas param sozinhas ao chegar a 256 caracteres.",
            ],
            "Funções de string.h recebem só um ponteiro, sem o tamanho do vetor. O cuidado com a capacidade é de "
            "quem programa.",
        ),
        lacuna(
            r'''
            char s[10] = "C";
            ____(s, "11");
            printf("%s\n", s);
            ''',
            "strcat",
            ["strcpy", "strcmp", "strlen"],
            "C11",
            "strcat acrescenta \"11\" ao \"C\". strcpy trocaria o texto por \"11\", e strcmp só compara.",
            inclui=("string.h",),
        ),
    ],
    "math": [
        saida(
            r'''printf("%.0f %.1f\n", sqrt(1764.0), pow(2.0, 0.5));''',
            "42 1.4",
            ["42 1.0", "41 1.4", "42.0 1.4"],
            "A raiz de 1764 é 42, e pow(2, 0.5) é a raiz de 2 (1.414...). %.0f mostra o número sem casas "
            "decimais.",
            inclui=("math.h",),
        ),
        conceito(
            "No Linux, ao usar math.h com o gcc, o que às vezes precisa ser acrescentado ao comando?",
            "-lm",
            ["-math", "-include libm", "-O3"],
            "As funções de math.h ficam na libm. Sem -lm, a ligação pode acusar referência indefinida a sqrt.",
        ),
        saida(
            r'''printf("%.1f %.1f\n", floor(2.7), ceil(2.1));''',
            "2.0 3.0",
            ["3.0 2.0", "2.7 2.1", "2.0 2.0"],
            "floor arredonda para baixo e ceil para cima.",
            inclui=("math.h",),
        ),
        conceito(
            "O que sqrt(-4.0) devolve?",
            "NaN, um valor inválido",
            ["-2.0, a raiz com o sinal negativo", "2.0, a raiz do valor absoluto", "0.0, porque não há resultado"],
            "Não existe raiz real de número negativo. Valide o domínio antes de chamar a função.",
        ),
    ],
}
