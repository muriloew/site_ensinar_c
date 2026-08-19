"""Desafios teoricos extras separados por modulo."""


DESAFIOS_TEORICOS_MODULO = {
    1: [
        {
            "pergunta": "O que acontece com um programa em C antes de ele ser executado?",
            "alternativas": [
                "Ele precisa ser compilado para virar um executavel.",
                "Ele roda diretamente como texto, sem traducao.",
                "Ele so funciona dentro do navegador.",
                "Ele ignora a funcao main."
            ],
            "resposta": "Ele precisa ser compilado para virar um executavel.",
            "explicacao": "C e uma linguagem compilada: o codigo-fonte passa por compilacao antes de executar."
        },
        {
            "pergunta": "Qual funcao marca o inicio da execucao de um programa C?",
            "alternativas": ["main", "printf", "include", "return"],
            "resposta": "main",
            "explicacao": "A execucao do programa comeca na funcao main."
        },
        {
            "pergunta": "Para que servem os comentarios no codigo?",
            "alternativas": [
                "Para explicar ideias sem alterar a execucao.",
                "Para substituir comandos obrigatorios.",
                "Para corrigir erros automaticamente.",
                "Para criar variaveis."
            ],
            "resposta": "Para explicar ideias sem alterar a execucao.",
            "explicacao": "Comentarios ajudam quem le o codigo, mas nao sao executados."
        }
    ],
    2: [
        {
            "pergunta": "Qual comando e usado para mostrar uma mensagem na tela?",
            "alternativas": ["printf", "scanf", "int", "return"],
            "resposta": "printf",
            "explicacao": "printf envia texto e valores para a saida do programa."
        },
        {
            "pergunta": "No scanf, por que usamos & antes de uma variavel int?",
            "alternativas": [
                "Para informar o endereco onde o valor sera guardado.",
                "Para somar dois numeros.",
                "Para pular uma linha.",
                "Para transformar int em texto."
            ],
            "resposta": "Para informar o endereco onde o valor sera guardado.",
            "explicacao": "scanf precisa do endereco da variavel para conseguir gravar o valor lido."
        },
        {
            "pergunta": "Qual especificador costuma ser usado para imprimir um int?",
            "alternativas": ["%d", "%f", "%s", "%c"],
            "resposta": "%d",
            "explicacao": "%d e usado para valores inteiros do tipo int."
        }
    ],
    3: [
        {
            "pergunta": "O que uma variavel faz em um programa?",
            "alternativas": [
                "Guarda uma informacao para ser usada depois.",
                "Apaga automaticamente todos os erros.",
                "Compila o programa.",
                "Cria uma nova biblioteca."
            ],
            "resposta": "Guarda uma informacao para ser usada depois.",
            "explicacao": "Variaveis armazenam valores, como numeros, letras e resultados."
        },
        {
            "pergunta": "Qual tipo e indicado para numeros inteiros?",
            "alternativas": ["int", "char", "double", "void"],
            "resposta": "int",
            "explicacao": "int guarda numeros inteiros, como 1, 20 ou -5."
        },
        {
            "pergunta": "Quando usamos const?",
            "alternativas": [
                "Quando um valor nao deve ser alterado depois de definido.",
                "Quando queremos ler o teclado.",
                "Quando queremos repetir um bloco.",
                "Quando queremos fechar um arquivo."
            ],
            "resposta": "Quando um valor nao deve ser alterado depois de definido.",
            "explicacao": "const deixa claro que aquele valor e fixo dentro do programa."
        }
    ],
    4: [
        {
            "pergunta": "Qual operador faz multiplicacao em C?",
            "alternativas": ["*", "+", "==", "&&"],
            "resposta": "*",
            "explicacao": "O asterisco e usado para multiplicar valores numericos."
        },
        {
            "pergunta": "Qual e a diferenca principal entre = e ==?",
            "alternativas": [
                "= atribui valor, == compara valores.",
                "= compara valores, == soma valores.",
                "Os dois fazem exatamente a mesma coisa.",
                "== serve apenas para textos."
            ],
            "resposta": "= atribui valor, == compara valores.",
            "explicacao": "Esse e um erro comum: atribuicao e comparacao sao operacoes diferentes."
        },
        {
            "pergunta": "O operador && significa que:",
            "alternativas": [
                "As duas condicoes precisam ser verdadeiras.",
                "Apenas uma condicao precisa ser verdadeira.",
                "A variavel deve ser apagada.",
                "O programa deve terminar."
            ],
            "resposta": "As duas condicoes precisam ser verdadeiras.",
            "explicacao": "&& representa E logico."
        }
    ],
    5: [
        {
            "pergunta": "Quando o bloco de um if e executado?",
            "alternativas": [
                "Quando a condicao e verdadeira.",
                "Sempre que o programa compila.",
                "Somente depois de um for.",
                "Quando a variavel tem nome curto."
            ],
            "resposta": "Quando a condicao e verdadeira.",
            "explicacao": "if permite executar um bloco apenas se uma condicao for atendida."
        },
        {
            "pergunta": "Para que serve o else?",
            "alternativas": [
                "Para definir o caminho quando o if e falso.",
                "Para declarar uma variavel.",
                "Para ler um numero.",
                "Para criar uma funcao."
            ],
            "resposta": "Para definir o caminho quando o if e falso.",
            "explicacao": "else representa o caso alternativo da decisao."
        },
        {
            "pergunta": "Em um switch, por que o break costuma ser usado?",
            "alternativas": [
                "Para evitar que a execucao continue nos proximos cases.",
                "Para repetir o mesmo case.",
                "Para transformar char em int.",
                "Para abrir um arquivo."
            ],
            "resposta": "Para evitar que a execucao continue nos proximos cases.",
            "explicacao": "Sem break, o programa pode continuar executando os cases seguintes."
        }
    ],
    6: [
        {
            "pergunta": "Quando o while testa a condicao?",
            "alternativas": [
                "Antes de executar o bloco.",
                "Somente depois de terminar o programa.",
                "Nunca testa condicao.",
                "Apenas dentro de funcoes."
            ],
            "resposta": "Antes de executar o bloco.",
            "explicacao": "while pode executar zero vezes se a condicao ja comecar falsa."
        },
        {
            "pergunta": "Qual estrutura combina bem com repeticao por contador?",
            "alternativas": ["for", "struct", "typedef", "fopen"],
            "resposta": "for",
            "explicacao": "for costuma reunir inicio, condicao e atualizacao do contador."
        },
        {
            "pergunta": "O que o break faz dentro de um laco?",
            "alternativas": [
                "Interrompe a repeticao atual.",
                "Cria uma nova variavel.",
                "Le dados do teclado.",
                "Compara duas strings."
            ],
            "resposta": "Interrompe a repeticao atual.",
            "explicacao": "break sai do laco antes da repeticao terminar naturalmente."
        }
    ],
    7: [
        {
            "pergunta": "Por que criar funcoes?",
            "alternativas": [
                "Para organizar e reutilizar partes do codigo.",
                "Para impedir qualquer erro de compilacao.",
                "Para substituir todos os tipos de variaveis.",
                "Para executar apenas no navegador."
            ],
            "resposta": "Para organizar e reutilizar partes do codigo.",
            "explicacao": "Funcoes deixam programas maiores mais organizados."
        },
        {
            "pergunta": "O que sao parametros?",
            "alternativas": [
                "Valores recebidos por uma funcao.",
                "Arquivos criados pelo compilador.",
                "Erros do sistema operacional.",
                "Bibliotecas obrigatorias."
            ],
            "resposta": "Valores recebidos por uma funcao.",
            "explicacao": "Parametros permitem enviar informacoes para uma funcao trabalhar."
        },
        {
            "pergunta": "Para que serve return em uma funcao que devolve valor?",
            "alternativas": [
                "Para entregar um resultado ao ponto de chamada.",
                "Para declarar um ponteiro.",
                "Para limpar a tela.",
                "Para iniciar um array."
            ],
            "resposta": "Para entregar um resultado ao ponto de chamada.",
            "explicacao": "return encerra a funcao e pode devolver um valor."
        }
    ],
    8: [
        {
            "pergunta": "Em C, qual e o indice do primeiro elemento de um array?",
            "alternativas": ["0", "1", "10", "-1"],
            "resposta": "0",
            "explicacao": "Arrays em C comecam na posicao zero."
        },
        {
            "pergunta": "Uma string em C normalmente termina com:",
            "alternativas": ["\\0", "\\n", "%d", "main"],
            "resposta": "\\0",
            "explicacao": "O caractere nulo marca o fim da string."
        },
        {
            "pergunta": "Por que fgets costuma ser mais segura que scanf(\"%s\", ...)?",
            "alternativas": [
                "Porque permite informar o tamanho do buffer.",
                "Porque nao precisa de variavel.",
                "Porque ordena o texto automaticamente.",
                "Porque so funciona com int."
            ],
            "resposta": "Porque permite informar o tamanho do buffer.",
            "explicacao": "Informar o tamanho ajuda a evitar escrita fora do limite."
        }
    ],
    9: [
        {
            "pergunta": "O operador & aplicado a uma variavel retorna:",
            "alternativas": ["O endereco dela", "O dobro dela", "O tipo dela", "O nome dela"],
            "resposta": "O endereco dela",
            "explicacao": "& permite descobrir onde a variavel esta na memoria."
        },
        {
            "pergunta": "O que significa desreferenciar um ponteiro?",
            "alternativas": [
                "Acessar o valor guardado no endereco apontado.",
                "Apagar o programa.",
                "Criar uma string.",
                "Fechar um arquivo."
            ],
            "resposta": "Acessar o valor guardado no endereco apontado.",
            "explicacao": "O operador * permite acessar o valor apontado."
        },
        {
            "pergunta": "Por que ponteiros exigem cuidado?",
            "alternativas": [
                "Porque podem apontar para locais invalidos da memoria.",
                "Porque nao podem ser usados em funcoes.",
                "Porque substituem todos os arrays.",
                "Porque sempre deixam o programa mais lento."
            ],
            "resposta": "Porque podem apontar para locais invalidos da memoria.",
            "explicacao": "Um ponteiro incorreto pode causar falhas e comportamento indefinido."
        }
    ],
    10: [
        {
            "pergunta": "malloc reserva memoria em qual regiao usada para alocacao dinamica?",
            "alternativas": ["heap", "stdin", "printf", "enum"],
            "resposta": "heap",
            "explicacao": "A memoria dinamica e reservada na heap."
        },
        {
            "pergunta": "Depois de usar memoria alocada com malloc, devemos:",
            "alternativas": ["chamar free", "chamar printf", "usar break", "trocar por char"],
            "resposta": "chamar free",
            "explicacao": "free libera a memoria reservada dinamicamente."
        },
        {
            "pergunta": "O que e memory leak?",
            "alternativas": [
                "Memoria alocada que nao foi liberada.",
                "Erro de acento no texto.",
                "Uma forma de comentario.",
                "Uma biblioteca padrao."
            ],
            "resposta": "Memoria alocada que nao foi liberada.",
            "explicacao": "Vazamentos acumulam memoria perdida durante a execucao."
        }
    ],
    11: [
        {
            "pergunta": "Para que serve uma struct?",
            "alternativas": [
                "Para agrupar dados relacionados em um tipo.",
                "Para repetir comandos automaticamente.",
                "Para compilar arquivos.",
                "Para ler apenas numeros inteiros."
            ],
            "resposta": "Para agrupar dados relacionados em um tipo.",
            "explicacao": "struct junta campos diferentes em uma mesma estrutura."
        },
        {
            "pergunta": "typedef e usado principalmente para:",
            "alternativas": [
                "Criar um nome alternativo para um tipo.",
                "Somar dois arrays.",
                "Abrir arquivos.",
                "Executar o programa."
            ],
            "resposta": "Criar um nome alternativo para um tipo.",
            "explicacao": "typedef pode deixar tipos compostos mais simples de usar."
        },
        {
            "pergunta": "enum ajuda a representar:",
            "alternativas": [
                "Estados ou opcoes com nomes legiveis.",
                "Textos longos sem tamanho.",
                "Arquivos de imagem.",
                "Memoria alocada automaticamente."
            ],
            "resposta": "Estados ou opcoes com nomes legiveis.",
            "explicacao": "enum troca numeros soltos por nomes com significado."
        }
    ],
    12: [
        {
            "pergunta": "Qual funcao abre um arquivo em C?",
            "alternativas": ["fopen", "printf", "strlen", "malloc"],
            "resposta": "fopen",
            "explicacao": "fopen tenta abrir um arquivo e retorna um ponteiro FILE."
        },
        {
            "pergunta": "Por que devemos chamar fclose?",
            "alternativas": [
                "Para fechar o arquivo e finalizar a gravacao/leitura corretamente.",
                "Para declarar uma variavel.",
                "Para criar um loop.",
                "Para comparar dois numeros."
            ],
            "resposta": "Para fechar o arquivo e finalizar a gravacao/leitura corretamente.",
            "explicacao": "Fechar o arquivo evita perda de dados e libera recursos."
        },
        {
            "pergunta": "fprintf e usado para:",
            "alternativas": [
                "Escrever texto formatado em um arquivo.",
                "Ler o teclado sem variavel.",
                "Criar uma struct.",
                "Liberar memoria."
            ],
            "resposta": "Escrever texto formatado em um arquivo.",
            "explicacao": "fprintf funciona como printf, mas escreve em um arquivo."
        }
    ],
    13: [
        {
            "pergunta": "O que costuma ficar em um arquivo .h?",
            "alternativas": [
                "Declaracoes e prototipos compartilhados.",
                "A senha do usuario.",
                "Somente imagens.",
                "O resultado final compilado."
            ],
            "resposta": "Declaracoes e prototipos compartilhados.",
            "explicacao": "Cabecalhos informam como outros arquivos podem usar funcoes e tipos."
        },
        {
            "pergunta": "O que costuma ficar em um arquivo .c?",
            "alternativas": [
                "Implementacoes das funcoes.",
                "Apenas comentarios.",
                "Somente dados do Git.",
                "O historico do navegador."
            ],
            "resposta": "Implementacoes das funcoes.",
            "explicacao": "Arquivos .c guardam codigo-fonte compilavel."
        },
        {
            "pergunta": "Include guards evitam:",
            "alternativas": [
                "Inclusao duplicada do mesmo cabecalho.",
                "Entrada de dados pelo usuario.",
                "Uso de printf.",
                "Criacao de variaveis locais."
            ],
            "resposta": "Inclusao duplicada do mesmo cabecalho.",
            "explicacao": "Eles protegem o arquivo .h contra repeticoes no mesmo build."
        }
    ],
    14: [
        {
            "pergunta": "Qual biblioteca traz printf e scanf?",
            "alternativas": ["stdio.h", "math.h", "time.h", "limits.h"],
            "resposta": "stdio.h",
            "explicacao": "stdio.h contem funcoes de entrada e saida padrao."
        },
        {
            "pergunta": "Qual biblioteca traz strlen, strcpy e strcmp?",
            "alternativas": ["string.h", "stdlib.h", "stdio.h", "float.h"],
            "resposta": "string.h",
            "explicacao": "string.h reune funcoes de manipulacao de strings."
        },
        {
            "pergunta": "stdlib.h e util para:",
            "alternativas": [
                "Alocacao dinamica e conversoes.",
                "Criar comentarios.",
                "Trocar a cor do terminal.",
                "Definir a funcao main."
            ],
            "resposta": "Alocacao dinamica e conversoes.",
            "explicacao": "stdlib.h inclui malloc, free, strtol e outras utilidades."
        }
    ],
    15: [
        {
            "pergunta": "Operadores bitwise trabalham com:",
            "alternativas": ["bits individuais", "linhas de texto", "arquivos HTML", "senhas"],
            "resposta": "bits individuais",
            "explicacao": "Eles atuam diretamente na representacao binaria dos valores."
        },
        {
            "pergunta": "Uma mascara de bits serve para:",
            "alternativas": [
                "Selecionar, ativar ou testar bits especificos.",
                "Apagar todos os arquivos.",
                "Criar uma string automaticamente.",
                "Substituir a funcao main."
            ],
            "resposta": "Selecionar, ativar ou testar bits especificos.",
            "explicacao": "Mascaras ajudam a manipular flags e permissoes."
        },
        {
            "pergunta": "Para deslocamentos de bits, costuma ser mais previsivel usar:",
            "alternativas": ["tipos unsigned", "scanf", "strings vazias", "arquivos .h"],
            "resposta": "tipos unsigned",
            "explicacao": "unsigned evita algumas ambiguidades com sinal em operacoes de baixo nivel."
        }
    ],
    16: [
        {
            "pergunta": "Um erro de sintaxe acontece quando:",
            "alternativas": [
                "O codigo viola as regras da linguagem.",
                "O programa roda, mas calcula errado.",
                "O usuario esquece a senha.",
                "O arquivo esta bonito."
            ],
            "resposta": "O codigo viola as regras da linguagem.",
            "explicacao": "Erros de sintaxe impedem a compilacao."
        },
        {
            "pergunta": "Um erro logico acontece quando:",
            "alternativas": [
                "O codigo compila, mas o resultado esta errado.",
                "Falta um ponto e virgula.",
                "A biblioteca nao existe.",
                "O computador esta desligado."
            ],
            "resposta": "O codigo compila, mas o resultado esta errado.",
            "explicacao": "Erros logicos precisam de testes e observacao do comportamento."
        },
        {
            "pergunta": "Ao receber varias mensagens do compilador, e melhor comecar por:",
            "alternativas": [
                "A primeira mensagem relevante.",
                "A ultima linha do arquivo sempre.",
                "Ignorar todas.",
                "Trocar o nome do projeto."
            ],
            "resposta": "A primeira mensagem relevante.",
            "explicacao": "Erros posteriores podem ser consequencia do primeiro problema."
        }
    ],
    17: [
        {
            "pergunta": "O que o GCC faz?",
            "alternativas": [
                "Compila codigo C para gerar um programa.",
                "Edita imagens.",
                "Cria uma conta de usuario.",
                "Substitui o sistema operacional."
            ],
            "resposta": "Compila codigo C para gerar um programa.",
            "explicacao": "GCC e um compilador muito usado para C."
        },
        {
            "pergunta": "Linking e a etapa que:",
            "alternativas": [
                "Junta objetos e bibliotecas para formar o executavel.",
                "Compara dois textos.",
                "Le a entrada do teclado.",
                "Formata uma string."
            ],
            "resposta": "Junta objetos e bibliotecas para formar o executavel.",
            "explicacao": "A ligacao resolve referencias entre partes do programa."
        },
        {
            "pergunta": "Um Makefile ajuda a:",
            "alternativas": [
                "Automatizar comandos de build.",
                "Trocar printf por scanf.",
                "Criar variaveis globais.",
                "Remover a necessidade de compilar."
            ],
            "resposta": "Automatizar comandos de build.",
            "explicacao": "Makefiles organizam comandos para recompilar projetos."
        }
    ],
    18: [
        {
            "pergunta": "Validar entrada significa:",
            "alternativas": [
                "Conferir se o dado recebido faz sentido antes de usar.",
                "Aceitar qualquer texto sempre.",
                "Ignorar o retorno de scanf.",
                "Remover todas as variaveis."
            ],
            "resposta": "Conferir se o dado recebido faz sentido antes de usar.",
            "explicacao": "Validacao evita estados inesperados e falhas."
        },
        {
            "pergunta": "Buffer overflow acontece quando:",
            "alternativas": [
                "Um dado ultrapassa o espaco reservado.",
                "Um loop termina normalmente.",
                "Um comentario tem acento.",
                "Um int recebe numero pequeno."
            ],
            "resposta": "Um dado ultrapassa o espaco reservado.",
            "explicacao": "Escrever fora do limite pode corromper memoria."
        },
        {
            "pergunta": "Uma boa pratica ao ler strings com scanf e:",
            "alternativas": [
                "Usar limite de tamanho no formato.",
                "Nao reservar vetor.",
                "Sempre usar %d.",
                "Ignorar o tamanho do buffer."
            ],
            "resposta": "Usar limite de tamanho no formato.",
            "explicacao": "Exemplo: %9s para um vetor com espaco para 10 caracteres."
        }
    ],
    19: [
        {
            "pergunta": "Uma pilha segue qual ordem?",
            "alternativas": ["LIFO: ultimo a entrar, primeiro a sair", "FIFO", "Ordem alfabetica", "Ordem aleatoria"],
            "resposta": "LIFO: ultimo a entrar, primeiro a sair",
            "explicacao": "Pilha funciona como uma pilha de pratos."
        },
        {
            "pergunta": "Uma fila segue qual ordem?",
            "alternativas": ["FIFO: primeiro a entrar, primeiro a sair", "LIFO", "Sempre decrescente", "Sempre por ponteiro duplo"],
            "resposta": "FIFO: primeiro a entrar, primeiro a sair",
            "explicacao": "Fila funciona como uma fila de atendimento."
        },
        {
            "pergunta": "Listas encadeadas usam nos que geralmente guardam:",
            "alternativas": [
                "Um valor e uma referencia para o proximo no.",
                "Apenas comentarios.",
                "Somente arquivos.",
                "A senha do sistema."
            ],
            "resposta": "Um valor e uma referencia para o proximo no.",
            "explicacao": "Cada no aponta para outro, formando a sequencia."
        }
    ],
    20: [
        {
            "pergunta": "A busca linear procura um item:",
            "alternativas": [
                "Verificando elemento por elemento.",
                "Apenas olhando o ultimo elemento.",
                "Sem acessar dados.",
                "Somente usando arquivos."
            ],
            "resposta": "Verificando elemento por elemento.",
            "explicacao": "Ela funciona mesmo quando os dados nao estao ordenados."
        },
        {
            "pergunta": "Bubble sort ordena dados trocando:",
            "alternativas": [
                "Elementos vizinhos fora de ordem.",
                "Bibliotecas do sistema.",
                "Nomes de variaveis.",
                "Arquivos .h por .c."
            ],
            "resposta": "Elementos vizinhos fora de ordem.",
            "explicacao": "Ele repete trocas ate a lista ficar ordenada."
        },
        {
            "pergunta": "Eficiencia em algoritmos observa principalmente:",
            "alternativas": [
                "Como tempo e memoria crescem com a entrada.",
                "A cor do editor.",
                "O nome do computador.",
                "A quantidade de comentarios apenas."
            ],
            "resposta": "Como tempo e memoria crescem com a entrada.",
            "explicacao": "Um algoritmo pode funcionar, mas ficar lento quando os dados aumentam."
        }
    ],
    21: [
        {
            "pergunta": "Por que criar projetos praticos no final?",
            "alternativas": [
                "Para integrar varios conteudos aprendidos.",
                "Para esquecer os modulos anteriores.",
                "Para evitar testes.",
                "Para remover a funcao main."
            ],
            "resposta": "Para integrar varios conteudos aprendidos.",
            "explicacao": "Projetos juntam entrada, saida, funcoes, dados e organizacao."
        },
        {
            "pergunta": "Antes de programar um projeto maior, e util:",
            "alternativas": [
                "Planejar dados, funcoes e fluxo principal.",
                "Comecar apagando todos os arquivos.",
                "Ignorar o objetivo.",
                "Usar apenas uma linha de codigo."
            ],
            "resposta": "Planejar dados, funcoes e fluxo principal.",
            "explicacao": "Planejamento reduz retrabalho e deixa o codigo mais claro."
        },
        {
            "pergunta": "Ao terminar um projeto, devemos:",
            "alternativas": [
                "Testar casos comuns e casos de erro.",
                "Nunca executar o programa.",
                "Remover todos os retornos.",
                "Trocar todas as variaveis por comentarios."
            ],
            "resposta": "Testar casos comuns e casos de erro.",
            "explicacao": "Testes mostram se o projeto funciona em situacoes diferentes."
        }
    ],
}
