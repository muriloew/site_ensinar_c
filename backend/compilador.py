"""Compilacao e execucao controlada de programas C."""

from collections import defaultdict, deque
from contextlib import contextmanager
import os
import shutil
import signal
import subprocess
import tempfile
import threading
import time

import requests

try:
    import pwd
except ImportError:  # Windows
    pwd = None


MAX_CODIGO_BYTES = 100_000
MAX_ENTRADA_BYTES = 100_000
MAX_SAIDA_BYTES = 160_000


def _inteiro_ambiente(nome, padrao, minimo, maximo):
    try:
        valor = int(os.environ.get(nome, str(padrao)))
    except (TypeError, ValueError):
        valor = padrao
    return max(minimo, min(maximo, valor))


# O Render gratuito pode entregar apenas uma fracao de CPU. O tempo de parede
# precisa ser maior que o limite de CPU para nao matar um GCC apenas lento.
TEMPO_COMPILACAO = _inteiro_ambiente("COMPILER_COMPILE_TIMEOUT", 30, 10, 90)
TEMPO_CPU_COMPILACAO = _inteiro_ambiente("COMPILER_COMPILE_CPU", 12, 5, 30)
TEMPO_EXECUCAO = _inteiro_ambiente("COMPILER_RUN_TIMEOUT", 8, 2, 30)
TEMPO_INTERATIVO = _inteiro_ambiente("COMPILER_INTERACTIVE_TIMEOUT", 120, 20, 300)
MAX_EXECUTAVEL_BYTES = _inteiro_ambiente(
    "COMPILER_MAX_EXECUTABLE_MB", 8, 1, 32
) * 1024 * 1024
MAX_EXECUCOES_SIMULTANEAS = _inteiro_ambiente("MAX_COMPILER_JOBS", 4, 1, 16)

_slots_execucao = threading.BoundedSemaphore(MAX_EXECUCOES_SIMULTANEAS)
_limite_lock = threading.Lock()
_execucoes_recentes = defaultdict(deque)


def validar_codigo(codigo, entrada=None):
    if not isinstance(codigo, str) or not codigo.strip():
        return "Escreva um programa C antes de compilar."
    if len(codigo.encode("utf-8")) > MAX_CODIGO_BYTES:
        return "O codigo ultrapassa o limite de 100 KB."
    if entrada is not None:
        if not isinstance(entrada, str):
            return "A entrada do programa precisa ser texto."
        if len(entrada.encode("utf-8")) > MAX_ENTRADA_BYTES:
            return "A entrada ultrapassa o limite de 100 KB."
    return ""


def permitir_execucao(chave, limite=12, janela_segundos=60):
    """Limite simples por usuario, adequado ao unico worker configurado."""
    agora = time.monotonic()
    with _limite_lock:
        registros = _execucoes_recentes[str(chave)]
        while registros and agora - registros[0] >= janela_segundos:
            registros.popleft()
        if len(registros) >= limite:
            return False
        registros.append(agora)
        return True


def adquirir_slot():
    return _slots_execucao.acquire(blocking=False)


def liberar_slot():
    try:
        _slots_execucao.release()
    except ValueError:
        pass


@contextmanager
def slot_execucao():
    adquirido = adquirir_slot()
    try:
        yield adquirido
    finally:
        if adquirido:
            liberar_slot()


def comando_gcc(arquivo_c, arquivo_saida):
    return [
        "gcc",
        "-std=c11",
        "-Wall",
        "-Wextra",
        "-pedantic",
        "-pipe",
        "-fdiagnostics-color=never",
        arquivo_c,
        "-o",
        arquivo_saida,
        "-lm",
    ]


def _identidade_runner():
    if os.name != "posix" or pwd is None:
        return None
    nome = os.environ.get("COMPILER_RUNNER_USER", "compiler-runner")
    try:
        usuario = pwd.getpwnam(nome)
    except KeyError:
        return None
    if os.geteuid() not in (0, usuario.pw_uid):
        return None
    return usuario.pw_uid, usuario.pw_gid


