"""Os 21 módulos da trilha de C e a montagem de cada lição."""

from backend.conteudo.exemplos import EXEMPLOS
from backend.conteudo.exercicios import (
    LICOES_SO_TEORIA,
    codigo_inicial,
    enunciado_exercicio,
    montar_dicas,
    regra_correcao,
)
from backend.conteudo.licoes import PLANOS_LICOES, montar_desafios_teoricos

TRILHA = (
    {
        "id": 1,
        "titulo": "Começando a programar",
        "descricao": "Entenda o que é um programa, como o C funciona e quais partes aparecem em um código básico.",
        "icone": "C",
        "licoes": ["O que é C", "Estrutura básica", "Comentários", "Compilação"],
    },
    {
        "id": 2,
        "titulo": "Conversando com o usuário",
        "descricao": "Aprenda a mostrar mensagens na tela e receber informações digitadas pela pessoa que usa o programa.",
        "icone": "io",
        "licoes": ["printf", "scanf"],
    },
    {
        "id": 3,
        "titulo": "Guardando informações",
        "descricao": "Aprenda a guardar números, letras e valores fixos para usar durante o programa.",
        "icone": "var",
        "licoes": ["int", "float e double", "char", "constantes", "#define", "escopo"],
    },
    {
        "id": 4,
        "titulo": "Fazendo contas e comparações",
        "descricao": "Use o C para somar, subtrair, comparar valores e montar pequenas expressões lógicas.",
        "icone": "+-",
        "licoes": [
            "soma", "subtração", "multiplicação", "divisão",
            "operadores relacionais", "operadores lógicos", "incremento",
        ],
    },
    {
        "id": 5,
        "titulo": "Tomando decisões",
        "descricao": "Faça o programa escolher caminhos diferentes dependendo de uma condição.",
        "icone": "if",
        "licoes": ["if", "else", "else if", "switch", "ternário"],
    },
    {
        "id": 6,
        "titulo": "Repetindo tarefas",
        "descricao": "Evite repetir o mesmo código várias vezes usando comandos que executam uma ação em sequência.",
        "icone": "for",
        "licoes": ["while", "do while", "for", "break", "continue"],
    },
    {
        "id": 7,
        "titulo": "Organizando o código",
        "descricao": "Divida o programa em partes menores para reutilizar ideias e deixar tudo mais fácil de entender.",
        "icone": "fn",
        "licoes": ["criando função", "parâmetros", "retorno", "protótipos", "recursão"],
    },
    {
        "id": 8,
        "titulo": "Listas e textos",
        "descricao": "Trabalhe com vários valores de uma vez e manipule palavras, nomes e frases.",
        "icone": "[]",
        "licoes": ["arrays", "matrizes", "strings", "strlen", "strcpy", "strcmp", "strcat", "fgets"],
    },
    {
        "id": 9,
        "titulo": "Como a memória funciona",
        "descricao": "Entenda como o computador guarda dados e como o C permite acessar esses locais com ponteiros.",
        "icone": "*",
        "licoes": ["memória", "operador &", "ponteiros + funções", "ponteiros + arrays", "ponteiro para ponteiro"],
    },
    {
        "id": 10,
        "titulo": "Usando memória quando precisar",
        "descricao": "Aprenda a reservar e liberar memória durante a execução do programa.",
        "icone": "mem",
        "licoes": ["malloc", "calloc", "realloc", "free", "memory leak"],
    },
    {
        "id": 11,
        "titulo": "Agrupando informações",
        "descricao": "Crie seus próprios tipos para juntar dados relacionados, como uma ficha de aluno ou produto.",
        "icone": "{}",
        "licoes": ["structs", "typedef", "unions", "enum"],
    },
    {
        "id": 12,
        "titulo": "Salvando dados",
        "descricao": "Grave informações em arquivos e leia esses dados novamente quando precisar.",
        "icone": "file",
        "licoes": ["fopen", "fclose", "fprintf", "fscanf"],
    },
    {
        "id": 13,
        "titulo": "Dividindo o programa em partes",
        "descricao": "Separe programas maiores em arquivos diferentes para facilitar organização e manutenção.",
        "icone": ".h",
        "licoes": [".h", ".c", "include guards"],
    },
    {
        "id": 14,
        "titulo": "Usando recursos prontos",
        "descricao": "Conheça bibliotecas que já trazem funções úteis para entrada, texto, memória e matemática.",
        "icone": "lib",
        "licoes": ["stdio", "stdlib", "string", "math"],
    },
    {
        "id": 15,
        "titulo": "Como o computador guarda informações",
        "descricao": "Veja como dados podem ser manipulados em zeros e uns usando operações de baixo nível.",
        "icone": "01",
        "licoes": ["bitwise", "máscaras"],
    },
    {
        "id": 16,
        "titulo": "Encontrando e corrigindo erros",
        "descricao": "Aprenda a identificar mensagens do compilador, erros de lógica e formas de investigar problemas.",
        "icone": "bug",
        "licoes": ["erros de sintaxe", "erros lógicos", "debug"],
    },
    {
        "id": 17,
        "titulo": "Transformando código em programa",
        "descricao": "Entenda como o compilador transforma arquivos de código em um programa executável.",
        "icone": "gcc",
        "licoes": ["gcc", "linking", "makefile"],
    },
    {
        "id": 18,
        "titulo": "Escrevendo programas seguros",
        "descricao": "Aprenda cuidados para evitar falhas comuns, entradas inválidas e problemas com memória.",
        "icone": "sec",
        "licoes": ["buffer overflow", "validação"],
    },
    {
        "id": 19,
        "titulo": "Organizando muitos dados",
        "descricao": "Use listas, pilhas, filas e árvores para organizar informações de formas diferentes.",
        "icone": "ds",
        "licoes": ["listas", "pilhas", "filas", "árvores"],
    },
    {
        "id": 20,
        "titulo": "Resolvendo problemas melhor",
        "descricao": "Aprenda formas de procurar, ordenar e comparar soluções para resolver problemas com mais eficiência.",
        "icone": "alg",
        "licoes": ["busca linear", "bubble sort", "eficiência"],
    },
    {
        "id": 21,
        "titulo": "Criando programas completos",
        "descricao": "Junte o que foi aprendido para criar projetos maiores do começo ao fim.",
        "icone": "app",
        "licoes": [
            "calculadora", "cadastro", "agenda", "jogo terminal",
            "sistema biblioteca", "editor texto", "projeto final",
        ],
    },
)

