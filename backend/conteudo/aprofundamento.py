"""Aprofundamento de cada lição: "Indo além", desenho da memória e a execução do exemplo.

- `alem`: o texto "Indo além", com detalhes, armadilhas e ferramentas.
- `saida` e `entrada`: a execução dos exemplos de exemplos.py. Os exemplos de exemplos_teoricos.py
  já trazem a própria execução. tests/test_theory_content.py confere a saída de todos.
- `passos`: passo a passo próprio, só nas lições cujo exemplo foi trocado depois que a leitura de
  teoria_ampliada.py foi escrita. Nas demais, a página usa o passo a passo da leitura.
- `memoria`: tabela "Como fica a memória" das lições de arrays, strings, ponteiros e alocação.

Trechos entre crases (`assim`) aparecem como código na página.
"""


def _licao(alem, saida=None, entrada=None, passos=None, memoria=None):
    item = {"alem": alem, "saida": saida, "entrada": entrada, "passos": passos, "memoria": None}
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
        "C foi criada por Dennis Ritchie no início dos anos 1970 para escrever o sistema Unix, e "
        "até hoje os núcleos do Linux, do Windows e do macOS têm grandes partes em C. A linguagem"
        " é padronizada pela ISO: C89, C99, C11, C17 e C23 são versões do padrão. Neste curso "
        "usamos C11, que o GCC aceita com a opção `-std=c11`. O mesmo código-fonte pode ser "
        "compilado para processadores diferentes: o que muda é o executável gerado.",
        saida="C transforma codigo-fonte em programas eficientes.\n",
    ),
    "Estrutura básica": _licao(
        "O compilador ignora espaços e quebras de linha extras: o programa inteiro caberia em uma"
        " linha só. A indentação existe para as pessoas enxergarem os blocos. Em C11, se main "
        "chegar à `}` sem `return`, o efeito é o mesmo de `return 0;`, mas escrever o return "
        "deixa a intenção clara. Fora das funções só ficam diretivas (`#include`, `#define`) e "
        "declarações; instruções como `printf` precisam estar dentro de uma função.",
        saida="Resposta: 42\n",
    ),
    "Comentários": _licao(
        "Comentários de bloco não se aninham: em `/* a /* b */ c */` o comentário termina no "
        "primeiro `*/` e o ` c */` que sobra vira erro de sintaxe. Para desativar um trecho "
        "grande, use `#if 0` ... `#endif`. Um bom comentário responde \"por quê?\" (por que o "
        "limite é 100, por exemplo); o \"o quê\" o próprio código já mostra. Texto entre aspas não "
        "é comentário: `printf(\"// oi\")` imprime `// oi`.",
        saida="Comentarios nao sao executados.\n",
    ),
    "Compilação": _licao(
        "Dá para ver cada etapa no GCC: `gcc -E programa.c` mostra o código depois do "
        "pré-processador, `gcc -S` gera o assembly, `gcc -c` gera o objeto `.o` e `gcc programa.o"
        " -o programa` faz a ligação. Erros de compilação aparecem com arquivo e linha, como "
        "`programa.c:5:20: error: ...`. Erros de ligação aparecem depois, com mensagens como "
        "`undefined reference to`, quando uma função foi declarada mas sua implementação não foi "
        "encontrada.",
        saida="Resultado compilado: 42\n",
    ),

    # Módulo 2 — Conversando com o usuário
    "printf": _licao(
        "Especificadores aceitam largura e precisão: `%5d` alinha o número em 5 colunas, `%-10s` "
        "alinha um texto à esquerda e `%08.3f` completa com zeros e mostra 3 casas. Para mostrar "
        "o próprio `%`, use `%%`; para aspas dentro do texto, `\\\"`. A saída costuma ficar "
        "guardada em um buffer e só aparece de fato na quebra de linha ou no fim do programa, por"
        " isso é bom terminar mensagens com `\\n`. printf devolve a quantidade de caracteres "
        "escritos.",
        saida="Ola, estudante!\nEstou aprendendo C.\n",
    ),
    "scanf": _licao(
        "Um único scanf pode ler vários valores: `scanf(\"%d %d\", &a, &b)` devolve 2 quando os "
        "dois foram lidos, e o espaço entre eles aceita espaços, tabulações ou Enter. Para "
        "`double` o especificador de leitura é `%lf`, diferente do printf, que usa `%f`. Quando a"
        " leitura falha, os caracteres inválidos continuam esperando na entrada; por isso um laço"
        " que repete scanf sem descartar a linha pode ficar preso. O `fflush(stdout)` do exemplo "
        "garante que a pergunta apareça antes da espera, algo importante em terminais que só "
        "mostram a saída na quebra de linha.",
    ),

    # Módulo 3 — Guardando informações
    "int": _licao(
        "Em PCs e servidores atuais um int tem 4 bytes (32 bits) e vai de -2.147.483.648 a "
        "2.147.483.647; os limites exatos estão em `<limits.h>` (`INT_MIN` e `INT_MAX`). Passar "
        "do limite em um int com sinal é comportamento indefinido: o resultado não é garantido. "
        "Existem variações como `short`, `long`, `long long` e as versões `unsigned`, que não "
        "guardam negativos. Para um tamanho exato, `<stdint.h>` oferece tipos como `int32_t` e "
        "`int64_t`.",
        saida="Idade: 18\n",
    ),
    "float e double": _licao(
        "Números com vírgula são guardados em binário e muitos decimais não têm representação "
        "exata: `0.1 + 0.2` resulta em 0.30000000000000004. Por isso não compare decimais com "
        "`==`; verifique se a diferença é menor que uma tolerância, como `fabs(a - b) < 1e-9`. "
        "double tem cerca de 15 dígitos de precisão e float cerca de 7, então prefira double. O "
        "literal `8.5` já é double; `8.5f` é float.",
        saida="Nota: 8.5\n",
    ),
    "char": _licao(
        "Como char é um número, dá para fazer contas: `'A' + 1` é `'B'` e `c - '0'` transforma o "
        "dígito `'7'` no número 7. `'C'` (aspas simples) é um caractere; `\"C\"` (aspas duplas) é "
        "uma string com dois bytes, `'C'` e o terminador `'\\0'`. Letras acentuadas em UTF-8 "
        "ocupam mais de um byte e não cabem em um único char, por isso os programas do curso "
        "evitam acentos na saída. `<ctype.h>` tem funções como `toupper` e `isdigit`.",
        saida="Inicial: C\n",
    ),
    "constantes": _licao(
        "Uma const precisa ser inicializada na declaração, porque não pode receber valor depois. "
        "Diferente de `#define`, ela tem tipo, respeita escopo e aparece no depurador. Em "
        "ponteiros, a posição do const importa: `const int *p` impede alterar o valor apontado, "
        "enquanto `int *const p` impede mudar para onde p aponta. Um parâmetro `const char "
        "*texto` avisa que a função só vai ler o texto.",
        saida="Limite: 100\n",
    ),
    "#define": _licao(
        "A macro é substituição de texto e não conhece tipos. Macros com parâmetros exigem "
        "parênteses: com `#define DOBRO(x) x * 2`, a expressão `DOBRO(1 + 2)` vira `1 + 2 * 2`, "
        "que dá 5; o certo é `#define DOBRO(x) ((x) * 2)`. Use `gcc -E` para ver o código depois "
        "das substituições. Para valores com tipo, prefira `const` ou `enum`; `#define` continua "
        "útil para tamanhos de arrays e para compilação condicional com `#ifdef`.",
        saida="Curso: C\n",
    ),
    "escopo": _licao(
        "Variáveis locais nascem ao entrar no bloco e morrem ao sair; o valor não é preservado "
        "entre chamadas de uma função, a não ser que a variável seja `static`. Uma variável "
        "interna com o mesmo nome de uma externa a esconde (sombreamento), e o GCC avisa com "
        "`-Wshadow`. Variáveis globais, declaradas fora das funções, valem para o arquivo inteiro"
        " e começam zeradas, mas deixam o programa difícil de acompanhar: passe valores por "
        "parâmetros sempre que puder.",
        saida="Dentro: 20\nFora: 10\n",
    ),

    # Módulo 4 — Fazendo contas e comparações
    "soma": _licao(
        "A soma de dois int é um int; se o resultado passar de `INT_MAX`, ocorre estouro "
        "(overflow), que em tipos com sinal é comportamento indefinido. Quando um dos lados é "
        "double, o outro é convertido e o resultado é double: `1 + 0.5` dá 1.5. O operador `+=` "
        "soma e guarda: `total += x;` é o mesmo que `total = total + x;`, muito usado para "
        "acumular valores em laços.",
        saida="Soma: 42\n",
    ),
    "subtração": _licao(
        "A ordem importa: `a - b` é diferente de `b - a`. O `-` também é unário: `-x` troca o "
        "sinal. Cuidado com `unsigned`: `3u - 5u` não dá -2, dá 4294967294, porque tipos sem "
        "sinal \"dão a volta\". Em regras de negócio, pense nos limites: um saque só deve acontecer"
        " se `retirada <= saldo`.",
        saida="Saldo: 42\n",
    ),
    "multiplicação": _licao(
        "Multiplicação e divisão têm precedência maior que soma e subtração: `2 + 3 * 4` é 14. "
        "Use parênteses para deixar a intenção clara, como `(2 + 3) * 4`. Multiplicar ints "
        "grandes estoura rápido: `100000 * 100000` não cabe em int; converta antes com `(long "
        "long)a * b`. C não tem operador de potência: use `x * x` ou `pow` de `<math.h>`.",
        saida="Celulas: 42\n",
    ),
    "divisão": _licao(
        "Na divisão inteira o C descarta a parte decimal em direção a zero: `7 / 2` é 3 e `-7 / "
        "2` é -3. O resto vem de `%`: `7 % 2` é 1, útil para saber se um número é par. Para obter"
        " decimal a partir de ints, converta um dos lados: `(double)soma / quantidade`. Dividir "
        "um inteiro por zero é comportamento indefinido e costuma derrubar o programa: confira o "
        "divisor antes.",
        saida="Resultado: 3.50\n",
    ),
    "operadores relacionais": _licao(
        "Não confunda `=` (atribuição) com `==` (comparação): `if (x = 5)` guarda 5 em x e é "
        "sempre verdadeiro, e o GCC avisa com `-Wall`. Comparações não se encadeiam como na "
        "matemática: `1 < x < 10` compara `(1 < x)`, que vale 0 ou 1, com 10, e dá sempre "
        "verdadeiro; escreva `x > 1 && x < 10`. Strings não se comparam com `==`: use `strcmp`. O"
        " cabeçalho `<stdbool.h>` oferece `bool`, `true` e `false`.",
        saida="a > b: 1 | a == b: 0\n",
    ),
    "operadores lógicos": _licao(
        "`&&` e `||` avaliam da esquerda para a direita e param assim que o resultado está "
        "definido (curto-circuito): em `x != 0 && 10 / x > 2`, a divisão nem acontece quando x é "
        "0. `!` inverte: `!0` é 1. `&&` tem precedência maior que `||`, então `a || b && c` é `a "
        "|| (b && c)`; na dúvida, use parênteses. Não confunda com `&` e `|`, que operam bit a "
        "bit (módulo 15).",
        saida="Resultado: 1\n",
    ),
    "incremento": _licao(
        "A diferença aparece dentro de expressões: `x++` devolve o valor antigo e depois "
        "incrementa; `++x` incrementa e devolve o novo. Com x = 5, `y = x++;` deixa y = 5 e x = "
        "6, enquanto `y = ++x;` deixa os dois em 6. Nunca altere a mesma variável duas vezes na "
        "mesma expressão, como em `i = i++ + 1;`: é comportamento indefinido. `--` funciona "
        "igual, subtraindo 1.",
        saida="42\n",
    ),

    # Módulo 5 — Tomando decisões
    "if": _licao(
        "Em C, qualquer valor diferente de zero é verdadeiro: `if (quantidade)` é o mesmo que `if"
        " (quantidade != 0)`. Um `;` logo depois do parêntese, como em `if (x > 3);`, cria um if "
        "vazio e o bloco seguinte executa sempre, um erro difícil de ver. Sem chaves, só a "
        "próxima instrução pertence ao if; por isso use chaves sempre. Condições podem combinar "
        "operadores lógicos: `if (nota >= 7 && frequencia >= 75)`.",
    ),
    "else": _licao(
        "Com ifs aninhados sem chaves, o else pertence ao if mais próximo, não ao que a "
        "indentação sugere (o chamado \"dangling else\"). Um if/else que só escolhe um valor pode "
        "virar operador ternário: `const char *tipo = numero % 2 == 0 ? \"par\" : \"impar\";`. Para "
        "negativos, `-7 % 2` é -1 em C: para testar ímpar, use `!= 0` em vez de `== 1`.",
        saida="7 e impar\n",
        passos=[
            "`numero % 2` calcula o resto da divisão por 2; para 7, o resto é 1.",
            "A condição `numero % 2 == 0` é falsa, então o bloco do if é pulado.",
            "O `else` executa exatamente quando o if não executou.",
            "Os caminhos são exclusivos: nunca aparecem as duas mensagens.",
        ],
    ),
    "else if": _licao(
        "A ordem das condições importa: se `nota >= 7` viesse antes de `nota >= 9`, um 10 "
        "receberia B. Organize as faixas da mais restrita para a mais ampla. `else if` não é um "
        "comando especial: é um `else` cujo bloco é outro if. Teste as fronteiras (6, 7, 8, 9) "
        "para garantir que cada valor cai na faixa certa.",
        saida="Conceito B\n",
    ),
    "switch": _licao(
        "switch só funciona com valores inteiros (int, char, enum) e os cases precisam ser "
        "constantes; para faixas ou strings, use if/else if. Esquecer o `break` gera "
        "\"fall-through\", às vezes intencional para agrupar casos, como `case 'a': case 'A':`. O "
        "GCC avisa sobre fall-through suspeito com `-Wextra`, e com `-Wall` avisa quando um valor"
        " de enum ficou sem case.",
        saida="Consultar\n",
    ),
    "ternário": _licao(
        "O ternário é uma expressão (produz um valor), enquanto o if é uma instrução. Ele é ótimo"
        " para escolhas curtas, como `printf(\"%s\\n\", ok ? \"sim\" : \"nao\");`. Ternários aninhados "
        "ficam difíceis de ler: prefira if/else. Os dois resultados devem ter tipos compatíveis; "
        "se um for int e o outro double, o resultado é double.",
        saida="Maior: 42\n",
    ),

    # Módulo 6 — Repetindo tarefas
    "while": _licao(
        "while testa antes de executar, então o corpo pode rodar zero vezes. É o laço ideal "
        "quando não se sabe quantas repetições haverá, como ler números até a pessoa digitar 0: "
        "`while (scanf(\"%d\", &x) == 1 && x != 0)`. Se o programa travar, confira se a variável da"
        " condição muda dentro do laço. `while (1)` com um `break` interno é um padrão comum em "
        "menus.",
        saida="1\n2\n3\n",
    ),
    "do while": _licao(
        "do while é natural para menus e validação de entrada: mostre o menu, leia a opção e "
        "repita enquanto ela for inválida. Com um while comum, este mesmo exemplo não mostraria a"
        " primeira linha. Todo do while pode ser reescrito como while, mas às vezes isso obriga a"
        " repetir código antes do laço.",
        saida="Executou com contador = 10\nO do while roda o bloco pelo menos uma vez.\n",
        passos=[
            "`contador` começa em 10, que já não satisfaz `contador <= 3`.",
            "Mesmo assim o bloco do `do` executa uma vez, porque o teste só acontece no fim.",
            "Depois da volta, `contador` vale 11 e o teste falha: o laço termina.",
            "Repare no `;` depois de `while (...)`: ele é obrigatório no do while.",
        ],
    ),
    "for": _licao(
        "Todo for pode ser escrito como while: `int i = 1; while (i <= 5) { ...; i++; }`. Para "
        "percorrer um array de n elementos, o padrão é `for (int i = 0; i < n; i++)`: começa em 0"
        " e usa `<`, não `<=`, para não acessar uma posição inexistente. Qualquer parte do "
        "cabeçalho pode ficar vazia; `for (;;)` é um laço infinito. Mostrar as variáveis a cada "
        "volta, com um printf dentro do laço, é uma técnica simples de depuração.",
    ),
    "break": _licao(
        "break sai apenas do laço (ou switch) mais interno. Para sair de dois laços aninhados, "
        "use uma variável de controle ou coloque o código em uma função e use return. break é "
        "útil em buscas: depois de encontrar o item, não há por que continuar percorrendo.",
        saida="1 2 3 4 5 \n",
    ),
    "continue": _licao(
        "Em um while, cuidado: se o incremento estiver depois do continue, ele é pulado e o laço "
        "pode ficar infinito. continue ajuda a descartar casos no início do corpo (\"se não serve,"
        " pula\"), evitando ifs aninhados. Muitas vezes o mesmo efeito sai com a condição "
        "invertida: `if (i % 2 != 0) printf(...)`.",
        saida="1 3 5 \n",
    ),

    # Módulo 7 — Organizando o código
    "criando função": _licao(
        "Uma função precisa ser declarada antes de ser chamada; aqui ela é definida acima de "
        "main. O nome deve descrever a ação, como `calcular_media` ou `mostrar_menu`. Funções "
        "curtas, com uma única responsabilidade, são mais fáceis de testar e reaproveitar. "
        "Variáveis declaradas dentro de uma função são locais a ela, e cada chamada tem as suas "
        "próprias.",
        saida="--------------------\n  Curso de C\n--------------------\n",
        passos=[
            "`void mostrar_linha(void)` define uma função que não recebe dados nem devolve valor.",
            "O corpo, entre chaves, contém o printf da linha tracejada.",
            "Em main, `mostrar_linha();` chama a função: a execução entra nela, roda o corpo e "
            "volta.",
            "A mesma função é chamada duas vezes sem repetir o código.",
        ],
    ),
    "parâmetros": _licao(
        "Argumento é o valor enviado na chamada; parâmetro é a variável que o recebe. Se a função"
        " precisar alterar a variável de quem chamou, ela recebe um ponteiro, como `void "
        "dobrar(int *x)` (módulo 9). Arrays parecem uma exceção: a função recebe o endereço do "
        "primeiro elemento e por isso altera o array original. Em `int f(void)` o `void` "
        "significa \"nenhum parâmetro\"; em C antigo, `int f()` significava \"parâmetros não "
        "informados\".",
        saida="Dentro da funcao: 99\nDepois da chamada: 10\nMedia de 7 e 10: 8.5\n",
        passos=[
            "`tentar_alterar(valor)` envia uma cópia de 10 para o parâmetro `numero`.",
            "Dentro da função, `numero = 99` muda só a cópia: aparece 99.",
            "De volta ao main, `valor` continua 10. Isso é passagem por valor.",
            "`media(7.0, 10.0)` recebe dois parâmetros, na ordem da assinatura, e devolve 8.5.",
        ],
    ),
    "retorno": _licao(
        "Uma função devolve um valor por vez; para devolver vários, use uma struct ou parâmetros "
        "ponteiro. Esquecer o return em uma função não void gera o aviso \"control reaches end of "
        "non-void function\", e usar esse valor é comportamento indefinido. Em funções void, "
        "`return;` sem valor encerra a função mais cedo. Nunca devolva o endereço de uma variável"
        " local: ela deixa de existir quando a função termina.",
        saida="Maior: 42\nDobro do maior entre 3 e 8: 16\n",
        passos=[
            "`int maior(int a, int b)` promete devolver um int.",
            "Se `a > b`, o primeiro `return a;` encerra a função na hora.",
            "Caso contrário, a execução chega a `return b;`: todos os caminhos devolvem um valor.",
            "O valor devolvido pode ser guardado (`resultado`) ou usado direto numa expressão "
            "(`maior(3, 8) * 2`).",
        ],
    ),
    "protótipos": _licao(
        "Sem o protótipo, o GCC mostra \"implicit declaration of function\": desde o C99 chamar uma"
        " função não declarada é proibido, e o GCC 14 em diante já recusa o código. Protótipos "
        "permitem deixar main no topo do arquivo e são a base dos cabeçalhos `.h`. No protótipo, "
        "os nomes dos parâmetros são opcionais (`int dobro(int);`), mas ajudam a documentar. Se "
        "protótipo e definição divergirem, o compilador aponta \"conflicting types\".",
    ),
    "recursão": _licao(
        "Cada chamada ocupa um pedaço da pilha de execução (stack) com seus parâmetros e "
        "variáveis locais; sem caso base, ou com recursão profunda demais, a pilha estoura (stack"
        " overflow) e o programa cai. O fatorial cresce rápido: 13! já não cabe em um int de 32 "
        "bits. Toda recursão pode virar um laço; ela é mais natural em estruturas recursivas, "
        "como árvores.",
        saida="120\n",
    ),

    # Módulo 8 — Listas e textos
    "arrays": _licao(
        "O C não confere limites: `valores[3]` lê fora do array, o que é comportamento indefinido"
        " e pode mostrar lixo, travar ou parecer funcionar. `sizeof valores / sizeof valores[0]` "
        "calcula a quantidade de elementos (só no array original, não em um parâmetro de função)."
        " Se a lista de inicialização for menor que o array, o resto é zerado: `int v[5] = {0};` "
        "zera tudo. Um array não pode ser atribuído a outro com `=`; copie elemento a elemento ou"
        " com `memcpy`.",
        saida="10\n20\n30\n",
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
        "Na memória, a matriz é guardada linha após linha: 10, 2, 3, 32 em sequência. Por isso "
        "percorrer com a linha no laço externo e a coluna no interno é mais rápido. Ao passar uma"
        " matriz para uma função, o número de colunas precisa aparecer no parâmetro: `void "
        "mostrar(int m[][2], int linhas)`.",
        saida="Diagonal: 42\n",
    ),
    "strings": _licao(
        "Em C, string é um array de char terminado por `'\\0'`, e todas as funções de `<string.h>`"
        " dependem desse terminador. Ao declarar o tamanho, reserve espaço para ele: \"casa\" "
        "precisa de `char s[5]`. Um literal acessado por ponteiro (`char *p = \"texto\";`) fica em "
        "memória somente leitura: altere apenas strings guardadas em arrays. `printf(\"%s\", "
        "texto)` imprime tudo até o `'\\0'`.",
        saida="Linguagem C\n",
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
        "`sizeof palavra` daria 9, porque inclui o `'\\0'`, enquanto `strlen(palavra)` dá 8. "
        "strlen percorre a string inteira a cada chamada; em `for (i = 0; i < strlen(s); i++)` "
        "ela é recalculada em toda volta, então guarde o tamanho numa variável antes. Sem `'\\0'`,"
        " strlen continua lendo memória além do array. Em UTF-8, uma letra acentuada conta como 2"
        " bytes.",
        saida="Tamanho: 8\n",
    ),
    "strcpy": _licao(
        "strcpy não sabe o tamanho do destino: se a origem for maior, ela escreve além do array "
        "(buffer overflow), uma das falhas de segurança mais comuns. Confira antes com "
        "`strlen(origem) < sizeof destino` ou use `snprintf(destino, sizeof destino, \"%s\", "
        "origem)`, que sempre respeita o limite e termina com `'\\0'`. `strncpy` parece segura, "
        "mas não coloca o `'\\0'` quando a origem é longa demais.",
        saida="C seguro\n",
    ),
    "strcmp": _licao(
        "`a == b` compara endereços, não o conteúdo: dois arrays com o mesmo texto têm endereços "
        "diferentes. A comparação segue os códigos dos caracteres, então maiúsculas vêm antes de "
        "minúsculas (\"Zebra\" vem antes de \"abelha\"). Não teste `strcmp(...) == 1`: o padrão só "
        "garante o sinal, não o valor. `strncmp(a, b, n)` compara só os n primeiros caracteres.",
        saida="Iguais\n",
    ),
    "strcat": _licao(
        "O destino precisa de espaço para as duas partes e o `'\\0'`: `strlen(destino) + "
        "strlen(origem) + 1 <= sizeof destino`. strcat também exige que o destino já seja uma "
        "string válida, terminada em `'\\0'`; um array não inicializado quebra a função. Para "
        "montar textos com números, `snprintf` é mais simples e seguro: `snprintf(buf, sizeof "
        "buf, \"Nota: %d\", n);`.",
        saida="Curso de C\n",
    ),
    "fgets": _licao(
        "Diferente de `scanf(\"%s\")`, fgets lê nomes compostos como \"Ana Maria\" e nunca ultrapassa"
        " o tamanho informado. Se a linha for maior que o array, o restante fica esperando para a"
        " próxima leitura. Um padrão robusto para números é ler a linha com fgets e converter com"
        " `strtol`, conferindo se a linha toda foi usada. Nunca use `gets`: ela foi removida do "
        "C11 por não ter limite.",
        saida="Nome: Ola, Ana\n",
        entrada="Ana\n",
    ),

    # Módulo 9 — Como a memória funciona
    "memória": _licao(
        "Os tamanhos de int e double podem variar entre plataformas; o padrão só garante mínimos "
        "e que `sizeof(char)` é 1. A saída acima é a de um PC de 64 bits comum. Variáveis locais "
        "ficam na pilha (stack) e somem no fim da função; memória pedida com malloc fica no heap "
        "até o free. O compilador pode deixar espaços entre variáveis para alinhá-las, então os "
        "endereços nem sempre ficam colados.",
        saida="int: 4 bytes\ndouble: 8 bytes\nchar: 1 byte\narray de 5 int: 20 bytes\n",
        passos=[
            "Cada variável ocupa um número de bytes definido pelo seu tipo.",
            "`sizeof` informa esse tamanho sem ler o valor; o resultado é `size_t`, mostrado com "
            "`%zu`.",
            "Um array ocupa a soma dos elementos: 5 ints × 4 bytes = 20 bytes.",
        ],
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
        "Para ver o endereço real, use `printf(\"%p\\n\", (void *)&valor);`; o número muda a cada "
        "execução porque o sistema sorteia as posições de memória (ASLR). O `*` tem dois papéis: "
        "na declaração (`int *p`) indica \"ponteiro para int\"; numa expressão (`*p`) acessa o "
        "valor apontado. É por isso que `scanf(\"%d\", &x)` precisa do `&`: scanf recebe o endereço"
        " de x para gravar nele.",
        saida="Valor: 42\n",
        memoria=(
            "O ponteiro guarda o endereço de outra variável.",
            [
                ("valor", "0x1000", "42", "int"),
                ("ponteiro", "0x1008", "0x1000", "aponta para valor; *ponteiro vale 42"),
            ],
        ),
    ),
    "ponteiros + funções": _licao(
        "Com passagem por valor, `void trocar(int a, int b)`, a troca aconteceria só nas cópias e"
        " main não veria diferença. Ponteiros também permitem \"devolver\" vários resultados: `void"
        " dividir(int a, int b, int *quociente, int *resto)`. Quando uma função recebe ponteiro, "
        "confira se ele pode ser NULL. Se a função só lê, use `const int *` para deixar isso "
        "explícito.",
        saida="42 10\n",
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
        "Array e ponteiro não são a mesma coisa: `sizeof valores` é 12 (o array inteiro) e "
        "`sizeof p` é 8 (o tamanho de um endereço). Ao passar um array para uma função, ela "
        "recebe só o ponteiro, por isso o tamanho precisa ir junto como parâmetro. Aritmética de "
        "ponteiros só é válida dentro do array (e até uma posição depois do fim, sem ler nela).",
        saida="42\n",
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
        "Ponteiros duplos aparecem quando uma função precisa alterar um ponteiro de quem a "
        "chamou, por exemplo para alocar memória: `void criar(int **saida) { *saida = "
        "malloc(sizeof **saida); }`. Também representam listas de strings, como `char **argv` em "
        "`int main(int argc, char **argv)`, que recebe os argumentos da linha de comando. Ao ler "
        "`**`, desenhe caixas e setas: cada asterisco é uma seta a seguir.",
        saida="42\n",
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
        "O conteúdo inicial do bloco é lixo; use calloc se precisar dele zerado. O exemplo "
        "escreve `sizeof *numero`, que continua certo mesmo se o tipo do ponteiro mudar. Em C não"
        " é preciso converter o retorno: `int *p = malloc(...)` já funciona. A grande vantagem é "
        "decidir o tamanho durante a execução: `malloc(n * sizeof *v)` cria um array com n "
        "elementos escolhidos pelo usuário.",
        memoria=(
            "O ponteiro fica na pilha; o bloco reservado fica no heap.",
            [
                ("numero", "0x1000 (pilha)", "0x5000", "endereço devolvido por malloc"),
                ("bloco", "0x5000 (heap)", "30", "existe até o free"),
            ],
        ),
    ),
    "calloc": _licao(
        "calloc recebe quantidade e tamanho separados e confere se a multiplicação estoura, o que"
        " `malloc(n * tamanho)` não faz. Zerar custa um pouco de tempo, então use calloc quando "
        "precisar do conteúdo inicial zerado, como contadores. O bloco se usa como array "
        "(`valores[i]`), mas `sizeof valores` dá o tamanho do ponteiro, não do bloco: guarde a "
        "quantidade em uma variável.",
        saida="0 0 0 42 \n",
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
        "Nunca escreva `v = realloc(v, ...)`: se realloc falhar, devolve NULL, você perde o único"
        " endereço do bloco antigo e cria um vazamento. Quando o bloco muda de lugar, realloc "
        "copia os dados e libera o endereço anterior, então qualquer outro ponteiro para o bloco "
        "antigo fica inválido. Para listas que crescem, dobre a capacidade a cada realloc em vez "
        "de aumentar de 1 em 1: fica muito mais rápido.",
        saida="42\n",
    ),
    "free": _licao(
        "Depois do free, o ponteiro ainda guarda o endereço antigo, mas o bloco não é mais seu: "
        "ler ou escrever ali (use-after-free) é comportamento indefinido. Liberar duas vezes "
        "(double free) também, e costuma derrubar o programa. `free(NULL)` é permitido e não faz "
        "nada, por isso zerar o ponteiro deixa um segundo free inofensivo. Só passe para free "
        "endereços vindos de malloc, calloc ou realloc.",
        saida="42\n",
        memoria=(
            "Depois do free o bloco não pode mais ser usado.",
            [
                ("valor", "0x1000 (pilha)", "0x5000 → NULL", "zerado depois do free"),
                ("bloco", "0x5000 (heap)", "42 → (liberado)", "devolvido ao sistema"),
            ],
        ),
    ),
    "memory leak": _licao(
        "Um vazamento acontece quando o último ponteiro para um bloco se perde sem free, por "
        "exemplo num return antecipado. Em programas curtos o sistema recupera tudo no fim, mas "
        "servidores e jogos que rodam por horas vão consumindo memória até travar. Ferramentas "
        "como o Valgrind (`valgrind --leak-check=full ./programa`) ou a opção "
        "`-fsanitize=address` do GCC apontam a linha de cada bloco não liberado. `static` na "
        "função indica que ela só é visível neste arquivo.",
        saida="42\n",
    ),

    # Módulo 11 — Agrupando informações
    "structs": _licao(
        "Structs podem ser copiadas com `=` e passadas para funções por valor, mas isso copia "
        "todos os bytes; para structs grandes, passe um ponteiro (`const struct Aluno *a`). "
        "Inicializadores designados deixam a ordem explícita: `{.nome = \"Ana\", .media = 8.5}`, e "
        "os campos omitidos ficam zerados. O `sizeof` de uma struct pode ser maior que a soma dos"
        " campos por causa do alinhamento. Structs não se comparam com `==`: compare campo a "
        "campo.",
        saida="Ana, 21 anos, media 8.5\n",
        passos=[
            "`struct Aluno { ... };` define um novo tipo com três campos.",
            "`struct Aluno aluno = {\"Ana\", 20, 8.5};` preenche os campos na ordem da declaração.",
            "`aluno.idade = 21;` altera um campo usando ponto.",
            "`p->idade` acessa o campo através do ponteiro; é o mesmo que `(*p).idade`.",
        ],
    ),
    "typedef": _licao(
        "typedef não cria um tipo novo: Contador e unsigned int são intercambiáveis e o "
        "compilador não impede misturar os dois. Uma struct que aponta para si mesma, como o nó "
        "de uma lista, precisa de nome: `typedef struct No { int v; struct No *prox; } No;`. "
        "Muitos projetos evitam typedef de ponteiros (`typedef int *IntPtr;`), porque esconde o "
        "`*` e confunde a leitura. A biblioteca padrão usa typedef em tipos como `size_t` e "
        "`FILE`.",
        saida="Visitas: 3\nPonto: (2.5, -1.0)\n",
        passos=[
            "`typedef unsigned int Contador;` cria o apelido Contador para unsigned int.",
            "`typedef struct { ... } Ponto;` dá nome a uma struct e dispensa escrever `struct` "
            "antes.",
            "`visitas` e `p` usam os apelidos como se fossem tipos comuns.",
        ],
    ),
    "unions": _licao(
        "O tamanho de uma union é o do seu maior membro. O uso típico é a \"união marcada\": uma "
        "struct com uma enum dizendo qual membro está ativo e a union com os dados, como `struct "
        "Token { enum Tipo tipo; union { int i; double d; } valor; };`. Isso economiza memória "
        "quando só uma alternativa existe por vez. Ler um membro diferente do último gravado "
        "reinterpreta os bytes e depende da plataforma.",
        saida="10\n",
        memoria=(
            "Os membros começam no mesmo endereço.",
            [
                ("v.inteiro", "0x1000", "10", "membro ativo (4 bytes)"),
                ("v.decimal", "0x1000", "mesmos bytes", "mesmo endereço de v.inteiro"),
            ],
        ),
    ),
    "enum": _licao(
        "Os valores podem ser escolhidos: `enum Mes {JAN = 1, FEV, MAR};` faz FEV valer 2. enum "
        "combina bem com switch: com `-Wall`, o GCC avisa se algum valor ficou sem case. Para "
        "mostrar o nome em vez do número, use um array de strings indexado pela enum: `const char"
        " *nomes[] = {\"ABERTO\", \"FECHADO\"};`. O C não impede atribuir qualquer inteiro a uma "
        "variável enum, então valide valores vindos de fora.",
        saida="0\n",
    ),

    # Módulo 12 — Salvando dados
    "fopen": _licao(
        "Modos principais: \"r\" lê (o arquivo precisa existir), \"w\" escreve apagando o conteúdo "
        "anterior e \"a\" acrescenta no fim. Com \"+\" (como \"r+\") o arquivo permite ler e escrever, "
        "e com \"b\" (\"rb\") abre em modo binário. Para saber por que falhou, use "
        "`perror(\"dados.txt\")`, que mostra a mensagem do sistema. O caminho é relativo à pasta "
        "onde o programa está rodando, não à pasta do código-fonte.",
    ),
    "fclose": _licao(
        "A escrita em arquivo passa por um buffer na memória; sem fclose (ou fflush), parte dos "
        "dados pode não chegar ao disco se o programa cair. Cada arquivo aberto consome um "
        "recurso do sistema, que tem um limite de arquivos abertos ao mesmo tempo. Depois de "
        "fechado, o `FILE *` não pode mais ser usado. Não chame fclose com NULL: confira o fopen "
        "primeiro.",
    ),
    "fprintf": _licao(
        "`fprintf(stdout, ...)` é igual a printf, e `fprintf(stderr, ...)` escreve na saída de "
        "erros, própria para mensagens que não devem se misturar com os resultados. Para gravar "
        "dados fáceis de ler depois, use um formato fixo, como um registro por linha e campos "
        "separados por `;` (formato CSV). fprintf devolve um número negativo se a escrita falhar.",
    ),
    "fscanf": _licao(
        "Para ler um arquivo inteiro, repita enquanto a leitura der certo: `while (fscanf(arq, "
        "\"%d\", &x) == 1) { ... }`. Evite `while (!feof(arq))`: feof só fica verdadeiro depois que"
        " uma leitura falha, e o último valor acaba processado duas vezes. Para linhas de texto "
        "com espaços, prefira fgets e depois `sscanf`.",
    ),

    # Módulo 13 — Dividindo o programa em partes
    ".h": _licao(
        "`#include \"arquivo.h\"` (aspas) procura primeiro na pasta do projeto; `#include "
        "<arquivo.h>` procura nas pastas do sistema. Um cabeçalho deve ter só declarações: se "
        "tiver a definição de uma função, incluí-lo em dois .c gera \"multiple definition\" no "
        "linker. Para compartilhar uma variável global, declare `extern int total;` no .h e "
        "defina `int total;` em um único .c.",
        saida="42 42\n",
        passos=[
            "O bloco de protótipos representa o conteúdo de calculos.h: só declarações.",
            "main usa `dobro` e `metade` conhecendo apenas as assinaturas.",
            "As definições, que ficariam em calculos.c, aparecem no fim.",
            "Em um projeto real, main.c teria `#include \"calculos.h\"` no lugar dos protótipos.",
        ],
    ),
    ".c": _licao(
        "Com vários arquivos, o comando fica `gcc main.c calculos.c -o programa`, ou em etapas: "
        "`gcc -c calculos.c` gera calculos.o e `gcc main.o calculos.o -o programa` liga tudo. "
        "Assim, ao mudar um arquivo, só ele precisa ser recompilado. Funções usadas apenas dentro"
        " de um .c devem ser `static`, o que as esconde dos outros arquivos e evita conflitos de "
        "nomes.",
        saida="42\n",
    ),
    "include guards": _licao(
        "Guards evitam erros de redefinição quando um cabeçalho chega por vários caminhos (a.h "
        "inclui b.h e main.c inclui os dois). O nome da macro precisa ser único no projeto; em "
        "geral é o nome do arquivo em maiúsculas. Muitos compiladores aceitam `#pragma once`, "
        "mais curto, mas ele não faz parte do padrão C.",
        saida="42\n",
    ),

    # Módulo 14 — Usando recursos prontos
    "stdio": _licao(
        "Três correntes já vêm abertas: stdin (teclado), stdout (tela) e stderr (erros). No "
        "terminal, a saída pode ser redirecionada: `./programa > saida.txt` grava o stdout em "
        "arquivo, enquanto o stderr continua na tela. Outras funções úteis: `puts` (texto e "
        "quebra de linha), `putchar` e `getchar` (um caractere), `snprintf` (formata dentro de "
        "uma string) e `sscanf` (lê de uma string).",
        saida="Saida padrao: 42\n",
    ),
    "stdlib": _licao(
        "`atoi` também converte, mas devolve 0 tanto para \"abc\" quanto para \"0\", sem diferenciar;"
        " strtol permite detectar o erro. stdlib.h traz ainda malloc e free, `rand` e `srand` "
        "(números pseudoaleatórios), `abs`, `qsort` (ordenação de qualquer tipo), `exit` e as "
        "constantes `EXIT_SUCCESS` e `EXIT_FAILURE`, que podem substituir 0 e 1 no return de "
        "main.",
    ),
    "string": _licao(
        "Além das funções de texto, string.h tem funções de memória: `memset` preenche bytes "
        "(`memset(v, 0, sizeof v)` zera um array), `memcpy` copia blocos e `memcmp` compara "
        "bytes. `strchr` e `strstr` procuram um caractere ou um trecho dentro de uma string e "
        "devolvem um ponteiro para a posição encontrada, ou NULL.",
        saida="C11: correto\n",
    ),
    "math": _licao(
        "Com GCC, programas que usam math.h podem precisar de `-lm` no fim do comando para ligar "
        "a biblioteca matemática; o compilador do site já usa essa opção. Outras funções: "
        "`pow(base, expoente)`, `fabs` (valor absoluto de double), `floor` e `ceil` (arredondar "
        "para baixo e para cima), `round`, `sin` e `cos` (ângulos em radianos). A raiz de um "
        "número negativo resulta em NaN (\"não é um número\").",
        saida="5\n",
    ),

    # Módulo 15 — Como o computador guarda informações
    "bitwise": _licao(
        "Os operadores bit a bit são `&` (E), `|` (OU), `^` (OU exclusivo), `~` (inverte todos os"
        " bits) e os deslocamentos `<<` e `>>`. `x >> 1` divide por 2 descartando o resto, e `x &"
        " 1` diz se x é ímpar. Prefira tipos unsigned: deslocar números negativos, ou deslocar "
        "mais bits do que o tipo tem, é comportamento indefinido ou depende do compilador.",
        saida="42\n",
    ),
    "máscaras": _licao(
        "As quatro operações com máscaras: ligar (`flags |= BIT`), desligar (`flags &= ~BIT`), "
        "inverter (`flags ^= BIT`) e testar (`(flags & BIT) != 0`). As permissões de arquivos do "
        "Linux (rwx, como em `chmod 755`) usam exatamente essa ideia. Um único unsigned de 32 "
        "bits guarda 32 opções de liga e desliga.",
        saida="Pode executar\n",
    ),

    # Módulo 16 — Encontrando e corrigindo erros
    "erros de sintaxe": _licao(
        "As mensagens do GCC seguem o formato `arquivo:linha:coluna: error: descrição`. As mais "
        "comuns: \"expected ';'\" (falta ponto e vírgula, geralmente no fim da linha anterior), "
        "\"expected declaration or statement at end of input\" (falta fechar uma `}`), \"undeclared\""
        " (variável não declarada ou nome digitado errado) e \"implicit declaration of function\" "
        "(falta um #include ou protótipo). A Consulta rápida do site tem uma tabela com essas "
        "mensagens.",
        saida="42\n",
    ),
    "erros lógicos": _licao(
        "Erros lógicos só aparecem testando: calcule à mão o resultado esperado de alguns casos e"
        " compare com a saída. Os clássicos são precedência de operadores, divisão inteira (`7 / "
        "2` dá 3), laço que roda uma vez a mais ou a menos (`<=` no lugar de `<`) e `=` no lugar "
        "de `==`. Casos de fronteira, como 0, negativos e lista vazia, revelam boa parte deles.",
        saida="10.00\n",
    ),
    "debug": _licao(
        "Depois de achar o problema, remova os printf de depuração ou use `fprintf(stderr, ...)` "
        "para separá-los da saída normal. Para investigar sem mudar o código, use um depurador: "
        "compile com `gcc -g programa.c -o programa` e rode `gdb ./programa`; os comandos `break "
        "main`, `next`, `print total` e `continue` percorrem o programa linha a linha. A opção "
        "`-fsanitize=address,undefined` detecta acessos inválidos no momento em que acontecem.",
        saida="i=0 total=10\ni=1 total=30\ni=2 total=42\n",
    ),

    # Módulo 17 — Transformando código em programa
    "gcc": _licao(
        "Outras opções úteis: `-g` (informações para o depurador), `-O2` (otimiza o executável), "
        "`-Werror` (trata avisos como erros), `-fsanitize=address` (detecta erros de memória "
        "durante a execução) e `-lm` (liga a biblioteca matemática). O compilador do site usa "
        "`-std=c11 -Wall -Wextra -pedantic`, então os avisos que aparecem aqui são os mesmos que "
        "você veria no seu computador.",
        saida="Programa C11 compilado com avisos habilitados.\n",
    ),
    "linking": _licao(
        "Se a definição de `resposta` for apagada, a compilação ainda passa, mas a ligação falha "
        "com \"undefined reference\" apontando para `resposta`. O erro inverso, \"multiple "
        "definition\", acontece quando a mesma função é definida em dois .c. Bibliotecas externas "
        "são ligadas com `-l`, como `-lm` para a matemática, e vêm depois dos arquivos que as "
        "usam.",
        saida="42\n",
    ),
    "makefile": _licao(
        "Um Makefile mínimo tem uma variável como `CFLAGS = -std=c11 -Wall -Wextra`, a regra "
        "`programa: main.c calculos.c` e, na linha seguinte, começando com uma tabulação, o "
        "comando `$(CC) $(CFLAGS) main.c calculos.c -o programa`. `make` compara as datas dos "
        "arquivos: se nada mudou, não recompila. É comum ter também um alvo `clean` que apaga os "
        "arquivos gerados. Em projetos maiores, ferramentas como o CMake geram os Makefiles.",
        saida="gcc -std=c11 -Wall main.c -o programa\n",
    ),

    # Módulo 18 — Escrevendo programas seguros
    "buffer overflow": _licao(
        "Sem o limite (`%s`), as letras extras seriam escritas depois do fim do array, "
        "sobrescrevendo outras variáveis ou o endereço de retorno da função: essa é a base de "
        "muitos ataques famosos. O compilador ajuda com proteções (stack protector, "
        "`-D_FORTIFY_SOURCE`), mas a responsabilidade é do código. Regra prática: sempre informe "
        "o tamanho (`%9s`, `fgets(buf, sizeof buf, stdin)`, `snprintf`) e confira índices antes "
        "de escrever em arrays.",
        saida="Uma palavra: Recebido: compilado\n",
        entrada="compilador\n",
    ),
    "validação": _licao(
        "O exemplo usa a abordagem mais robusta: lê a linha inteira com fgets, recusa linhas "
        "longas demais, converte com strtol e confere se havia dígitos, se sobrou texto depois do"
        " número e se o valor estourou (`errno == ERANGE`). Com scanf, uma entrada inválida fica "
        "parada na entrada e precisa ser descartada antes de tentar de novo: `int c; while ((c = "
        "getchar()) != '\\n' && c != EOF) {}`. Valide tudo o que vem de fora do programa: teclado,"
        " arquivos e rede. Teste com letras, negativos, os limites exatos (0 e 120), espaços "
        "antes e depois e números enormes.",
    ),

    # Módulo 19 — Organizando muitos dados
    "listas": _licao(
        "O exemplo insere cada nó novo no início da lista: é rápido (só troca dois ponteiros), "
        "mas deixa os valores na ordem inversa da leitura, por isso a lista fica 10 → 20 → 12. "
        "Para manter a ordem, guarde também um ponteiro para o último nó e insira no fim. Achar o"
        " n-ésimo elemento exige percorrer a lista desde o início, o contrário do array. A função"
        " `liberar` guarda o próximo antes do free, porque depois de liberar um nó não se pode "
        "mais ler `atual->proximo`.",
        memoria=(
            "Cada nó foi criado com malloc; o último inserido fica no início.",
            [
                ("inicio", "0x1000 (pilha)", "0x5040", "primeiro nó da lista"),
                ("nó 10", "0x5040 (heap)", "{10, 0x5020}", "inserido por último"),
                ("nó 20", "0x5020 (heap)", "{20, 0x5000}", ""),
                ("nó 12", "0x5000 (heap)", "{12, NULL}", "inserido primeiro; NULL marca o fim"),
            ],
        ),
    ),
    "pilhas": _licao(
        "Pilha é LIFO: o último a entrar é o primeiro a sair, como uma pilha de pratos. O exemplo"
        " guarda os dados e a quantidade em uma struct e faz `push` e `pop` devolverem 1 ou 0: "
        "assim quem chama sabe se a operação aconteceu, e a pilha nunca escreve além do array nem"
        " lê uma posição vazia. Pilhas aparecem no desfazer dos editores, no botão voltar do "
        "navegador, na verificação de parênteses balanceados e na própria pilha de chamadas de "
        "funções.",
    ),
    "filas": _licao(
        "Fila é FIFO: o primeiro a entrar é o primeiro a sair, como uma fila de banco. O exemplo "
        "é uma fila circular: `(inicio + quantidade) % CAPACIDADE` calcula onde entra o próximo, "
        "e o `%` faz o índice voltar ao começo do array, reaproveitando as posições liberadas; "
        "por isso, depois de remover o 10, ainda cabe o 30. Guardar a quantidade separada evita "
        "confundir fila cheia com fila vazia. Filas organizam impressões, mensagens entre "
        "programas e a busca em largura em grafos.",
    ),
    "árvores": _licao(
        "Em uma árvore binária de busca equilibrada, procurar um valor descarta metade da árvore "
        "a cada passo: com 1 milhão de itens, cerca de 20 comparações. Se os dados entram já "
        "ordenados, a árvore vira uma \"lista torta\" e perde essa vantagem; árvores balanceadas "
        "(AVL, rubro-negra) corrigem isso. Outros percursos: pré-ordem (nó, esquerda, direita) e "
        "pós-ordem (esquerda, direita, nó), usada para liberar a árvore.",
        saida="10 20 42 \n",
    ),

    # Módulo 20 — Resolvendo problemas melhor
    "busca linear": _licao(
        "No pior caso a busca linear olha os n elementos: ela é O(n) e funciona em qualquer "
        "array, ordenado ou não. Devolver a posição (ou -1) em vez de imprimir dentro da função, "
        "como faz `buscar`, permite reaproveitá-la para editar, remover ou mostrar o item "
        "encontrado; `const int valores[]` indica que a busca só lê o array. Em arrays ordenados,"
        " a busca binária é muito mais rápida (O(log n)), e `bsearch` da stdlib já a implementa.",
    ),
    "bubble sort": _licao(
        "Bubble sort faz cerca de n²/2 comparações (O(n²)): ótimo para aprender, lento para "
        "muitos dados. Uma melhoria simples é parar quando uma passada inteira não fizer nenhuma "
        "troca. Na prática, use `qsort` da stdlib, que ordena qualquer tipo com uma função de "
        "comparação, ou algoritmos O(n log n) como merge sort e quicksort.",
        saida="1 2 3\n",
    ),
    "eficiência": _licao(
        "A notação O descreve como o tempo cresce com a entrada: O(1) constante, O(log n) na "
        "busca binária, O(n) em um laço, O(n log n) nas boas ordenações e O(n²) em dois laços "
        "aninhados. Com 1 milhão de itens, O(n) faz cerca de 1 milhão de passos e O(n²) cerca de "
        "1 trilhão. Antes de otimizar detalhes, escolha o algoritmo certo e evite trabalho "
        "repetido dentro de laços.",
        saida="Pares: 3\n",
    ),

    # Módulo 21 — Criando programas completos
    "calculadora": _licao(
        "A função `calcular` separa a regra da entrada e da saída: devolve 1 ou 0 para sucesso e "
        "grava o resultado por ponteiro, então pode ser testada sem teclado. `isfinite`, de "
        "`<math.h>`, recusa resultados como infinito, que aparecem com números enormes. Comparar "
        "`b == 0.0` é aceitável aqui porque o objetivo é só impedir a divisão por zero. Para "
        "fazer várias contas, coloque a leitura em um laço com uma opção de saída e descarte a "
        "linha quando a entrada for inválida.",
    ),
    "cadastro": _licao(
        "O exemplo guarda a capacidade separada da quantidade usada e valida tudo antes de "
        "gravar: nome vazio, nome grande demais para o campo e idade fora da faixa são recusados "
        "sem alterar o cadastro. As operações clássicas (CRUD) são criar, listar, atualizar e "
        "remover; para remover do meio do array, desloque os registros seguintes uma posição para"
        " trás. Para os dados sobreviverem ao fim do programa, grave em arquivo com fprintf e "
        "leia de volta com fgets (módulo 12).",
    ),
    "agenda": _licao(
        "Telefones são guardados como texto, não como número: podem ter zeros à esquerda, traços "
        "e parênteses. Com vários contatos, a busca percorre o array comparando nomes; para "
        "ignorar maiúsculas, compare cópias convertidas com `tolower`. Leia nomes com fgets para "
        "aceitar espaços e confira o limite do array antes de adicionar um contato novo.",
    ),
    "jogo terminal": _licao(
        "O exemplo usa um segredo fixo para que a saída seja previsível. Para sortear, chame "
        "`srand((unsigned)time(NULL));` uma vez no início e use `rand() % 20 + 1` (inclua "
        "`<stdlib.h>` e `<time.h>`). Um contador de tentativas com limite máximo deixa o jogo "
        "mais interessante. Repare na estrutura: estado (segredo e palpite), entrada (ler), "
        "atualização (comparar) e saída (mensagens), o mesmo ciclo de jogos maiores; palpites "
        "fora da faixa usam `continue` para pedir outro sem encerrar.",
    ),
    "sistema biblioteca": _licao(
        "O estado do livro é uma pequena máquina de estados: DISPONIVEL → EMPRESTADO → "
        "DISPONIVEL. As funções só aceitam as transições válidas e devolvem 0 nas outras, então "
        "um livro emprestado não pode ser emprestado de novo. Para crescer, acrescente um estado "
        "RESERVADO, um array de livros buscado pelo `id` e o registro de quem pegou cada livro. "
        "Separar as regras das mensagens permite testá-las isoladamente, como o exemplo faz com "
        "as quatro chamadas.",
    ),
    "editor texto": _licao(
        "Um editor simples guarda o documento como um array de linhas (`char linhas[100][81]`) e "
        "oferece comandos como inserir, apagar e procurar (`strstr`). Todo ponto que escreve "
        "texto precisa conferir o tamanho, como o exemplo faz. Para salvar e abrir, grave cada "
        "linha com fprintf e leia com fgets.",
        saida="Aprender C\n",
    ),
    "projeto final": _licao(
        "Para um projeto maior: escreva primeiro o que o programa deve fazer, divida em funções "
        "pequenas, teste cada uma com valores conhecidos e só então junte tudo em main. Compile "
        "com `-Wall -Wextra` e corrija todos os avisos. Guarde versões com Git para poder voltar "
        "atrás. Um bom projeto final combina structs, arrays, funções, arquivos e validação de "
        "entrada.",
    ),
}
