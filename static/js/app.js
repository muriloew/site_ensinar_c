
function abrirConsole() {
    const modal = document.getElementById("janelaConsole");
    if (modal) {
        modal.classList.add("ativo");
    }
}

function fecharConsole() {
    const modal = document.getElementById("janelaConsole");
    if (modal) {
        modal.classList.remove("ativo");
    }
}

function trocarAbaConsole(aba, botao) {
    document.querySelectorAll(".console-tabs button").forEach(btn => {
        btn.classList.remove("active");
    });

    document.querySelectorAll(".console-panel").forEach(panel => {
        panel.classList.remove("active");
    });

    botao.classList.add("active");

    const painel = document.getElementById("aba" + aba.charAt(0).toUpperCase() + aba.slice(1));
    if (painel) {
        painel.classList.add("active");
    }
}

function abrirAbaConsole(aba) {
    abrirConsole();
    const botoes = document.querySelectorAll(".console-tabs button");
    if (!botoes.length) {
        return;
    }
    botoes.forEach(btn => {
        const texto = btn.textContent.toLowerCase();
        if (texto.includes(aba)) {
            btn.click();
        }
    });
}


document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".quiz button[data-resposta]").forEach((botao) => {
        botao.addEventListener("click", () => {
            const quiz = botao.closest(".quiz");
            const licaoId = Number(quiz.dataset.licaoId);
            const resposta = botao.dataset.resposta;
            verificarResposta(licaoId, resposta, botao);
        });
    });

    document.querySelectorAll(".quiz").forEach((quiz) => {
        const licaoId = Number(quiz.dataset.licaoId);
        let respostaSalva = quiz.dataset.respostaSalva;
        let correta = quiz.dataset.correta === "1";

        if (!respostaSalva) {
            const local = localStorage.getItem("quiz_licao_" + licaoId);
            if (local) {
                try {
                    const dados = JSON.parse(local);
                    respostaSalva = dados.resposta;
                    correta = !!dados.correta;
                } catch {}
            }
        }

        if (respostaSalva) {
            quiz.querySelectorAll("button[data-resposta]").forEach((btn) => {
                if (btn.dataset.resposta === respostaSalva) {
                    btn.classList.add(correta ? "correct" : "wrong");
                }
            });
        }
    });
});

async function verificarResposta(licaoId, resposta, botao) {
    const resultado = document.getElementById("resultadoQuiz");
    const quiz = botao.closest(".quiz");

    document.querySelectorAll(".quiz button").forEach(btn => {
        btn.classList.remove("correct", "wrong");
    });

    try {
        const retorno = await fetch("/verificar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({licao_id: licaoId, resposta: resposta})
        });

        const dados = await retorno.json();

        if (!retorno.ok) {
            resultado.textContent = dados.mensagem || "Erro no servidor ao verificar resposta.";
            return;
        }

        if (dados.correta) {
            botao.classList.add("correct");
            resultado.textContent = "Resposta salva: correta.";
        } else {
            botao.classList.add("wrong");
            resultado.textContent = "Resposta salva: incorreta.";
        }

        if (quiz) {
            quiz.dataset.respostaSalva = resposta;
            quiz.dataset.correta = dados.correta ? "1" : "0";
        }

        localStorage.setItem("quiz_licao_" + licaoId, JSON.stringify({
            resposta: resposta,
            correta: dados.correta
        }));
    } catch (erro) {
        resultado.textContent = "Erro ao verificar resposta. Recarregue a página e tente novamente.";
    }
}

async function compilarExecutar(licaoId, tipo) {
    abrirConsole();
    await executarCodigo(licaoId, tipo);
}