EXPLICACAO_EXEMPLO = (
    "Observe a ordem das declarações, os tipos usados e como a saída confirma o resultado. "
    "O exemplo é completo, compatível com C11 e pode ser compilado como um único arquivo."
)


def _montar_licao(licao_id, conteudo, modulo_id):
    plano = PLANOS_LICOES[conteudo]
    pratica = conteudo not in LICOES_SO_TEORIA
    exercicio = enunciado_exercicio(conteudo, plano)

    pontos_chave = [plano["fundamento"]]
    if pratica:
        pontos_chave.append(f"Aplicação prática: {exercicio}")
    pontos_chave.append("Compile com avisos habilitados e teste também valores de fronteira.")

    correcao = regra_correcao(conteudo, plano)
    desafios = montar_desafios_teoricos(
        conteudo, plano, aplicacao=exercicio, semente=f"{modulo_id}-{licao_id}"
    )
    return {
        "id": licao_id,
        "titulo": conteudo,
        "conteudo": plano["teoria"],
        "pontos_chave": pontos_chave,
        "erro_comum": plano["cuidado"],
        "explicacao_codigo": EXPLICACAO_EXEMPLO,
        "codigo": EXEMPLOS[conteudo],
        "pergunta": desafios[0]["pergunta"],
        "alternativas": desafios[0]["alternativas"],
        "resposta": desafios[0]["resposta"],
        "exercicio_codigo": exercicio,
        "codigo_minimo": codigo_inicial(conteudo),
        "correcao": correcao,
        "dicas": montar_dicas(plano, correcao),
        "pratica_codigo": pratica,
        "desafios_teoricos": desafios,
    }


def _montar_trilha():
    modulos = []
    proximo_id = 1
    for modulo in TRILHA:
        licoes = []
        for conteudo in modulo["licoes"]:
            licoes.append(_montar_licao(proximo_id, conteudo, modulo["id"]))
            proximo_id += 1
        modulos.append({**modulo, "licoes": licoes})
    return modulos


MODULOS = _montar_trilha()
TOTAL_LICOES = sum(len(modulo["licoes"]) for modulo in MODULOS)
_LICOES_POR_ID = {
    licao["id"]: (modulo, licao) for modulo in MODULOS for licao in modulo["licoes"]
}


def encontrar_licao(licao_id):
    return _LICOES_POR_ID.get(licao_id, (None, None))


def modulo_por_id(modulo_id):
    return next((modulo for modulo in MODULOS if modulo["id"] == modulo_id), None)
