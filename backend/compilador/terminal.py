"""Terminal interativo via WebSocket: compila com GCC e liga o programa a um pseudo-terminal."""

import os
import select
import shutil
import threading
import time
from datetime import date

from flask import request, session
from flask_socketio import SocketIO, emit

from backend.aluno.gamificacao import registrar_atividade
from backend.aluno.situacao import SituacaoAluno
from backend.banco.conexao import transacao
from backend.compilador import executor
from backend.compilador.correcao import avaliar_codigo
from backend.compilador.historico import registrar_historico_codigo

try:
    import pty
except ImportError:  # Windows
    pty = None

socketio = SocketIO()

PROCESSOS_TERMINAL = {}
TERMINAL_POR_USUARIO = {}
PROCESSOS_TERMINAL_LOCK = threading.RLock()

MENSAGEM_DESAFIO_BLOQUEADO = "Conclua o módulo 1 para desbloquear os desafios diários."


def salvar_execucao_licao(usuario_id, licao_id, codigo, entrada, saida, execucao_ok, build_log="", origem=""):
    modulo, licao, erro = SituacaoAluno(usuario_id).licao_acessivel(licao_id, exigir_pratica=True)
    if erro:
        return {"ok": False, "mensagem": erro[0]}

    validacao = avaliar_codigo(codigo, execucao_ok, saida, licao["correcao"])
    with transacao() as conn:
        conn.execute(
            """
            INSERT INTO progresso (usuario_id, licao_id, modulo_id, codigo_usuario, saida_codigo,
                                   entrada_codigo, codigo_enviado, codigo_validado, feedback_codigo,
                                   atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
            ON CONFLICT(usuario_id, licao_id)
            DO UPDATE SET codigo_usuario = excluded.codigo_usuario,
                          saida_codigo = excluded.saida_codigo,
                          entrada_codigo = excluded.entrada_codigo,
                          codigo_enviado = 1,
                          codigo_validado = excluded.codigo_validado,
                          feedback_codigo = excluded.feedback_codigo,
                          atualizado_em = excluded.atualizado_em
            """,
            (usuario_id, licao["id"], modulo["id"], codigo, saida, entrada,
             1 if validacao["ok"] else 0, validacao["mensagem"], str(date.today())),
        )
        registrar_historico_codigo(
            conn, usuario_id, codigo, entrada, saida, build_log,
            contexto="licao", licao_id=licao["id"], modulo_id=modulo["id"],
            aprovado=validacao["ok"], origem=origem,
        )
        if validacao["ok"]:
            registrar_atividade(conn, usuario_id)
    return validacao


def salvar_execucao_desafio(usuario_id, codigo, entrada, saida, execucao_ok, build_log="", origem=""):
    hoje = str(date.today())
    desafio = SituacaoAluno(usuario_id).desafio_do_dia(hoje)
    if not desafio:
        return {"ok": False, "mensagem": MENSAGEM_DESAFIO_BLOQUEADO}

    validacao = avaliar_codigo(codigo, execucao_ok, saida, desafio["correcao"])
    with transacao() as conn:
        conn.execute(
            """
            INSERT INTO desafios_diarios (usuario_id, data, desafio_id, codigo_usuario, saida_codigo,
                                          entrada_codigo, codigo_validado, feedback_codigo, concluido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(usuario_id, data)
            DO UPDATE SET desafio_id = excluded.desafio_id,
                          codigo_usuario = excluded.codigo_usuario,
                          saida_codigo = excluded.saida_codigo,
                          entrada_codigo = excluded.entrada_codigo,
                          codigo_validado = excluded.codigo_validado,
                          feedback_codigo = excluded.feedback_codigo
            """,
            (usuario_id, hoje, desafio["id"], codigo, saida, entrada,
             1 if validacao["ok"] else 0, validacao["mensagem"]),
        )
        registrar_historico_codigo(
            conn, usuario_id, codigo, entrada, saida, build_log,
            contexto="diario", licao_id=desafio["licao_id"], modulo_id=desafio["modulo_id"],
            aprovado=validacao["ok"], origem=origem,
        )
        if validacao["ok"]:
            registrar_atividade(conn, usuario_id)
    return validacao


def salvar_execucao_livre(usuario_id, codigo, entrada, saida, execucao_ok, build_log="", origem=""):
    with transacao() as conn:
        registrar_historico_codigo(
            conn, usuario_id, codigo, entrada, saida, build_log,
            contexto="livre", aprovado=bool(execucao_ok), origem=origem,
        )
        if execucao_ok:
            registrar_atividade(conn, usuario_id)


