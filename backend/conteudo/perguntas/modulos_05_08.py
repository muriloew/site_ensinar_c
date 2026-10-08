"""Perguntas dos módulos 5 a 8: decisões, repetições, funções, vetores e textos."""

from backend.conteudo.perguntas.base import conceito, erro, lacuna, saida

PERGUNTAS = {
    # ------------------------------------------------------------------ Módulo 5
    "if": [
        erro(
            r'''
            int n = -5;
            if (n > 0);
            {
                printf("Positivo\n");
            }
            ''',
            "O ; logo depois do if encerra a decisão, e o bloco de baixo sempre executa.",
            [
                "if precisa de um else para funcionar.",
                "A condição deveria ser escrita n => 0.",
                "Faltam chaves em volta da condição n > 0.",
            ],
            "if (n > 0); decide sobre uma instrução vazia. O bloco seguinte não pertence ao if e roda sempre, "
            "mostrando Positivo até para -5.",
        ),
        saida(
            r'''
            int nota = 7;
            if (nota >= 7) {
                printf("Aprovado\n");
            }
            printf("Fim\n");
            ''',
            "Aprovado\nFim",
            ["Aprovado", "Fim", "Fim\nAprovado"],
            "7 >= 7 é verdadeiro, então o bloco roda. O printf de Fim está fora do if e roda de qualquer jeito.",
        ),
        saida(
            r'''
            int x = 0;
            if (x) {
                printf("A\n");
            }
            if (-3) {
                printf("B\n");
            }
            ''',
            "B",
            ["A\nB", "A", "B\nA"],
            "Em C, 0 é falso e qualquer outro valor, inclusive negativo, é verdadeiro.",
        ),
        lacuna(
            r'''
            int temperatura = 30;
            if (____) {
                printf("Calor\n");
            }
            ''',
            "temperatura >= 30",
            ["temperatura > 30", "temperatura < 30", "temperatura == 31"],
            "Calor",
            "Para incluir o próprio 30, a comparação precisa ser >=. Com > 30, o valor 30 fica de fora.",
            pergunta="A regra é \"30 graus ou mais é calor\". O que completa a lacuna para o programa mostrar "
                     "`Calor`?",
        ),
    ],
    "else": [
        saida(
            r'''
            int idade = 18;
            if (idade > 18) {
                printf("Maior\n");
            } else {
                printf("Menor\n");
            }
            ''',
            "Menor",
            ["Maior", "Maior\nMenor", "Menor\nMaior"],
            "18 > 18 é falso, então roda o else. Cuidado com o limite: para incluir o 18, use >=.",
        ),
        saida(
            r'''
            int a = 0, b = 1;
            if (a)
                if (b)
                    printf("X\n");
            else
                printf("Y\n");
            printf("Fim\n");
            ''',
            "Fim",
            ["Y\nFim", "X\nFim", "X\nY\nFim"],
            "O else pertence ao if mais próximo, if (b), apesar do recuo. Como a é 0, nada dentro do primeiro if "
            "roda. Use chaves para evitar essa confusão.",
        ),
        erro(
            r'''
            int n = 4;
            if (n > 0) {
                printf("Positivo\n");
            } else (n < 0) {
                printf("Negativo\n");
            }
            ''',
            "else não recebe condição; para testar outra condição use else if.",
            [
                "Falta ponto e vírgula depois de if (n > 0).",
                "O else deveria vir antes do if.",
                "As chaves do else não são permitidas.",
            ],
            "else é o caminho \"caso contrário\" e não tem condição própria. Para outro teste, escreva "
            "else if (n < 0).",
            compila=False,
        ),
        saida(
            r'''
            int nota = 8;
            if (nota >= 7) {
                printf("Aprovado\n");
            }
            if (nota >= 5) {
                printf("Recuperacao\n");
            }
            ''',
            "Aprovado\nRecuperacao",
            ["Aprovado", "Recuperacao", "Recuperacao\nAprovado"],
            "São dois if separados, e os dois são verdadeiros para 8. Com else entre eles, só o primeiro rodaria.",
        ),
    ],
    "else if": [
        saida(
            r'''
            int nota = 9;
            if (nota >= 7) {
                printf("B\n");
            } else if (nota >= 9) {
                printf("A\n");
            } else {
                printf("C\n");
            }
            ''',
            "B",
            ["A", "B\nA", "A\nB"],
            "A cadeia para na primeira condição verdadeira. 9 >= 7 já é verdadeiro, então o teste >= 9 nem é feito.",
        ),
        conceito(
            "Para classificar notas em A (9 ou mais), B (7 ou mais) e C, qual ordem de testes funciona?",
            "Testar >= 9 primeiro, depois >= 7, e deixar o C no else.",
            [
                "Testar >= 7 primeiro e depois >= 9.",
                "Tanto faz a ordem, porque o C testa todas as condições da cadeia antes de escolher.",
                "Começar pelo else e depois testar >= 9 e >= 7.",
            ],
            "Teste do caso mais específico para o mais geral. Se >= 7 viesse primeiro, uma nota 10 receberia B.",
        ),
        saida(
            r'''
            int x = 15;
            if (x > 10) {
                printf("A");
            } else if (x > 5) {
                printf("B");
            }
            if (x > 0) {
                printf("C");
            }
            printf("\n");
            ''',
            "AC",
            ["ABC", "A", "BC"],
            "Na cadeia if/else if, só o A roda. O if (x > 0) é independente e também roda.",
        ),
        lacuna(
            r'''
            int temp = 15;
            if (temp < 10) {
                printf("Frio\n");
            } ____ (temp < 25) {
                printf("Agradavel\n");
            } else {
                printf("Quente\n");
            }
            ''',
            "else if",
            ["else", "elif", "elseif"],
            "Agradavel",
            "Em C, o segundo teste da cadeia é escrito else if, com espaço. elif e elseif não existem, e else "
            "não recebe condição.",
        ),
    ],
    "switch": [
        saida(
            r'''
            int opcao = 2;
            switch (opcao) {
                case 1:
                    printf("Um\n");
                case 2:
                    printf("Dois\n");
                case 3:
                    printf("Tres\n");
                    break;
                default:
                    printf("Outro\n");
            }
            ''',
            "Dois\nTres",
            ["Dois", "Dois\nTres\nOutro", "Um\nDois"],
            "Sem break no case 2, a execução continua no case 3 até encontrar o break.",
        ),
        erro(
            r'''
            int idade = 20;
            switch (idade) {
                case idade >= 18:
                    printf("Adulto\n");
                    break;
            }
            ''',
            "case só aceita valores constantes; uma condição como idade >= 18 não é permitida.",
            [
                "Falta o default no fim do switch.",
                "switch não funciona com variáveis int.",
                "break não pode aparecer dentro de um case.",
            ],
            "Cada case compara com um valor fixo, como case 18:. Para faixas de valores, use if e else if.",
            compila=False,
        ),
        saida(
            r'''
            int opcao = 7;
            switch (opcao) {
                case 1:
                    printf("Cadastrar\n");
                    break;
                default:
                    printf("Invalida\n");
                    break;
                case 2:
                    printf("Consultar\n");
                    break;
            }
            ''',
            "Invalida",
            ["Invalida\nConsultar", "Consultar", "Cadastrar"],
            "Nenhum case vale 7, então roda o default, mesmo no meio. O break dele impede seguir para o case 2.",
        ),
        conceito(
            "Que tipo de valor pode aparecer em um case do switch?",
            "Valores inteiros constantes, como 1, 2 ou 'a'.",
            [
                "Qualquer texto, como \"sim\" ou \"nao\".",
                "Números decimais, como 2.5.",
                "Intervalos de valores, como de 1 a 10 ou de 'a' a 'z'.",
            ],
            "switch trabalha com inteiros (char também é inteiro). Para textos, use strcmp com if.",
        ),
    ],
    "ternário": [
        saida(
            r'''
            int idade = 16;
            printf("%s\n", idade >= 18 ? "Adulto" : "Jovem");
            ''',
            "Jovem",
            ["Adulto", "16", "Adulto Jovem"],
            "A condição é falsa, então o ternário escolhe o valor depois dos dois-pontos.",
        ),
        saida(
            r'''
            int x = 5;
            int y = x > 3 ? x * 2 : x + 2;
            printf("%d\n", y);
            ''',
            "10",
            ["7", "5", "1"],
            "5 > 3 é verdadeiro, então y recebe x * 2.",
        ),
        lacuna(
            r'''
            int a = 8, b = 3;
            int menor = ____;
            printf("%d\n", menor);
            ''',
            "a < b ? a : b",
            ["a < b ? b : a", "a > b ? a : b", "a > b ? b + 1 : a"],
            "3",
            "Lê-se \"se a < b, então a; senão, b\". Como 8 < 3 é falso, o resultado é b.",
        ),
        conceito(
            "Quando é melhor usar if/else em vez do operador ternário?",
            "Quando cada caminho precisa executar várias ações, e não só escolher um valor.",
            [
                "Sempre que um dos valores for negativo, pois o ternário não aceita números negativos.",
                "Quando a condição usa ==, que o ternário não aceita.",
                "Nunca: o ternário substitui qualquer if.",
            ],
            "O ternário é uma expressão que produz um valor. Para blocos com várias instruções, if/else fica mais "
            "claro.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 6
    "while": [
        saida(
            r'''
            int i = 1;
            while (i <= 3) {
                printf("%d ", i);
                i++;
            }
            printf("\n");
            ''',
            "1 2 3",
            ["1 2", "0 1 2 3", "1 2 3 4"],
            "O laço roda enquanto i <= 3. Quando i chega a 4, a condição fica falsa e o laço para.",
        ),
        saida(
            r'''
            int n = 10;
            while (n < 5) {
                printf("Dentro\n");
                n++;
            }
            printf("%d\n", n);
            ''',
            "10",
            ["Dentro\n10", "5", "Dentro\n11"],
            "while testa antes de entrar. 10 < 5 já é falso, então o corpo executa zero vezes.",
        ),
        erro(
            r'''
            int i = 0;
            while (i < 5) {
                printf("%d\n", i);
            }
            ''',
            "i nunca muda dentro do laço, então ele não termina.",
            [
                "while precisa de ponto e vírgula depois da condição.",
                "i deveria começar em 1.",
                "O laço executa só uma vez porque falta um break.",
            ],
            "O corpo precisa mudar algo da condição. Sem i++, i fica 0 para sempre (laço infinito).",
        ),
        saida(
            r'''
            int soma = 0, n = 1;
            while (soma < 10) {
                soma = soma + n;
                n++;
            }
            printf("%d %d\n", soma, n);
            ''',
            "10 5",
            ["10 4", "15 6", "6 4"],
            "soma passa por 1, 3, 6 e 10 enquanto n vai a 5. Quando soma chega a 10, a condição fica falsa.",
        ),
    ],
    "do while": [
        saida(
            r'''
            int n = 10;
            do {
                printf("%d\n", n);
                n++;
            } while (n < 5);
            ''',
            "10",
            ["11", "10\n11", "5"],
            "do while executa o bloco antes de testar. Mostra 10 uma vez e só então vê que 11 < 5 é falso.",
        ),
        erro(
            r'''
            int i = 1;
            do {
                printf("%d\n", i);
                i++;
            } while (i <= 3)
            ''',
            "Falta o ponto e vírgula depois de while (i <= 3).",
            [
                "do precisa de uma condição entre parênteses logo depois dele.",
                "i++ não pode ficar dentro de um do.",
                "As chaves do do while devem ser removidas.",
            ],
            "Diferente do while comum, o do while termina com ; depois da condição.",
            compila=False,
        ),
        conceito(
            "Qual situação combina melhor com do while?",
            "Mostrar um menu e pedir a opção pelo menos uma vez antes de decidir se repete.",
            [
                "Percorrer um vetor de tamanho conhecido do início ao fim.",
                "Repetir uma ação que, dependendo dos dados, pode não precisar executar nenhuma vez.",
                "Escolher uma ação entre opções fixas, como 1, 2 e 3.",
            ],
            "do while garante uma passagem antes do teste, o que é útil em menus e validações de entrada.",
        ),
        saida(
            r'''
            int i = 3;
            do {
                printf("%d ", i);
                i--;
            } while (i > 0);
            printf("\n");
            ''',
            "3 2 1",
            ["3 2 1 0", "2 1", "3 2"],
            "Mostra 3, 2 e 1. Depois de mostrar o 1, i vira 0 e i > 0 fica falso.",
        ),
    ],
    "for": [
        saida(
            r'''
            for (int i = 0; i < 3; i++) {
                printf("%d ", i);
            }
            printf("\n");
            ''',
            "0 1 2",
            ["1 2 3", "0 1 2 3", "0 1"],
            "O laço começa em 0 e para antes de 3: mostra 0, 1 e 2 (três repetições).",
        ),
        saida(
            r'''
            for (int i = 10; i > 0; i = i - 3) {
                printf("%d ", i);
            }
            printf("\n");
            ''',
            "10 7 4 1",
            ["10 7 4", "10 7 4 1 -2", "7 4 1"],
            "i vale 10, 7, 4 e 1. O próximo seria -2, mas aí i > 0 já é falso.",
        ),
        erro(
            r'''
            int notas[5] = {7, 8, 6, 9, 10};
            int soma = 0;
            for (int i = 0; i <= 5; i++) {
                soma = soma + notas[i];
            }
            printf("%d\n", soma);
            ''',
            "Com i <= 5 o laço acessa notas[5], que não existe: o vetor vai de 0 a 4.",
            [
                "O for deveria começar em i = 1.",
                "soma precisa ser double para somar notas.",
                "Falta um break no fim do laço.",
            ],
            "Para percorrer um vetor de tamanho N, use i < N. O <= faz uma volta a mais, fora do vetor.",
        ),
        saida(
            r'''
            int total = 0;
            for (int i = 1; i <= 4; i++) {
                total = total + i;
            }
            printf("%d\n", total);
            ''',
            "10",
            ["4", "6", "15"],
            "O laço soma 1 + 2 + 3 + 4 = 10.",
        ),
    ],
    "break": [
        saida(
            r'''
            for (int i = 1; i <= 10; i++) {
                if (i == 4) {
                    break;
                }
                printf("%d ", i);
            }
            printf("\n");
            ''',
            "1 2 3",
            ["1 2 3 4", "1 2 3 5 6 7 8 9 10", "4"],
            "Quando i chega a 4, o break encerra o laço antes do printf.",
        ),
        saida(
            r'''
            for (int i = 1; i <= 2; i++) {
                for (int j = 1; j <= 3; j++) {
                    if (j == 2) {
                        break;
                    }
                    printf("%d%d ", i, j);
                }
            }
            printf("\n");
            ''',
            "11 21",
            ["11", "11 12 13 21 22 23", "11 13 21 23"],
            "break sai só do laço mais interno (o de j). O laço de i continua normalmente.",
        ),
        conceito(
            "Depois de um break dentro de um while, onde a execução continua?",
            "Na primeira instrução depois do while.",
            [
                "No início do while, testando a condição de novo.",
                "No fim de main, encerrando o programa.",
                "Na próxima repetição, pulando só o resto do bloco.",
            ],
            "break encerra o laço. Quem pula só o resto da repetição atual é o continue.",
        ),
        lacuna(
            r'''
            int i = 1;
            while (1) {
                if (i * i > 50) {
                    ____;
                }
                i++;
            }
            printf("%d\n", i);
            ''',
            "break",
            ["continue", "i = 0", "i--"],
            "8",
            "while (1) nunca para sozinho. O break sai do laço quando i * i passa de 50, o que acontece com i = 8.",
        ),
    ],
    "continue": [
        saida(
            r'''
            for (int i = 1; i <= 5; i++) {
                if (i == 3) {
                    continue;
                }
                printf("%d ", i);
            }
            printf("\n");
            ''',
            "1 2 4 5",
            ["1 2", "1 2 3 4 5", "1 2 4"],
            "continue pula o printf quando i é 3, mas o laço segue até 5.",
        ),
        erro(
            r'''
            int i = 0;
            while (i < 5) {
                if (i == 2) {
                    continue;
                }
                printf("%d\n", i);
                i++;
            }
            ''',
            "Quando i vale 2, o continue pula o i++ e o laço nunca termina.",
            [
                "continue não pode ser usado dentro de while.",
                "O laço para em 2, porque continue funciona como break.",
                "Falta um else depois do if.",
            ],
            "No while, a atualização fica no corpo. Se o continue pula essa linha, i fica preso em 2. No for, a "
            "atualização roda mesmo com continue.",
        ),
        conceito(
            "Qual a diferença entre break e continue?",
            "break sai do laço; continue pula só o resto da repetição atual.",
            [
                "break pula só a repetição atual; continue sai do laço.",
                "Os dois encerram o programa imediatamente, sem passar pelo resto de main.",
                "continue reinicia o laço com o contador no valor inicial.",
            ],
            "Depois de um continue, o laço segue para a próxima repetição (no for, passando pela atualização).",
        ),
        saida(
            r'''
            int soma = 0;
            for (int i = 1; i <= 6; i++) {
                if (i == 2 || i == 5) {
                    continue;
                }
                soma = soma + i;
            }
            printf("%d\n", soma);
            ''',
            "14",
            ["21", "7", "10"],
            "Os valores 2 e 5 são pulados: 1 + 3 + 4 + 6 = 14.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 7
    "criando função": [
        saida(
            r'''
            #include <stdio.h>

            void ola(void) {
                printf("Ola\n");
            }

            int main(void) {
                printf("Inicio\n");
                ola();
                ola();
                printf("Fim\n");
                return 0;
            }
            ''',
            "Inicio\nOla\nOla\nFim",
            ["Ola\nInicio\nFim", "Inicio\nOla\nFim", "Ola\nOla\nInicio\nFim"],
            "A função só roda quando é chamada, e cada chamada roda de novo. A execução começa em main.",
        ),
        erro(
            r'''
            #include <stdio.h>

            void ola(void) {
                printf("Ola\n");
            }

            int main(void) {
                ola;
                return 0;
            }
            ''',
            "Faltam os parênteses: ola; não chama a função; o certo é ola();.",
            [
                "A função deveria se chamar main2, pois só pode haver uma main.",
                "Funções void não podem ser chamadas dentro de main.",
                "Funções precisam ser chamadas com printf(ola).",
            ],
            "Sem parênteses, o nome só se refere à função, sem executá-la. O programa compila (com aviso) e não "
            "mostra nada.",
        ),
        conceito(
            "Qual a principal vantagem de transformar um trecho repetido em função?",
            "Mudar o trecho em um único lugar e reaproveitá-lo pelo nome.",
            [
                "O programa sempre fica mais rápido, porque funções são executadas antes de main.",
                "Funções não ocupam memória.",
                "Variáveis dentro de funções nunca dão erro.",
            ],
            "Com o código em um lugar só, uma correção vale para todas as chamadas, e main fica mais fácil de ler.",
        ),
        conceito(
            "O que significa cada void em `void mostrar(void)`?",
            "O primeiro: não devolve valor. O segundo: não recebe parâmetros.",
            [
                "Que a função está vazia e não executa nada quando é chamada.",
                "Que a função só pode ser chamada uma vez.",
                "Que a função limpa a tela e as variáveis antes de mostrar alguma coisa.",
            ],
            "void antes do nome é o tipo de retorno (nenhum). Entre parênteses, indica que não há parâmetros.",
        ),
    ],
    "parâmetros": [
        saida(
            r'''
            #include <stdio.h>

            void dobrar(int x) {
                x = x * 2;
            }

            int main(void) {
                int n = 5;
                dobrar(n);
                printf("%d\n", n);
                return 0;
            }
            ''',
            "5",
            ["10", "0", "25"],
            "O parâmetro x recebe uma cópia de n. Mudar x dentro da função não altera n. Para isso, a função "
            "precisaria devolver o valor ou receber um ponteiro.",
        ),
        saida(
            r'''
            #include <stdio.h>

            int diferenca(int a, int b) {
                return a - b;
            }

            int main(void) {
                int maior = 10, menor = 3;
                printf("%d\n", diferenca(menor, maior));
                return 0;
            }
            ''',
            "-7",
            ["7", "13", "3"],
            "Os argumentos vão na ordem da chamada: a recebe menor (3) e b recebe maior (10). Os nomes das variáveis "
            "não importam.",
        ),
        erro(
            r'''
            #include <stdio.h>

            int soma(int a, int b) {
                return a + b;
            }

            int main(void) {
                printf("%d\n", soma(19));
                return 0;
            }
            ''',
            "soma espera dois argumentos, mas recebeu só um.",
            [
                "Falta declarar a e b dentro de main.",
                "printf não pode receber a chamada de uma função.",
                "soma deveria ser void, porque é usada dentro do printf.",
            ],
            "A chamada precisa combinar com a assinatura: dois int, na ordem. soma(19, 23) estaria correto.",
            compila=False,
        ),
        conceito(
            "Em `int soma(int a, int b)` chamada como `soma(19, 23)`, o que são a, b, 19 e 23?",
            "19 e 23 são argumentos; a e b são parâmetros.",
            [
                "a e b são argumentos; 19 e 23 são parâmetros.",
                "19 e 23 são constantes globais; a e b são variáveis de main.",
                "a e b são os valores que a função devolve com return.",
            ],
            "Na chamada, cada argumento é copiado para o parâmetro da mesma posição.",
        ),
    ],
    "retorno": [
        saida(
            r'''
            #include <stdio.h>

            int quadrado(int n) {
                return n * n;
                printf("Calculado\n");
            }

            int main(void) {
                printf("%d\n", quadrado(4) + 1);
                return 0;
            }
            ''',
            "17",
            ["Calculado\n17", "16", "Calculado\n16"],
            "return encerra a função na hora, então o printf depois dele nunca roda. O valor 16 volta e soma 1.",
        ),
        erro(
            r'''
            #include <stdio.h>

            int sinal(int n) {
                if (n > 0) {
                    return 1;
                } else if (n < 0) {
                    return -1;
                }
            }

            int main(void) {
                printf("%d\n", sinal(0));
                return 0;
            }
            ''',
            "Quando n é 0, a função chega ao fim sem return, e o valor devolvido é indefinido.",
            [
                "Funções int não podem devolver números negativos.",
                "Não pode haver return dentro de else if.",
                "Falta void antes de int na declaração de sinal.",
            ],
            "Todos os caminhos de uma função não void precisam de return. Faltou o caso n == 0 (return 0;).",
        ),
        saida(
            r'''
            #include <stdio.h>

            int maior(int a, int b) {
                if (a > b) {
                    return a;
                }
                return b;
            }

            int main(void) {
                int m = maior(3, maior(9, 4));
                printf("%d\n", m);
                return 0;
            }
            ''',
            "9",
            ["3", "4", "16"],
            "Primeiro roda maior(9, 4), que devolve 9. Depois, maior(3, 9) devolve 9.",
        ),
        conceito(
            "O que acontece com uma função quando ela executa return?",
            "Ela termina na hora e devolve o valor para o trecho que a chamou.",
            [
                "Ela recomeça do início com o novo valor.",
                "Ela mostra o valor na tela.",
                "Ela continua até a última linha e só então devolve o valor.",
            ],
            "As linhas depois do return não rodam. Para mostrar o valor, quem chamou precisa usar printf.",
        ),
    ],
    "protótipos": [
        conceito(
            "O que o protótipo `int dobro(int n);` escrito antes de main permite?",
            "Chamar dobro antes da definição, com o compilador conferindo os tipos.",
            [
                "Executar dobro antes de main, assim que o programa começa a rodar no computador.",
                "Criar uma cópia mais rápida da função dobro.",
                "Dispensar a definição da função, porque o protótipo já basta.",
            ],
            "O protótipo informa nome, parâmetros e retorno. A implementação ainda precisa existir em algum lugar.",
        ),
        erro(
            r'''
            #include <stdio.h>

            int dobro(int n);

            int main(void) {
                printf("%d\n", dobro(21));
                return 0;
            }

            double dobro(int n) {
                return n * 2;
            }
            ''',
            "O protótipo diz que dobro devolve int, mas a definição diz double: os tipos entram em conflito.",
            [
                "Protótipos não podem ficar antes de main.",
                "Falta ponto e vírgula depois da definição de dobro.",
                "O parâmetro do protótipo deveria ter outro nome.",
            ],
            "Protótipo e definição precisam ter a mesma assinatura. O nome dos parâmetros pode mudar, mas os tipos "
            "não.",
            compila=False,
        ),
        conceito(
            "Qual protótipo combina com `double media(int a, int b) { ... }`?",
            "`double media(int a, int b);`",
            [
                "`double media(int a, int b)`, sem ponto e vírgula",
                "`media(int, int);`",
                "`int media(double a, double b);`",
            ],
            "O protótipo repete o tipo de retorno, o nome e os parâmetros, e termina com ;.",
        ),
        conceito(
            "Onde costumam ficar os protótipos que vários arquivos .c usam?",
            "Em um arquivo de cabeçalho .h, incluído com #include.",
            [
                "Dentro da função main.",
                "No fim de cada arquivo .c.",
                "Em um comentário no início do programa, para o compilador ler primeiro.",
            ],
            "O .h reúne as declarações compartilhadas, e cada .c que usa as funções o inclui.",
        ),
    ],
    "recursão": [
        saida(
            r'''
            #include <stdio.h>

            int soma_ate(int n) {
                if (n == 0) {
                    return 0;
                }
                return n + soma_ate(n - 1);
            }

            int main(void) {
                printf("%d\n", soma_ate(4));
                return 0;
            }
            ''',
            "10",
            ["4", "24", "6"],
            "soma_ate(4) = 4 + soma_ate(3) = 4 + 3 + 2 + 1 + 0 = 10. O caso-base n == 0 encerra as chamadas.",
        ),
        saida(
            r'''
            #include <stdio.h>

            void contar(int n) {
                if (n == 0) {
                    return;
                }
                contar(n - 1);
                printf("%d ", n);
            }

            int main(void) {
                contar(3);
                printf("\n");
                return 0;
            }
            ''',
            "1 2 3",
            ["3 2 1", "0 1 2 3", "3"],
            "Cada chamada só mostra seu n depois que a chamada menor termina. Por isso o 1 aparece primeiro.",
        ),
        erro(
            r'''
            #include <stdio.h>

            int potencia(int base, int expoente) {
                if (expoente == 0) {
                    return 1;
                }
                return base * potencia(base, expoente - 2);
            }

            int main(void) {
                printf("%d\n", potencia(2, 3));
                return 0;
            }
            ''',
            "Com expoente 3, a recursão passa por 3, 1, -1... e nunca chega ao caso-base 0.",
            [
                "Funções recursivas não podem ter dois parâmetros.",
                "Falta um laço for dentro da função.",
                "O caso-base deveria vir depois da chamada recursiva.",
            ],
            "Cada chamada precisa se aproximar do caso-base. Diminuindo de 2 em 2 a partir de um ímpar, o 0 é "
            "pulado e a pilha cresce até o programa falhar.",
        ),
        conceito(
            "Toda função recursiva correta precisa de quê?",
            "De um caso-base e de um passo que se aproxima dele.",
            [
                "De um laço while dentro dela.",
                "De pelo menos dois parâmetros.",
                "De uma variável global que conta as chamadas e interrompe a função no limite.",
            ],
            "Sem caso-base alcançável, as chamadas não acabam e a pilha estoura.",
        ),
    ],
    # ------------------------------------------------------------------ Módulo 8
    "arrays": [
        saida(
            r'''
            int v[4] = {3, 6, 9, 12};
            printf("%d %d\n", v[1], v[3]);
            ''',
            "6 12",
            ["3 9", "6 9", "9 12"],
            "Os índices começam em 0: v[0] é 3, v[1] é 6 e v[3] é 12.",
        ),
        saida(
            r'''
            int v[5] = {1, 2};
            printf("%d %d\n", v[1], v[4]);
            ''',
            "2 0",
            ["2 2", "1 0", "2 1"],
            "Quando a inicialização tem menos valores que o vetor, as posições restantes recebem 0.",
        ),
        conceito(
            "Em `int v[10];`, quais são o primeiro e o último índice válidos?",
            "0 e 9",
            ["1 e 10", "0 e 10", "1 e 9"],
            "Um vetor de tamanho N vai de 0 até N - 1. v[10] já está fora do vetor.",
        ),
        saida(
            r'''
            #include <stdio.h>

            void zerar(int v[], int n) {
                for (int i = 0; i < n; i++) {
                    v[i] = 0;
                }
            }

            int main(void) {
                int dados[3] = {5, 6, 7};
                zerar(dados, 3);
                printf("%d\n", dados[1]);
                return 0;
            }
            ''',
            "0",
            ["6", "5", "7"],
            "Um vetor passado para uma função não é copiado: a função recebe o endereço do primeiro elemento e "
            "altera o vetor original.",
        ),
    ],
    "matrizes": [
        saida(
            r'''
            int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
            printf("%d\n", m[1][2]);
            ''',
            "6",
            ["5", "2", "3"],
            "m[1] é a segunda linha, {4, 5, 6}, e o índice 2 dela é o 6.",
        ),
        conceito(
            "Quantos int cabem em `int m[3][4];`?",
            "12",
            ["7", "4", "20"],
            "São 3 linhas com 4 colunas cada: 3 * 4 = 12 elementos.",
        ),
        saida(
            r'''
            int m[2][2] = {{1, 2}, {3, 4}};
            int soma = 0;
            for (int i = 0; i < 2; i++) {
                soma = soma + m[i][1];
            }
            printf("%d\n", soma);
            ''',
            "6",
            ["7", "4", "10"],
            "O laço muda a linha e mantém a coluna 1: soma m[0][1] + m[1][1] = 2 + 4.",
        ),
        saida(
            r'''
            int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
            for (int i = 0; i < 2; i++) {
                for (int j = 0; j < 3; j++) {
                    printf("%d", m[i][j]);
                }
                printf("\n");
            }
            ''',
            "123\n456",
            ["14\n25\n36", "123456", "1\n2\n3\n4\n5\n6"],
            "O laço de fora percorre as linhas, o de dentro as colunas, e o \\n quebra a linha ao terminar cada "
            "uma.",
        ),
    ],
    "strings": [
        conceito(
            "Quantos char são necessários para guardar \"Ana\"?",
            "4: as 3 letras e o '\\0' no final.",
            [
                "3, uma posição por letra.",
                "5, porque toda string reserva duas posições extras.",
                "4, sendo a última para o \\n.",
            ],
            "Toda string termina com '\\0', que marca o fim do texto e também ocupa uma posição.",
        ),
        saida(
            r'''
            char nome[] = "Carla";
            printf("%c%c\n", nome[0], nome[4]);
            ''',
            "Ca",
            ["Cl", "ar", "Cr"],
            "nome[0] é 'C' e nome[4] é o último 'a' (C-a-r-l-a ocupa os índices 0 a 4).",
        ),
        saida(
            r'''
            char texto[] = "Programa";
            texto[3] = '\0';
            printf("%s\n", texto);
            ''',
            "Pro",
            ["Programa", "Prog", "Pr"],
            "%s mostra os caracteres até encontrar '\\0'. Colocar o terminador no índice 3 corta o texto ali.",
        ),
        erro(
            r'''
            char nome[3] = "Ana";
            printf("%s\n", nome);
            ''',
            "nome não tem espaço para o '\\0', então o printf com %s pode ler além do vetor.",
            [
                "Strings não podem ser inicializadas na declaração.",
                "O certo seria char nome = \"Ana\";, sem colchetes.",
                "\"Ana\" deveria estar entre aspas simples.",
            ],
            "\"Ana\" precisa de 4 posições. Com 3, o '\\0' fica de fora, e o %s não sabe onde o texto termina. Use "
            "char nome[4] ou char nome[].",
        ),
    ],
    "strlen": [
        saida(
            r'''
            char palavra[20] = "casa";
            printf("%zu %zu\n", strlen(palavra), sizeof(palavra));
            ''',
            "4 20",
            ["4 4", "5 20", "20 20"],
            "strlen conta os caracteres até o '\\0' (4). sizeof mede o vetor inteiro, que foi declarado com 20.",
            inclui=("string.h",),
        ),
        saida(
            r'''printf("%zu\n", strlen("Ola mundo"));''',
            "9",
            ["8", "10", "3"],
            "O espaço também é um caractere: O-l-a, espaço, m-u-n-d-o somam 9. O '\\0' não entra na conta.",
            inclui=("string.h",),
        ),
        saida(
            r'''
            char s[] = "abc\0def";
            printf("%zu\n", strlen(s));
            ''',
            "3",
            ["7", "8", "6"],
            "strlen para no primeiro '\\0'. O \"def\" depois dele continua no vetor, mas não conta.",
            inclui=("string.h",),
        ),
        conceito(
            "Qual especificador do printf combina com o valor devolvido por strlen?",
            "%zu",
            ["%d", "%s", "%ld"],
            "strlen devolve size_t, que se mostra com %zu. Usar %d mistura tipos diferentes.",
        ),
    ],
    "strcpy": [
        saida(
            r'''
            char destino[20] = "antigo";
            strcpy(destino, "novo");
            printf("%s\n", destino);
            ''',
            "novo",
            ["antigo", "novogo", "antigonovo"],
            "strcpy copia \"novo\" junto com o '\\0', então o texto termina logo depois do \"novo\". O resto de "
            "\"antigo\" fica no vetor, mas não aparece.",
            inclui=("string.h",),
        ),
        erro(
            r'''
            char curto[4];
            strcpy(curto, "Programar");
            printf("%s\n", curto);
            ''',
            "curto tem 4 posições e \"Programar\" precisa de 10: strcpy escreve além do vetor.",
            [
                "strcpy copia só os 4 primeiros caracteres, então o texto sai cortado.",
                "Falta o & antes de curto no strcpy.",
                "curto precisa ser preenchido com zeros antes do strcpy.",
            ],
            "strcpy não conhece o tamanho do destino e copia tudo, inclusive o '\\0'. Isso é um buffer overflow.",
            inclui=("string.h",),
        ),
        erro(
            r'''
            char nome[20];
            nome = "Ana";
            printf("%s\n", nome);
            ''',
            "Não se atribui texto a um vetor com =; o certo é strcpy(nome, \"Ana\").",
            [
                "Falta indicar o tamanho entre colchetes na atribuição.",
                "\"Ana\" deveria estar entre aspas simples.",
                "nome precisa ser declarado depois da atribuição.",
            ],
            "Vetores não podem receber atribuição depois de declarados. Para copiar texto, use strcpy (ou "
            "inicialize na declaração).",
            compila=False,
        ),
        conceito(
            "Antes de chamar `strcpy(destino, origem)`, o que é preciso conferir?",
            "Se destino tem espaço para todos os caracteres de origem e mais o '\\0' do final.",
            [
                "Se origem e destino foram declarados com exatamente o mesmo tamanho.",
                "Se destino está vazio, porque strcpy não sobrescreve texto.",
                "Nada: strcpy confere o tamanho sozinha.",
            ],
            "strcpy não faz nenhuma verificação. Quem chama precisa garantir o espaço.",
        ),
    ],
    "strcmp": [
        saida(
            r'''
            char a[] = "casa";
            char b[] = "casa";
            if (a == b) {
                printf("Iguais\n");
            } else {
                printf("Diferentes\n");
            }
            ''',
            "Diferentes",
            ["Iguais", "Iguais\nDiferentes", "casa"],
            "a == b compara os endereços dos dois vetores, que são diferentes. Para comparar o texto, use strcmp.",
        ),
        saida(
            r'''
            int r1 = strcmp("ana", "bia");
            int r2 = strcmp("bia", "ana");
            printf("%s %s\n", r1 < 0 ? "antes" : "depois", r2 < 0 ? "antes" : "depois");
            ''',
            "antes depois",
            ["depois antes", "antes antes", "depois depois"],
            "strcmp é negativo quando a primeira string vem antes na ordem alfabética, e positivo quando vem depois.",
            inclui=("string.h",),
        ),
        erro(
            r'''
            char senha[] = "1234";
            if (strcmp(senha, "1234")) {
                printf("Acesso liberado\n");
            }
            ''',
            "strcmp devolve 0 quando as strings são iguais, e 0 é falso: o if só entra quando elas são diferentes.",
            [
                "strcmp devolve 1 quando as strings são iguais, então o código está certo.",
                "Strings não podem ser comparadas com strcmp dentro de um if.",
                "Falta o & antes de senha no strcmp.",
            ],
            "Escreva strcmp(senha, \"1234\") == 0 para testar se são iguais.",
            inclui=("string.h",),
        ),
        lacuna(
            r'''
            char resposta[] = "sim";
            if (____) {
                printf("Confirmado\n");
            }
            ''',
            "strcmp(resposta, \"sim\") == 0",
            ["resposta == \"sim\"", "strcmp(resposta, \"sim\")", "strcmp(resposta, \"sim\") == 1"],
            "Confirmado",
            "Só strcmp(...) == 0 testa se os textos são iguais. == compara endereços, e strcmp sozinho é 0 (falso) "
            "quando são iguais.",
            inclui=("string.h",),
        ),
    ],
    "strcat": [
        saida(
            r'''
            char texto[30] = "Curso";
            strcat(texto, " de ");
            strcat(texto, "C");
            printf("%s\n", texto);
            ''',
            "Curso de C",
            ["C de Curso", "Curso", " de C"],
            "Cada strcat acrescenta o texto no fim do que já existe no destino.",
            inclui=("string.h",),
        ),
        erro(
            r'''
            char saudacao[6] = "Ola";
            strcat(saudacao, ", Maria");
            printf("%s\n", saudacao);
            ''',
            "saudacao tem 6 posições, mas o resultado precisa de 11: strcat escreve além do vetor.",
            [
                "strcat não pode juntar textos que têm vírgula.",
                "strcat apaga \"Ola\" antes de escrever \", Maria\".",
                "saudacao precisa ser declarada como const.",
            ],
            "\"Ola, Maria\" tem 10 caracteres e precisa de mais 1 para o '\\0'. O destino precisa caber o "
            "resultado.",
            inclui=("string.h",),
        ),
        erro(
            r'''
            char nome[20];
            strcat(nome, "Bruno");
            printf("%s\n", nome);
            ''',
            "nome não contém uma string válida (não tem '\\0'), então strcat não sabe onde começar.",
            [
                "strcat só funciona com vetores de 30 posições ou mais.",
                "\"Bruno\" deveria estar entre aspas simples.",
                "O certo seria strcat(\"Bruno\", nome).",
            ],
            "strcat procura o '\\0' do destino para começar a escrever. Inicialize com char nome[20] = \"\"; ou use "
            "strcpy.",
            inclui=("string.h",),
        ),
        conceito(
            "Para juntar \"Bom\" e \" dia\" com strcat, qual o tamanho mínimo do vetor de destino?",
            "8: os 7 caracteres de \"Bom dia\" (contando o espaço) mais o '\\0'.",
            [
                "7: um para cada caractere de \"Bom dia\".",
                "4: o tamanho de \" dia\", que é o maior dos dois.",
                "6: as letras, sem contar o espaço.",
            ],
            "O destino precisa guardar o texto todo, contando o espaço, e ainda o terminador.",
        ),
    ],
    "fgets": [
        saida(
            r'''
            char nome[20];
            fgets(nome, sizeof nome, stdin);
            printf("[%s]\n", nome);
            ''',
            "[Ana Lima\n]",
            ["[Ana Lima]", "[Ana]", "[Ana Lima ]"],
            "fgets lê a linha inteira, com espaços, e guarda também o Enter (\\n). Por isso o ] aparece na linha "
            "de baixo.",
            pergunta="Se o usuário digitar `Ana Lima` e apertar Enter, o que o programa mostra?",
            entrada="Ana Lima\n",
        ),
        lacuna(
            r'''
            char nome[20];
            fgets(nome, sizeof nome, stdin);
            nome[strcspn(nome, ____)] = '\0';
            printf("[%s]\n", nome);
            ''',
            r'"\n"',
            [r'"\0"', '" "', '"B"'],
            "[Bia]",
            "strcspn devolve a posição do primeiro \\n. Gravar '\\0' ali remove a quebra de linha que o fgets "
            "guardou.",
            pergunta="Se o usuário digitar `Bia`, o que completa a lacuna para o programa mostrar `[Bia]`?",
            inclui=("string.h",),
            entrada="Bia\n",
        ),
        conceito(
            "Por que fgets é mais segura que `scanf(\"%s\", nome)` para ler texto?",
            "Porque recebe o tamanho do vetor e nunca escreve além dele.",
            [
                "Porque remove automaticamente o Enter que o usuário digitou no final do texto.",
                "Porque converte o texto lido em número.",
                "Porque só aceita letras e recusa números.",
            ],
            "fgets lê no máximo tamanho - 1 caracteres. Mas ela não remove o \\n: isso fica por conta do programa.",
        ),
        saida(
            r'''
            int idade;
            char nome[20];
            scanf("%d", &idade);
            fgets(nome, sizeof nome, stdin);
            printf("[%s]\n", nome);
            ''',
            "[\n]",
            ["[Ana\n]", "[Ana]", "[20]"],
            "O scanf leu o 20 e deixou o Enter na entrada. O fgets encontra esse \\n e termina na hora, sem ler "
            "\"Ana\".",
            pergunta="Se o usuário digitar `20`, Enter, `Ana`, Enter, o que o programa mostra?",
            entrada="20\nAna\n",
        ),
    ],
}