async function compilarCodigo() {
    const editor = document.getElementById("editorCodigo");
    const buildLog = document.getElementById("buildLog");

    if (!buildLog) {
        return;
    }

    abrirAbaConsole("build");
    buildLog.textContent = "Compilando...";

    try {
        const retorno = await fetch("/compilar-codigo", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                codigo: editor.value
            })
        });

        let dados;
        try {
            dados = await retorno.json();
        } catch {
            buildLog.textContent = "Erro no servidor: resposta inválida. Veja os logs do Render.";
            return;
        }

        buildLog.textContent = dados.build || "Compilação finalizada.";
    } catch (erro) {
        buildLog.textContent = "Erro de conexão ao compilar. Verifique se o site está online.";
    }
}


async function executarCodigo(licaoId, tipo) {
    const editor = document.getElementById("editorCodigo");
    const entradaTerminal = document.getElementById("entradaTerminal");
    const saida = document.getElementById("saidaCodigo");
    const buildLog = document.getElementById("buildLog");

    abrirAbaConsole("saida");
    saida.textContent = "Executando programa...";
    if (buildLog) {
        buildLog.textContent = "Compilando antes de executar...";
    }

    try {
        const retorno = await fetch("/executar-codigo", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: licaoId,
                tipo: tipo,
                codigo: editor.value,
                entrada: entradaTerminal ? entradaTerminal.value : ""
            })
        });

        let dados;
        try {
            dados = await retorno.json();
        } catch {
            saida.textContent = "Erro no servidor: resposta inválida. Veja os logs do Render.";
            return;
        }

        if (buildLog) {
            buildLog.textContent = dados.build || "Build finalizado.";
        }
        saida.textContent = dados.saida || dados.mensagem || "Execução finalizada sem mensagem.";
    } catch (erro) {
        saida.textContent = "Erro de conexão ao executar. Verifique se o site está online e tente novamente.";
    }
}

async function concluirLicao(licaoId) {
    const retorno = await fetch(`/concluir/${licaoId}`, {method: "POST"});
    const dados = await retorno.json();

    alert(dados.mensagem || "Lição concluída!");

    if (dados.ok) {
        window.location.href = "/dashboard";
    }
}

async function concluirDesafioDiario() {
    const retorno = await fetch("/concluir-desafio-diario", {method: "POST"});
    const dados = await retorno.json();

    alert(dados.mensagem);

    if (dados.ok) {
        window.location.reload();
    }
}

function limparEditor() {
    const editor = document.getElementById("editorCodigo");
    editor.value = "";
}


function abrirJanelaTerminal() {
    const modal = document.getElementById("terminalModal");
    if (modal) {
        modal.classList.add("ativo");
    }
}

function fecharJanelaTerminal() {
    const modal = document.getElementById("terminalModal");
    if (modal) {
        modal.classList.remove("ativo");
    }
}

async function executarCompiladorOnline() {
    const codigo = document.getElementById("codigoCompilador");
    const entrada = document.getElementById("entradaCompilador");
    const saida = document.getElementById("saidaCompilador");
    const build = document.getElementById("buildCompilador");

    if (!codigo || !saida || !build) {
        return;
    }

    abrirJanelaTerminal();
    saida.textContent = "Executando...";
    build.textContent = "Compilando...";

    try {
        const retorno = await fetch("/api/compilador/executar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                codigo: codigo.value,
                entrada: entrada ? entrada.value : ""
            })
        });

        const dados = await retorno.json();

        build.textContent = (dados.build || "Build finalizado.") + (dados.origem ? "\n\nOrigem: " + dados.origem : "");
        saida.textContent = dados.saida || "Programa executado sem saída.";
    } catch (erro) {
        build.textContent = "Erro de conexão.";
        saida.textContent = "Não foi possível executar o compilador agora.";
    }
}

function limparCompilador() {
    const codigo = document.getElementById("codigoCompilador");
    const entrada = document.getElementById("entradaCompilador");
    const saida = document.getElementById("saidaCompilador");
    const build = document.getElementById("buildCompilador");

    if (codigo) codigo.value = "";
    if (entrada) entrada.value = "";
    if (saida) saida.textContent = "Aguardando compilação.";
    if (build) build.textContent = "Aguardando build.";
}

