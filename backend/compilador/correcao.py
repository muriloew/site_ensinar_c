"""Correção automática: confere o código do aluno e a saída dos testes."""

import re
import unicodedata

from backend.compilador import executor


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", (texto or "").lower())
    return "".join(char for char in texto if unicodedata.category(char) != "Mn")


def limpar_saida_para_correcao(saida):
    linhas = []
    for linha in (saida or "").splitlines():
        normalizada = normalizar_texto(linha).strip()
        if normalizada.startswith(("process returned", "press any key", "origem:")):
            continue
        linhas.append(linha)
    return "\n".join(linhas).strip()


def remover_comentarios_c(codigo):
    """Remove comentários sem apagar textos e caracteres literais."""
    resultado = []
    indice = 0
    estado = "codigo"
    escape = False
    codigo = codigo or ""

    while indice < len(codigo):
        atual = codigo[indice]
        proximo = codigo[indice + 1] if indice + 1 < len(codigo) else ""

        if estado == "linha":
            if atual == "\n":
                resultado.append(atual)
                estado = "codigo"
            indice += 1
            continue

        if estado == "bloco":
            if atual == "*" and proximo == "/":
                estado = "codigo"
                indice += 2
                continue
            if atual == "\n":
                resultado.append(atual)
            indice += 1
            continue

        if estado in {"texto", "caractere"}:
            resultado.append(atual)
            if escape:
                escape = False
            elif atual == "\\":
                escape = True
            elif (estado == "texto" and atual == '"') or (estado == "caractere" and atual == "'"):
                estado = "codigo"
            indice += 1
            continue

        if atual == "/" and proximo == "/":
            estado = "linha"
            indice += 2
        elif atual == "/" and proximo == "*":
            estado = "bloco"
            indice += 2
        else:
            resultado.append(atual)
            if atual == '"':
                estado = "texto"
            elif atual == "'":
                estado = "caractere"
            indice += 1

    return "".join(resultado)


def validar_regras_estaticas(codigo, regra):
    falhas = []
    codigo_normalizado = normalizar_texto(remover_comentarios_c(codigo))

    for termo in regra.get("codigo_contem", []):
        if normalizar_texto(termo) not in codigo_normalizado:
            falhas.append(f"O código precisa usar: {termo}.")

    for termo in regra.get("codigo_nao_contem", []):
        if normalizar_texto(termo) in codigo_normalizado:
            falhas.append(f"Remova o uso de: {termo}.")

    for termo, minimo in regra.get("min_ocorrencias_codigo", {}).items():
        if codigo_normalizado.count(normalizar_texto(termo)) < minimo:
            falhas.append(f"Use {termo} pelo menos {minimo} vezes.")

    return falhas


def validar_saida(saida, regra):
    falhas = []
    saida_limpa = limpar_saida_para_correcao(saida)
    saida_normalizada = normalizar_texto(saida_limpa)

    if regra.get("saida_obrigatoria") and not saida_limpa:
        falhas.append("O programa precisa mostrar alguma saída na tela.")

    for termo in regra.get("saida_contem", []):
        if normalizar_texto(termo) not in saida_normalizada:
            falhas.append(f"A saída precisa conter: {termo}.")

    for termo in regra.get("saida_nao_contem", []):
        if normalizar_texto(termo) in saida_normalizada:
            falhas.append(f"A saída não pode conter: {termo}.")

    for expressao in regra.get("saida_regex", []):
        if not re.search(expressao, saida_normalizada, re.I):
            falhas.append("A saída ainda não bate com o resultado esperado.")

    minimo_linhas = regra.get("min_linhas_saida")
    if minimo_linhas:
        linhas = [linha for linha in saida_limpa.splitlines() if linha.strip()]
        if len(linhas) < minimo_linhas:
            falhas.append(f"A saída precisa ter pelo menos {minimo_linhas} linhas.")

    return falhas


def avaliar_codigo(codigo, execucao_ok, saida, regra):
    """Aprova o código quando ele executou, usa os recursos pedidos e passa nos testes."""
    if not execucao_ok:
        return {
            "ok": False,
            "mensagem": "Corrija os erros de compilação ou execução antes de concluir.",
        }

    regra = regra or {"saida_obrigatoria": True}
    falhas = validar_regras_estaticas(codigo, regra)

    testes = regra.get("testes", [])
    if testes:
        for indice, teste in enumerate(testes, start=1):
            resultado_teste = executor.executar_codigo(codigo, teste.get("entrada", ""))
            if not resultado_teste.get("ok", False):
                falhas.append(f"O teste automático {indice} não executou corretamente.")
                continue
            falhas.extend(validar_saida(resultado_teste.get("saida", ""), {
                "saida_contem": teste.get("saida_contem", []),
                "saida_nao_contem": teste.get("saida_nao_contem", []),
                "saida_regex": teste.get("saida_regex", []),
                "saida_obrigatoria": teste.get("saida_obrigatoria", True),
            }))
    else:
        falhas.extend(validar_saida(saida, regra))

    if falhas:
        return {"ok": False, "mensagem": " ".join(falhas[:3])}
    return {"ok": True, "mensagem": "Correção automática aprovada. Você pode concluir."}
