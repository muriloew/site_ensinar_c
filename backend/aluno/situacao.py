"""Onde o aluno está na trilha: lições concluídas, módulos liberados e próxima lição."""

from backend.banco.conexao import transacao
from backend.conteudo.desafios_diarios import (
    DESAFIOS_DIARIOS,
    desafios_disponiveis_por_progresso,
    escolher_desafio_do_dia,
)
from backend.conteudo.trilha import MODULOS, encontrar_licao, modulo_por_id


class SituacaoAluno:
    """Lê o progresso do aluno uma única vez e responde às regras de liberação."""

    def __init__(self, usuario_id, conn=None):
        self.usuario_id = usuario_id
        consulta = "SELECT licao_id, modulo_id, concluida FROM progresso WHERE usuario_id = ?"
        if conn is None:
            with transacao() as nova_conexao:
                linhas = nova_conexao.execute(consulta, (usuario_id,)).fetchall()
        else:
            linhas = conn.execute(consulta, (usuario_id,)).fetchall()

        self.concluidas = {linha["licao_id"] for linha in linhas if linha["concluida"] == 1}
        self.modulos_iniciados = {linha["modulo_id"] for linha in linhas}

    @property
    def total_concluidas(self):
        return len(self.concluidas)

    def progresso_modulo(self, modulo):
        ids = [licao["id"] for licao in modulo["licoes"]]
        if not ids:
            return 0
        feitas = sum(1 for licao_id in ids if licao_id in self.concluidas)
        return int((feitas / len(ids)) * 100)

    def modulo_liberado(self, modulo_id):
        if modulo_id == 1:
            return True
        anterior = modulo_por_id(modulo_id - 1)
        if not anterior:
            return False
        return all(licao["id"] in self.concluidas for licao in anterior["licoes"])

    def modulo_acessivel(self, modulo_id):
        # Módulos já começados continuam abertos para o aluno rever o que fez.
        return self.modulo_liberado(modulo_id) or modulo_id in self.modulos_iniciados

    def licao_acessivel(self, licao_id, exigir_pratica=False):
        """Devolve (modulo, licao, erro); erro é (mensagem, status HTTP) ou None."""
        try:
            licao_id = int(licao_id)
        except (TypeError, ValueError):
            return None, None, ("Informe uma lição válida.", 400)

        modulo, licao = encontrar_licao(licao_id)
        if not licao:
            return None, None, ("Lição não encontrada.", 404)
        if not self.modulo_acessivel(modulo["id"]):
            return None, None, ("Conclua os módulos anteriores para acessar esta lição.", 403)
        if exigir_pratica and not licao["pratica_codigo"]:
            return None, None, ("Esta lição possui apenas atividades teóricas.", 400)
        return modulo, licao, None

    def modulo_maximo_liberado(self):
        maximo = 1
        for modulo in MODULOS:
            if not self.modulo_liberado(modulo["id"]):
                break
            maximo = modulo["id"]
        return maximo

    def desafios_disponiveis(self):
        """Desafios diários dos módulos já liberados e o maior módulo liberado."""
        maximo = self.modulo_maximo_liberado()
        return desafios_disponiveis_por_progresso(DESAFIOS_DIARIOS, maximo), maximo

    def desafio_do_dia(self, data_texto=None):
        desafios, _ = self.desafios_disponiveis()
        return escolher_desafio_do_dia(desafios, data_texto)

    def proxima_licao(self):
        for modulo in MODULOS:
            if not self.modulo_liberado(modulo["id"]):
                break
            for licao in modulo["licoes"]:
                if licao["id"] not in self.concluidas:
                    return {
                        "modulo_id": modulo["id"],
                        "modulo": modulo["titulo"],
                        "licao_id": licao["id"],
                        "licao": licao["titulo"],
                        "progresso": self.progresso_modulo(modulo),
                        "concluido": False,
                    }

        ultimo_modulo = MODULOS[-1]
        ultima_licao = ultimo_modulo["licoes"][-1]
        return {
            "modulo_id": ultimo_modulo["id"],
            "modulo": ultimo_modulo["titulo"],
            "licao_id": ultima_licao["id"],
            "licao": ultima_licao["titulo"],
            "progresso": 100,
            "concluido": True,
        }

    def modulos_com_estado(self):
        """Módulos com progresso, estrelas e estado para as telas da jornada."""
        modulos = []
        for modulo in MODULOS:
            progresso = self.progresso_modulo(modulo)
            liberado = self.modulo_liberado(modulo["id"])
            modulos.append({
                **modulo,
                "progresso": progresso,
                "liberado": liberado,
                "estrelas": 3 if progresso == 100 else 2 if progresso >= 67 else 1 if progresso > 0 else 0,
                "estado": "concluido" if progresso == 100 else "atual" if liberado else "bloqueado",
            })
        return modulos