function carregarHistorico(codigo, entrada) {
    const editor = document.getElementById("codigoCompilador");
    const input = document.getElementById("entradaCompilador");

    if (editor) editor.value = codigo || "";
    if (input) input.value = entrada || "";
}



let exercicioAtualId = null;

function abrirEntradaModal() {
    const modal = document.getElementById("entradaModal");
    if (modal) modal.classList.add("ativo");
}

function fecharEntradaModal() {
    const modal = document.getElementById("entradaModal");
    if (modal) modal.classList.remove("ativo");
}

function abrirBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.add("ativo");
}

function fecharBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.remove("ativo");
}

function abrirTerminalExercicio() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.add("ativo");
}

function fecharTerminalExercicio() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.remove("ativo");
}

function compilarExercicio(licaoId) {
    exercicioAtualId = licaoId;
    abrirEntradaModal();
}

async function executarExercicioComEntrada() {
    const codigo = document.getElementById("codigoExercicio");
    const entrada = document.getElementById("entradaExercicio");
    const saida = document.getElementById("saidaExercicio");
    const build = document.getElementById("buildExercicio");

    fecharEntradaModal();

    if (!codigo || !saida || !build) return;

    build.textContent = "Compilando...";
    saida.textContent = "Executando...";

    try {
        const retorno = await fetch("/api/exercicio/compilar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: exercicioAtualId,
                codigo: codigo.value,
                entrada: entrada ? entrada.value : ""
            })
        });

        const dados = await retorno.json();

        build.textContent = dados.build || "Build finalizado.";

        if (dados.ok) {
            saida.textContent = dados.saida || "Programa executado sem saída.";
            abrirTerminalExercicio();
        } else {
            saida.textContent = dados.saida || "";
            abrirBuildModal();
        }
    } catch (erro) {
        build.textContent = "Erro de conexão com o compilador.";
        abrirBuildModal();
    }
}

function limparExercicio() {
    const codigo = document.getElementById("codigoExercicio");
    const entrada = document.getElementById("entradaExercicio");
    const saida = document.getElementById("saidaExercicio");
    const build = document.getElementById("buildExercicio");

    if (codigo) codigo.value = "";
    if (entrada) entrada.value = "";
    if (saida) saida.textContent = "Aguardando compilação.";
    if (build) build.textContent = "Aguardando build.";
}


// Versão 14: terminal interativo na mesma janela, sem popup separado.
let exercicioAtualIdV14 = null;

function abrirTerminalInterativo(licaoId) {
    exercicioAtualIdV14 = licaoId;
    const terminal = document.getElementById("terminalModalExercicio");
    const saida = document.getElementById("saidaExercicio");

    if (saida && !saida.textContent.trim()) {
        saida.textContent = "Digite a entrada abaixo, se o programa usar scanf, e clique em Compilar.";
    }

    if (terminal) {
        terminal.classList.add("ativo");
    }
}

function fecharTerminalExercicio() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.remove("ativo");
}

function abrirBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.add("ativo");
}

function fecharBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.remove("ativo");
}

async function executarExercicioComEntrada() {
    const codigo = document.getElementById("codigoExercicio");
    const entrada = document.getElementById("entradaExercicio");
    const saida = document.getElementById("saidaExercicio");
    const build = document.getElementById("buildExercicio");

    if (!codigo || !saida || !build) return;

    build.textContent = "Compilando...";
    saida.textContent = "Executando...";

    try {
        const retorno = await fetch("/api/exercicio/compilar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: exercicioAtualIdV14 || exercicioAtualId,
                codigo: codigo.value,
                entrada: entrada ? entrada.value : ""
            })
        });

        const dados = await retorno.json();
        build.textContent = dados.build || "Build finalizado.";

        if (dados.ok) {
            saida.textContent = dados.saida || "Programa executado sem saída.";
        } else {
            saida.textContent = dados.saida || "";
            abrirBuildModal();
        }
    } catch (erro) {
        build.textContent = "Erro de conexão com o compilador.";
        abrirBuildModal();
    }
}

