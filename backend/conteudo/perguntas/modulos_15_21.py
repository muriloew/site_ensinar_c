"""Perguntas dos módulos 15 a 21: bits, depuração, compilação, segurança, estruturas de dados e projetos."""

from backend.conteudo.perguntas.base import conceito, erro, lacuna, saida

FLAGS = r'''
#include <stdio.h>

#define LER (1u << 0)
#define ESCREVER (1u << 1)
#define EXECUTAR (1u << 2)
'''

PERGUNTAS = {
    # ------------------------------------------------------------------ Módulo 15
    "bitwise": [
        saida(
            r'''printf("%d %d %d\n", 6 & 3, 6 | 3, 6 ^ 3);''',
            "2 7 5",
            ["1 1 0", "2 7 9", "9 18 3"],
            "Em binário, 6 é 110 e 3 é 011. & mantém os bits comuns (010), | junta todos (111) e ^ marca os "
            "diferentes (101).",
        ),
        saida(
            r'''printf("%d %d\n", 5 << 2, 40 >> 3);''',
            "20 5",
            ["7 37", "10 20", "20 37"],
            "Deslocar n bits para a esquerda multiplica por 2^n (5 * 4), e para a direita divide (40 / 8).",
        ),
        saida(
            r'''
            int a = 2, b = 1;
            printf("%d %d\n", a & b, a && b);
            ''',
            "0 1",
            ["1 1", "0 0", "3 1"],
            "2 (10) e 1 (01) não têm bits em comum, então a & b é 0. Já a && b só pergunta se os dois são "
            "diferentes de zero.",
        ),
        conceito(
            "Em um int de 32 bits, `1 << 40` é uma operação válida?",
            "Não: deslocar por mais bits do que o tipo tem é comportamento indefinido.",
            [
                "Sim: o resultado é 0, porque o bit sai pela esquerda.",
                "Sim: o bit dá a volta e reaparece pela direita do número.",
                "Sim: o int vira long automaticamente para caber o resultado.",
            ],
            "O deslocamento precisa ser menor que a largura do tipo. Para bits altos, use um tipo maior, como "
            "unsigned long long.",
        ),
    ],
    "máscaras": [
        saida(
            FLAGS + r'''
            int main(void) {
                unsigned int permissoes = LER | EXECUTAR;
                printf("%u\n", permissoes);
                return 0;
            }
            ''',
            "5",
            ["3", "6", "1"],
            "LER é o bit 0 (1) e EXECUTAR é o bit 2 (4). O | liga os dois: 1 + 4 = 5.",
        ),
        lacuna(
            FLAGS + r'''
            int main(void) {
                unsigned int permissoes = LER | ESCREVER | EXECUTAR;
                permissoes = ____;
                printf("%u\n", permissoes);
                return 0;
            }
            ''',
            "permissoes & ~ESCREVER",
            ["permissoes & ESCREVER", "permissoes | ~ESCREVER", "~permissoes & ESCREVER"],
            "5",
            "~ESCREVER tem todos os bits ligados, menos o de ESCREVER. O & com ele desliga só essa opção.",
            pergunta="O que completa a lacuna para desligar ESCREVER e o programa mostrar `5`?",
        ),
        lacuna(
            FLAGS + r'''
            int main(void) {
                unsigned int permissoes = LER | EXECUTAR;
                if (____) {
                    printf("Pode executar\n");
                }
                return 0;
            }
            ''',
            "permissoes & EXECUTAR",
            ["permissoes == EXECUTAR", "permissoes & ESCREVER", "!(permissoes & EXECUTAR)"],
            "Pode executar",
            "permissoes & EXECUTAR é diferente de zero quando o bit está ligado. == compararia o valor inteiro "
            "(5), e não só o bit.",
        ),
        conceito(
            "Por que escrever `#define EXECUTAR (1u << 2)` em vez de usar 4 diretamente?",
            "O nome e a posição do bit deixam claro o que cada valor representa.",
            [
                "Porque o número 4 não funciona com o operador |.",
                "Porque 1u << 2 ocupa menos memória que 4.",
                "Porque o deslocamento é refeito a cada uso, o que deixa o programa mais seguro.",
            ],
            "permissoes & EXECUTAR se lê sozinho. Já permissoes & 4 obriga a lembrar o que o 4 significa.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 16
    "erros de sintaxe": [
        erro(
            r'''
            int resposta = 42
            printf("%d\n", resposta);
            ''',
            "Na linha de cima: falta o ponto e vírgula depois de 42.",
            [
                "No printf: falta o & antes de resposta.",
                "No printf: %d não funciona com int.",
                "No #include, que deveria vir depois de main.",
            ],
            "O compilador só percebe que faltou o ; ao chegar na linha seguinte. Por isso, olhe também a linha de "
            "cima da indicada.",
            pergunta="O compilador aponta o erro na linha do printf. Onde está a causa?",
            compila=False,
        ),
        erro(
            r'''
            #include <stdio.h>

            int main(void) {
                for (int i = 0; i < 3; i++) {
                    printf("%d\n", i);

                return 0;
            }
            ''',
            "Falta fechar a chave do for; o compilador só percebe no fim do arquivo.",
            [
                "return 0; não pode aparecer depois de um for.",
                "O certo seria ++i em vez de i++.",
                "printf não pode ficar dentro de um for.",
            ],
            "A chave que deveria fechar main acabou fechando o for, e main ficou sem fechamento. Recuo "
            "consistente ajuda a enxergar isso.",
            compila=False,
        ),
        conceito(
            "O que é um erro de sintaxe?",
            "Código fora das regras de escrita da linguagem, como um parêntese sem par.",
            [
                "Um programa que compila, mas mostra o resultado errado.",
                "Um erro que só aparece quando o usuário digita algo inválido.",
                "Um aviso do compilador sobre algo suspeito, que ainda deixa o programa compilar.",
            ],
            "Erros de sintaxe impedem a compilação. Programas que compilam e erram a resposta têm erros de "
            "lógica.",
        ),
        erro(
            r'''
            int total = 10;
            printf("%d\n", totl);
            ''',
            "totl não foi declarada: o nome foi digitado errado.",
            [
                "total precisa ser uma variável global.",
                "printf não aceita variáveis int.",
                "Falta o & antes de totl.",
            ],
            "O compilador avisa que totl não foi declarada e às vezes até sugere o nome parecido, total.",
            compila=False,
        ),
    ],
    "erros lógicos": [
        erro(
            r'''
            int a = 8, b = 10, c = 12;
            double media = a + b + c / 3;
            printf("%.2f\n", media);
            ''',
            "Faltam parênteses: só c é dividido por 3; o certo é (a + b + c) / 3.0.",
            [
                "media deveria ser declarada como int.",
                "%.2f não mostra valores double.",
                "As variáveis deveriam ser declaradas em linhas separadas.",
            ],
            "O programa compila e mostra 22.00 em vez de 10.00. Um erro de lógica só aparece comparando com o "
            "resultado esperado.",
        ),
        saida(
            r'''
            int contagem = 0;
            for (int i = 1; i < 10; i++) {
                contagem++;
            }
            printf("%d\n", contagem);
            ''',
            "9",
            ["10", "11", "1"],
            "De 1 a 9 são nove repetições. Para contar até 10 seria preciso i <= 10, um erro clássico de "
            "fronteira.",
            pergunta="Este laço deveria contar de 1 a 10. O que ele mostra?",
        ),
        conceito(
            "Uma função valida idades de 0 a 120. Quais valores ajudam mais a achar erros nela?",
            "Os de fronteira, como -1, 0, 120 e 121.",
            [
                "Só o 30, que é um valor comum.",
                "Nenhum: basta o programa compilar.",
                "Só valores muito grandes, como 99999 ou 1000000.",
            ],
            "Erros de < no lugar de <= aparecem exatamente nos limites da faixa.",
        ),
        erro(
            r'''
            int soma = 25, quantidade = 2;
            double media = soma / quantidade;
            printf("%.1f\n", media);
            ''',
            "soma / quantidade é uma divisão inteira (dá 12), e a parte decimal se perde antes de virar double.",
            [
                "%.1f deveria ser %d.",
                "media precisaria ser float, e não double.",
                "25 / 2 dá erro porque a divisão não é exata.",
            ],
            "O programa mostra 12.0 em vez de 12.5. Converta um dos lados: (double) soma / quantidade.",
        ),
    ],
    "debug": [
        conceito(
            "Um programa dá resultado errado. Qual é o primeiro passo de uma boa depuração?",
            "Reproduzir o erro e observar o estado das variáveis.",
            [
                "Reescrever o programa inteiro do zero.",
                "Mudar várias linhas ao mesmo tempo até o resultado ficar certo.",
                "Trocar todos os int por double.",
            ],
            "Com o erro reproduzível, dá para comparar o valor das variáveis com o esperado e achar onde divergem.",
        ),
        conceito(
            "Por que mudar uma coisa de cada vez ao depurar?",
            "Para saber exatamente qual mudança resolveu, ou piorou, o problema investigado.",
            [
                "Porque o compilador só aceita uma mudança por vez.",
                "Porque mudar mais de uma linha de uma vez apaga o histórico do arquivo.",
                "Para o programa compilar mais rápido.",
            ],
            "Cada mudança testa uma hipótese. Várias mudanças juntas misturam as causas.",
        ),
        saida(
            r'''
            int v[3] = {10, 20, 12};
            int total = 0;
            for (int i = 0; i < 3; i++) {
                total = total + v[i];
                printf("i=%d total=%d\n", i, total);
            }
            ''',
            "i=0 total=10\ni=1 total=30\ni=2 total=42",
            [
                "i=1 total=10\ni=2 total=30\ni=3 total=42",
                "i=0 total=0\ni=1 total=10\ni=2 total=30",
                "i=0 total=10\ni=1 total=20\ni=2 total=12",
            ],
            "Um printf dentro do laço mostra o estado a cada passo. O total aparece depois da soma de cada "
            "elemento.",
        ),
        conceito(
            "O que `assert(divisor != 0);` faz?",
            "Se a condição for falsa, encerra o programa e mostra onde falhou.",
            [
                "Troca o divisor por 1 automaticamente.",
                "Pula a linha seguinte quando o divisor é 0.",
                "Mostra um aviso na tela e deixa o programa continuar normalmente com o divisor.",
            ],
            "assert (de assert.h) confere uma suposição do programa e para cedo, perto da causa do erro.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 17
    "gcc": [
        conceito(
            "O que faz o comando `gcc programa.c -o calculadora`?",
            "Compila programa.c e cria o executável com o nome calculadora.",
            [
                "Abre o programa calculadora para edição no editor padrão do sistema.",
                "Compila só se já existir um arquivo chamado calculadora.",
                "Cria um arquivo de código chamado calculadora.c.",
            ],
            "-o (de output) escolhe o nome do arquivo gerado. Sem ele, o gcc usa a.out (ou a.exe no Windows).",
        ),
        conceito(
            "Para que servem as opções -Wall e -Wextra?",
            "Ligam mais avisos e ajudam a encontrar problemas cedo.",
            [
                "Deixam o programa mais rápido.",
                "Escondem todos os avisos, para a saída do compilador ficar limpa.",
                "Compilam todos os arquivos da pasta.",
            ],
            "Os avisos apontam variáveis não usadas, formatos errados no printf e outros defeitos comuns.",
        ),
        conceito(
            "O que a opção -std=c11 garante?",
            "Que o código siga as regras do padrão C11, do mesmo jeito em qualquer ambiente.",
            [
                "Que o programa rode 11 vezes mais rápido.",
                "Que apareçam no máximo 11 avisos.",
                "Que o programa também possa ser compilado como C++, sem mudanças.",
            ],
            "Sem fixar o padrão, cada compilador pode aceitar extensões diferentes.",
        ),
        erro(
            r'''
            int total = 10;
            printf("Total: %d\n");
            ''',
            "Falta o argumento do %d; o printf vai mostrar um valor qualquer.",
            [
                "%d não pode ser usado logo depois de dois-pontos dentro do texto.",
                "total deveria ser declarada depois do printf que a mostra.",
                "O \\n precisa ficar no começo do texto, antes de Total.",
            ],
            "Com -Wall, o gcc avisa que o formato pede um int que não foi passado. Sem a opção, o erro passaria "
            "despercebido.",
            pergunta="Compilando com gcc -Wall, o compilador avisa sobre este código. Qual é o problema?",
        ),
    ],
    "linking": [
        erro(
            r'''
            #include <stdio.h>

            int resposta(void);

            int main(void) {
                printf("%d\n", resposta());
                return 0;
            }
            ''',
            "resposta foi declarada, mas não foi implementada: a ligação não encontra a função.",
            [
                "O protótipo de resposta deveria ficar depois de main.",
                "Funções sem parâmetros não podem devolver int.",
                "printf não pode receber o valor de uma função como argumento.",
            ],
            "O protótipo basta para compilar main, mas o linker precisa do corpo da função e acusa \"undefined "
            "reference to resposta\".",
            pergunta="O gcc compila este arquivo, mas não consegue gerar o executável. Por quê?",
            compila=False,
        ),
        conceito(
            "Quando aparece o erro `multiple definition of 'somar'`?",
            "Quando somar é implementada em dois arquivos do mesmo programa.",
            [
                "Quando somar é chamada duas vezes.",
                "Quando o protótipo de somar aparece em dois arquivos .h diferentes do projeto.",
                "Quando somar recebe dois parâmetros.",
            ],
            "Declarações podem se repetir. A implementação de cada função só pode existir em um lugar.",
        ),
        conceito(
            "Qual etapa junta main.o e util.o em um executável?",
            "A ligação (linking).",
            ["O pré-processamento.", "A compilação de main.c.", "A execução do programa."],
            "Cada .c vira um .o separado, e o linker os combina, resolvendo as chamadas entre eles.",
        ),
        conceito(
            "Qual destes problemas só aparece na ligação, e não na compilação?",
            "Chamar uma função declarada que não foi implementada em nenhum arquivo.",
            [
                "Esquecer um ponto e vírgula.",
                "Usar uma variável que não foi declarada.",
                "Chamar uma função com o número errado de argumentos.",
            ],
            "Os outros três o compilador já detecta ao olhar um arquivo sozinho.",
        ),
    ],
    "makefile": [
        conceito(
            "Em um Makefile, o que significa a linha `app: main.o util.o`?",
            "app depende de main.o e util.o e é refeito quando eles mudam.",
            [
                "app será apagado e recriado do zero sempre que main.o e util.o forem criados.",
                "main.o e util.o serão executados em sequência.",
                "É um comentário com a lista de arquivos do projeto.",
            ],
            "O make compara as datas: se uma dependência é mais nova que o alvo, ele roda o comando do alvo.",
        ),
        conceito(
            "Por que as linhas de comando de um Makefile começam com tabulação?",
            "Porque o make exige tabulação nas linhas de comando.",
            [
                "Só por estética: espaços funcionam do mesmo jeito em qualquer versão do make.",
                "Para marcar a linha como comentário.",
                "Para o comando rodar em paralelo.",
            ],
            "Com espaços no lugar da tabulação, o make costuma acusar o erro \"missing separator\".",
        ),
        conceito(
            "util.h mudou, mas não está listado como dependência de main.o. O que pode acontecer?",
            "O make pode não recompilar main.o, e o programa fica desatualizado.",
            [
                "O make percebe a mudança sozinho e recompila todos os arquivos automaticamente.",
                "O make apaga o arquivo util.h.",
                "O make mostra um erro de sintaxe.",
            ],
            "O make só sabe das dependências que foram declaradas. Faltando uma, mudanças passam despercebidas.",
        ),
        conceito(
            "Para que servem as variáveis CC e CFLAGS em um Makefile?",
            "Para definir compilador e opções em um só lugar.",
            [
                "Para guardar os dados digitados pelo usuário durante a compilação.",
                "Para contar quantos arquivos foram compilados.",
                "Para criar variáveis globais no programa em C.",
            ],
            "Para trocar -O0 por -O2, por exemplo, basta mudar CFLAGS, e todas as regras passam a usar a opção "
            "nova.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 18
    "buffer overflow": [
        conceito(
            "Por que `scanf(\"%s\", nome)` com `char nome[10]` é perigoso?",
            "Sem largura máxima, uma palavra longa passa das 10 posições.",
            [
                "Porque %s não lê letras maiúsculas.",
                "Porque falta o & antes de nome.",
                "Porque scanf apaga o conteúdo anterior de nome antes de gravar a palavra nova.",
            ],
            "Use %9s, deixando uma posição para o '\\0'. Vetores já são endereços, por isso não levam &.",
        ),
        lacuna(
            r'''
            char nome[10];
            if (scanf("____", nome) == 1) {
                printf("%s\n", nome);
            }
            ''',
            "%9s",
            ["%10s", "%s", "%11s"],
            "Programac",
            "Com %9s, o scanf lê no máximo 9 caracteres e o '\\0' ocupa a décima posição. As outras opções "
            "escrevem além do vetor.",
            pergunta="Se o usuário digitar `Programacao`, o que completa a lacuna para ler com segurança e "
                     "mostrar `Programac`?",
            entrada="Programacao\n",
        ),
        conceito(
            "Quantos caracteres de texto cabem com segurança em `char codigo[8]`?",
            "7",
            ["8", "9", "16"],
            "A capacidade de texto é sempre o tamanho do vetor menos 1.",
        ),
        conceito(
            "Qual destas funções nunca deve ser usada, por não ter nenhum limite de tamanho?",
            "gets",
            ["fgets", "strncpy", "snprintf"],
            "gets foi removida do C11 justamente por isso. As outras três recebem um limite de tamanho.",
        ),
    ],
    "validação": [
        saida(
            r'''
            int idade;
            if (scanf("%d", &idade) != 1) {
                printf("Entrada invalida\n");
            } else if (idade < 0 || idade > 120) {
                printf("Fora da faixa\n");
            } else {
                printf("Idade valida\n");
            }
            ''',
            "Entrada invalida",
            ["Fora da faixa", "Idade valida", "0"],
            "abc não é um número, então scanf devolve 0 e a primeira verificação já trata o caso.",
            pergunta="Se o usuário digitar `abc`, o que o programa mostra?",
            entrada="abc\n",
        ),
        conceito(
            "Quando um dado digitado deve ser validado?",
            "Logo depois de ser lido, antes de ser usado em qualquer cálculo ou decisão.",
            [
                "Depois do cálculo, conferindo se o resultado final parece razoável.",
                "Só no final do programa.",
                "Não é preciso, se o usuário for avisado do formato.",
            ],
            "Um valor inválido usado em uma conta já pode ter causado dano, como uma divisão por zero.",
        ),
        lacuna(
            r'''
            int nota = 11;
            if (____) {
                printf("Nota invalida\n");
            }
            ''',
            "nota < 0 || nota > 10",
            ["nota < 0 && nota > 10", "nota >= 0 && nota <= 10", "nota < 0"],
            "Nota invalida",
            "Uma nota é inválida se estiver abaixo de 0 OU acima de 10. Com &&, a condição nunca seria verdadeira.",
            pergunta="Notas válidas vão de 0 a 10. O que completa a lacuna para o programa mostrar "
                     "`Nota invalida`?",
        ),
        conceito(
            "Por que tratar \"entrada inválida\" e \"valor fora da faixa\" como casos separados?",
            "Para orientar melhor: abc não é número; 150 é número fora da faixa.",
            [
                "Porque o C exige duas mensagens de erro.",
                "Porque valores fora da faixa travam o programa assim que são lidos pelo scanf.",
                "Não há motivo: os dois casos são iguais.",
            ],
            "Cada caso pede uma orientação diferente para o usuário, e o programa fica previsível.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 19
    "listas": [
        saida(
            r'''
            #include <stdio.h>

            struct No {
                int valor;
                struct No *proximo;
            };

            int main(void) {
                struct No c = {30, NULL};
                struct No b = {20, &c};
                struct No a = {10, &b};
                for (struct No *p = &a; p != NULL; p = p->proximo) {
                    printf("%d ", p->valor);
                }
                printf("\n");
                return 0;
            }
            ''',
            "10 20 30",
            ["30 20 10", "10", "10 20"],
            "O percurso começa em a e segue os ponteiros proximo até encontrar NULL.",
        ),
        conceito(
            "Qual a vantagem de inserir no início de uma lista encadeada?",
            "É rápido e não depende do tamanho da lista: só se ajustam dois ponteiros.",
            [
                "A lista fica ordenada automaticamente.",
                "A memória dos outros nós é liberada.",
                "Qualquer posição da lista passa a ser acessada diretamente, como em um vetor.",
            ],
            "O novo nó aponta para o antigo primeiro, e o início passa a ser o novo nó. É O(1).",
        ),
        erro(
            r'''
            #include <stdlib.h>

            struct No {
                int valor;
                struct No *proximo;
            };

            void liberar(struct No *inicio) {
                struct No *atual = inicio;
                while (atual != NULL) {
                    free(atual);
                    atual = atual->proximo;
                }
            }

            int main(void) {
                liberar(NULL);
                return 0;
            }
            ''',
            "atual->proximo é lido depois de free(atual); é preciso guardar o próximo antes de liberar.",
            [
                "free não pode ser chamado dentro de um while.",
                "A liberação deveria começar pelo último nó.",
                "atual deveria ser um vetor, e não um ponteiro.",
            ],
            "Guarde struct No *proximo = atual->proximo; antes do free, e depois avance para ele.",
        ),
        conceito(
            "Para acessar o 50º elemento de uma lista encadeada, o que é preciso fazer?",
            "Percorrer os nós desde o início, um a um, seguindo os ponteiros.",
            [
                "Usar lista[49], como em um vetor.",
                "Liberar os 49 primeiros nós.",
                "Nada, porque cada nó guarda o próprio índice.",
            ],
            "Os nós ficam espalhados na memória, ligados só pelos ponteiros. O acesso por posição é O(n).",
        ),
    ],
    "pilhas": [
        saida(
            r'''
            int pilha[5];
            int topo = 0;
            pilha[topo++] = 1;
            pilha[topo++] = 2;
            pilha[topo++] = 3;
            printf("%d ", pilha[--topo]);
            printf("%d\n", pilha[--topo]);
            ''',
            "3 2",
            ["1 2", "3 3", "2 1"],
            "Pilha é LIFO: o último a entrar (3) é o primeiro a sair, depois o 2.",
        ),
        conceito(
            "Qual destas situações funciona como uma pilha (LIFO)?",
            "O botão Desfazer de um editor, que desfaz primeiro a ação mais recente.",
            [
                "Uma fila de atendimento no banco.",
                "Uma lista de chamada em ordem alfabética.",
                "Uma impressora que atende os pedidos na ordem em que eles chegaram.",
            ],
            "As ações são empilhadas, e Desfazer retira sempre a do topo, a mais recente.",
        ),
        erro(
            r'''
            #include <stdio.h>

            #define CAPACIDADE 3

            int pilha[CAPACIDADE];
            int topo = 0;

            void push(int valor) {
                pilha[topo] = valor;
                topo++;
            }

            int main(void) {
                for (int i = 1; i <= 5; i++) {
                    push(i);
                }
                printf("%d\n", topo);
                return 0;
            }
            ''',
            "push não confere se a pilha está cheia; o 4º e o 5º valores são escritos fora do vetor.",
            [
                "topo deveria começar em 1.",
                "push deveria devolver int.",
                "A pilha deveria ser uma variável local de main.",
            ],
            "Antes de empilhar, teste if (topo == CAPACIDADE) e recuse o valor.",
        ),
        saida(
            r'''
            #include <stdio.h>

            int pilha[10];
            int topo = 0;

            void push(int valor) {
                if (topo < 10) {
                    pilha[topo++] = valor;
                }
            }

            int pop(void) {
                if (topo == 0) {
                    return -1;
                }
                return pilha[--topo];
            }

            int main(void) {
                push(7);
                int a = pop();
                int b = pop();
                printf("%d %d\n", a, b);
                return 0;
            }
            ''',
            "7 -1",
            ["7 7", "-1 7", "7 0"],
            "O primeiro pop tira o 7. No segundo, a pilha está vazia, e pop devolve -1 em vez de ler fora do vetor.",
        ),
    ],
    "filas": [
        saida(
            r'''
            int fila[5];
            int inicio = 0, fim = 0;
            fila[fim++] = 42;
            fila[fim++] = 10;
            fila[fim++] = 7;
            printf("%d ", fila[inicio++]);
            printf("%d\n", fila[inicio++]);
            ''',
            "42 10",
            ["7 10", "42 42", "10 7"],
            "Fila é FIFO: sai primeiro quem entrou primeiro (42), depois o 10.",
        ),
        conceito(
            "Qual é a regra de uma fila?",
            "FIFO: o primeiro a entrar é o primeiro a sair, como em uma fila de banco.",
            [
                "LIFO: o último a entrar é o primeiro a sair.",
                "O maior valor sai primeiro.",
                "Qualquer elemento pode sair a qualquer momento.",
            ],
            "Como em uma fila de banco: entra no fim, sai pelo início.",
        ),
        saida(
            r'''
            int capacidade = 4;
            int fim = 3;
            fim = (fim + 1) % capacidade;
            printf("%d\n", fim);
            ''',
            "0",
            ["4", "3", "1"],
            "Na fila circular, o índice que passaria do fim volta para 0. O resto da divisão faz essa volta.",
        ),
        conceito(
            "Por que usar uma fila circular em vez de mover todos os elementos a cada remoção?",
            "Para remover em tempo constante, só avançando o início.",
            [
                "Porque a fila circular aceita infinitos elementos.",
                "Porque mover elementos não compila em C.",
                "Para manter os elementos sempre em ordem crescente dentro do vetor.",
            ],
            "Mover tudo custa O(n) por remoção. Com índices que dão a volta, cada operação é O(1).",
        ),
    ],
    "árvores": [
        conceito(
            "Em uma árvore binária de busca com raiz 20, onde fica o 15?",
            "À esquerda da raiz, porque é menor que 20.",
            [
                "À direita da raiz, porque é o segundo valor inserido.",
                "Na raiz, no lugar do 20.",
                "Em qualquer lado, porque a ordem não importa.",
            ],
            "Na árvore de busca, os menores ficam à esquerda e os maiores à direita, em cada nó.",
        ),
        saida(
            r'''
            #include <stdio.h>

            struct No {
                int valor;
                struct No *esq;
                struct No *dir;
            };

            void em_ordem(struct No *no) {
                if (no == NULL) {
                    return;
                }
                em_ordem(no->esq);
                printf("%d ", no->valor);
                em_ordem(no->dir);
            }

            int main(void) {
                struct No a = {5, NULL, NULL};
                struct No c = {30, NULL, NULL};
                struct No b = {10, &a, NULL};
                struct No raiz = {20, &b, &c};
                em_ordem(&raiz);
                printf("\n");
                return 0;
            }
            ''',
            "5 10 20 30",
            ["20 10 5 30", "5 10 30 20", "20 30 10 5"],
            "O percurso em ordem visita a esquerda, depois o nó, depois a direita. Em uma árvore de busca, isso "
            "dá os valores em ordem crescente.",
        ),
        conceito(
            "Inserir 1, 2, 3, 4 e 5, nessa ordem, em uma árvore de busca sem balanceamento gera o quê?",
            "Uma árvore que parece uma lista, com busca lenta (tempo linear).",
            [
                "Uma árvore perfeitamente balanceada.",
                "Uma árvore com o 1 na raiz e os outros quatro como filhos diretos dele.",
                "Um erro, porque valores em ordem não podem ser inseridos.",
            ],
            "Cada valor maior vai sempre para a direita do anterior, formando uma linha. Por isso existem árvores "
            "que se balanceiam.",
        ),
        conceito(
            "Qual percurso de uma árvore de busca mostra os valores em ordem crescente?",
            "Em ordem: esquerda, depois o nó, depois a direita.",
            [
                "Pré-ordem: nó, esquerda, direita.",
                "Pós-ordem: esquerda, direita, nó.",
                "Por nível, da raiz para baixo.",
            ],
            "Como tudo à esquerda é menor e tudo à direita é maior, visitar nessa ordem produz a sequência "
            "ordenada.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 20
    "busca linear": [
        saida(
            r'''
            int v[] = {7, 3, 9, 3};
            int posicao = -1;
            for (int i = 0; i < 4; i++) {
                if (v[i] == 3) {
                    posicao = i;
                    break;
                }
            }
            printf("%d\n", posicao);
            ''',
            "1",
            ["3", "2", "-1"],
            "A busca para na primeira ocorrência, no índice 1. Sem o break, terminaria com o último 3, no "
            "índice 3.",
        ),
        saida(
            r'''
            int v[] = {4, 8, 15};
            int posicao = -1;
            for (int i = 0; i < 3; i++) {
                if (v[i] == 16) {
                    posicao = i;
                    break;
                }
            }
            printf("%d\n", posicao);
            ''',
            "-1",
            ["3", "0", "2"],
            "Nenhum elemento é 16, então posicao mantém o valor inicial -1, que significa \"não encontrado\".",
        ),
        conceito(
            "No pior caso, quantas comparações a busca linear faz em um vetor de 1000 elementos?",
            "1000",
            ["1", "10000", "500"],
            "Se o alvo for o último ou não existir, ela olha todos os elementos: custo O(n).",
        ),
        conceito(
            "A busca linear exige que o vetor esteja ordenado?",
            "Não: ela olha os elementos um a um.",
            [
                "Sim, senão ela não encontra nada.",
                "Sim, em ordem crescente, para poder parar no meio.",
                "Só quando há números repetidos.",
            ],
            "Essa é a vantagem dela. Buscas mais rápidas, como a binária, precisam de dados ordenados.",
        ),
    ],
    "bubble sort": [
        saida(
            r'''
            int v[4] = {5, 1, 4, 2};
            for (int j = 0; j < 3; j++) {
                if (v[j] > v[j + 1]) {
                    int t = v[j];
                    v[j] = v[j + 1];
                    v[j + 1] = t;
                }
            }
            printf("%d %d %d %d\n", v[0], v[1], v[2], v[3]);
            ''',
            "1 4 2 5",
            ["1 2 4 5", "1 5 4 2", "5 4 2 1"],
            "Esta é só uma passada: o 5 vai sendo trocado com os vizinhos até o fim. O resto ainda não está em "
            "ordem.",
        ),
        conceito(
            "Depois da primeira passada completa do bubble sort em ordem crescente, o que é garantido?",
            "O maior elemento já está na última posição do vetor.",
            [
                "O menor elemento está na primeira posição.",
                "O vetor inteiro já está ordenado.",
                "A primeira metade do vetor está ordenada.",
            ],
            "O maior valor é carregado até o fim em cada passada. Por isso cada passada seguinte pode ir uma "
            "posição a menos.",
        ),
        conceito(
            "Aproximadamente quantas comparações o bubble sort faz para ordenar 100 elementos?",
            "Cerca de 5.000",
            ["Cerca de 100", "Cerca de 200", "Cerca de 10.000"],
            "São n(n-1)/2 = 4950 comparações. Dobrar o tamanho quadruplica o trabalho.",
        ),
        lacuna(
            r'''
            int v[4] = {3, 9, 1, 7};
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3 - i; j++) {
                    if (____) {
                        int t = v[j];
                        v[j] = v[j + 1];
                        v[j + 1] = t;
                    }
                }
            }
            printf("%d %d %d %d\n", v[0], v[1], v[2], v[3]);
            ''',
            "v[j] < v[j + 1]",
            ["v[j] > v[j + 1]", "v[j + 1] < v[j]", "v[j] == v[j + 1]"],
            "9 7 3 1",
            "Para ordem decrescente, troca-se quando o da esquerda é menor que o da direita. > ordenaria em ordem "
            "crescente.",
        ),
    ],
    "eficiência": [
        conceito(
            "Um algoritmo O(n) leva 1 segundo para 1000 itens. Quanto leva, aproximadamente, para 2000?",
            "2 segundos",
            ["4 segundos", "1 segundo", "1000 segundos"],
            "O tempo cresce na mesma proporção da entrada: o dobro de itens leva o dobro do tempo.",
        ),
        conceito(
            "Um algoritmo O(n²) leva 1 segundo para 1000 itens. Quanto leva, aproximadamente, para 2000?",
            "4 segundos",
            ["2 segundos", "1 segundo", "8 segundos"],
            "Com n², dobrar a entrada multiplica o tempo por 2² = 4.",
        ),
        saida(
            r'''
            int operacoes = 0;
            int n = 4;
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    operacoes++;
                }
            }
            printf("%d\n", operacoes);
            ''',
            "16",
            ["8", "4", "10"],
            "Dois laços aninhados de n voltas fazem n * n operações. Esse é o comportamento O(n²).",
        ),
        conceito(
            "Um programa está lento. O que verificar primeiro?",
            "Se o algoritmo é adequado, como trocar uma solução O(n²) por uma O(n).",
            [
                "Trocar i++ por ++i em todos os laços, que é mais rápido.",
                "Remover os comentários do código.",
                "Usar nomes de variáveis mais curtos.",
            ],
            "Ajustes pequenos quase não mudam o tempo. A escolha do algoritmo muda a forma como ele cresce.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 21
    "calculadora": [
        erro(
            r'''
            double a = 10, b = 0;
            double r = a / b;
            if (b == 0) {
                printf("Erro: divisao por zero\n");
            } else {
                printf("%.2f\n", r);
            }
            ''',
            "A divisão é feita antes de verificar se b é zero; a verificação deveria vir antes da conta.",
            [
                "double não aceita o valor 0.",
                "%.2f não mostra resultados de divisão.",
                "O else deveria vir antes do if.",
            ],
            "Com double, a divisão por zero dá infinito; com int, pode encerrar o programa. Valide o divisor antes "
            "de dividir.",
        ),
        saida(
            r'''
            double a = 20, b = 22;
            char op = '*';
            switch (op) {
                case '+':
                    printf("%.2f\n", a + b);
                    break;
                case '-':
                    printf("%.2f\n", a - b);
                    break;
                default:
                    printf("Operador invalido\n");
            }
            ''',
            "Operador invalido",
            ["440.00", "42.00", "0.00"],
            "Não existe case '*', então roda o default. Toda operação aceita precisa do seu case.",
        ),
        conceito(
            "Por que colocar o cálculo em uma função como `double calcular(double a, char op, double b)`?",
            "Para separar o cálculo da leitura e poder testá-lo sozinho.",
            [
                "Porque o switch só funciona dentro de funções.",
                "Porque main não pode fazer contas.",
                "Para o programa ocupar menos memória enquanto espera o usuário digitar.",
            ],
            "Com o cálculo isolado, dá para testar calcular(20, '+', 22) sem digitar nada.",
        ),
        saida(
            r'''
            double a, b;
            char op;
            if (scanf("%lf %c %lf", &a, &op, &b) == 3) {
                printf("%c %.2f\n", op, a + b);
            }
            ''',
            "+ 42.00",
            ["+ 42", "20 + 22", "42.00 +"],
            "O scanf lê o número, o operador como char e o outro número. O espaço antes de %c pula os espaços "
            "digitados.",
            pergunta="Se o usuário digitar `20 + 22`, o que o programa mostra?",
            entrada="20 + 22\n",
        ),
    ],
    "cadastro": [
        conceito(
            "Por que ler o nome com `scanf(\"%29s\", p.nome)` quando o campo é `char nome[30]`?",
            "Para ler no máximo 29 caracteres e não invadir os outros campos da struct.",
            [
                "Porque %29s aceita nomes com espaços.",
                "Porque o nome precisa ter exatamente 29 letras.",
                "Porque, sem o número, o nome não é salvo dentro da struct Pessoa.",
            ],
            "Sem limite, um nome longo invade a memória dos outros campos, como a idade.",
        ),
        saida(
            r'''
            #include <stdio.h>

            struct Pessoa {
                char nome[30];
                int idade;
            };

            int main(void) {
                struct Pessoa p;
                if (scanf("%29s %d", p.nome, &p.idade) == 2) {
                    printf("%s tem %d anos\n", p.nome, p.idade);
                } else {
                    printf("Cadastro invalido\n");
                }
                return 0;
            }
            ''',
            "Cadastro invalido",
            ["Ana Maria tem 20 anos", "Ana tem 20 anos", "Ana tem 0 anos"],
            "%s para no espaço: o nome recebe só \"Ana\", e o %d encontra \"Maria\", que não é número. O scanf "
            "devolve 1 e o cadastro é recusado.",
            pergunta="Se o usuário digitar `Ana Maria 20`, o que o programa mostra?",
            entrada="Ana Maria 20\n",
        ),
        conceito(
            "Em um cadastro guardado em vetor, como identificar cada registro?",
            "Com um código único ou com a posição no vetor, que não muda com o tempo.",
            [
                "Pelo nome, já que nomes nunca se repetem.",
                "Pela idade da pessoa, que é um número e fica fácil de comparar.",
                "Pelo endereço de memória mostrado com %p.",
            ],
            "Nomes podem se repetir e mudar. Um identificador fixo evita alterar o registro errado.",
        ),
        conceito(
            "Ao ler a idade no cadastro, o que deve ser validado?",
            "Se a leitura funcionou e se o valor está numa faixa possível, como de 0 a 120 anos.",
            [
                "Se a idade é um número par.",
                "Nada, porque o scanf com %d já garante que o número é uma idade válida.",
                "Se a idade tem exatamente dois dígitos.",
            ],
            "O scanf pode falhar (texto no lugar de número) e pode aceitar valores absurdos, como -5.",
        ),
    ],
    "agenda": [
        erro(
            r'''
            #include <stdio.h>
            #include <string.h>

            struct Contato {
                char nome[30];
                char telefone[15];
            };

            struct Contato agenda[2];
            int total = 0;

            void adicionar(const char *nome, const char *telefone) {
                strcpy(agenda[total].nome, nome);
                strcpy(agenda[total].telefone, telefone);
                total++;
            }

            int main(void) {
                adicionar("Ana", "4242-4242");
                adicionar("Bia", "1111-1111");
                adicionar("Caio", "3333-3333");
                printf("%d\n", total);
                return 0;
            }
            ''',
            "adicionar não confere se a agenda já está cheia; o terceiro contato é gravado fora do vetor.",
            [
                "strcpy não pode copiar para campos de struct.",
                "total deveria começar em 1.",
                "Structs não podem ficar em vetores globais.",
            ],
            "Antes de inserir, teste if (total == 2) e avise que a agenda está cheia.",
        ),
        saida(
            r'''
            #include <stdio.h>
            #include <string.h>

            struct Contato {
                char nome[20];
                char telefone[15];
            };

            int main(void) {
                struct Contato agenda[3] = {
                    {"Bia", "1111-1111"},
                    {"Ana", "4242-4242"},
                    {"Caio", "3333-3333"},
                };
                int achou = 0;
                for (int i = 0; i < 3; i++) {
                    if (strcmp(agenda[i].nome, "ana") == 0) {
                        printf("%s\n", agenda[i].telefone);
                        achou = 1;
                    }
                }
                if (!achou) {
                    printf("Nao encontrado\n");
                }
                return 0;
            }
            ''',
            "Nao encontrado",
            ["4242-4242", "1111-1111", "Ana"],
            "strcmp diferencia maiúsculas de minúsculas: \"ana\" não é igual a \"Ana\".",
        ),
        conceito(
            "Por que separar a agenda em funções como inserir, listar e buscar?",
            "Cada função cuida de uma tarefa, com a regra em um só lugar.",
            [
                "Porque structs só podem ser usadas dentro de funções separadas de main.",
                "Porque main não pode ter mais que 10 linhas.",
                "Para não precisar de vetor.",
            ],
            "Se a regra de inserir mudar, por exemplo para impedir nomes repetidos, só uma função muda.",
        ),
        conceito(
            "Para listar os contatos em ordem alfabética, qual função compara dois nomes?",
            "strcmp",
            ["strlen", "strcpy", "O operador =="],
            "strcmp diz qual nome vem antes, que é o que um algoritmo de ordenação precisa saber.",
        ),
    ],
    "jogo terminal": [
        saida(
            r'''
            int alvo = 42, palpite = 0, tentativas = 0;
            do {
                if (scanf("%d", &palpite) != 1) {
                    break;
                }
                tentativas++;
                if (palpite < alvo) {
                    printf("Maior\n");
                } else if (palpite > alvo) {
                    printf("Menor\n");
                }
            } while (palpite != alvo);
            printf("Acertou em %d\n", tentativas);
            ''',
            "Maior\nMenor\nAcertou em 3",
            ["Menor\nMaior\nAcertou em 3", "Maior\nMenor\nAcertou em 2", "Acertou em 3"],
            "10 é pouco (Maior), 50 é muito (Menor) e 42 acerta na terceira tentativa.",
            pergunta="Se o jogador digitar 10, 50 e 42, um por linha, o que o programa mostra?",
            entrada="10\n50\n42\n",
        ),
        conceito(
            "Por que chamar `srand(time(NULL))` só uma vez, no começo do jogo?",
            "Para iniciar o sorteio uma vez; repetir no mesmo segundo repete os números.",
            [
                "Porque srand só pode ser chamada uma vez, senão o programa não compila.",
                "Porque cada chamada de srand gasta muita memória.",
                "Porque time(NULL) só funciona uma vez por programa e depois devolve sempre zero.",
            ],
            "srand define o ponto de partida dos números de rand. Reiniciar com o mesmo segundo repete a "
            "sequência.",
        ),
        conceito(
            "Por que é bom testar o jogo com um alvo fixo, como 42?",
            "Com o alvo conhecido, o teste pode ser repetido e conferido.",
            [
                "Porque rand não funciona durante os testes e devolve sempre o mesmo número.",
                "Porque 42 é o único número que rand consegue gerar.",
                "Para deixar o jogo mais difícil.",
            ],
            "Um resultado previsível torna o teste repetível. O sorteio volta depois que a lógica estiver certa.",
        ),
        conceito(
            "O que evita que o jogador fique preso no laço principal do jogo?",
            "Um limite de tentativas ou uma opção para sair.",
            [
                "Usar for em vez de while.",
                "Mostrar o alvo na tela.",
                "Declarar o palpite como double em vez de int, para aceitar mais valores.",
            ],
            "Todo laço precisa de um caminho de saída, e isso inclui a entrada acabar ou ser inválida.",
        ),
    ],
    "sistema biblioteca": [
        saida(
            r'''
            #include <stdio.h>

            struct Livro {
                int disponivel;
            };

            int emprestar(struct Livro *livro) {
                if (!livro->disponivel) {
                    return 0;
                }
                livro->disponivel = 0;
                return 1;
            }

            int main(void) {
                struct Livro livro = {1};
                printf("%d ", emprestar(&livro));
                printf("%d\n", emprestar(&livro));
                return 0;
            }
            ''',
            "1 0",
            ["1 1", "0 0", "0 1"],
            "O primeiro empréstimo funciona e marca o livro como indisponível. O segundo é recusado pela regra.",
        ),
        conceito(
            "Por que mudar o campo disponivel só pela função emprestar, e não direto em vários lugares?",
            "Para a regra de empréstimo ficar em um só lugar e não ser esquecida.",
            [
                "Porque campos de struct não podem ser alterados fora de funções.",
                "Porque chamar a função deixa o programa mais rápido do que mudar o campo direto.",
                "Para economizar memória.",
            ],
            "Se cada parte do programa mudar o campo do seu jeito, basta uma esquecer a verificação para surgir "
            "um estado impossível.",
        ),
        erro(
            r'''
            #include <stdio.h>

            struct Livro {
                int disponivel;
            };

            void emprestar(struct Livro livro) {
                livro.disponivel = 0;
            }

            int main(void) {
                struct Livro livro = {1};
                emprestar(livro);
                printf("%d\n", livro.disponivel);
                return 0;
            }
            ''',
            "emprestar recebe uma cópia da struct, então a mudança não chega ao livro original.",
            [
                "Uma struct não pode ser parâmetro de função.",
                "O campo disponivel deveria ser char.",
                "Falta return no fim de emprestar.",
            ],
            "Structs também são passadas por cópia. Para alterar o original, receba struct Livro * e use ->.",
        ),
        conceito(
            "Qual destes é um \"estado impossível\" que o sistema da biblioteca deve impedir?",
            "Devolver um livro que não estava emprestado, como se ele tivesse saído.",
            [
                "Cadastrar dois livros com títulos diferentes.",
                "Emprestar um livro disponível.",
                "Listar os livros em ordem alfabética.",
            ],
            "As funções de domínio conferem o estado atual antes de mudá-lo, para os dados não ficarem "
            "contraditórios.",
        ),
    ],
    "editor texto": [
        saida(
            r'''
            char buffer[10] = "abc";
            const char *extra = "defghij";
            if (strlen(buffer) + strlen(extra) + 1 <= sizeof(buffer)) {
                strcat(buffer, extra);
            } else {
                printf("Sem espaco\n");
            }
            printf("%s\n", buffer);
            ''',
            "Sem espaco\nabc",
            ["abcdefghij", "Sem espaco\nabcdefghij", "abcdefghi"],
            "3 + 7 + 1 = 11 posições não cabem em 10. A verificação recusa a inserção, e o texto continua \"abc\".",
            inclui=("string.h",),
        ),
        conceito(
            "Antes de inserir texto no buffer de um editor, o que conferir?",
            "Se o tamanho atual, mais o texto novo, mais o '\\0' cabe no buffer.",
            [
                "Se o texto novo tem só letras.",
                "Se o buffer está vazio, porque só é possível inserir em um buffer vazio.",
                "Nada, se o buffer for uma variável global.",
            ],
            "Essa conta, feita antes de cada inserção, impede o buffer overflow.",
        ),
        saida(
            r'''
            char buffer[8];
            snprintf(buffer, sizeof buffer, "%s%s", "Ola, ", "mundo");
            printf("%s\n", buffer);
            ''',
            "Ola, mu",
            ["Ola, mundo", "Ola, mun", "Ola,"],
            "snprintf respeita o tamanho: grava no máximo 7 caracteres mais o '\\0' e corta o resto, sem "
            "estourar o vetor.",
        ),
        conceito(
            "Em um editor, por que guardar a posição do cursor em uma variável?",
            "Para saber onde inserir ou apagar o próximo caractere.",
            [
                "Para o texto ser salvo em arquivo automaticamente.",
                "Porque strlen precisa dessa posição para contar os caracteres.",
                "Para contar quantas teclas o usuário apertou.",
            ],
            "Os comandos do editor alteram o buffer a partir dessa posição, que também precisa ficar dentro dos "
            "limites.",
        ),
    ],
    "projeto final": [
        conceito(
            "Qual é a melhor ordem para construir o projeto final?",
            "Fazer um fluxo pequeno funcionar de ponta a ponta e só depois acrescentar recursos.",
            [
                "Escrever todos os recursos de uma vez e testar só no final.",
                "Começar pelo visual do menu e deixar as regras e os testes para o final.",
                "Escrever tudo em main e separar em funções só se sobrar tempo.",
            ],
            "Uma versão pequena que funciona é testada cedo, e cada recurso novo entra sobre uma base confiável.",
        ),
        saida(
            r'''
            #include <stdio.h>

            double media(double a, double b, double c) {
                return (a + b + c) / 3;
            }

            int main(void) {
                printf("Media: %.2f\n", media(7, 8, 9.5));
                return 0;
            }
            ''',
            "Media: 8.17",
            ["Media: 8.16", "Media: 8.00", "Media: 8.2"],
            "(7 + 8 + 9.5) / 3 = 8.1666..., e %.2f arredonda para 8.17.",
        ),
        conceito(
            "Por que separar interface (menus), regras e armazenamento em funções diferentes?",
            "Para mudar uma parte sem quebrar as outras.",
            [
                "Porque o C não permite printf e fopen na mesma função.",
                "Porque funções separadas deixam o executável menor.",
                "Porque cada função só pode ter 5 linhas.",
            ],
            "Com responsabilidades separadas, cada parte pode ser testada e alterada com menos risco.",
        ),
        lacuna(
            r'''
            #include <stdio.h>

            int nota_valida(double nota) {
                return ____;
            }

            int main(void) {
                printf("%d %d %d\n", nota_valida(-1), nota_valida(7.5), nota_valida(10.5));
                return 0;
            }
            ''',
            "nota >= 0 && nota <= 10",
            ["nota >= 0 || nota <= 10", "nota >= 0", "nota <= 10"],
            "0 1 0",
            "A nota precisa estar acima do mínimo E abaixo do máximo. Com ||, qualquer número passaria.",
        ),
    ],
}
