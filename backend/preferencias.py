"""Preferências da conta: aparência, editor de código e estudo. Ficam no banco e valem em qualquer aparelho."""

import json
from datetime import datetime, timezone

# Cada preferência: valor padrão e valores aceitos. Caixas de seleção usam "sim"/"nao".
OPCOES = {
    "tema": ("sistema", ("sistema", "claro", "escuro")),
    "texto_licao": ("normal", ("normal", "grande", "muito_grande")),
    "reduzir_animacoes": ("nao", ("sim", "nao")),
    "cor_avatar": ("azul", ("azul", "verde", "roxo", "laranja", "rosa", "cinza")),
    "fonte_editor": ("normal", ("normal", "16", "18", "20")),
    "tab_editor": ("4", ("2", "4")),
    "quebrar_linhas": ("nao", ("sim", "nao")),
    "fechar_parenteses": ("sim", ("sim", "nao")),
    "dicas": ("automaticas", ("automaticas", "pedir", "desligadas")),
    "confirmar_limpar": ("sim", ("sim", "nao")),
}
CAIXAS = {chave for chave, (_, aceitos) in OPCOES.items() if aceitos == ("sim", "nao")}
PADROES = {chave: padrao for chave, (padrao, _) in OPCOES.items()}


def ler_preferencias(conn, usuario_id):
    linha = conn.execute(
        "SELECT dados FROM preferencias_usuario WHERE usuario_id = ?", (usuario_id,)
    ).fetchone()
    salvas = {}
    if linha:
        try:
            salvas = json.loads(linha["dados"] or "{}")
        except ValueError:
            salvas = {}
    return {
        chave: salvas.get(chave) if salvas.get(chave) in aceitos else padrao
        for chave, (padrao, aceitos) in OPCOES.items()
    }


def preferencias_do_formulario(formulario, atuais):
    """Valida o envio: valores desconhecidos são ignorados e mantêm o que já estava salvo."""
    novas = dict(atuais)
    for chave, (_, aceitos) in OPCOES.items():
        if chave in CAIXAS:
            # Caixa desmarcada não é enviada; o campo oculto avisa que ela estava no formulário.
            if f"{chave}__presente" in formulario:
                novas[chave] = "sim" if formulario.get(chave) in ("sim", "on", "1") else "nao"
        elif formulario.get(chave) in aceitos:
            novas[chave] = formulario.get(chave)
    return novas


def salvar_preferencias(conn, usuario_id, preferencias):
    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    dados = json.dumps(preferencias, sort_keys=True)
    conn.execute(
        """
        INSERT INTO preferencias_usuario (usuario_id, dados, atualizado_em) VALUES (?, ?, ?)
        ON CONFLICT(usuario_id) DO UPDATE SET dados = excluded.dados, atualizado_em = excluded.atualizado_em
        """,
        (usuario_id, dados, agora),
    )