function limparExercicio() {
    const codigo = document.getElementById("codigoExercicio");
    const entrada = document.getElementById("entradaExercicio");
    const saida = document.getElementById("saidaExercicio");
    const build = document.getElementById("buildExercicio");

    if (codigo) codigo.value = "";
    if (entrada) entrada.value = "";
    if (saida) saida.textContent = "Digite a entrada abaixo, se precisar, e clique em Compilar.";
    if (build) build.textContent = "Aguardando build.";
}


// Versão 15: terminal estilo Code::Blocks com entrada dentro da própria janela.
let exercicioTerminalAtual = null;
let codigoTerminalAtual = "";

function fecharTerminalExercicio() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.remove("ativo");
}

function abrirTerminalExercicio() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.add("ativo");
}

function abrirBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.add("ativo");
}

function fecharBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.remove("ativo");
}

async function prepararTerminalCodeblocks(licaoId) {
    const codigo = document.getElementById("codigoExercicio");
    const build = document.getElementById("buildExercicio");
    const prompt = document.getElementById("terminalPrompt");
    const entrada = document.getElementById("entradaExercicio");
    const preview = document.getElementById("entradaDigitadaPreview");
    const btn = document.getElementById("btnEnviarEntrada");

    exercicioTerminalAtual = licaoId;
    codigoTerminalAtual = codigo ? codigo.value : "";

    if (build) build.textContent = "Compilando...";
    if (prompt) prompt.textContent = "Compilando...";
    if (entrada) entrada.value = "";
    if (preview) preview.textContent = "";
    if (btn) btn.style.display = "inline-block";

    try {
        const retorno = await fetch("/api/exercicio/preparar-terminal", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({codigo: codigoTerminalAtual})
        });

        const dados = await retorno.json();

        if (!dados.ok) {
            if (build) build.textContent = dados.build || "Build failed.";
            abrirBuildModal();
            return;
        }

        if (build) build.textContent = dados.build || "Build finished successfully.";

        const textoPrompt = dados.prompt && dados.prompt.trim() ? dados.prompt : "";
        if (prompt) {
            prompt.textContent = textoPrompt;
        }

        abrirTerminalExercicio();

        setTimeout(() => {
            if (entrada) entrada.focus();
        }, 100);

        // Se não houver scanf, executa direto.
        if (!textoPrompt) {
            await enviarEntradaTerminal();
        }
    } catch (erro) {
        if (build) build.textContent = "Erro de conexão ao compilar.";
        abrirBuildModal();
    }
}

async function enviarEntradaTerminal() {
    const entrada = document.getElementById("entradaExercicio");
    const prompt = document.getElementById("terminalPrompt");
    const preview = document.getElementById("entradaDigitadaPreview");
    const btn = document.getElementById("btnEnviarEntrada");

    const valor = entrada ? entrada.value : "";

    if (preview) {
        preview.textContent = valor ? valor : "";
    }

    if (entrada) {
        entrada.style.display = "none";
    }

    if (btn) {
        btn.style.display = "none";
    }

    try {
        const retorno = await fetch("/api/exercicio/compilar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: exercicioTerminalAtual,
                codigo: codigoTerminalAtual,
                entrada: valor
            })
        });

        const dados = await retorno.json();

        if (!dados.ok) {
            const build = document.getElementById("buildExercicio");
            if (build) build.textContent = dados.build || "Build failed.";
            abrirBuildModal();
            return;
        }

        const tela = document.getElementById("terminalTela");
        if (tela) {
            tela.innerHTML = "";
            const pre = document.createElement("pre");
            pre.className = "terminal-final-output";
            pre.textContent = dados.saida || "Programa executado sem saída.";
            tela.appendChild(pre);
        }
    } catch (erro) {
        const tela = document.getElementById("terminalTela");
        if (tela) {
            tela.textContent = "Erro de conexão ao executar.";
        }
    }
}

