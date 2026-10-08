"""Formatos das perguntas dos desafios teóricos.

Cada lição tem quatro perguntas escritas para o assunto dela, de quatro tipos:

- conceito: pergunta sobre a ideia da lição; as alternativas erradas são enganos comuns.
- saida: mostra um programa e pergunta o que ele mostra na tela.
- erro: mostra um código com um problema e pergunta qual é.
- lacuna: mostra um código com ____ e pergunta o que completa para chegar à saída indicada.

Os programas de "saida" e "lacuna" são compilados e executados pelos testes (tests/test_perguntas_teoricas.py),
que conferem se a alternativa certa é mesmo a saída do programa e se as erradas não chegam à mesma saída.
"""

import textwrap

LACUNA = "____"


def programa(codigo, inclui=()):
    """Completa um trecho com os #include e a função main; um programa que já tem main fica como está."""
    codigo = textwrap.dedent(codigo).strip("\n")
    if "main(" in codigo:
        return codigo
    cabecalhos = "".join(f"#include <{nome}>\n" for nome in ("stdio.h", *inclui))
    corpo = textwrap.indent(codigo, "    ")
    return f"{cabecalhos}\nint main(void) {{\n{corpo}\n    return 0;\n}}"


def _pergunta(tipo, pergunta, certa, erradas, explicacao, **extras):
    erradas = list(erradas)
    assert len(erradas) == 3 and certa not in erradas and len(set(erradas)) == 3, (pergunta, certa, erradas)
    return {"tipo": tipo, "pergunta": pergunta, "resposta": certa, "erradas": erradas,
            "explicacao": explicacao, **extras}


def conceito(pergunta, certa, erradas, explicacao):
    return _pergunta("conceito", pergunta, certa, erradas, explicacao)


def saida(codigo, certa, erradas, explicacao, pergunta="", inclui=(), entrada=""):
    """O programa recebe `entrada` no teclado (stdin) e a alternativa certa é exatamente o que ele mostra."""
    if not pergunta:
        pergunta = "O que este programa mostra na tela?"
    return _pergunta("saida", pergunta, certa, erradas, explicacao,
                     codigo=programa(codigo, inclui), entrada=entrada)


def erro(codigo, certa, erradas, explicacao, pergunta="", inclui=(), compila=True):
    """`compila` diz se o código passa pelo compilador; os testes conferem isso."""
    if not pergunta:
        pergunta = "Qual é o problema deste código?" if compila else "Por que este código não compila?"
    return _pergunta("erro", pergunta, certa, erradas, explicacao,
                     codigo=programa(codigo, inclui), compila=compila)


def lacuna(codigo, certa, erradas, saida_esperada, explicacao, pergunta="", inclui=(), entrada=""):
    """Com a alternativa certa no lugar de ____, o programa mostra `saida_esperada`; com as erradas, não."""
    if not pergunta:
        pergunta = f"O que deve ocupar a lacuna ____ para o programa mostrar `{saida_esperada}`?"
    codigo = programa(codigo, inclui)
    assert codigo.count(LACUNA) == 1, codigo
    return _pergunta("lacuna", pergunta, certa, erradas, explicacao,
                     codigo=codigo, saida_esperada=saida_esperada, entrada=entrada)
