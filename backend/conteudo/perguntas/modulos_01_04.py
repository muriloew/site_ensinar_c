"""Perguntas dos módulos 1 a 4: começando a programar, entrada e saída, variáveis e operadores."""

from backend.conteudo.perguntas.base import conceito, erro, lacuna, saida

PERGUNTAS = {
    # ------------------------------------------------------------------ Módulo 1
    "O que é C": [
        conceito(
            "O que significa dizer que C é uma linguagem compilada?",
            "O código-fonte é traduzido para código de máquina antes de o programa ser executado.",
            [
                "Cada linha do arquivo é traduzida e executada uma por vez, enquanto o programa está rodando.",
                "O computador lê o arquivo .c diretamente, sem nenhuma tradução.",
                "O programa só funciona se houver um compilador aberto durante a execução.",
            ],
            "O compilador gera um executável em código de máquina. Depois disso, o programa roda sem o compilador.",
        ),
        conceito(
            "Em qual destes projetos C costuma ser escolhida?",
            "No firmware de um microcontrolador com pouca memória.",
            [
                "Na estilização visual de uma página web, no lugar do CSS.",
                "Em consultas a um banco de dados, no lugar do SQL.",
                "Em fórmulas de planilha, no lugar das funções do Excel.",
            ],
            "C é usada onde controle e eficiência importam: sistemas operacionais, embarcados e bibliotecas.",
        ),
        conceito(
            "Por que se diz que C é uma linguagem \"próxima do hardware\"?",
            "Porque permite acessar a memória diretamente, com endereços e ponteiros.",
            [
                "Porque só pode ser usada para programar placas eletrônicas.",
                "Porque o código precisa ser escrito em zeros e uns.",
                "Porque cada marca de processador tem uma linguagem C com comandos diferentes.",
            ],
            "C dá acesso a endereços de memória e a detalhes de representação dos dados, com pouca camada entre o "
            "programa e a máquina.",
        ),
        conceito(
            "C dá muito controle sobre a memória. O que isso significa para quem programa?",
            "A linguagem não confere acessos inválidos: evitar isso é tarefa de quem programa.",
            [
                "A memória é organizada automaticamente, então não há como errar com ela.",
                "O sistema operacional corrige qualquer acesso inválido antes que cause problemas.",
                "O compilador analisa o código e garante que nenhum programa em C trave durante a execução.",
            ],
            "Com o controle vem a responsabilidade: um acesso fora dos limites não é barrado pela linguagem e pode "
            "corromper dados ou derrubar o programa.",
        ),
    ],
    "Estrutura básica": [
        conceito(
            "Onde começa a execução de um programa em C?",
            "Na função main.",
            [
                "Na primeira linha do arquivo, que costuma ser o #include.",
                "Na última função escrita no arquivo.",
                "Na função que tem o mesmo nome do arquivo.",
            ],
            "Não importa onde main esteja no arquivo: a execução sempre começa por ela.",
        ),
        erro(
            r'''
            #include <stdio.h>

            int main(void) {
                printf("Ola\n")
                return 0;
            }
            ''',
            "Falta o ponto e vírgula no fim da linha do printf.",
            [
                "Falta escrever void também entre as chaves de main.",
                "O #include deveria ficar dentro da função main.",
                "return 0; não pode aparecer depois de um printf.",
            ],
            "Cada instrução termina com ;. Sem ele, o compilador junta a linha do printf com a de baixo e acusa o "
            "erro perto do return.",
            compila=False,
        ),
        conceito(
            "O que as chaves { e } fazem no programa?",
            "Marcam o início e o fim de um bloco, como o corpo da função main.",
            [
                "Indicam um comentário, que o compilador ignora.",
                "Servem só para organizar o código visualmente e podem ser removidas sem mudar nada.",
                "Marcam o texto que será mostrado na tela.",
            ],
            "Tudo o que está entre { e } forma um bloco. É assim que o C sabe quais instruções pertencem a main.",
        ),
        conceito(
            "Se todo o código de main for escrito sem recuo (indentação), o que muda?",
            "Nada na execução; o código só fica mais difícil de ler.",
            [
                "O programa não compila, porque C exige recuo dentro dos blocos.",
                "As linhas sem recuo passam a ser executadas fora de main.",
                "O programa passa a mostrar toda a saída em uma única linha.",
            ],
            "Em C, quem define os blocos são as chaves, não o recuo. A indentação existe para as pessoas lerem.",
        ),
    ],
    "Comentários": [
        saida(
            r'''
            // printf("A\n");
            printf("B\n");
            /* printf("C\n"); */
            printf("D\n");
            ''',
            "B\nD",
            ["A\nB\nC\nD", "A\nC", "B\nC\nD"],
            "As linhas com A e C estão dentro de comentários (// e /* */), então o compilador as ignora.",
        ),
        conceito(
            "Qual destes comentários é mais útil?",
            "`int tentativas = 3; // limite do banco antes de bloquear`",
            [
                "`total = total + preco; // soma o preco ao total`",
                "`int quantidade = 0; // declara a variavel quantidade`",
                "`printf(\"Bem-vindo\"); // mostra a mensagem Bem-vindo na tela`",
            ],
            "Um bom comentário explica o motivo ou uma restrição. Repetir o que o comando já diz não ajuda quem lê.",
        ),
        erro(
            r'''
            #include <stdio.h>

            int main(void) {
                /* mostra a saudação
                printf("Ola\n");
                return 0;
            }
            ''',
            "O comentário aberto com /* nunca é fechado, então o resto do arquivo vira comentário.",
            [
                "O comentário termina no fim da linha, mas falta um ; depois dele.",
                "Comentários não podem ficar dentro da função main.",
                "Comentários de bloco não podem conter acentos, como em saudação.",
            ],
            "Um comentário /* só termina em */. Sem o fechamento, o compilador ignora até o fim do arquivo e acusa o "
            "erro.",
            pergunta="Por que este código não compila?",
            compila=False,
        ),
        conceito(
            "Qual é a forma de comentar várias linhas de uma vez em C?",
            "/* ... */",
            ["// ... //", "<!-- ... -->", "# ... #"],
            "// comenta até o fim da linha. Para um trecho com várias linhas, use /* no início e */ no fim.",
        ),
    ],
    "Compilação": [
        conceito(
            "Qual é a ordem das etapas para transformar código C em executável?",
            "Pré-processamento → compilação → montagem → ligação",
            [
                "Compilação → pré-processamento → ligação → montagem",
                "Ligação → compilação → montagem → pré-processamento",
                "Montagem → ligação → pré-processamento → compilação",
            ],
            "Primeiro o pré-processador trata as linhas com #, depois o código vira assembly, o assembly vira código "
            "objeto e, por fim, a ligação junta tudo em um executável.",
        ),
        conceito(
            "O compilador mostrou 12 mensagens de erro. Por onde começar?",
            "Pela primeira, porque as outras costumam ser consequência dela e somem juntas.",
            [
                "Pela última, que costuma ser a mais importante.",
                "Pela que aponta o maior número de linha.",
                "Por qualquer uma, porque as 12 são sempre problemas independentes.",
            ],
            "Um único erro, como um ; esquecido, confunde o compilador e gera várias mensagens seguidas. Corrija a "
            "primeira e compile de novo.",
        ),
        erro(
            r'''
            int idade = 20;
            printf("Ola\n");
            ''',
            "Só um aviso: idade foi declarada e não é usada. O programa compila e mostra Ola.",
            [
                "Um erro: toda variável declarada precisa ser usada, então o executável não é gerado.",
                "Um erro: printf não pode aparecer depois da declaração de uma variável.",
                "Nada: o gcc só comenta problemas de sintaxe, nunca sobre variáveis.",
            ],
            "Avisos apontam algo suspeito, mas deixam compilar. Erros impedem gerar o executável. Vale corrigir os "
            "dois.",
            pergunta="Ao compilar com gcc -Wall, o que o compilador aponta neste código?",
        ),
        conceito(
            "Qual etapa trata as linhas que começam com #, como #include <stdio.h>?",
            "O pré-processamento.",
            ["A ligação (linking).", "A montagem.", "A execução do programa."],
            "O pré-processador roda antes da compilação: copia o conteúdo dos #include e faz as substituições dos "
            "#define.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 2
    "printf": [
        saida(
            r'''printf("%d + %d = %d\n", 2, 3, 2 + 3);''',
            "2 + 3 = 5",
            ["%d + %d = %d", "2 + 3 = 2 + 3", "d + d = d"],
            "Cada %d é trocado, na ordem, pelos argumentos: 2, 3 e o resultado de 2 + 3.",
        ),
        saida(
            r'''printf("%.2f\n", 3.14159);''',
            "3.14",
            ["3.14159", "3.142", "3.141590"],
            "%.2f mostra o número com exatamente duas casas decimais, arredondando.",
        ),
        saida(
            r'''
            printf("A");
            printf("B\n");
            printf("C\n");
            ''',
            "AB\nC",
            ["A\nB\nC", "ABC", "A B\nC"],
            "printf só muda de linha quando encontra \\n. Como \"A\" não tem \\n, o B aparece logo depois dele.",
        ),
        lacuna(
            r'''
            char letra = 'X';
            printf("Letra: ____\n", letra);
            ''',
            "%c",
            ["%s", "%d", "%f"],
            "Letra: X",
            "%c mostra um caractere. %d mostraria o código numérico de 'X' (88), e %s e %f esperam outros tipos.",
        ),
    ],
    "scanf": [
        erro(
            r'''
            int idade;
            scanf("%d", idade);
            printf("%d\n", idade);
            ''',
            "Falta o & antes de idade: scanf precisa do endereço da variável.",
            [
                "Falta um \\n dentro de \"%d\" para o scanf funcionar.",
                "scanf só lê números quando a variável é float.",
                "O printf deveria vir antes do scanf.",
            ],
            "scanf grava o valor lido na memória da variável, por isso recebe o endereço: &idade.",
        ),
        saida(
            r'''
            int n = 0;
            int lidos = scanf("%d", &n);
            printf("%d %d\n", lidos, n);
            ''',
            "0 0",
            ["1 0", "-1 0", "3 0"],
            "scanf devolve quantos campos conseguiu converter. abc não é um inteiro, então nenhum campo foi lido e n "
            "continua 0.",
            pergunta="Se o usuário digitar `abc`, o que o programa mostra?",
            entrada="abc\n",
        ),
        saida(
            r'''
            int a, b;
            scanf("%d %d", &a, &b);
            printf("%d\n", a * b);
            ''',
            "56",
            ["78", "15", "7 8"],
            "O scanf lê 7 em a e 8 em b; o printf mostra o produto, 56.",
            pergunta="Se o usuário digitar `7 8`, o que o programa mostra?",
            entrada="7 8\n",
        ),
        conceito(
            "Por que é bom conferir o valor que scanf devolve?",
            "Para saber se a leitura deu certo antes de usar o valor guardado na variável.",
            [
                "Porque o valor devolvido é o próprio número que o usuário digitou.",
                "Porque sem conferir o retorno o programa não compila.",
                "Para descobrir quantas teclas o usuário apertou.",
            ],
            "O retorno é a quantidade de campos lidos. Se for menor que o esperado, a variável não recebeu um valor "
            "confiável.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 3
    "int": [
        saida(
            r'''
            int a = 7, b = 2;
            printf("%d\n", a / b);
            ''',
            "3",
            ["3.5", "4", "3.500000"],
            "Entre dois int, a divisão descarta a parte fracionária: 7 / 2 dá 3.",
        ),
        erro(
            r'''
            int total;
            total = total + 5;
            printf("%d\n", total);
            ''',
            "total é usada sem ter recebido um valor inicial, então o resultado é imprevisível.",
            [
                "total precisa ser float para aceitar a soma.",
                "Em C a atribuição deve ser escrita total + 5 = total.",
                "Nada: variáveis int começam sempre com 0, então o código mostra 5.",
            ],
            "Uma variável local não inicializada guarda lixo. Inicialize com int total = 0;.",
        ),
        conceito(
            "Qual destes nomes de variável é válido em C?",
            "`nota_final`",
            ["`2nota`", "`nota final`", "`int`"],
            "Nomes podem ter letras, dígitos e _, mas não podem começar com dígito, ter espaço ou ser palavra "
            "reservada como int.",
        ),
        saida(
            r'''
            int a = 5;
            int b = a;
            a = 9;
            printf("%d %d\n", a, b);
            ''',
            "9 5",
            ["9 9", "5 5", "5 9"],
            "int b = a; copia o valor 5 naquele momento. Mudar a depois não altera b.",
        ),
    ],
    "float e double": [
        saida(
            r'''
            double x = 9.5;
            printf("%f\n", x);
            ''',
            "9.500000",
            ["9.5", "9.50", "10"],
            "Sem indicar as casas, %f mostra seis casas decimais. Para 9.5, use %.1f.",
        ),
        conceito(
            "Qual especificador o scanf usa para ler uma variável double?",
            "%lf",
            ["%f", "%d", "%df"],
            "No scanf, %f é para float e %lf para double. No printf, os dois usam %f.",
        ),
        saida(
            r'''
            double media = (7 + 8) / 2;
            printf("%.1f\n", media);
            ''',
            "7.0",
            ["7.5", "7", "8.0"],
            "(7 + 8) / 2 é uma divisão entre int e dá 7, antes de virar double. Para obter 7.5, escreva / 2.0.",
        ),
        conceito(
            "Por que `0.1 + 0.2 == 0.3` pode dar falso em C?",
            "Porque 0.1 e 0.2 não são exatos em binário, e a soma fica um pouco diferente de 0.3.",
            [
                "Porque o operador == só funciona com int; com double ele compara os endereços das variáveis.",
                "Porque o C arredonda 0.1 + 0.2 para 0.",
                "Porque o compilador transforma 0.3 em int antes de comparar.",
            ],
            "Decimais são aproximações. Para compará-los, verifique se a diferença é menor que uma tolerância.",
        ),
    ],
    "char": [
        saida(
            r'''
            char c = 'A';
            printf("%c %d\n", c, c);
            ''',
            "A 65",
            ["A A", "65 A", "A 1"],
            "Um char guarda um número. Com %c ele aparece como letra e com %d como código ASCII: 'A' é 65.",
        ),
        saida(
            r'''
            char c = 'a';
            c = c + 1;
            printf("%c\n", c);
            ''',
            "b",
            ["a1", "98", "a"],
            "As letras têm códigos seguidos na tabela ASCII, então 'a' + 1 é 'b'.",
        ),
        conceito(
            "Para guardar a letra C em uma variável char, qual linha está correta?",
            "`char letra = 'C';`",
            ["`char letra = \"C\";`", "`char letra = C;`", "`char letra = 'Ce';`"],
            "Um caractere usa aspas simples. Aspas duplas criam uma string, e C sem aspas seria o nome de uma "
            "variável.",
        ),
        saida(
            r'''
            char d = '7';
            printf("%d\n", d - '0');
            ''',
            "7",
            ["55", "'7'", "0"],
            "Os dígitos também têm códigos seguidos: '7' - '0' dá 7. O código do caractere '7' sozinho é 55.",
        ),
    ],
    "constantes": [
        erro(
            r'''
            const int ANO = 2026;
            ANO = 2027;
            printf("%d\n", ANO);
            ''',
            "ANO foi declarada com const e não pode receber outro valor.",
            [
                "Constantes devem ter o nome em letras minúsculas.",
                "Falta o tipo int na segunda linha.",
                "Constantes só podem ser usadas fora de main.",
            ],
            "const avisa ao compilador que o valor não muda. A atribuição ANO = 2027 é recusada.",
            compila=False,
        ),
        conceito(
            "Por que usar `const double TAXA = 0.05;` em vez de escrever 0.05 em vários lugares?",
            "Para dar nome ao valor e mudá-lo em um único lugar se a taxa mudar.",
            [
                "Porque const deixa qualquer conta mais rápida que um número escrito direto.",
                "Porque números decimais só podem ser usados por meio de constantes.",
                "Para que o valor possa ser alterado durante a execução.",
            ],
            "Um nome explica o que o número significa e evita esquecer alguma ocorrência quando o valor muda.",
        ),
        saida(
            r'''
            const int PONTOS_POR_ACERTO = 10;
            int acertos = 4;
            printf("%d\n", acertos * PONTOS_POR_ACERTO);
            ''',
            "40",
            ["410", "14", "10"],
            "A constante vale 10 e participa da conta como qualquer variável: 4 * 10 = 40.",
        ),
        conceito(
            "Qual declaração cria corretamente uma constante inteira?",
            "`const int LIMITE = 100;`",
            [
                "`const int LIMITE;` e, na linha seguinte, `LIMITE = 100;`",
                "`constant int LIMITE = 100;`",
                "`int LIMITE = const 100;`",
            ],
            "A constante recebe o valor na declaração. Depois, nenhuma atribuição é aceita.",
        ),
    ],
    "#define": [
        saida(
            r'''
            #include <stdio.h>
            #define QUADRADO(x) x * x

            int main(void) {
                printf("%d\n", QUADRADO(1 + 2));
                return 0;
            }
            ''',
            "5",
            ["9", "6", "3"],
            "A macro troca texto: QUADRADO(1 + 2) vira 1 + 2 * 1 + 2, que dá 5. Por isso se usa ((x) * (x)).",
        ),
        lacuna(
            r'''
            #include <stdio.h>
            #define DOBRO(x) ____

            int main(void) {
                printf("%d\n", 100 / DOBRO(5));
                return 0;
            }
            ''',
            "((x) * 2)",
            ["x * 2", "(x) * 2", "x + x"],
            "10",
            "Só com parênteses em volta de tudo a macro vira 100 / ((5) * 2) = 10. Sem eles, a divisão acontece "
            "antes: 100 / 5 * 2 = 40.",
        ),
        conceito(
            "Quando acontece a substituição feita por um #define?",
            "No pré-processamento, antes de compilar: o nome é trocado pelo texto.",
            [
                "Durante a execução, toda vez que o programa passa por uma linha que usa o nome.",
                "Na ligação, quando o executável é montado.",
                "Só quando o valor é mostrado com printf.",
            ],
            "#define não cria variável: o pré-processador apenas troca o texto antes de o compilador ver o código.",
        ),
        erro(
            r'''
            #include <stdio.h>
            #define LIMITE 10;

            int main(void) {
                printf("%d\n", LIMITE);
                return 0;
            }
            ''',
            "O ; no fim do #define entra junto na substituição e quebra a linha do printf.",
            [
                "#define precisa de = entre o nome e o valor.",
                "Nomes criados com #define precisam ser minúsculos.",
                "Falta indicar o tipo int no #define.",
            ],
            "Depois da troca, a linha vira printf(\"%d\\n\", 10;); e isso não é C válido. #define não leva ;.",
            compila=False,
        ),
    ],
    "escopo": [
        saida(
            r'''
            int x = 1;
            {
                int x = 2;
                printf("%d ", x);
            }
            printf("%d\n", x);
            ''',
            "2 1",
            ["2 2", "1 1", "1 2"],
            "O x de dentro do bloco é outra variável, que esconde o de fora só até o fim do bloco.",
        ),
        erro(
            r'''
            #include <stdio.h>

            void mostrar(void) {
                printf("%d\n", total);
            }

            int main(void) {
                int total = 30;
                mostrar();
                return 0;
            }
            ''',
            "total é local de main; dentro de mostrar ela não existe.",
            [
                "mostrar deveria ser chamada antes de declarar total.",
                "printf não pode ser usado fora de main.",
                "Falta return 0; no fim de mostrar.",
            ],
            "Variáveis locais só existem no bloco onde foram declaradas. Para usar o valor, passe-o como parâmetro.",
            compila=False,
        ),
        conceito(
            "Por que é melhor preferir variáveis locais a globais?",
            "Porque menos partes do código podem alterá-la, e os erros ficam mais fáceis de achar.",
            [
                "Porque variáveis globais não podem guardar números.",
                "Porque variáveis locais não ocupam memória, já que o compilador as guarda dentro do código.",
                "Porque o C só permite uma variável global por programa.",
            ],
            "Uma global pode ser mudada por qualquer função, e aí fica difícil descobrir quem alterou o valor.",
        ),
        saida(
            r'''
            #include <stdio.h>

            int contador = 0;

            void contar(void) {
                contador = contador + 1;
            }

            int main(void) {
                contar();
                contar();
                printf("%d\n", contador);
                return 0;
            }
            ''',
            "2",
            ["0", "1", "3"],
            "contador é global: as duas chamadas de contar alteram a mesma variável que main mostra.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 4
    "soma": [
        saida(
            r'''printf("%d\n", 7 + 3 * 2);''',
            "13",
            ["20", "12", "17"],
            "A multiplicação vem antes da soma: 3 * 2 = 6 e 7 + 6 = 13.",
        ),
        saida(
            r'''
            int a = 5;
            double b = 2.5;
            printf("%.1f\n", a + b);
            ''',
            "7.5",
            ["7.0", "7", "52.5"],
            "Com um double na conta, o int é promovido e o resultado também é double: 7.5.",
        ),
        saida(
            r'''
            char c = '1';
            printf("%d\n", c + 1);
            ''',
            "50",
            ["2", "11", "1"],
            "'1' é o caractere de código 49, e não o número 1. Por isso c + 1 dá 50.",
        ),
        lacuna(
            r'''
            int a = 18, b = 24;
            int media = ____;
            printf("%d\n", media);
            ''',
            "(a + b) / 2",
            ["a + b / 2", "(a + b) * 2", "a / 2 + b"],
            "21",
            "Sem parênteses, só b seria dividido. (a + b) / 2 soma primeiro e depois divide: 42 / 2 = 21.",
        ),
    ],
    "subtração": [
        saida(
            r'''printf("%d\n", 10 - 4 - 3);''',
            "3",
            ["9", "-3", "17"],
            "Subtrações seguidas são feitas da esquerda para a direita: (10 - 4) - 3 = 3.",
        ),
        saida(
            r'''
            unsigned int estoque = 2;
            estoque = estoque - 3;
            printf("%u\n", estoque);
            ''',
            "4294967295",
            ["-1", "0", "2"],
            "unsigned não guarda negativos: abaixo de zero o valor dá a volta e vira o maior número do tipo.",
        ),
        saida(
            r'''
            int x = 5;
            printf("%d\n", -x + 2);
            ''',
            "-3",
            ["3", "-7", "7"],
            "O - antes de x troca o sinal (-5) e só depois soma 2.",
        ),
        conceito(
            "Que tipo usar para guardar a variação de temperatura entre dois dias, que pode ser negativa?",
            "`int`, ou outro tipo com sinal.",
            [
                "`unsigned int`, porque diferenças nunca são negativas.",
                "`char`, porque ele guarda o sinal de menos como letra.",
                "`unsigned char`, para economizar memória.",
            ],
            "Tipos unsigned não representam negativos. Uma queda de temperatura viraria um número enorme.",
        ),
    ],
    "multiplicação": [
        saida(
            r'''printf("%d\n", (2 + 3) * 4);''',
            "20",
            ["14", "24", "9"],
            "Os parênteses fazem a soma primeiro: 5 * 4 = 20. Sem eles, seria 2 + 12 = 14.",
        ),
        saida(
            r'''
            double preco = 2.5;
            int quantidade = 3;
            printf("%.2f\n", preco * quantidade);
            ''',
            "7.50",
            ["7.00", "6.00", "7.5"],
            "2.5 * 3 = 7.5, e %.2f mostra com duas casas: 7.50.",
        ),
        conceito(
            "Um int tem normalmente 32 bits (máximo 2147483647). O que acontece em `int x = 100000 * 100000;`?",
            "O resultado ultrapassa a faixa de int, e o valor guardado não é confiável (overflow).",
            [
                "x recebe 10000000000 sem problemas.",
                "O compilador percebe o número grande e transforma x em double automaticamente.",
                "x recebe 0, porque o C zera números grandes.",
            ],
            "100000 * 100000 = 10 bilhões, que não cabe em int. A conta estoura antes mesmo de chegar a x.",
        ),
        conceito(
            "Em `int *p;` e em `a * b`, o * significa a mesma coisa?",
            "Não: em `int *p;` declara um ponteiro; em `a * b` multiplica.",
            [
                "Sim: os dois multiplicam.",
                "Sim: os dois criam ponteiros.",
                "Não: em `int *p;` o * multiplica p pelo tamanho de um int na memória.",
            ],
            "O mesmo símbolo tem papéis diferentes conforme o contexto. Ponteiros aparecem no módulo 9.",
        ),
    ],
    "divisão": [
        saida(
            r'''printf("%.2f\n", 7 / 2.0);''',
            "3.50",
            ["3.00", "3.5", "3"],
            "Como 2.0 é double, a divisão mantém a parte decimal: 3.5, mostrado com duas casas.",
        ),
        saida(
            r'''
            double r = 7 / 2;
            printf("%.2f\n", r);
            ''',
            "3.00",
            ["3.50", "3.5", "4.00"],
            "7 / 2 é calculado entre int e dá 3. Só depois o 3 é guardado no double. A variável ser double não "
            "muda a conta.",
        ),
        lacuna(
            r'''
            int a = 10, b = 4;
            double r = ____;
            printf("%.2f\n", r);
            ''',
            "1.0 * a / b",
            ["a / b * 1.0", "a / b", "a / b + 0.0"],
            "2.50",
            "1.0 * a vira double antes da divisão. Nas outras, a / b é feito primeiro entre int e dá 2.",
        ),
        conceito(
            "Por que conferir se o divisor é zero antes de dividir inteiros?",
            "Porque a divisão inteira por zero é inválida e pode encerrar o programa.",
            [
                "Porque o resultado seria 0 e isso atrapalharia a conta.",
                "Porque o C devolve infinito nessa conta, e infinito não cabe em uma variável int.",
                "Não é preciso: o compilador sempre avisa sobre divisões por zero.",
            ],
            "O divisor costuma vir de uma entrada ou de uma conta, então o compilador não tem como prever. A "
            "verificação é do programa.",
        ),
    ],
    "operadores relacionais": [
        saida(
            r'''printf("%d %d\n", 5 <= 5, 3 > 7);''',
            "1 0",
            ["0 0", "1 1", "true false"],
            "Comparações em C produzem 1 (verdadeiro) ou 0 (falso). 5 <= 5 é verdadeiro e 3 > 7 é falso.",
        ),
        saida(
            r'''
            int x = 3;
            if (x = 5) {
                printf("Cinco\n");
            }
            printf("%d\n", x);
            ''',
            "Cinco\n5",
            ["3", "Cinco\n3", "5"],
            "x = 5 é uma atribuição, não uma comparação: x passa a valer 5, e 5 é verdadeiro. Para comparar, use "
            "==.",
        ),
        conceito(
            "Qual expressão testa se idade NÃO é igual a 18?",
            "`idade != 18`",
            ["`idade =! 18`", "`idade <> 18`", "`!idade == 18`"],
            "!= significa \"diferente de\". Cuidado: idade =! 18 compila, mas atribui !18 (que é 0) a idade.",
        ),
        saida(
            r'''printf("%d\n", 10 > 5 > 1);''',
            "0",
            ["1", "10", "5"],
            "C compara da esquerda para a direita: 10 > 5 vale 1, e 1 > 1 é falso. Para testar faixas, use &&.",
        ),
    ],
    "operadores lógicos": [
        saida(
            r'''
            int idade = 20, tem_ingresso = 0;
            printf("%d %d\n", idade >= 18 && tem_ingresso, idade >= 18 || tem_ingresso);
            ''',
            "0 1",
            ["1 1", "0 0", "1 0"],
            "&& exige as duas condições (falta o ingresso), e || se contenta com uma (a idade).",
        ),
        saida(
            r'''
            int x = 0;
            if (x != 0 && 10 / x > 1) {
                printf("Grande\n");
            } else {
                printf("Seguro\n");
            }
            ''',
            "Seguro",
            ["Grande", "Grande\nSeguro", "0"],
            "Com x igual a 0, a primeira parte do && já é falsa, e a divisão nem é feita (curto-circuito).",
        ),
        conceito(
            "Qual a diferença entre & e &&?",
            "&& é o E lógico, com curto-circuito; & é o E bit a bit, que avalia os dois lados.",
            [
                "São iguais; && é só uma forma mais curta de escrever.",
                "& compara textos e && compara números.",
                "&& só funciona dentro de if e & só funciona dentro de while.",
            ],
            "Trocar && por & muda a operação e remove o curto-circuito que protege expressões como a do ponteiro "
            "nulo.",
        ),
        saida(
            r'''
            int a = 0;
            printf("%d %d\n", !a, !!5);
            ''',
            "1 1",
            ["0 5", "1 5", "0 0"],
            "! troca verdadeiro por falso: !0 é 1. !!5 aplica duas vezes: !5 é 0 e !0 é 1.",
        ),
    ],
    "incremento": [
        saida(
            r'''
            int i = 5;
            int a = i++;
            printf("%d %d\n", a, i);
            ''',
            "5 6",
            ["6 6", "5 5", "6 5"],
            "Na forma pós-fixa (i++), a recebe o valor antigo (5) e só depois i aumenta para 6.",
        ),
        saida(
            r'''
            int i = 5;
            int b = ++i;
            printf("%d %d\n", b, i);
            ''',
            "6 6",
            ["5 6", "6 5", "5 5"],
            "Na forma prefixa (++i), i aumenta primeiro, e b recebe o valor já atualizado.",
        ),
        conceito(
            "O que acontece em `i = i++ + ++i;`?",
            "Comportamento indefinido: i muda duas vezes na mesma expressão.",
            ["i aumenta exatamente 2, porque há dois operadores ++ na expressão.", "i aumenta exatamente 3.", "i volta ao valor original, porque um incremento cancela o outro na mesma linha."],
            "O padrão não define a ordem dessas alterações, então compiladores diferentes dão resultados diferentes. "
            "Use comandos separados.",
        ),
        saida(
            r'''
            int x = 10;
            x--;
            --x;
            printf("%d\n", x);
            ''',
            "8",
            ["9", "10", "11"],
            "Isoladas, x-- e --x fazem a mesma coisa: cada uma tira 1 de x.",
        ),
    ],
}