function limparExercicio() {
    const codigo = document.getElementById("codigoExercicio");
    const entrada = document.getElementById("entradaExercicio");
    const build = document.getElementById("buildExercicio");
    const prompt = document.getElementById("terminalPrompt");
    const preview = document.getElementById("entradaDigitadaPreview");

    if (codigo) codigo.value = "";
    if (entrada) {
        entrada.value = "";
        entrada.style.display = "inline-block";
    }
    if (build) build.textContent = "Aguardando build.";
    if (prompt) prompt.textContent = "Aguardando compilação.";
    if (preview) preview.textContent = "";
}


// Versão 16: não usa /api/exercicio/preparar-terminal.
// O prompt é detectado no navegador para evitar erro 500 antes da execução.
function detectarPromptNoCliente(codigo) {
    const regex = /printf\s*\(\s*"([^"]*)"\s*\)\s*;\s*scanf/s;
    const achou = codigo.match(regex);

    if (achou && achou[1]) {
        return achou[1].replaceAll("\\n", "\n").replaceAll("\\t", "\t");
    }

    if (codigo.includes("scanf")) {
        return "Entrada: ";
    }

    return "";
}

function registrarTentativaCodigo(falhou) {
    const path = window.location.pathname;
    const chave = "tentativas_codigo_" + path;
    let total = Number(localStorage.getItem(chave) || "0");

    if (falhou) {
        total += 1;
        localStorage.setItem(chave, String(total));
    }

    const dica = document.getElementById("dicaTentativas");
    if (dica && total >= 3) {
        dica.classList.remove("hidden-hint");
    }
}

async function prepararTerminalCodeblocks(licaoId) {
    const codigo = document.getElementById("codigoExercicio");
    const prompt = document.getElementById("terminalPrompt");
    const entrada = document.getElementById("entradaExercicio");
    const preview = document.getElementById("entradaDigitadaPreview");
    const btn = document.getElementById("btnEnviarEntrada");

    exercicioTerminalAtual = licaoId;
    codigoTerminalAtual = codigo ? codigo.value : "";

    const textoPrompt = detectarPromptNoCliente(codigoTerminalAtual);

    if (prompt) {
        prompt.textContent = textoPrompt || "Executando programa...";
    }

    if (entrada) {
        entrada.value = "";
        entrada.style.display = textoPrompt ? "inline-block" : "none";
    }

    if (preview) {
        preview.textContent = "";
    }

    if (btn) {
        btn.style.display = textoPrompt ? "inline-block" : "none";
    }

    abrirTerminalExercicio();

    if (textoPrompt) {
        setTimeout(() => {
            if (entrada) entrada.focus();
        }, 100);
    } else {
        await enviarEntradaTerminal();
    }
}

async function enviarEntradaTerminal() {
    const entrada = document.getElementById("entradaExercicio");
    const preview = document.getElementById("entradaDigitadaPreview");
    const btn = document.getElementById("btnEnviarEntrada");

    const valor = entrada ? entrada.value : "";

    if (preview) {
        preview.textContent = valor ? valor : "";
    }

    if (entrada) {
        entrada.style.display = "none";
    }

    if (btn) {
        btn.style.display = "none";
    }

    try {
        const retorno = await fetch("/api/exercicio/compilar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: exercicioTerminalAtual,
                codigo: codigoTerminalAtual,
                entrada: valor
            })
        });

        const dados = await retorno.json();

        if (!dados.ok) {
            registrarTentativaCodigo(true);
            const build = document.getElementById("buildExercicio");
            if (build) build.textContent = dados.build || "Build failed.";
            abrirBuildModal();
            return;
        }

        registrarTentativaCodigo(false);

        const tela = document.getElementById("terminalTela");
        if (tela) {
            tela.innerHTML = "";
            const pre = document.createElement("pre");
            pre.className = "terminal-final-output";
            pre.textContent = dados.saida || "Programa executado sem saída.";
            tela.appendChild(pre);
        }
    } catch (erro) {
        registrarTentativaCodigo(true);
        const build = document.getElementById("buildExercicio");
        if (build) build.textContent = "Erro de conexão ao executar.";
        abrirBuildModal();
    }
}


