"""Aprofundamento de cada lição: passo a passo do exemplo, saída real, "Indo além" e desenho da memória.

Trechos entre crases (`assim`) aparecem como código na página. A saída de cada exemplo é
conferida por tests/test_conteudo.py, que compila e executa todos os exemplos.
"""


def _licao(passos, saida, alem, entrada=None, memoria=None):
    item = {"passos": passos, "saida": saida, "alem": alem, "entrada": entrada, "memoria": None}
    if memoria:
        legenda, linhas = memoria
        item["memoria"] = {
            "legenda": legenda,
            "linhas": [
                {"nome": nome, "endereco": endereco, "conteudo": conteudo, "observacao": observacao}
                for nome, endereco, conteudo, observacao in linhas
            ],
        }
    return item


APROFUNDAMENTO = {
    # Módulo 1 — Começando a programar
    "O que é C": _licao(
        [
            "`#include <stdio.h>` pede ao pré-processador as declarações de entrada e saída, como a de `printf`.",
            "`int main(void)` é onde a execução começa; `void` indica que main não recebe argumentos.",
            "`printf(...)` escreve o texto na tela; o `\\n` no fim pula para a próxima linha.",
            "`return 0;` avisa ao sistema operacional que o programa terminou com sucesso.",
        ],
        "C transforma codigo-fonte em programas eficientes.",
        "C foi criada por Dennis Ritchie no início dos anos 1970 para escrever o sistema Unix, e até hoje "
        "os núcleos do Linux, do Windows e do macOS têm grandes partes em C. A linguagem é padronizada pela "
        "ISO: C89, C99, C11, C17 e C23 são versões do padrão. Neste curso usamos C11, que o GCC aceita com a "
        "opção `-std=c11`. O mesmo código-fonte pode ser compilado para processadores diferentes: o que muda "
        "é o executável gerado.",
    ),
    "Estrutura básica": _licao(
        [
            "`#include <stdio.h>` traz as declarações da biblioteca padrão de entrada e saída.",
            "`int main(void) {` abre a função principal; tudo entre as chaves `{ }` faz parte dela.",
            "`int resposta = 42;` declara uma variável inteira e já guarda 42 nela; o `;` encerra a instrução.",
            "`printf(\"Resposta: %d\\n\", resposta);` troca o `%d` pelo valor de `resposta`.",
            "`return 0;` encerra main com sucesso e a `}` final fecha o bloco.",
        ],
        "Resposta: 42",
        "O compilador ignora espaços e quebras de linha extras: o programa inteiro caberia em uma linha só. "
        "A indentação existe para as pessoas enxergarem os blocos. Em C11, se main chegar à `}` sem `return`, "
        "o efeito é o mesmo de `return 0;`, mas escrever o return deixa a intenção clara. Fora das funções só "
        "ficam diretivas (`#include`, `#define`) e declarações; instruções como `printf` precisam estar "
        "dentro de uma função.",
    ),
    "Comentários": _licao(
        [
            "`// Comentario de uma linha` vale do `//` até o fim da linha.",
            "`/* ... */` pode ocupar várias linhas e termina no primeiro `*/` encontrado.",
            "Os dois comentários são removidos antes da compilação: o executável é idêntico ao de um código sem eles.",
            "Só o `printf` produz saída.",
        ],
        "Comentarios nao sao executados.",
        "Comentários de bloco não se aninham: em `/* a /* b */ c */` o comentário termina no primeiro `*/` e "
        "o ` c */` que sobra vira erro de sintaxe. Para desativar um trecho grande, use `#if 0` ... `#endif`. "
        "Um bom comentário responde \"por quê?\" (por que o limite é 100, por exemplo); o \"o quê\" o próprio "
        "código já mostra. Texto entre aspas não é comentário: `printf(\"// oi\")` imprime `// oi`.",
    ),
    "Compilação": _licao(
        [
            "O pré-processador substitui `#include <stdio.h>` pelo conteúdo do cabeçalho.",
            "O compilador traduz o C para instruções de máquina e já calcula `6 * 7`, porque é uma constante.",
            "O montador gera um arquivo objeto e o linker o junta à biblioteca que contém `printf`.",
            "Ao rodar o executável, `printf` troca `%d` por 42.",
        ],
        "Resultado compilado: 42",
        "Dá para ver cada etapa no GCC: `gcc -E programa.c` mostra o código depois do pré-processador, "
        "`gcc -S` gera o assembly, `gcc -c` gera o objeto `.o` e `gcc programa.o -o programa` faz a ligação. "
        "Erros de compilação aparecem com arquivo e linha, como `programa.c:5:20: error: ...`. Erros de "
        "ligação aparecem depois, com mensagens como `undefined reference to`, quando uma função foi "
        "declarada mas sua implementação não foi encontrada.",
    ),

    # Módulo 2 — Conversando com o usuário
    "printf": _licao(
        [
            "Cada `printf` recebe um texto entre aspas duplas.",
            "`\\n` é uma sequência de escape: não aparece na tela, apenas pula para a próxima linha.",
            "Sem o `\\n` no primeiro printf, as duas frases sairiam grudadas na mesma linha.",
            "Os printf são executados na ordem em que aparecem no código.",
        ],
        "Ola, estudante!\nEstou aprendendo C.",
        "Especificadores aceitam largura e precisão: `%5d` alinha o número em 5 colunas, `%-10s` alinha um "
        "texto à esquerda e `%08.3f` completa com zeros e mostra 3 casas. Para mostrar o próprio `%`, use "
        "`%%`; para aspas dentro do texto, `\\\"`. A saída costuma ficar guardada em um buffer e só aparece de "
        "fato na quebra de linha ou no fim do programa, por isso é bom terminar mensagens com `\\n`. printf "
        "devolve a quantidade de caracteres escritos.",
    ),
    "scanf": _licao(
        [
            "`int numero;` reserva espaço para um inteiro, ainda sem valor definido.",
            "O primeiro `printf` mostra a pergunta sem `\\n`, para o cursor ficar na mesma linha.",
            "`scanf(\"%d\", &numero);` lê um inteiro; o `&` entrega o endereço de `numero` para scanf gravar lá.",
            "O último `printf` mostra o valor que foi guardado.",
        ],
        "Digite um numero: 42\nNumero: 42",
        "scanf devolve quantos valores conseguiu ler: `scanf(\"%d\", &numero)` retorna 1 quando deu certo e 0 "
        "se a pessoa digitou letras. Conferir esse retorno é a forma correta de tratar entradas inválidas, "
        "assunto da lição de validação. `%d` pula espaços e Enter antes do número, mas `%c` não: por isso se "
        "escreve `scanf(\" %c\", &letra)`, com um espaço antes. Para ler `double` o especificador é `%lf`, "
        "diferente do printf, que usa `%f`.",
        entrada="42",
    ),

    # Módulo 3 — Guardando informações
    "int": _licao(
        [
            "`int idade = 18;` declara uma variável do tipo int chamada idade e a inicializa com 18.",
            "O nome da variável é usado depois para ler o valor guardado.",
            "`%d` é o especificador de printf para int.",
        ],
        "Idade: 18",
        "Em PCs e servidores atuais um int tem 4 bytes (32 bits) e vai de -2.147.483.648 a 2.147.483.647; os "
        "limites exatos estão em `<limits.h>` (`INT_MIN` e `INT_MAX`). Passar do limite em um int com sinal é "
        "comportamento indefinido: o resultado não é garantido. Existem variações como `short`, `long`, "
        "`long long` e as versões `unsigned`, que não guardam negativos. Para um tamanho exato, `<stdint.h>` "
        "oferece tipos como `int32_t` e `int64_t`.",
    ),
    "float e double": _licao(
        [
            "`double nota = 8.5;` guarda um número com parte decimal; o separador é ponto, não vírgula.",
            "`%.1f` mostra o valor com 1 casa decimal.",
            "No printf, o mesmo `%f` serve para float e para double.",
        ],
        "Nota: 8.5",
        "Números com vírgula são guardados em binário e muitos decimais não têm representação exata: "
        "`0.1 + 0.2` resulta em 0.30000000000000004. Por isso não compare decimais com `==`; verifique se a "
        "diferença é menor que uma tolerância, como `fabs(a - b) < 1e-9`. double tem cerca de 15 dígitos de "
        "precisão e float cerca de 7, então prefira double. O literal `8.5` já é double; `8.5f` é float.",
    ),
    "char": _licao(
        [
            "`char inicial = 'C';` guarda um único caractere; caracteres usam aspas simples.",
            "Por dentro, o char guarda um número pequeno: 'C' é 67 na tabela ASCII.",
            "`%c` mostra o caractere; com `%d` apareceria 67.",
        ],
        "Inicial: C",
        "Como char é um número, dá para fazer contas: `'A' + 1` é `'B'` e `c - '0'` transforma o dígito "
        "`'7'` no número 7. `'C'` (aspas simples) é um caractere; `\"C\"` (aspas duplas) é uma string com dois "
        "bytes, `'C'` e o terminador `'\\0'`. Letras acentuadas em UTF-8 ocupam mais de um byte e não cabem em "
        "um único char, por isso os programas do curso evitam acentos na saída. `<ctype.h>` tem funções como "
        "`toupper` e `isdigit`.",
    ),
    "constantes": _licao(
        [
            "`const int LIMITE = 100;` cria uma variável somente leitura.",
            "Qualquer tentativa de escrever `LIMITE = 200;` gera erro de compilação.",
            "O nome em maiúsculas é uma convenção para indicar um valor fixo.",
        ],
        "Limite: 100",
        "Uma const precisa ser inicializada na declaração, porque não pode receber valor depois. Diferente de "
        "`#define`, ela tem tipo, respeita escopo e aparece no depurador. Em ponteiros, a posição do const "
        "importa: `const int *p` impede alterar o valor apontado, enquanto `int *const p` impede mudar para "
        "onde p aponta. Um parâmetro `const char *texto` avisa que a função só vai ler o texto.",
    ),
    "#define": _licao(
        [
            "`#define CURSO \"C\"` cria uma macro: antes da compilação, cada `CURSO` vira `\"C\"`.",
            "Diretivas não terminam com `;`, senão o ponto e vírgula entraria na substituição.",
            "`%s` no printf mostra a string resultante.",
        ],
        "Curso: C",
        "A macro é substituição de texto e não conhece tipos. Macros com parâmetros exigem parênteses: com "
        "`#define DOBRO(x) x * 2`, a expressão `DOBRO(1 + 2)` vira `1 + 2 * 2`, que dá 5; o certo é "
        "`#define DOBRO(x) ((x) * 2)`. Use `gcc -E` para ver o código depois das substituições. Para valores "
        "com tipo, prefira `const` ou `enum`; `#define` continua útil para tamanhos de arrays e para "
        "compilação condicional com `#ifdef`.",
    ),
    "escopo": _licao(
        [
            "`fora` é declarada no bloco de main e vale até a última `}` de main.",
            "As chaves internas `{ }` criam um bloco novo; `dentro` só existe ali.",
            "Depois da `}` interna, `dentro` deixa de existir; usá-la ali seria erro de compilação.",
            "`fora` continua visível em todo o main, inclusive dentro do bloco interno.",
        ],
        "Dentro: 20\nFora: 10",
        "Variáveis locais nascem ao entrar no bloco e morrem ao sair; o valor não é preservado entre chamadas "
        "de uma função, a não ser que a variável seja `static`. Uma variável interna com o mesmo nome de uma "
        "externa a esconde (sombreamento), e o GCC avisa com `-Wshadow`. Variáveis globais, declaradas fora "
        "das funções, valem para o arquivo inteiro e começam zeradas, mas deixam o programa difícil de "
        "acompanhar: passe valores por parâmetros sempre que puder.",
    ),

    # Módulo 4 — Fazendo contas e comparações
    "soma": _licao(
        [
            "`a` e `b` guardam 19 e 23.",
            "A expressão `a + b` é calculada dentro do próprio printf, sem variável extra.",
            "O resultado, 42, substitui o `%d`.",
        ],
        "Soma: 42",
        "A soma de dois int é um int; se o resultado passar de `INT_MAX`, ocorre estouro (overflow), que em "
        "tipos com sinal é comportamento indefinido. Quando um dos lados é double, o outro é convertido e o "
        "resultado é double: `1 + 0.5` dá 1.5. O operador `+=` soma e guarda: `total += x;` é o mesmo que "
        "`total = total + x;`, muito usado para acumular valores em laços.",
    ),
    "subtração": _licao(
        [
            "`saldo` começa com 100 e `retirada` com 58.",
            "`saldo - retirada` calcula 42 sem alterar as variáveis.",
            "Para mudar o saldo de verdade seria preciso atribuir: `saldo -= retirada;`.",
        ],
        "Saldo: 42",
        "A ordem importa: `a - b` é diferente de `b - a`. O `-` também é unário: `-x` troca o sinal. Cuidado "
        "com `unsigned`: `3u - 5u` não dá -2, dá 4294967294, porque tipos sem sinal \"dão a volta\". Em regras "
        "de negócio, pense nos limites: um saque só deve acontecer se `retirada <= saldo`.",
    ),
    "multiplicação": _licao(
        [
            "`linhas` e `colunas` guardam 6 e 7.",
            "`linhas * colunas` resulta em 42 células.",
            "Entre dois valores, `*` é multiplicação; nos ponteiros o mesmo símbolo terá outro papel.",
        ],
        "Celulas: 42",
        "Multiplicação e divisão têm precedência maior que soma e subtração: `2 + 3 * 4` é 14. Use parênteses "
        "para deixar a intenção clara, como `(2 + 3) * 4`. Multiplicar ints grandes estoura rápido: "
        "`100000 * 100000` não cabe em int; converta antes com `(long long)a * b`. C não tem operador de "
        "potência: use `x * x` ou `pow` de `<math.h>`.",
    ),
    "divisão": _licao(
        [
            "`7.0 / 2.0` divide dois double, então o resultado mantém a parte decimal: 3.5.",
            "`%.2f` mostra duas casas: 3.50.",
            "Se fosse `7 / 2` (dois int), o resultado seria 3, sem a parte decimal.",
        ],
        "Resultado: 3.50",
        "Na divisão inteira o C descarta a parte decimal em direção a zero: `7 / 2` é 3 e `-7 / 2` é -3. O "
        "resto vem de `%`: `7 % 2` é 1, útil para saber se um número é par. Para obter decimal a partir de "
        "ints, converta um dos lados: `(double)soma / quantidade`. Dividir um inteiro por zero é "
        "comportamento indefinido e costuma derrubar o programa: confira o divisor antes.",
    ),
    "operadores relacionais": _licao(
        [
            "`a > b` compara 42 com 20 e produz 1 (verdadeiro).",
            "`a == b` produz 0 (falso), porque os valores são diferentes.",
            "Em C, comparações resultam em int: 1 para verdadeiro e 0 para falso.",
        ],
        "a > b: 1 | a == b: 0",
        "Não confunda `=` (atribuição) com `==` (comparação): `if (x = 5)` guarda 5 em x e é sempre "
        "verdadeiro, e o GCC avisa com `-Wall`. Comparações não se encadeiam como na matemática: `1 < x < 10` "
        "compara `(1 < x)`, que vale 0 ou 1, com 10, e dá sempre verdadeiro; escreva `x > 1 && x < 10`. "
        "Strings não se comparam com `==`: use `strcmp`. O cabeçalho `<stdbool.h>` oferece `bool`, `true` e "
        "`false`.",
    ),
    "operadores lógicos": _licao(
        [
            "`(10 > 5)` vale 1 e `(3 < 8)` vale 1.",
            "`&&` (E) só é verdadeiro quando os dois lados são verdadeiros; aqui resulta 1.",
            "O resultado é guardado em `resultado` e mostrado com `%d`.",
        ],
        "Resultado: 1",
        "`&&` e `||` avaliam da esquerda para a direita e param assim que o resultado está definido "
        "(curto-circuito): em `x != 0 && 10 / x > 2`, a divisão nem acontece quando x é 0. `!` inverte: `!0` "
        "é 1. `&&` tem precedência maior que `||`, então `a || b && c` é `a || (b && c)`; na dúvida, use "
        "parênteses. Não confunda com `&` e `|`, que operam bit a bit (módulo 15).",
    ),
    "incremento": _licao(
        [
            "`contador` começa em 40.",
            "`contador++;` soma 1 e o valor passa a 41.",
            "`++contador;` soma mais 1 e chega a 42. Sozinhas numa linha, as duas formas fazem o mesmo.",
        ],
        "42",
        "A diferença aparece dentro de expressões: `x++` devolve o valor antigo e depois incrementa; `++x` "
        "incrementa e devolve o novo. Com x = 5, `y = x++;` deixa y = 5 e x = 6, enquanto `y = ++x;` deixa os "
        "dois em 6. Nunca altere a mesma variável duas vezes na mesma expressão, como em `i = i++ + 1;`: é "
        "comportamento indefinido. `--` funciona igual, subtraindo 1.",
    ),

    # Módulo 5 — Tomando decisões
    "if": _licao(
        [
            "`temperatura` vale 31.",
            "`if (temperatura > 30)` testa a condição: 31 > 30 é verdadeiro, então o bloco entre chaves executa.",
            "Com 25 graus, a mensagem de dia quente seria pulada.",
            "O último `printf` está fora do if e executa sempre.",
        ],
        "Dia quente: beba agua\nTemperatura: 31 graus",
        "Em C, qualquer valor diferente de zero é verdadeiro: `if (quantidade)` é o mesmo que "
        "`if (quantidade != 0)`. Um `;` logo depois do parêntese, como em `if (x > 3);`, cria um if vazio e o "
        "bloco seguinte executa sempre, um erro difícil de ver. Sem chaves, só a próxima instrução pertence "
        "ao if; por isso use chaves sempre. Condições podem combinar operadores lógicos: "
        "`if (nota >= 7 && frequencia >= 75)`.",
    ),
    "else": _licao(
        [
            "`numero % 2` calcula o resto da divisão por 2; para 7, o resto é 1.",
            "A condição `numero % 2 == 0` é falsa, então o bloco do if é pulado.",
            "O `else` executa exatamente quando o if não executou.",
            "Os caminhos são exclusivos: nunca aparecem as duas mensagens.",
        ],
        "7 e impar",
        "Com ifs aninhados sem chaves, o else pertence ao if mais próximo, não ao que a indentação sugere "
        "(o chamado \"dangling else\"). Um if/else que só escolhe um valor pode virar operador ternário: "
        "`const char *tipo = numero % 2 == 0 ? \"par\" : \"impar\";`. Para negativos, `-7 % 2` é -1 em C: "
        "para testar ímpar, use `!= 0` em vez de `== 1`.",
    ),
    "else if": _licao(
        [
            "As condições são testadas de cima para baixo.",
            "`nota >= 9` é falso para 8; o teste seguinte, `nota >= 7`, é verdadeiro.",
            "Na primeira condição verdadeira, só aquele bloco executa e o resto da cadeia é pulado.",
            "O `else` final pega todos os casos que não entraram antes.",
        ],
        "Conceito B",
        "A ordem das condições importa: se `nota >= 7` viesse antes de `nota >= 9`, um 10 receberia B. "
        "Organize as faixas da mais restrita para a mais ampla. `else if` não é um comando especial: é um "
        "`else` cujo bloco é outro if. Teste as fronteiras (6, 7, 8, 9) para garantir que cada valor cai na "
        "faixa certa.",
    ),
    "switch": _licao(
        [
            "`switch (opcao)` compara o valor de `opcao` com cada `case`.",
            "Como opcao vale 2, a execução pula para `case 2:` e mostra \"Consultar\".",
            "`break` sai do switch; sem ele, a execução continuaria no case seguinte.",
            "`default` trata qualquer valor que não tenha case.",
        ],
        "Consultar",
        "switch só funciona com valores inteiros (int, char, enum) e os cases precisam ser constantes; para "
        "faixas ou strings, use if/else if. Esquecer o `break` gera \"fall-through\", às vezes intencional "
        "para agrupar casos, como `case 'a': case 'A':`. O GCC avisa sobre fall-through suspeito com "
        "`-Wextra`, e com `-Wall` avisa quando um valor de enum ficou sem case.",
    ),
    "ternário": _licao(
        [
            "`a > b ? a : b` lê-se: se a > b, use a; senão, use b.",
            "17 > 42 é falso, então a expressão vale `b`, ou seja, 42.",
            "O resultado é guardado em `maior`.",
        ],
        "Maior: 42",
        "O ternário é uma expressão (produz um valor), enquanto o if é uma instrução. Ele é ótimo para "
        "escolhas curtas, como `printf(\"%s\\n\", ok ? \"sim\" : \"nao\");`. Ternários aninhados ficam difíceis "
        "de ler: prefira if/else. Os dois resultados devem ter tipos compatíveis; se um for int e o outro "
        "double, o resultado é double.",
    ),

    # Módulo 6 — Repetindo tarefas
    "while": _licao(
        [
            "`contador` começa em 1.",
            "Antes de cada volta, o `while` testa `contador <= 3`.",
            "O corpo mostra o valor e `contador++` avança; sem essa linha o laço seria infinito.",
            "Quando contador chega a 4, a condição fica falsa e o laço termina.",
        ],
        "1\n2\n3",
        "while testa antes de executar, então o corpo pode rodar zero vezes. É o laço ideal quando não se "
        "sabe quantas repetições haverá, como ler números até a pessoa digitar 0: "
        "`while (scanf(\"%d\", &x) == 1 && x != 0)`. Se o programa travar, confira se a variável da condição "
        "muda dentro do laço. `while (1)` com um `break` interno é um padrão comum em menus.",
    ),
    "do while": _licao(
        [
            "`contador` começa em 10, que já não satisfaz `contador <= 3`.",
            "Mesmo assim o bloco do `do` executa uma vez, porque o teste só acontece no fim.",
            "Depois da volta, `contador` vale 11 e o teste falha: o laço termina.",
            "Repare no `;` depois de `while (...)`: ele é obrigatório no do while.",
        ],
        "Executou com contador = 10\nO do while roda o bloco pelo menos uma vez.",
        "do while é natural para menus e validação de entrada: mostre o menu, leia a opção e repita enquanto "
        "ela for inválida. Com um while comum, este mesmo exemplo não mostraria a primeira linha. Todo do "
        "while pode ser reescrito como while, mas às vezes isso obriga a repetir código antes do laço.",
    ),
    "for": _licao(
        [
            "`int i = 1` executa uma única vez, antes de tudo.",
            "`i <= 5` é testado antes de cada volta.",
            "O corpo acumula `soma += i` e mostra o andamento.",
            "`i++` executa ao fim de cada volta; quando i vira 6, o laço acaba.",
            "A variável `i` só existe dentro do for.",
        ],
        "i = 1, soma = 1\ni = 2, soma = 3\ni = 3, soma = 6\ni = 4, soma = 10\ni = 5, soma = 15\nTotal: 15",
        "Todo for pode ser escrito como while: `int i = 1; while (i <= 5) { ...; i++; }`. Para percorrer um "
        "array de n elementos, o padrão é `for (int i = 0; i < n; i++)`: começa em 0 e usa `<`, não `<=`, "
        "para não acessar uma posição inexistente. Qualquer parte do cabeçalho pode ficar vazia; `for (;;)` "
        "é um laço infinito. Mostrar as variáveis a cada volta, como no exemplo, é uma técnica simples de "
        "depuração.",
    ),
    "break": _licao(
        [
            "O for iria de 1 a 10.",
            "Quando `i == 6`, o `break` sai do laço imediatamente.",
            "Por isso só aparecem 1 a 5; o printf da quebra de linha executa depois do laço.",
        ],
        "1 2 3 4 5",
        "break sai apenas do laço (ou switch) mais interno. Para sair de dois laços aninhados, use uma "
        "variável de controle ou coloque o código em uma função e use return. break é útil em buscas: "
        "depois de encontrar o item, não há por que continuar percorrendo.",
    ),
    "continue": _licao(
        [
            "O for percorre i de 1 a 6.",
            "`i % 2 == 0` identifica os pares; para eles, `continue` pula o resto da volta.",
            "No for, depois do continue ainda acontece o `i++`, então o laço segue normalmente.",
            "Só os ímpares chegam ao printf.",
        ],
        "1 3 5",
        "Em um while, cuidado: se o incremento estiver depois do continue, ele é pulado e o laço pode ficar "
        "infinito. continue ajuda a descartar casos no início do corpo (\"se não serve, pula\"), evitando ifs "
        "aninhados. Muitas vezes o mesmo efeito sai com a condição invertida: `if (i % 2 != 0) printf(...)`.",
    ),

    # Módulo 7 — Organizando o código
    "criando função": _licao(
        [
            "`void mostrar_linha(void)` define uma função que não recebe dados nem devolve valor.",
            "O corpo, entre chaves, contém o printf da linha tracejada.",
            "Em main, `mostrar_linha();` chama a função: a execução entra nela, roda o corpo e volta.",
            "A mesma função é chamada duas vezes sem repetir o código.",
        ],
        "--------------------\n  Curso de C\n--------------------",
        "Uma função precisa ser declarada antes de ser chamada; aqui ela é definida acima de main. O nome "
        "deve descrever a ação, como `calcular_media` ou `mostrar_menu`. Funções curtas, com uma única "
        "responsabilidade, são mais fáceis de testar e reaproveitar. Variáveis declaradas dentro de uma "
        "função são locais a ela, e cada chamada tem as suas próprias.",
    ),
    "parâmetros": _licao(
        [
            "`tentar_alterar(valor)` envia uma cópia de 10 para o parâmetro `numero`.",
            "Dentro da função, `numero = 99` muda só a cópia: aparece 99.",
            "De volta ao main, `valor` continua 10. Isso é passagem por valor.",
            "`media(7.0, 10.0)` recebe dois parâmetros, na ordem da assinatura, e devolve 8.5.",
        ],
        "Dentro da funcao: 99\nDepois da chamada: 10\nMedia de 7 e 10: 8.5",
        "Argumento é o valor enviado na chamada; parâmetro é a variável que o recebe. Se a função precisar "
        "alterar a variável de quem chamou, ela recebe um ponteiro, como `void dobrar(int *x)` (módulo 9). "
        "Arrays parecem uma exceção: a função recebe o endereço do primeiro elemento e por isso altera o "
        "array original. Em `int f(void)` o `void` significa \"nenhum parâmetro\"; em C antigo, `int f()` "
        "significava \"parâmetros não informados\".",
    ),
    "retorno": _licao(
        [
            "`int maior(int a, int b)` promete devolver um int.",
            "Se `a > b`, o primeiro `return a;` encerra a função na hora.",
            "Caso contrário, a execução chega a `return b;`: todos os caminhos devolvem um valor.",
            "O valor devolvido pode ser guardado (`resultado`) ou usado direto numa expressão (`maior(3, 8) * 2`).",
        ],
        "Maior: 42\nDobro do maior entre 3 e 8: 16",
        "Uma função devolve um valor por vez; para devolver vários, use uma struct ou parâmetros ponteiro. "
        "Esquecer o return em uma função não void gera o aviso \"control reaches end of non-void function\", "
        "e usar esse valor é comportamento indefinido. Em funções void, `return;` sem valor encerra a função "
        "mais cedo. Nunca devolva o endereço de uma variável local: ela deixa de existir quando a função "
        "termina.",
    ),
    "protótipos": _licao(
        [
            "`int quadrado(int n);` é o protótipo: a assinatura seguida de `;`, sem corpo.",
            "Graças a ele, o compilador já conhece tipos e parâmetros quando main chama `quadrado(7)`.",
            "A definição completa aparece depois de main e precisa ter a mesma assinatura.",
        ],
        "Quadrado de 7: 49",
        "Sem o protótipo, o GCC mostra \"implicit declaration of function\": desde o C99 chamar uma função "
        "não declarada é proibido, e o GCC 14 em diante já recusa o código. "
        "Protótipos permitem deixar main no topo do arquivo e são a base dos cabeçalhos `.h`. No protótipo, "
        "os nomes dos parâmetros são opcionais (`int quadrado(int);`), mas ajudam a documentar. Se protótipo "
        "e definição divergirem, o compilador aponta \"conflicting types\".",
    ),
    "recursão": _licao(
        [
            "`fatorial(5)` chama `fatorial(4)`, que chama `fatorial(3)`, e assim por diante.",
            "O caso base `if (n <= 1) return 1;` interrompe as chamadas.",
            "Na volta, cada chamada multiplica: 2 × 1 = 2, 3 × 2 = 6, 4 × 6 = 24, 5 × 24 = 120.",
        ],
        "120",
        "Cada chamada ocupa um pedaço da pilha de execução (stack) com seus parâmetros e variáveis locais; "
        "sem caso base, ou com recursão profunda demais, a pilha estoura (stack overflow) e o programa cai. "
        "O fatorial cresce rápido: 13! já não cabe em um int de 32 bits. Toda recursão pode virar um laço; "
        "ela é mais natural em estruturas recursivas, como árvores.",
    ),

    # Módulo 8 — Listas e textos
    "arrays": _licao(
        [
            "`int valores[3] = {10, 20, 30};` reserva 3 ints seguidos na memória.",
            "Os índices vão de 0 a 2; `valores[0]` é 10.",
            "O for usa `i < 3` para visitar exatamente as posições válidas.",
        ],
        "10\n20\n30",
        "O C não confere limites: `valores[3]` lê fora do array, o que é comportamento indefinido e pode "
        "mostrar lixo, travar ou parecer funcionar. `sizeof valores / sizeof valores[0]` calcula a quantidade "
        "de elementos (só no array original, não em um parâmetro de função). Se a lista de inicialização for "
        "menor que o array, o resto é zerado: `int v[5] = {0};` zera tudo. Um array não pode ser atribuído a "
        "outro com `=`; copie elemento a elemento ou com `memcpy`.",
        memoria=(
            "Os elementos ficam lado a lado; cada int ocupa 4 bytes.",
            [
                ("valores[0]", "0x1000", "10", "primeiro elemento"),
                ("valores[1]", "0x1004", "20", "4 bytes depois"),
                ("valores[2]", "0x1008", "30", "último índice válido é 2"),
            ],
        ),
    ),
    "matrizes": _licao(
        [
            "`int matriz[2][2]` tem 2 linhas e 2 colunas; cada `{ }` interno é uma linha.",
            "`matriz[i][i]` pega os elementos da diagonal: `[0][0]` = 10 e `[1][1]` = 32.",
            "O for acumula esses valores em `diagonal`.",
        ],
        "Diagonal: 42",
        "Na memória, a matriz é guardada linha após linha: 10, 2, 3, 32 em sequência. Por isso percorrer com "
        "a linha no laço externo e a coluna no interno é mais rápido. Ao passar uma matriz para uma função, "
        "o número de colunas precisa aparecer no parâmetro: `void mostrar(int m[][2], int linhas)`.",
    ),
    "strings": _licao(
        [
            "`char texto[] = \"Linguagem C\";` cria um array com as 11 letras e mais o `'\\0'` no fim (12 bytes).",
            "O for anda pelas posições até encontrar o terminador `'\\0'`.",
            "`putchar` escreve um caractere por vez.",
        ],
        "Linguagem C",
        "Em C, string é um array de char terminado por `'\\0'`, e todas as funções de `<string.h>` dependem "
        "desse terminador. Ao declarar o tamanho, reserve espaço para ele: \"casa\" precisa de `char s[5]`. "
        "Um literal acessado por ponteiro (`char *p = \"texto\";`) fica em memória somente leitura: altere "
        "apenas strings guardadas em arrays. `printf(\"%s\", texto)` imprime tudo até o `'\\0'`.",
        memoria=(
            "Cada caractere ocupa 1 byte; o terminador marca o fim.",
            [
                ("texto[0]", "0x1000", "'L'", ""),
                ("texto[1]", "0x1001", "'i'", ""),
                ("...", "...", "...", "as outras letras"),
                ("texto[10]", "0x100A", "'C'", "última letra"),
                ("texto[11]", "0x100B", "'\\0'", "terminador (valor 0)"),
            ],
        ),
    ),
    "strlen": _licao(
        [
            "`strlen` vem de `<string.h>`.",
            "Ela conta os caracteres até o `'\\0'`, sem contar o terminador: \"compilar\" tem 8.",
            "O retorno é `size_t`, mostrado com `%zu`.",
        ],
        "Tamanho: 8",
        "`sizeof palavra` daria 9, porque inclui o `'\\0'`, enquanto `strlen(palavra)` dá 8. strlen percorre a "
        "string inteira a cada chamada; em `for (i = 0; i < strlen(s); i++)` ela é recalculada em toda volta, "
        "então guarde o tamanho numa variável antes. Sem `'\\0'`, strlen continua lendo memória além do "
        "array. Em UTF-8, uma letra acentuada conta como 2 bytes.",
    ),
    "strcpy": _licao(
        [
            "`char destino[20];` reserva 20 bytes.",
            "`strcpy(destino, \"C seguro\")` copia as 8 letras e o `'\\0'` (9 bytes), que cabem com folga.",
            "Strings não podem ser atribuídas com `=`; a cópia precisa de strcpy.",
        ],
        "C seguro",
        "strcpy não sabe o tamanho do destino: se a origem for maior, ela escreve além do array (buffer "
        "overflow), uma das falhas de segurança mais comuns. Confira antes com "
        "`strlen(origem) < sizeof destino` ou use `snprintf(destino, sizeof destino, \"%s\", origem)`, que "
        "sempre respeita o limite e termina com `'\\0'`. `strncpy` parece segura, mas não coloca o `'\\0'` "
        "quando a origem é longa demais.",
    ),
    "strcmp": _licao(
        [
            "`strcmp(a, b)` compara as strings letra por letra.",
            "Devolve 0 quando são iguais, um número negativo se a vem antes e positivo se vem depois.",
            "Por isso o teste é `strcmp(a, b) == 0`.",
        ],
        "Iguais",
        "`a == b` compara endereços, não o conteúdo: dois arrays com o mesmo texto têm endereços diferentes. "
        "A comparação segue os códigos dos caracteres, então maiúsculas vêm antes de minúsculas "
        "(\"Zebra\" vem antes de \"abelha\"). Não teste `strcmp(...) == 1`: o padrão só garante o sinal, não o "
        "valor. `strncmp(a, b, n)` compara só os n primeiros caracteres.",
    ),
    "strcat": _licao(
        [
            "`destino` começa com \"Curso \" e tem 30 bytes no total.",
            "`strcat` procura o `'\\0'` de destino e copia \"de C\" a partir dali.",
            "O resultado, \"Curso de C\", usa 11 bytes, dentro do limite.",
        ],
        "Curso de C",
        "O destino precisa de espaço para as duas partes e o `'\\0'`: "
        "`strlen(destino) + strlen(origem) + 1 <= sizeof destino`. strcat também exige que o destino já seja "
        "uma string válida, terminada em `'\\0'`; um array não inicializado quebra a função. Para montar textos "
        "com números, `snprintf` é mais simples e seguro: `snprintf(buf, sizeof buf, \"Nota: %d\", n);`.",
    ),
    "fgets": _licao(
        [
            "`fgets(nome, sizeof(nome), stdin)` lê a linha inteira, inclusive espaços, sem passar de 40 bytes.",
            "Se a leitura falhar (fim da entrada), fgets devolve NULL e o if pula o bloco.",
            "fgets guarda também o `'\\n'` do Enter; `strcspn(nome, \"\\n\")` acha a posição dele.",
            "Trocar esse `'\\n'` por `'\\0'` remove a quebra de linha do nome.",
        ],
        "Nome: Ana\nOla, Ana",
        "Diferente de `scanf(\"%s\")`, fgets lê nomes compostos como \"Ana Maria\" e nunca ultrapassa o tamanho "
        "informado. Se a linha for maior que o array, o restante fica esperando para a próxima leitura. Um "
        "padrão robusto para números é ler a linha com fgets e converter com `strtol`, conferindo se a linha "
        "toda foi usada. Nunca use `gets`: ela foi removida do C11 por não ter limite.",
        entrada="Ana",
    ),

    # Módulo 9 — Como a memória funciona
    "memória": _licao(
        [
            "Cada variável ocupa um número de bytes definido pelo seu tipo.",
            "`sizeof` informa esse tamanho sem ler o valor; o resultado é `size_t`, mostrado com `%zu`.",
            "Um array ocupa a soma dos elementos: 5 ints × 4 bytes = 20 bytes.",
        ],
        "int: 4 bytes\ndouble: 8 bytes\nchar: 1 byte\narray de 5 int: 20 bytes",
        "Os tamanhos de int e double podem variar entre plataformas; o padrão só garante mínimos e que "
        "`sizeof(char)` é 1. A saída acima é a de um PC de 64 bits comum. Variáveis locais ficam na pilha "
        "(stack) e somem no fim da função; memória pedida com malloc fica no heap até o free. O compilador "
        "pode deixar espaços entre variáveis para alinhá-las, então os endereços nem sempre ficam colados.",
        memoria=(
            "Cada tipo ocupa uma quantidade diferente de bytes.",
            [
                ("idade", "0x1000", "20", "int: 4 bytes"),
                ("nota", "0x1008", "8.5", "double: 8 bytes"),
                ("letra", "0x1010", "'C'", "char: 1 byte"),
                ("notas", "0x1014", "0 0 0 0 0", "5 × int = 20 bytes"),
            ],
        ),
    ),
    "operador &": _licao(
        [
            "`&valor` produz o endereço onde `valor` está guardado.",
            "`int *ponteiro = &valor;` guarda esse endereço em um ponteiro para int.",
            "`*ponteiro` segue o endereço e lê o valor que está lá: 42.",
        ],
        "Valor: 42",
        "Para ver o endereço real, use `printf(\"%p\\n\", (void *)&valor);`; o número muda a cada execução "
        "porque o sistema sorteia as posições de memória (ASLR). O `*` tem dois papéis: na declaração "
        "(`int *p`) indica \"ponteiro para int\"; numa expressão (`*p`) acessa o valor apontado. É por isso "
        "que `scanf(\"%d\", &x)` precisa do `&`: scanf recebe o endereço de x para gravar nele.",
        memoria=(
            "O ponteiro guarda o endereço de outra variável.",
            [
                ("valor", "0x1000", "42", "int"),
                ("ponteiro", "0x1008", "0x1000", "aponta para valor; *ponteiro vale 42"),
            ],
        ),
    ),
    "ponteiros + funções": _licao(
        [
            "`trocar(&a, &b)` envia os endereços de a e b, não cópias dos valores.",
            "Dentro da função, `*a` e `*b` acessam as variáveis originais do main.",
            "`temporario` guarda 10, `*a` recebe 42 e `*b` recebe o 10 guardado.",
            "De volta ao main, os valores estão trocados.",
        ],
        "42 10",
        "Com passagem por valor, `void trocar(int a, int b)`, a troca aconteceria só nas cópias e main não "
        "veria diferença. Ponteiros também permitem \"devolver\" vários resultados: "
        "`void dividir(int a, int b, int *quociente, int *resto)`. Quando uma função recebe ponteiro, confira "
        "se ele pode ser NULL. Se a função só lê, use `const int *` para deixar isso explícito.",
        memoria=(
            "Os parâmetros de trocar guardam endereços das variáveis de main.",
            [
                ("a (main)", "0x1000", "10 → 42", "alterada através do ponteiro"),
                ("b (main)", "0x1004", "42 → 10", "alterada através do ponteiro"),
                ("a (trocar)", "0x2000", "0x1000", "ponteiro para o a de main"),
                ("b (trocar)", "0x2008", "0x1004", "ponteiro para o b de main"),
                ("temporario", "0x2010", "10", "cópia usada na troca"),
            ],
        ),
    ),
    "ponteiros + arrays": _licao(
        [
            "`int *p = valores;`: o nome do array vira o endereço do primeiro elemento.",
            "`p + i` avança i elementos, não i bytes; o compilador multiplica pelo tamanho do int.",
            "`*(p + i)` é exatamente o mesmo que `p[i]` e que `valores[i]`.",
            "O laço soma 10 + 20 + 12.",
        ],
        "42",
        "Array e ponteiro não são a mesma coisa: `sizeof valores` é 12 (o array inteiro) e `sizeof p` é 8 "
        "(o tamanho de um endereço). Ao passar um array para uma função, ela recebe só o ponteiro, por isso o "
        "tamanho precisa ir junto como parâmetro. Aritmética de ponteiros só é válida dentro do array (e até "
        "uma posição depois do fim, sem ler nela).",
        memoria=(
            "p + i aponta para o elemento i do array.",
            [
                ("valores[0]", "0x1000", "10", "p aponta aqui"),
                ("valores[1]", "0x1004", "20", "p + 1"),
                ("valores[2]", "0x1008", "12", "p + 2"),
                ("p", "0x1010", "0x1000", "endereço do primeiro elemento"),
            ],
        ),
    ),
    "ponteiro para ponteiro": _licao(
        [
            "`p` guarda o endereço de `valor`.",
            "`pp` guarda o endereço de `p`; por isso o tipo tem dois asteriscos.",
            "`*pp` é `p`, e `**pp` é `valor`; `**pp = 42` altera valor.",
        ],
        "42",
        "Ponteiros duplos aparecem quando uma função precisa alterar um ponteiro de quem a chamou, por "
        "exemplo para alocar memória: `void criar(int **saida) { *saida = malloc(sizeof **saida); }`. Também "
        "representam listas de strings, como `char **argv` em `int main(int argc, char **argv)`, que recebe "
        "os argumentos da linha de comando. Ao ler `**`, desenhe caixas e setas: cada asterisco é uma seta a "
        "seguir.",
        memoria=(
            "Cada nível guarda o endereço do anterior.",
            [
                ("valor", "0x1000", "10 → 42", "alterado por **pp"),
                ("p", "0x1008", "0x1000", "aponta para valor"),
                ("pp", "0x1010", "0x1008", "aponta para p"),
            ],
        ),
    ),

    # Módulo 10 — Usando memória quando precisar
    "malloc": _licao(
        [
            "`malloc(sizeof(int))` pede espaço para um int no heap e devolve o endereço.",
            "`if (numero == NULL) return 1;` trata o caso raro em que não há memória disponível.",
            "`*numero = 30` grava no espaço reservado.",
            "`free(numero)` devolve a memória quando ela não é mais necessária.",
        ],
        "30",
        "O conteúdo inicial do bloco é lixo; use calloc se precisar dele zerado. Escrever `sizeof *numero` em "
        "vez de `sizeof(int)` continua certo mesmo se o tipo do ponteiro mudar. Em C não é preciso converter "
        "o retorno: `int *p = malloc(...)` já funciona. A grande vantagem é decidir o tamanho durante a "
        "execução: `malloc(n * sizeof *v)` cria um array com n elementos escolhidos pelo usuário.",
        memoria=(
            "O ponteiro fica na pilha; o bloco reservado fica no heap.",
            [
                ("numero", "0x1000 (pilha)", "0x5000", "endereço devolvido por malloc"),
                ("bloco", "0x5000 (heap)", "30", "existe até o free"),
            ],
        ),
    ),
    "calloc": _licao(
        [
            "`calloc(4, sizeof(*valores))` reserva 4 ints e zera todos os bytes.",
            "O teste `valores == NULL` trata a falta de memória.",
            "Só `valores[3]` recebe 42; os demais continuam 0.",
            "`free(valores)` libera o bloco inteiro de uma vez.",
        ],
        "0 0 0 42",
        "calloc recebe quantidade e tamanho separados e confere se a multiplicação estoura, o que "
        "`malloc(n * tamanho)` não faz. Zerar custa um pouco de tempo, então use calloc quando precisar do "
        "conteúdo inicial zerado, como contadores. O bloco se usa como array (`valores[i]`), mas "
        "`sizeof valores` dá o tamanho do ponteiro, não do bloco: guarde a quantidade em uma variável.",
        memoria=(
            "calloc entrega o bloco já zerado.",
            [
                ("valores", "0x1000 (pilha)", "0x5000", "ponteiro para o bloco"),
                ("valores[0]", "0x5000 (heap)", "0", "zerado por calloc"),
                ("valores[1]", "0x5004 (heap)", "0", ""),
                ("valores[2]", "0x5008 (heap)", "0", ""),
                ("valores[3]", "0x500C (heap)", "42", "único valor gravado"),
            ],
        ),
    ),
    "realloc": _licao(
        [
            "O bloco começa com espaço para 2 ints.",
            "`realloc(valores, 3 * sizeof(*valores))` pede para aumentar para 3; o bloco pode mudar de endereço.",
            "O resultado vai para `temporario`: se falhar (NULL), o bloco antigo continua válido e é liberado.",
            "Só depois do sucesso vem `valores = temporario`, e aí as três posições podem ser usadas.",
        ],
        "42",
        "Nunca escreva `v = realloc(v, ...)`: se realloc falhar, devolve NULL, você perde o único endereço do "
        "bloco antigo e cria um vazamento. Quando o bloco muda de lugar, realloc copia os dados e libera o "
        "endereço anterior, então qualquer outro ponteiro para o bloco antigo fica inválido. Para listas que "
        "crescem, dobre a capacidade a cada realloc em vez de aumentar de 1 em 1: fica muito mais rápido.",
    ),
    "free": _licao(
        [
            "O bloco é alocado, verificado e usado normalmente.",
            "`free(valor)` devolve a memória ao sistema.",
            "`valor = NULL` evita usar o endereço antigo por engano (ponteiro pendente).",
        ],
        "42",
        "Depois do free, o ponteiro ainda guarda o endereço antigo, mas o bloco não é mais seu: ler ou "
        "escrever ali (use-after-free) é comportamento indefinido. Liberar duas vezes (double free) também, e "
        "costuma derrubar o programa. `free(NULL)` é permitido e não faz nada, por isso zerar o ponteiro deixa "
        "um segundo free inofensivo. Só passe para free endereços vindos de malloc, calloc ou realloc.",
        memoria=(
            "Depois do free o bloco não pode mais ser usado.",
            [
                ("valor", "0x1000 (pilha)", "0x5000 → NULL", "zerado depois do free"),
                ("bloco", "0x5000 (heap)", "42 → (liberado)", "devolvido ao sistema"),
            ],
        ),
    ),
    "memory leak": _licao(
        [
            "`executar` aloca um int, usa e copia o valor para uma variável local comum.",
            "Antes de retornar, faz `free(valor)`: todo malloc tem seu free no mesmo caminho.",
            "A função devolve o número (uma cópia), não o ponteiro, então nada fica pendente.",
        ],
        "42",
        "Um vazamento acontece quando o último ponteiro para um bloco se perde sem free, por exemplo num "
        "return antecipado. Em programas curtos o sistema recupera tudo no fim, mas servidores e jogos que "
        "rodam por horas vão consumindo memória até travar. Ferramentas como o Valgrind "
        "(`valgrind --leak-check=full ./programa`) ou a opção `-fsanitize=address` do GCC apontam a linha de "
        "cada bloco não liberado. `static` na função indica que ela só é visível neste arquivo.",
    ),

    # Módulo 11 — Agrupando informações
    "structs": _licao(
        [
            "`struct Aluno { ... };` define um novo tipo com três campos.",
            "`struct Aluno aluno = {\"Ana\", 20, 8.5};` preenche os campos na ordem da declaração.",
            "`aluno.idade = 21;` altera um campo usando ponto.",
            "`p->idade` acessa o campo através do ponteiro; é o mesmo que `(*p).idade`.",
        ],
        "Ana, 21 anos, media 8.5",
        "Structs podem ser copiadas com `=` e passadas para funções por valor, mas isso copia todos os bytes; "
        "para structs grandes, passe um ponteiro (`const struct Aluno *a`). Inicializadores designados deixam "
        "a ordem explícita: `{.nome = \"Ana\", .media = 8.5}`, e os campos omitidos ficam zerados. O `sizeof` "
        "de uma struct pode ser maior que a soma dos campos por causa do alinhamento. Structs não se comparam "
        "com `==`: compare campo a campo.",
    ),
    "typedef": _licao(
        [
            "`typedef unsigned int Contador;` cria o apelido Contador para unsigned int.",
            "`typedef struct { ... } Ponto;` dá nome a uma struct e dispensa escrever `struct` antes.",
            "`visitas` e `p` usam os apelidos como se fossem tipos comuns.",
        ],
        "Visitas: 3\nPonto: (2.5, -1.0)",
        "typedef não cria um tipo novo: Contador e unsigned int são intercambiáveis e o compilador não impede "
        "misturar os dois. Uma struct que aponta para si mesma, como o nó de uma lista, precisa de nome: "
        "`typedef struct No { int v; struct No *prox; } No;`. Muitos projetos evitam typedef de ponteiros "
        "(`typedef int *IntPtr;`), porque esconde o `*` e confunde a leitura. A biblioteca padrão usa typedef "
        "em tipos como `size_t` e `FILE`.",
    ),
    "unions": _licao(
        [
            "`union Valor` tem dois membros que ocupam o mesmo espaço de memória.",
            "`v.inteiro = 10;` grava no espaço compartilhado, e inteiro passa a ser o membro ativo.",
            "Ler `v.decimal` agora interpretaria os mesmos bytes como float e mostraria outro número.",
        ],
        "10",
        "O tamanho de uma union é o do seu maior membro. O uso típico é a \"união marcada\": uma struct com uma "
        "enum dizendo qual membro está ativo e a union com os dados, como "
        "`struct Token { enum Tipo tipo; union { int i; double d; } valor; };`. Isso economiza memória quando "
        "só uma alternativa existe por vez. Ler um membro diferente do último gravado reinterpreta os bytes e "
        "depende da plataforma.",
        memoria=(
            "Os membros começam no mesmo endereço.",
            [
                ("v.inteiro", "0x1000", "10", "membro ativo (4 bytes)"),
                ("v.decimal", "0x1000", "mesmos bytes", "mesmo endereço de v.inteiro"),
            ],
        ),
    ),
    "enum": _licao(
        [
            "`enum Status {ABERTO, FECHADO};` cria constantes: ABERTO vale 0 e FECHADO vale 1.",
            "`enum Status atual = ABERTO;` guarda o estado com um nome legível.",
            "Por baixo é um inteiro, por isso `%d` mostra 0.",
        ],
        "0",
        "Os valores podem ser escolhidos: `enum Mes {JAN = 1, FEV, MAR};` faz FEV valer 2. enum combina bem "
        "com switch: com `-Wall`, o GCC avisa se algum valor ficou sem case. Para mostrar o nome em vez do "
        "número, use um array de strings indexado pela enum: `const char *nomes[] = {\"ABERTO\", \"FECHADO\"};`. "
        "O C não impede atribuir qualquer inteiro a uma variável enum, então valide valores vindos de fora.",
    ),

    # Módulo 12 — Salvando dados
    "fopen": _licao(
        [
            "`fopen(\"dados.txt\", \"w\")` abre o arquivo para escrita; se ele não existir, é criado.",
            "O retorno é um `FILE *`; NULL indica falha (sem permissão, pasta inexistente...).",
            "Depois de usar, `fclose` fecha o arquivo.",
        ],
        "Arquivo aberto",
        "Modos principais: \"r\" lê (o arquivo precisa existir), \"w\" escreve apagando o conteúdo anterior e "
        "\"a\" acrescenta no fim. Com \"+\" (como \"r+\") o arquivo permite ler e escrever, e com \"b\" (\"rb\") "
        "abre em modo binário. Para saber por que falhou, use `perror(\"dados.txt\")`, que mostra a mensagem "
        "do sistema. O caminho é relativo à pasta onde o programa está rodando, não à pasta do código-fonte.",
    ),
    "fclose": _licao(
        [
            "O arquivo é aberto e recebe o número 42 com fprintf.",
            "`fclose(arquivo)` grava o que estava no buffer e libera o arquivo.",
            "fclose devolve 0 quando tudo deu certo, por isso o teste `== 0`.",
        ],
        "Arquivo fechado",
        "A escrita em arquivo passa por um buffer na memória; sem fclose (ou fflush), parte dos dados pode não "
        "chegar ao disco se o programa cair. Cada arquivo aberto consome um recurso do sistema, que tem um "
        "limite de arquivos abertos ao mesmo tempo. Depois de fechado, o `FILE *` não pode mais ser usado. "
        "Não chame fclose com NULL: confira o fopen primeiro.",
    ),
    "fprintf": _licao(
        [
            "fprintf funciona como printf, mas o primeiro argumento diz para onde escrever.",
            "`fprintf(arquivo, \"Resposta: %d\\n\", 42)` grava a linha em resultado.txt, não na tela.",
            "O printf final só confirma na tela que a gravação aconteceu.",
        ],
        "Gravado",
        "`fprintf(stdout, ...)` é igual a printf, e `fprintf(stderr, ...)` escreve na saída de erros, própria "
        "para mensagens que não devem se misturar com os resultados. Para gravar dados fáceis de ler depois, "
        "use um formato fixo, como um registro por linha e campos separados por `;` (formato CSV). fprintf "
        "devolve um número negativo se a escrita falhar.",
    ),
    "fscanf": _licao(
        [
            "Primeiro o programa cria numeros.txt com o texto \"19 23\".",
            "Depois reabre o arquivo em modo \"r\" para leitura.",
            "`fscanf(arquivo, \"%d %d\", &a, &b)` lê dois inteiros e devolve 2 quando os dois foram lidos.",
            "Só então a soma 42 é mostrada.",
        ],
        "42",
        "Para ler um arquivo inteiro, repita enquanto a leitura der certo: "
        "`while (fscanf(arq, \"%d\", &x) == 1) { ... }`. Evite `while (!feof(arq))`: feof só fica verdadeiro "
        "depois que uma leitura falha, e o último valor acaba processado duas vezes. Para linhas de texto com "
        "espaços, prefira fgets e depois `sscanf`.",
    ),

    # Módulo 13 — Dividindo o programa em partes
    ".h": _licao(
        [
            "O bloco de protótipos representa o conteúdo de calculos.h: só declarações.",
            "main usa `dobro` e `metade` conhecendo apenas as assinaturas.",
            "As definições, que ficariam em calculos.c, aparecem no fim.",
            "Em um projeto real, main.c teria `#include \"calculos.h\"` no lugar dos protótipos.",
        ],
        "42 42",
        "`#include \"arquivo.h\"` (aspas) procura primeiro na pasta do projeto; `#include <arquivo.h>` procura "
        "nas pastas do sistema. Um cabeçalho deve ter só declarações: se tiver a definição de uma função, "
        "incluí-lo em dois .c gera \"multiple definition\" no linker. Para compartilhar uma variável global, "
        "declare `extern int total;` no .h e defina `int total;` em um único .c.",
    ),
    ".c": _licao(
        [
            "O protótipo `int triplo(int valor);` avisa ao compilador como chamar a função.",
            "main chama `triplo(14)`.",
            "A implementação poderia estar em outro arquivo .c, compilado separadamente.",
        ],
        "42",
        "Com vários arquivos, o comando fica `gcc main.c calculos.c -o programa`, ou em etapas: "
        "`gcc -c calculos.c` gera calculos.o e `gcc main.o calculos.o -o programa` liga tudo. Assim, ao mudar "
        "um arquivo, só ele precisa ser recompilado. Funções usadas apenas dentro de um .c devem ser `static`, "
        "o que as esconde dos outros arquivos e evita conflitos de nomes.",
    ),
    "include guards": _licao(
        [
            "`#ifndef MATEMATICA_H` pergunta: essa macro ainda não foi definida?",
            "Na primeira vez não foi, então `#define MATEMATICA_H` a define e o protótipo entra no código.",
            "Se o cabeçalho fosse incluído de novo, o `#ifndef` seria falso e tudo até `#endif` seria pulado.",
        ],
        "42",
        "Guards evitam erros de redefinição quando um cabeçalho chega por vários caminhos (a.h inclui b.h e "
        "main.c inclui os dois). O nome da macro precisa ser único no projeto; em geral é o nome do arquivo "
        "em maiúsculas. Muitos compiladores aceitam `#pragma once`, mais curto, mas ele não faz parte do "
        "padrão C.",
    ),

    # Módulo 14 — Usando recursos prontos
    "stdio": _licao(
        [
            "stdio.h declara as funções de entrada e saída e as correntes padrão.",
            "`stdout` é a saída padrão (a tela); `fprintf(stdout, ...)` é igual a printf.",
        ],
        "Saida padrao: 42",
        "Três correntes já vêm abertas: stdin (teclado), stdout (tela) e stderr (erros). No terminal, a saída "
        "pode ser redirecionada: `./programa > saida.txt` grava o stdout em arquivo, enquanto o stderr "
        "continua na tela. Outras funções úteis: `puts` (texto e quebra de linha), `putchar` e `getchar` (um "
        "caractere), `snprintf` (formata dentro de uma string) e `sscanf` (lê de uma string).",
    ),
    "stdlib": _licao(
        [
            "`strtol(texto, &fim, 10)` converte o texto \"42\" para número na base 10.",
            "Ao terminar, `fim` aponta para o primeiro caractere que não foi convertido.",
            "`*fim == '\\0'` confirma que o texto inteiro era um número válido.",
        ],
        "42",
        "`atoi` também converte, mas devolve 0 tanto para \"abc\" quanto para \"0\", sem diferenciar; strtol "
        "permite detectar o erro. stdlib.h traz ainda malloc e free, `rand` e `srand` (números "
        "pseudoaleatórios), `abs`, `qsort` (ordenação de qualquer tipo), `exit` e as constantes "
        "`EXIT_SUCCESS` e `EXIT_FAILURE`, que podem substituir 0 e 1 no return de main.",
    ),
    "string": _licao(
        [
            "`strcpy` coloca \"C\" em texto; `strcat` acrescenta \"11\".",
            "`strcmp(texto, \"C11\") == 0` confirma que o resultado é \"C11\".",
            "O ternário escolhe a palavra \"correto\" ou \"erro\" para o printf.",
        ],
        "C11: correto",
        "Além das funções de texto, string.h tem funções de memória: `memset` preenche bytes "
        "(`memset(v, 0, sizeof v)` zera um array), `memcpy` copia blocos e `memcmp` compara bytes. `strchr` e "
        "`strstr` procuram um caractere ou um trecho dentro de uma string e devolvem um ponteiro para a "
        "posição encontrada, ou NULL.",
    ),
    "math": _licao(
        [
            "`#include <math.h>` declara sqrt e outras funções matemáticas.",
            "`sqrt(25)` devolve o double 5.0.",
            "`%.0f` mostra sem casas decimais: 5.",
        ],
        "5",
        "Com GCC, programas que usam math.h podem precisar de `-lm` no fim do comando para ligar a biblioteca "
        "matemática; o compilador do site já usa essa opção. Outras funções: `pow(base, expoente)`, `fabs` "
        "(valor absoluto de double), `floor` e `ceil` (arredondar para baixo e para cima), `round`, `sin` e "
        "`cos` (ângulos em radianos). A raiz de um número negativo resulta em NaN (\"não é um número\").",
    ),

    # Módulo 15 — Como o computador guarda informações
    "bitwise": _licao(
        [
            "21 em binário é 10101.",
            "`valor << 1` desloca todos os bits uma posição para a esquerda: 101010, que é 42.",
            "Deslocar 1 bit para a esquerda equivale a multiplicar por 2.",
            "`unsigned` e `%u` evitam problemas com o bit de sinal.",
        ],
        "42",
        "Os operadores bit a bit são `&` (E), `|` (OU), `^` (OU exclusivo), `~` (inverte todos os bits) e os "
        "deslocamentos `<<` e `>>`. `x >> 1` divide por 2 descartando o resto, e `x & 1` diz se x é ímpar. "
        "Prefira tipos unsigned: deslocar números negativos, ou deslocar mais bits do que o tipo tem, é "
        "comportamento indefinido ou depende do compilador.",
    ),
    "máscaras": _licao(
        [
            "Cada permissão é um bit: LER = 001, ESCREVER = 010 e EXECUTAR = 100, em binário.",
            "`LER | EXECUTAR` liga os dois bits: 101.",
            "`permissoes & EXECUTAR` isola o bit de execução; se não for zero, a permissão existe.",
        ],
        "Pode executar",
        "As quatro operações com máscaras: ligar (`flags |= BIT`), desligar (`flags &= ~BIT`), inverter "
        "(`flags ^= BIT`) e testar (`(flags & BIT) != 0`). As permissões de arquivos do Linux (rwx, como em "
        "`chmod 755`) usam exatamente essa ideia. Um único unsigned de 32 bits guarda 32 opções de liga e "
        "desliga.",
    ),

    # Módulo 16 — Encontrando e corrigindo erros
    "erros de sintaxe": _licao(
        [
            "Este exemplo é a versão correta: cada instrução termina com `;` e as chaves estão balanceadas.",
            "Apague o `;` depois de `int resposta = 42` e compile: o GCC reclama com \"expected ',' or ';' before 'printf'\".",
            "Corrija só o primeiro erro e compile de novo: os seguintes muitas vezes somem.",
        ],
        "42",
        "As mensagens do GCC seguem o formato `arquivo:linha:coluna: error: descrição`. As mais comuns: "
        "\"expected ';'\" (falta ponto e vírgula, geralmente no fim da linha anterior), \"expected declaration "
        "or statement at end of input\" (falta fechar uma `}`), \"undeclared\" (variável não declarada ou nome "
        "digitado errado) e \"implicit declaration of function\" (falta um #include ou protótipo). A Consulta "
        "rápida do site tem uma tabela com essas mensagens.",
    ),
    "erros lógicos": _licao(
        [
            "O programa compila sem erro, mas isso não garante que o cálculo esteja certo.",
            "Os parênteses em `(8.0 + 10.0 + 12.0) / 3.0` fazem a soma antes da divisão.",
            "Sem eles, só 12.0 seria dividido por 3 e a média sairia 22.00: um erro lógico.",
        ],
        "10.00",
        "Erros lógicos só aparecem testando: calcule à mão o resultado esperado de alguns casos e compare com "
        "a saída. Os clássicos são precedência de operadores, divisão inteira (`7 / 2` dá 3), laço que roda "
        "uma vez a mais ou a menos (`<=` no lugar de `<`) e `=` no lugar de `==`. Casos de fronteira, como 0, "
        "negativos e lista vazia, revelam boa parte deles.",
    ),
    "debug": _licao(
        [
            "O laço soma os valores do array.",
            "O printf dentro do laço mostra i e total a cada volta: é um rastreio da execução.",
            "Assim dá para ver em qual volta um valor começa a sair errado.",
        ],
        "i=0 total=10\ni=1 total=30\ni=2 total=42",
        "Depois de achar o problema, remova os printf de depuração ou use `fprintf(stderr, ...)` para separá-los "
        "da saída normal. Para investigar sem mudar o código, use um depurador: compile com "
        "`gcc -g programa.c -o programa` e rode `gdb ./programa`; os comandos `break main`, `next`, "
        "`print total` e `continue` percorrem o programa linha a linha. A opção `-fsanitize=address,undefined` "
        "detecta acessos inválidos no momento em que acontecem.",
    ),

    # Módulo 17 — Transformando código em programa
    "gcc": _licao(
        [
            "O código é simples; o assunto da lição é o comando que o compila.",
            "`gcc -std=c11 -Wall -Wextra -pedantic programa.c -o programa` compila em C11 com avisos extras.",
            "`-o programa` escolhe o nome do executável; sem ele, o GCC gera `a.out`.",
        ],
        "Programa C11 compilado com avisos habilitados.",
        "Outras opções úteis: `-g` (informações para o depurador), `-O2` (otimiza o executável), `-Werror` "
        "(trata avisos como erros), `-fsanitize=address` (detecta erros de memória durante a execução) e `-lm` "
        "(liga a biblioteca matemática). O compilador do site usa `-std=c11 -Wall -Wextra -pedantic`, então os "
        "avisos que aparecem aqui são os mesmos que você veria no seu computador.",
    ),
    "linking": _licao(
        [
            "O protótipo de `resposta` permite compilar main antes da definição.",
            "O compilador gera um arquivo objeto em que main tem uma referência pendente a `resposta`.",
            "O linker encontra a definição no fim do arquivo e liga as duas partes.",
        ],
        "42",
        "Se a definição de `resposta` for apagada, a compilação ainda passa, mas a ligação falha com "
        "\"undefined reference\" apontando para `resposta`. O erro inverso, \"multiple definition\", acontece quando a mesma "
        "função é definida em dois .c. Bibliotecas externas são ligadas com `-l`, como `-lm` para a "
        "matemática, e vêm depois dos arquivos que as usam.",
    ),
    "makefile": _licao(
        [
            "O programa só mostra o comando de compilação que um Makefile automatizaria.",
            "Um Makefile guarda esse comando numa regra, e `make` o executa apenas quando main.c muda.",
        ],
        "gcc -std=c11 -Wall main.c -o programa",
        "Um Makefile mínimo tem uma variável como `CFLAGS = -std=c11 -Wall -Wextra`, a regra "
        "`programa: main.c calculos.c` e, na linha seguinte, começando com uma tabulação, o comando "
        "`$(CC) $(CFLAGS) main.c calculos.c -o programa`. `make` compara as datas dos arquivos: se nada mudou, "
        "não recompila. É comum ter também um alvo `clean` que apaga os arquivos gerados. Em projetos "
        "maiores, ferramentas como o CMake geram os Makefiles.",
    ),

    # Módulo 18 — Escrevendo programas seguros
    "buffer overflow": _licao(
        [
            "`char nome[10]` comporta 9 letras e o `'\\0'`.",
            "`%9s` limita a leitura a 9 caracteres, deixando espaço para o terminador.",
            "Digitando \"compilador\" (10 letras), só \"compilado\" é guardado: o resto não invade a memória vizinha.",
            "O retorno de scanf, 1, confirma que uma palavra foi lida.",
        ],
        "Uma palavra: compilador\nRecebido: compilado",
        "Sem o limite (`%s`), as letras extras seriam escritas depois do fim do array, sobrescrevendo outras "
        "variáveis ou o endereço de retorno da função: essa é a base de muitos ataques famosos. O compilador "
        "ajuda com proteções (stack protector, `-D_FORTIFY_SOURCE`), mas a responsabilidade é do código. "
        "Regra prática: sempre informe o tamanho (`%9s`, `fgets(buf, sizeof buf, stdin)`, `snprintf`) e "
        "confira índices antes de escrever em arrays.",
        entrada="compilador",
    ),
    "validação": _licao(
        [
            "`scanf` devolve quantos valores leu; `!= 1` significa que a pessoa não digitou um número.",
            "Depois do formato, vem a faixa: idades abaixo de 0 ou acima de 130 são recusadas.",
            "Cada caso inválido tem uma mensagem própria e retorna 1 (erro).",
            "Só um valor que passou pelas duas verificações é usado.",
        ],
        "Idade: 25\nIdade aceita: 25",
        "Quando scanf falha, os caracteres inválidos continuam na entrada; para pedir de novo, descarte a "
        "linha com `while (getchar() != '\\n');` antes de ler outra vez. Uma alternativa robusta é ler a linha "
        "com fgets e converter com strtol, conferindo se sobrou lixo. Valide tudo o que vem de fora do "
        "programa: teclado, arquivos e rede. Teste com letras, negativos, zero, o limite exato e valores "
        "enormes.",
        entrada="25",
    ),

    # Módulo 19 — Organizando muitos dados
    "listas": _licao(
        [
            "Cada `struct No` guarda um valor e o endereço do próximo nó.",
            "Os nós são ligados: primeiro → segundo → terceiro → NULL.",
            "O for começa em `&primeiro` e avança com `p = p->proximo` até chegar a NULL.",
            "A soma percorre 10 + 20 + 12.",
        ],
        "42",
        "Aqui os nós estão na pilha para simplificar; em programas reais cada nó é criado com malloc e a lista "
        "cresce durante a execução. Inserir no início é rápido (só troca ponteiros), mas achar o n-ésimo "
        "elemento exige percorrer a lista, o contrário do array. Ao liberar, guarde o próximo antes do free: "
        "`struct No *prox = p->proximo; free(p); p = prox;`.",
        memoria=(
            "Os nós não precisam estar vizinhos: cada um aponta para o próximo.",
            [
                ("primeiro", "0x1000", "{10, 0x1010}", "valor e endereço de segundo"),
                ("segundo", "0x1010", "{20, 0x1020}", "valor e endereço de terceiro"),
                ("terceiro", "0x1020", "{12, NULL}", "NULL marca o fim da lista"),
            ],
        ),
    ),
    "pilhas": _licao(
        [
            "`topo` indica a próxima posição livre e começa em 0 (pilha vazia).",
            "`pilha[topo++] = 10;` empilha (push): grava na posição 0 e avança o topo.",
            "Depois de empilhar 42, topo vale 2.",
            "`pilha[--topo]` desempilha (pop): recua o topo e lê o último valor, 42.",
        ],
        "Pop: 42",
        "Pilha é LIFO: o último a entrar é o primeiro a sair, como uma pilha de pratos. Antes do push confira "
        "`topo < 3` (pilha cheia) e antes do pop confira `topo > 0` (pilha vazia). Pilhas aparecem no desfazer "
        "dos editores, no botão voltar do navegador, na verificação de parênteses balanceados e na própria "
        "pilha de chamadas de funções.",
    ),
    "filas": _licao(
        [
            "`inicio` indica quem sai; `fim` indica onde o próximo entra.",
            "`fila[fim++] = 42;` e `fila[fim++] = 10;` enfileiram dois valores.",
            "`fila[inicio++]` remove o mais antigo: 42.",
        ],
        "Primeiro: 42",
        "Fila é FIFO: o primeiro a entrar é o primeiro a sair, como uma fila de banco. Neste formato simples, "
        "as posições do início não são reaproveitadas; a fila circular resolve isso com "
        "`fim = (fim + 1) % TAMANHO`. A fila está vazia quando `inicio == fim`. Filas organizam impressões, "
        "mensagens entre programas e a busca em largura em grafos.",
    ),
    "árvores": _licao(
        [
            "Cada nó tem um valor e dois ponteiros: esquerda e direita.",
            "A raiz 20 tem 10 à esquerda e 42 à direita: menores à esquerda, maiores à direita.",
            "`emOrdem` visita a esquerda, depois o nó, depois a direita, de forma recursiva.",
            "O resultado sai em ordem crescente: 10 20 42.",
        ],
        "10 20 42",
        "Em uma árvore binária de busca equilibrada, procurar um valor descarta metade da árvore a cada passo: "
        "com 1 milhão de itens, cerca de 20 comparações. Se os dados entram já ordenados, a árvore vira uma "
        "\"lista torta\" e perde essa vantagem; árvores balanceadas (AVL, rubro-negra) corrigem isso. Outros "
        "percursos: pré-ordem (nó, esquerda, direita) e pós-ordem (esquerda, direita, nó), usada para liberar "
        "a árvore.",
    ),

    # Módulo 20 — Resolvendo problemas melhor
    "busca linear": _licao(
        [
            "O for compara cada elemento com `alvo`.",
            "Na posição 2 o valor é 15, igual ao alvo, e \"Encontrado\" é mostrado.",
            "O laço continua até o fim; um `break` pararia assim que encontrasse.",
        ],
        "Encontrado",
        "No pior caso a busca linear olha os n elementos: ela é O(n) e funciona em qualquer array, ordenado ou "
        "não. Uma versão reutilizável devolve a posição: `int buscar(const int v[], int n, int alvo)` retorna "
        "o índice ou -1 se não achar. Em arrays ordenados, a busca binária é muito mais rápida (O(log n)), e "
        "`bsearch` da stdlib já a implementa.",
    ),
    "bubble sort": _licao(
        [
            "O laço interno compara vizinhos, `v[j]` e `v[j + 1]`, e troca os dois se estiverem fora de ordem.",
            "1ª passada: {3, 1, 2} → {1, 3, 2} → {1, 2, 3}; o maior valor \"borbulha\" até o fim.",
            "A cada passada, `2 - i` diminui, porque o fim do array já está ordenado.",
            "A troca usa `temp` para não perder um dos valores.",
        ],
        "1 2 3",
        "Bubble sort faz cerca de n²/2 comparações (O(n²)): ótimo para aprender, lento para muitos dados. Uma "
        "melhoria simples é parar quando uma passada inteira não fizer nenhuma troca. Na prática, use `qsort` "
        "da stdlib, que ordena qualquer tipo com uma função de comparação, ou algoritmos O(n log n) como "
        "merge sort e quicksort.",
    ),
    "eficiência": _licao(
        [
            "O laço passa uma única vez por cada um dos 5 elementos.",
            "`valores[i] % 2 == 0` testa se o número é par; 2, 8 e 42 são.",
            "O trabalho cresce na mesma proporção do tamanho do array: O(n).",
        ],
        "Pares: 3",
        "A notação O descreve como o tempo cresce com a entrada: O(1) constante, O(log n) na busca binária, "
        "O(n) em um laço, O(n log n) nas boas ordenações e O(n²) em dois laços aninhados. Com 1 milhão de "
        "itens, O(n) faz cerca de 1 milhão de passos e O(n²) cerca de 1 trilhão. Antes de otimizar detalhes, "
        "escolha o algoritmo certo e evite trabalho repetido dentro de laços.",
    ),

    # Módulo 21 — Criando programas completos
    "calculadora": _licao(
        [
            "`a`, `b` e `operador` representam o que o usuário digitaria.",
            "O if compara o operador com o caractere `'+'` (aspas simples).",
            "O resultado, 42.0, sai com duas casas: 42.00.",
        ],
        "Resultado: 42.00",
        "Uma versão completa lê `%lf %c %lf` com scanf, usa switch para os quatro operadores e trata a divisão "
        "por zero antes de calcular. Separe a conta em uma função, como "
        "`double calcular(double a, char op, double b, int *ok)`, e deixe main cuidar da entrada e da saída: "
        "assim a lógica pode ser testada sozinha. Um laço permite fazer várias contas até o usuário escolher "
        "sair.",
    ),
    "cadastro": _licao(
        [
            "`struct Pessoa` reúne nome e idade em um só tipo.",
            "A variável `pessoa` é criada já com os dados.",
            "O printf acessa os campos com ponto.",
        ],
        "Ana tem 42 anos",
        "Um cadastro real guarda várias pessoas em um array de structs (`struct Pessoa pessoas[100]`) com um "
        "contador de quantas posições estão preenchidas. As operações clássicas (CRUD) são criar, listar, "
        "atualizar e remover. Para os dados sobreviverem ao fim do programa, grave em arquivo com fprintf e "
        "leia de volta com fgets (módulo 12).",
    ),
    "agenda": _licao(
        [
            "`struct Contato` guarda nome e telefone como strings.",
            "`strcmp(contato.nome, \"Ana\") == 0` procura o contato pelo nome.",
            "Quando encontra, mostra o telefone.",
        ],
        "4242-4242",
        "Telefones são guardados como texto, não como número: podem ter zeros à esquerda, traços e "
        "parênteses. Com vários contatos, a busca percorre o array comparando nomes; para ignorar maiúsculas, "
        "compare cópias convertidas com `tolower`. Leia nomes com fgets para aceitar espaços e confira o "
        "limite do array antes de adicionar um contato novo.",
    ),
    "jogo terminal": _licao(
        [
            "`alvo` é o número secreto e `tentativa` é o palpite.",
            "O if compara os dois; iguais, o jogo mostra \"Acertou\".",
        ],
        "Acertou",
        "Um jogo de adivinhação completo sorteia o alvo com `srand((unsigned)time(NULL));` e "
        "`rand() % 100 + 1` (inclua `<stdlib.h>` e `<time.h>`), lê palpites em um laço, responde \"maior\" ou "
        "\"menor\" e conta as tentativas. Organize o jogo em estado (variáveis), entrada (ler o palpite), "
        "atualização (comparar) e saída (mensagens): o mesmo ciclo de jogos maiores.",
    ),
    "sistema biblioteca": _licao(
        [
            "`struct Livro` guarda o título e se o livro está disponível (1) ou não (0).",
            "O empréstimo só acontece se `livro.disponivel` for verdadeiro.",
            "Ao emprestar, o campo muda para 0, e um novo empréstimo seria recusado.",
        ],
        "Emprestado",
        "Esse campo é uma pequena máquina de estados: disponível → emprestado → disponível. Um sistema maior "
        "teria arrays de livros e de leitores, funções como `emprestar` e `devolver` que informam sucesso ou "
        "erro, e gravação em arquivo. Uma enum com `DISPONIVEL`, `EMPRESTADO` e `RESERVADO` deixa os estados "
        "mais claros que 0 e 1.",
    ),
    "editor texto": _licao(
        [
            "`texto` tem 50 bytes e começa com \"Aprender \".",
            "Antes de concatenar, o if confere se o texto atual, o \"C\" e o `'\\0'` cabem no array.",
            "Como cabem, strcat acrescenta \"C\".",
        ],
        "Aprender C",
        "Um editor simples guarda o documento como um array de linhas (`char linhas[100][81]`) e oferece "
        "comandos como inserir, apagar e procurar (`strstr`). Todo ponto que escreve texto precisa conferir o "
        "tamanho, como o exemplo faz. Para salvar e abrir, grave cada linha com fprintf e leia com fgets.",
    ),
    "projeto final": _licao(
        [
            "`media` recebe três notas e devolve a média; `static` a deixa visível só neste arquivo.",
            "Os parênteses garantem que a soma acontece antes da divisão.",
            "main só chama a função e mostra o resultado com duas casas.",
        ],
        "Media: 8.00",
        "Para um projeto maior: escreva primeiro o que o programa deve fazer, divida em funções pequenas, "
        "teste cada uma com valores conhecidos e só então junte tudo em main. Compile com `-Wall -Wextra` e "
        "corrija todos os avisos. Guarde versões com Git para poder voltar atrás. Um bom projeto final combina "
        "structs, arrays, funções, arquivos e validação de entrada.",
    ),
}