def encerrar_processo_socket(sid):
    with PROCESSOS_TERMINAL_LOCK:
        dados = PROCESSOS_TERMINAL.pop(sid, None)
        if dados and TERMINAL_POR_USUARIO.get(dados["usuario_id"]) == sid:
            TERMINAL_POR_USUARIO.pop(dados["usuario_id"], None)
    if not dados:
        return

    executor.encerrar_processo(dados["proc"])
    try:
        os.close(dados["fd"])
    except OSError:
        pass
    shutil.rmtree(dados["temp_dir"], ignore_errors=True)

    if dados.get("vaga_interativa"):
        dados["vaga_interativa"] = False
        executor.liberar_vaga_interativa()


def leitor_terminal(sid):
    with PROCESSOS_TERMINAL_LOCK:
        dados = PROCESSOS_TERMINAL.get(sid)
    if not dados:
        return

    proc = dados["proc"]
    fd = dados["fd"]
    saida_total = ""
    total_bytes = 0
    motivo_interrupcao = ""
    inicio = time.monotonic()

    def enviar(texto):
        nonlocal saida_total
        saida_total += texto
        socketio.emit("terminal_saida", {"texto": texto}, to=sid)

    def consumir_saida(bloco):
        nonlocal total_bytes, motivo_interrupcao
        restante = executor.MAX_SAIDA_BYTES - total_bytes
        trecho = bloco[:max(restante, 0)]
        total_bytes += len(trecho)
        if trecho:
            enviar(trecho.decode("utf-8", errors="replace"))
        if len(bloco) > len(trecho):
            motivo_interrupcao = "limite de saída atingido"
            return False
        return True

    while True:
        if time.monotonic() - inicio > executor.TEMPO_INTERATIVO:
            motivo_interrupcao = f"tempo limite de {executor.TEMPO_INTERATIVO} s excedido"
            executor.encerrar_processo(proc)
            break

        try:
            pronto, _, _ = select.select([fd], [], [], 0.2)
            if fd in pronto:
                bloco = os.read(fd, 4096)
                if not bloco:
                    if proc.poll() is not None:
                        break
                elif not consumir_saida(bloco):
                    executor.encerrar_processo(proc)
                    break
        except OSError:
            # O pseudo-terminal fecha quando o programa termina.
            if proc.poll() is None:
                motivo_interrupcao = "erro na leitura do terminal"
                executor.encerrar_processo(proc)
            break
        except Exception:
            motivo_interrupcao = "erro na leitura do terminal"
            executor.encerrar_processo(proc)
            break

        if proc.poll() is not None:
            # O programa pode terminar antes de toda a saída ser lida: esvazia o pseudo-terminal.
            while True:
                try:
                    pronto, _, _ = select.select([fd], [], [], 0)
                    if fd not in pronto:
                        break
                    bloco = os.read(fd, 4096)
                    if not bloco or not consumir_saida(bloco):
                        break
                except OSError:
                    break
            break

    codigo_saida = proc.poll()
    if codigo_saida is None:
        executor.encerrar_processo(proc)
        codigo_saida = proc.poll()
    if codigo_saida is None:
        codigo_saida = -1

    execucao_ok = codigo_saida == 0 and not motivo_interrupcao
    if execucao_ok:
        enviar("\n\nProcess returned 0 (0x0)\n")
    else:
        enviar(f"\n\n{executor.texto_retorno(codigo_saida, motivo_interrupcao)}\n")
    socketio.emit("terminal_finalizado", {"codigo": codigo_saida}, to=sid)

    if dados.get("vaga_interativa"):
        dados["vaga_interativa"] = False
        executor.liberar_vaga_interativa()

    execucao = {
        "codigo": dados["codigo"],
        "entrada": dados["entrada"],
        "saida": saida_total,
        "execucao_ok": execucao_ok,
        "build_log": dados["build_log"],
        "origem": dados["origem"],
    }
    try:
        validacao = None
        if dados["tipo"] == "diario":
            validacao = salvar_execucao_desafio(dados["usuario_id"], **execucao)
        elif dados["tipo"] == "licao":
            validacao = salvar_execucao_licao(dados["usuario_id"], dados["licao_id"], **execucao)
        else:
            salvar_execucao_livre(dados["usuario_id"], **execucao)
        if validacao:
            socketio.emit("correcao_resultado", validacao, to=sid)
    except Exception:
        socketio.emit("correcao_resultado", {
            "ok": False,
            "mensagem": "A execução terminou, mas não foi possível salvar a correção.",
        }, to=sid)
    finally:
        encerrar_processo_socket(sid)