// Versão 17: simulação visual estilo Code::Blocks.
// Mostra o prompt, usuário digita no terminal e depois o programa executa com essa entrada.
let licaoSimuladaAtual = null;
let codigoSimuladoAtual = "";

function detectarPromptNoClienteV17(codigo) {
    const regex = /printf\s*\(\s*"([^"]*)"\s*\)\s*;\s*scanf/s;
    const achou = codigo.match(regex);

    if (achou && achou[1]) {
        return achou[1].replaceAll("\\n", "\n").replaceAll("\\t", "\t");
    }

    if (codigo.includes("scanf")) {
        return "Entrada:";
    }

    return "";
}

function abrirTerminalSimulado(licaoId) {
    const codigo = document.getElementById("codigoExercicio");
    const tela = document.getElementById("terminalTela");
    const entrada = document.getElementById("entradaExercicio");
    const btn = document.getElementById("btnEnviarEntrada");

    licaoSimuladaAtual = licaoId;
    codigoSimuladoAtual = codigo ? codigo.value : "";

    const prompt = detectarPromptNoClienteV17(codigoSimuladoAtual);

    if (tela) {
        tela.innerHTML = "";

        const span = document.createElement("span");
        span.id = "terminalPrompt";
        span.textContent = prompt || "Executando programa...";

        tela.appendChild(span);

        if (prompt) {
            const input = document.createElement("textarea");
            input.id = "entradaExercicio";
            input.className = "terminal-real-input";
            input.spellcheck = false;
            tela.appendChild(input);

            setTimeout(() => input.focus(), 100);

            input.addEventListener("keydown", (event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    enviarEntradaSimulada();
                }
            });

            if (btn) btn.style.display = "inline-block";
        } else {
            if (btn) btn.style.display = "none";
            setTimeout(() => enviarEntradaSimulada(), 200);
        }
    }

    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.add("ativo");
}

function fecharTerminalExercicio() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.remove("ativo");
}

function abrirBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.add("ativo");
}

function fecharBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.remove("ativo");
}

function registrarTentativaCodigoV17(falhou) {
    const path = window.location.pathname;
    const chave = "tentativas_codigo_" + path;
    let total = Number(localStorage.getItem(chave) || "0");

    if (falhou) {
        total += 1;
        localStorage.setItem(chave, String(total));
    }

    const dica = document.getElementById("dicaTentativas");
    if (dica && total >= 3) {
        dica.classList.remove("hidden-hint");
    }
}

async function enviarEntradaSimulada() {
    const entrada = document.getElementById("entradaExercicio");
    const tela = document.getElementById("terminalTela");
    const build = document.getElementById("buildExercicio");
    const btn = document.getElementById("btnEnviarEntrada");

    const valor = entrada ? entrada.value.trim() : "";

    if (entrada) {
        const digitado = document.createElement("span");
        digitado.textContent = valor;
        entrada.replaceWith(digitado);
    }

    if (btn) btn.style.display = "none";
    if (build) build.textContent = "Compilando...";

    try {
        const retorno = await fetch("/api/exercicio/compilar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: licaoSimuladaAtual,
                codigo: codigoSimuladoAtual,
                entrada: valor
            })
        });

        const dados = await retorno.json();
        if (build) build.textContent = dados.build || "Build finalizado.";

        if (!dados.ok) {
            registrarTentativaCodigoV17(true);
            abrirBuildModal();
            return;
        }

        registrarTentativaCodigoV17(false);

        if (tela) {
            tela.innerHTML = "";
            const pre = document.createElement("pre");
            pre.className = "terminal-final-output";
            pre.textContent = dados.saida || "Programa executado sem saída.";
            tela.appendChild(pre);
        }
    } catch (erro) {
        registrarTentativaCodigoV17(true);
        if (build) build.textContent = "Erro de conexão ao executar.";
        abrirBuildModal();
    }
}