def _preparar_workspace(codigo):
    temp_dir = tempfile.mkdtemp(prefix="ensinar_c_")
    arquivo_c = os.path.join(temp_dir, "programa.c")
    arquivo_saida = os.path.join(temp_dir, "programa")
    with open(arquivo_c, "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo)

    identidade = _identidade_runner()
    os.chmod(temp_dir, 0o700)
    os.chmod(arquivo_c, 0o600)
    if identidade and os.name == "posix" and os.geteuid() == 0:
        uid, gid = identidade
        os.chown(temp_dir, uid, gid)
        os.chown(arquivo_c, uid, gid)
    return temp_dir, arquivo_c, arquivo_saida


def _ambiente_minimo(temp_dir):
    return {
        "PATH": "/usr/local/bin:/usr/bin:/bin" if os.name == "posix" else os.environ.get("PATH", ""),
        "HOME": temp_dir,
        "TMPDIR": temp_dir,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }


def _com_limites(comando, modo):
    if os.name != "posix":
        return comando

    prlimit = shutil.which("prlimit")
    if not prlimit:
        return comando

    if modo == "compilar":
        cpu, memoria = TEMPO_CPU_COMPILACAO, 512 * 1024 * 1024
        tamanho_arquivo = MAX_EXECUTAVEL_BYTES
    elif modo == "interativo":
        cpu, memoria = 20, 160 * 1024 * 1024
        tamanho_arquivo = MAX_SAIDA_BYTES
    else:
        cpu, memoria = TEMPO_EXECUCAO, 160 * 1024 * 1024
        tamanho_arquivo = MAX_SAIDA_BYTES

    limitado = [
        prlimit,
        f"--cpu={cpu}:{cpu + 1}",
        f"--as={memoria}",
        f"--fsize={tamanho_arquivo}",
        "--nproc=24",
        "--nofile=64",
        "--core=0",
        "--",
        *comando,
    ]
    setpriv = shutil.which("setpriv")
    if setpriv:
        limitado = [setpriv, "--no-new-privs", "--", *limitado]
    return limitado


def _popen_kwargs(temp_dir):
    kwargs = {
        "cwd": temp_dir,
        "env": _ambiente_minimo(temp_dir),
    }
    if os.name == "posix":
        kwargs["start_new_session"] = True
        identidade = _identidade_runner()
        if identidade:
            kwargs["user"], kwargs["group"] = identidade
            kwargs["extra_groups"] = []
            kwargs["umask"] = 0o077
    return kwargs


def encerrar_processo(proc, tolerancia=0.35):
    if not proc or proc.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        else:
            proc.terminate()
        proc.wait(timeout=tolerancia)
        return
    except Exception:
        pass
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        else:
            proc.kill()
        proc.wait(timeout=1)
    except Exception:
        pass


def _ler_log(caminho):
    try:
        with open(caminho, "rb") as arquivo:
            dados = arquivo.read(MAX_SAIDA_BYTES + 1)
    except OSError:
        return "", False
    truncada = len(dados) > MAX_SAIDA_BYTES
    dados = dados[:MAX_SAIDA_BYTES]
    texto = dados.decode("utf-8", errors="replace")
    if truncada:
        texto += "\n\n[Saida interrompida: limite atingido.]"
    return texto, truncada


def _executar_processo(comando, temp_dir, modo, entrada=b"", timeout=5):
    caminho_log = os.path.join(temp_dir, f"{modo}.log")
    inicio = time.monotonic()
    with open(caminho_log, "w+b") as log:
        proc = subprocess.Popen(
            _com_limites(comando, modo),
            stdin=subprocess.PIPE,
            stdout=log,
            stderr=subprocess.STDOUT,
            **_popen_kwargs(temp_dir),
        )
        excedeu_tempo = False
        try:
            proc.communicate(input=entrada, timeout=timeout)
        except subprocess.TimeoutExpired:
            excedeu_tempo = True
            encerrar_processo(proc)

    texto, truncada = _ler_log(caminho_log)
    return {
        "codigo": proc.returncode,
        "texto": texto,
        "tempo_excedido": excedeu_tempo,
        "saida_truncada": truncada,
        "duracao_segundos": time.monotonic() - inicio,
    }


def _build_log(resultado):
    texto = resultado.get("texto", "").strip()
    duracao = resultado.get("duracao_segundos", 0)
    if resultado.get("tempo_excedido"):
        return (
            f"Tempo de compilacao excedido apos {TEMPO_COMPILACAO} segundos. "
            "O processo foi interrompido; tente novamente em alguns instantes."
        )
    if resultado.get("codigo") != 0:
        return "Build failed.\n\n" + (texto or "O GCC encerrou com erro.")
    if texto:
        return f"Build finished successfully in {duracao:.2f}s, com avisos:\n\n" + texto
    return f"Build finished successfully in {duracao:.2f}s.\n0 errors, 0 warnings."


def _compilar_workspace(temp_dir, arquivo_c, arquivo_saida):
    try:
        resultado = _executar_processo(
            comando_gcc(arquivo_c, arquivo_saida),
            temp_dir,
            "compilar",
            timeout=TEMPO_COMPILACAO,
        )
    except FileNotFoundError:
        return {
            "ok": False,
            "build": "GCC nao esta disponivel no servidor.",
            "saida": "",
        }
    except Exception as erro:
        return {"ok": False, "build": f"Erro ao compilar: {erro}", "saida": ""}

    return {
        "ok": resultado["codigo"] == 0 and not resultado["tempo_excedido"],
        "build": _build_log(resultado),
        "saida": "",
    }


def compilar_codigo(codigo):
    erro = validar_codigo(codigo)
    if erro:
        return {"ok": False, "build": erro, "saida": "", "origem": "Validacao"}

    with slot_execucao() as adquirido:
        if not adquirido:
            return {
                "ok": False,
                "build": "O compilador esta ocupado. Aguarde alguns segundos e tente novamente.",
                "saida": "",
                "origem": "Fila local",
            }
        temp_dir, arquivo_c, arquivo_saida = _preparar_workspace(codigo)
        try:
            resultado = _compilar_workspace(temp_dir, arquivo_c, arquivo_saida)
            resultado["origem"] = "GCC local protegido"
            return resultado
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


def executar_codigo_local(codigo, entrada=""):
    erro = validar_codigo(codigo, entrada)
    if erro:
        return {"ok": False, "build": erro, "saida": "", "origem": "Validacao"}

    with slot_execucao() as adquirido:
        if not adquirido:
            return {
                "ok": False,
                "build": "O compilador esta ocupado. Aguarde alguns segundos e tente novamente.",
                "saida": "",
                "origem": "Fila local",
            }
        temp_dir, arquivo_c, arquivo_saida = _preparar_workspace(codigo)
        try:
            compilacao = _compilar_workspace(temp_dir, arquivo_c, arquivo_saida)
            if not compilacao["ok"]:
                compilacao["origem"] = "GCC local protegido"
                return compilacao

            execucao = _executar_processo(
                [arquivo_saida],
                temp_dir,
                "executar",
                entrada.encode("utf-8"),
                TEMPO_EXECUCAO,
            )
            if execucao["tempo_excedido"]:
                saida = "Tempo de execucao excedido. Verifique loops infinitos ou entradas ausentes."
            else:
                saida = execucao["texto"] or "Programa executado sem saida na tela."
            saida = saida.rstrip() + f"\n\nProcess returned {execucao['codigo']}."
            return {
                "ok": execucao["codigo"] == 0 and not execucao["tempo_excedido"] and not execucao["saida_truncada"],
                "build": compilacao["build"],
                "saida": saida,
                "origem": "GCC local protegido",
            }
        except Exception as erro_execucao:
            return {
                "ok": False,
                "build": "Erro durante build/run.",
                "saida": f"Erro ao executar o codigo: {erro_execucao}",
                "origem": "GCC local protegido",
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


def executar_piston(codigo, entrada=""):
    erro = validar_codigo(codigo, entrada)
    if erro:
        return {"ok": False, "build": erro, "saida": "", "origem": "Validacao"}

    base = os.environ.get("PISTON_URL", "").rstrip("/")
    if not base:
        return {
            "ok": False,
            "build": "PISTON_URL nao foi configurada.",
            "saida": "",
            "origem": "Piston",
        }
    url = base if base.endswith("/execute") else base + "/execute"
    headers = {"Content-Type": "application/json"}
    token = os.environ.get("PISTON_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = {
        "language": "c",
        "version": os.environ.get("PISTON_C_VERSION", "*"),
        "files": [{"name": "main.c", "content": codigo}],
        "stdin": entrada,
        "args": [],
        "compile_timeout": TEMPO_COMPILACAO * 1000,
        "run_timeout": TEMPO_EXECUCAO * 1000,
        "compile_cpu_time": TEMPO_COMPILACAO * 1000,
        "run_cpu_time": TEMPO_EXECUCAO * 1000,
        "compile_memory_limit": 512 * 1024 * 1024,
        "run_memory_limit": 160 * 1024 * 1024,
    }
    resposta = requests.post(url, json=payload, headers=headers, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    compile_out = dados.get("compile") or {}
    run_out = dados.get("run")

    build = "".join(filter(None, [compile_out.get("stdout", ""), compile_out.get("stderr", "")]))
    if compile_out and (compile_out.get("code") != 0 or compile_out.get("status")):
        return {
            "ok": False,
            "build": "Build failed.\n\n" + (build or compile_out.get("message") or "Erro de compilacao."),
            "saida": "",
            "origem": "Piston configurado",
        }
    if not isinstance(run_out, dict):
        return {
            "ok": False,
            "build": build or dados.get("message") or "O executor nao retornou a etapa de execucao.",
            "saida": "",
            "origem": "Piston configurado",
        }

    saida = "".join(filter(None, [run_out.get("stdout", ""), run_out.get("stderr", "")]))
    saida = saida[:MAX_SAIDA_BYTES]
    codigo_saida = run_out.get("code")
    ok = codigo_saida == 0 and not run_out.get("status")
    return {
        "ok": ok,
        "build": build or "Build finished successfully.\n0 errors, 0 warnings.",
        "saida": (saida or "Programa executado sem saida na tela.").rstrip()
        + f"\n\nProcess returned {codigo_saida}.",
        "origem": "Piston configurado",
    }


def executar_codigo(codigo, entrada=""):
    if os.environ.get("COMPILER_BACKEND", "local").lower() == "piston":
        try:
            return executar_piston(codigo, entrada)
        except Exception as erro:
            return {
                "ok": False,
                "build": f"Falha no servico Piston configurado: {erro}",
                "saida": "",
                "origem": "Piston configurado",
            }
    return executar_codigo_local(codigo, entrada)


def preparar_terminal(codigo):
    erro = validar_codigo(codigo)
    if erro:
        return {"ok": False, "build": erro, "saida": ""}
    temp_dir, arquivo_c, arquivo_saida = _preparar_workspace(codigo)
    resultado = _compilar_workspace(temp_dir, arquivo_c, arquivo_saida)
    if not resultado["ok"]:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return resultado
    resultado.update({"temp_dir": temp_dir, "executavel": arquivo_saida})
    return resultado


def iniciar_terminal(executavel, temp_dir, slave_fd):
    return subprocess.Popen(
        _com_limites([executavel], "interativo"),
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        text=False,
        close_fds=True,
        **_popen_kwargs(temp_dir),
    )