@socketio.on("compilar_real")
def compilar_real(dados):
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        emit("build_log", {"ok": False, "texto": "Usuário não logado."})
        return

    sid = request.sid
    encerrar_processo_socket(sid)

    if not executor.permitir_execucao(usuario_id):
        emit("build_log", {"ok": False, "texto": "Muitas compilações em pouco tempo. Aguarde um minuto."})
        return

    dados = dados or {}
    codigo = dados.get("codigo", "")
    licao_id = dados.get("licao_id")
    tipo = dados.get("tipo", "licao")

    if tipo == "licao":
        _, licao, erro = SituacaoAluno(usuario_id).licao_acessivel(licao_id, exigir_pratica=True)
        if erro:
            emit("build_log", {"ok": False, "texto": erro[0]})
            return
        licao_id = licao["id"]
    elif tipo == "diario":
        if not SituacaoAluno(usuario_id).desafio_do_dia(str(date.today())):
            emit("build_log", {"ok": False, "texto": MENSAGEM_DESAFIO_BLOQUEADO})
            return
    elif tipo == "compilador":
        licao_id = None
    else:
        emit("build_log", {"ok": False, "texto": "Tipo de execução inválido."})
        return

    erro_validacao = executor.validar_codigo(codigo)
    if erro_validacao:
        emit("build_log", {"ok": False, "texto": erro_validacao})
        return

    if pty is None:
        emit("build_log", {
            "ok": False,
            "texto": "O terminal interativo funciona no Linux/Docker. No Windows, rode o site pelo Dockerfile do projeto.",
        })
        return

    with PROCESSOS_TERMINAL_LOCK:
        sid_existente = TERMINAL_POR_USUARIO.get(usuario_id)
        if sid_existente and sid_existente != sid:
            emit("build_log", {
                "ok": False,
                "texto": "Já existe um terminal em execução nesta conta. Feche a outra aba ou aguarde o término.",
            })
            return

    if not executor.adquirir_vaga_interativa():
        emit("build_log", {
            "ok": False,
            "texto": "Muitos programas abertos no servidor agora. Aguarde alguns segundos e compile de novo.",
        })
        return

    with PROCESSOS_TERMINAL_LOCK:
        TERMINAL_POR_USUARIO[usuario_id] = sid

    vaga_reservada = True
    temp_dir = None
    master_fd = None
    slave_fd = None
    try:
        # A compilação usa CPU: uma por vez, com uma fila curta. A vaga é liberada ao terminar de compilar.
        with executor.slot_execucao() as compilador_livre:
            if not compilador_livre:
                emit("build_log", {
                    "ok": False,
                    "texto": "O compilador está ocupado com outros alunos. Aguarde alguns segundos e tente de novo.",
                })
                return
            preparacao = executor.preparar_terminal(codigo)
        if not preparacao.get("ok"):
            emit("build_log", {"ok": False, "texto": preparacao.get("build", "Falha ao compilar.")})
            return

        temp_dir = preparacao["temp_dir"]
        build_log = preparacao.get("build", "Build finished successfully.")
        emit("build_log", {"ok": True, "texto": build_log})

        master_fd, slave_fd = pty.openpty()
        proc = executor.iniciar_terminal(preparacao["executavel"], temp_dir, slave_fd)
        os.close(slave_fd)
        slave_fd = None

        with PROCESSOS_TERMINAL_LOCK:
            PROCESSOS_TERMINAL[sid] = {
                "proc": proc,
                "fd": master_fd,
                "temp_dir": temp_dir,
                "usuario_id": usuario_id,
                "licao_id": licao_id,
                "tipo": tipo,
                "codigo": codigo,
                "entrada": "",
                "build_log": build_log,
                "origem": f"{preparacao.get('compilador', 'GCC')} interativo protegido",
                "vaga_interativa": True,
            }
        vaga_reservada = False
        master_fd = None
        temp_dir = None

        socketio.start_background_task(leitor_terminal, sid)
    except Exception as erro:
        emit("build_log", {"ok": False, "texto": f"Erro ao compilar: {erro}"})
    finally:
        for descritor in (slave_fd, master_fd):
            if descritor is not None:
                try:
                    os.close(descritor)
                except OSError:
                    pass
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        if vaga_reservada:
            with PROCESSOS_TERMINAL_LOCK:
                if TERMINAL_POR_USUARIO.get(usuario_id) == sid:
                    TERMINAL_POR_USUARIO.pop(usuario_id, None)
            executor.liberar_vaga_interativa()


@socketio.on("terminal_entrada")
def terminal_entrada(dados):
    texto = str((dados or {}).get("texto", ""))[:10_000]
    with PROCESSOS_TERMINAL_LOCK:
        processo = PROCESSOS_TERMINAL.get(request.sid)
    if not processo:
        return

    tamanho = len(processo["entrada"].encode("utf-8")) + len(texto.encode("utf-8"))
    if tamanho > executor.MAX_ENTRADA_BYTES:
        emit("terminal_saida", {"texto": "\nLimite de entrada do terminal atingido.\n"})
        return

    processo["entrada"] += texto
    try:
        os.write(processo["fd"], texto.encode("utf-8"))
    except OSError:
        pass


@socketio.on("terminal_cancelar")
def cancelar_terminal():
    encerrar_processo_socket(request.sid)
    emit("terminal_finalizado", {"codigo": -1})


@socketio.on("disconnect")
def desconectar_terminal():
    encerrar_processo_socket(request.sid)