function limparExercicio() {
    const codigo = document.getElementById("codigoExercicio");
    const build = document.getElementById("buildExercicio");
    const tela = document.getElementById("terminalTela");

    if (codigo) codigo.value = "";
    if (build) build.textContent = "Aguardando build.";
    if (tela) tela.textContent = "Aguardando compilação.";
}


// Versão 18: compilador real com WebSocket + stdin/stdout.
let socketTerminal = null;
let terminalFinalizado = false;

function iniciarSocketTerminal() {
    if (socketTerminal) {
        return socketTerminal;
    }

    socketTerminal = io();

    socketTerminal.on("build_log", (dados) => {
        const build = document.getElementById("buildExercicio");
        if (build) build.textContent = dados.texto || "";

        if (!dados.ok) {
            abrirBuildModal();
        } else {
            abrirTerminalReal();
        }
    });

    socketTerminal.on("terminal_saida", (dados) => {
        const saida = document.getElementById("terminalSaidaReal");
        if (!saida) return;

        saida.textContent += dados.texto || "";
        saida.scrollTop = saida.scrollHeight;
    });

    socketTerminal.on("terminal_finalizado", () => {
        terminalFinalizado = true;
        const input = document.getElementById("terminalInputReal");
        if (input) {
            input.disabled = true;
            input.placeholder = "Processo finalizado.";
        }
    });

    return socketTerminal;
}

function compilarReal(licaoId) {
    const codigo = document.getElementById("codigoExercicio");
    const saida = document.getElementById("terminalSaidaReal");
    const input = document.getElementById("terminalInputReal");
    const build = document.getElementById("buildExercicio");

    terminalFinalizado = false;

    if (saida) saida.textContent = "";
    if (input) {
        input.value = "";
        input.disabled = false;
        input.placeholder = "Digite aqui e pressione Enter";
    }
    if (build) build.textContent = "Compilando...";

    const socket = iniciarSocketTerminal();

    socket.emit("compilar_real", {
        licao_id: licaoId,
        codigo: codigo ? codigo.value : ""
    });
}

function abrirTerminalReal() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.add("ativo");

    setTimeout(() => {
        const input = document.getElementById("terminalInputReal");
        if (input) input.focus();
    }, 100);
}

function fecharTerminalReal() {
    const modal = document.getElementById("terminalModalExercicio");
    if (modal) modal.classList.remove("ativo");
}

function abrirBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.add("ativo");
}

function fecharBuildModal() {
    const modal = document.getElementById("buildModal");
    if (modal) modal.classList.remove("ativo");
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("terminalInputReal");

    if (input) {
        input.addEventListener("keydown", (event) => {
            if (event.key === "Enter" && !terminalFinalizado) {
                event.preventDefault();

                const texto = input.value + "\n";
                input.value = "";

                const socket = iniciarSocketTerminal();
                socket.emit("terminal_entrada", {texto: texto});
            }
        });
    }
});

function limparTerminalReal() {
    const codigo = document.getElementById("codigoExercicio");
    const saida = document.getElementById("terminalSaidaReal");
    const input = document.getElementById("terminalInputReal");
    const build = document.getElementById("buildExercicio");

    if (codigo) codigo.value = "";
    if (saida) saida.textContent = "";
    if (input) {
        input.value = "";
        input.disabled = false;
    }
    if (build) build.textContent = "Aguardando compilação.";
}
