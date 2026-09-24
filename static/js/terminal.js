// Compilador e terminal interativo (WebSocket) do exercício, do desafio diário e da prática livre.

let socketTerminal = null;
let terminalFinalizado = true;

function obterCodigoDoEditor(editor) {
    if (typeof window.obterValorEditor === "function") return window.obterValorEditor(editor);
    return editor ? editor.value : "";
}

function definirCodigoNoEditor(editor, valor) {
    if (typeof window.definirValorEditor === "function") {
        window.definirValorEditor(editor, valor);
    } else if (editor) {
        editor.value = valor || "";
        editor.dispatchEvent(new Event("input", {bubbles: true}));
    }
}

function alternarModal(id, aberto) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.toggle("ativo", aberto);
}

function abrirBuildModal() { alternarModal("buildModal", true); }
function fecharBuildModal() { alternarModal("buildModal", false); }
function abrirJanelaTerminal() { alternarModal("terminalModal", true); }

function cancelarExecucao() {
    if (!terminalFinalizado && socketTerminal) {
        socketTerminal.emit("terminal_cancelar");
        terminalFinalizado = true;
        definirCompilacaoEmAndamento(false);
    }
}

function fecharJanelaTerminal() {
    cancelarExecucao();
    alternarModal("terminalModal", false);
}

function abrirTerminalReal() {
    alternarModal("terminalModalExercicio", true);
    setTimeout(() => document.getElementById("terminalInputReal")?.focus(), 100);
}

function fecharTerminalReal() {
    cancelarExecucao();
    alternarModal("terminalModalExercicio", false);
}

function definirCompilacaoEmAndamento(ocupado) {
    document.querySelectorAll('button[onclick*="compilarReal"], button[onclick*="compilarCompiladorInterativo"]')
        .forEach((botao) => {
            botao.disabled = ocupado;
            if (ocupado) botao.setAttribute("aria-busy", "true");
            else botao.removeAttribute("aria-busy");
        });
}

// Cada tentativa sem sucesso libera mais uma dica do exercício (a contagem fica no navegador).
let tentativasSemLocalStorage = 0;

function registrarTentativaCodigo(falhou) {
    const painel = document.getElementById("dicasProgressivas");
    if (!painel) return;

    const chave = "tentativas_" + painel.dataset.chave;
    let total;
    try {
        total = Number(localStorage.getItem(chave) || "0") + (falhou ? 1 : 0);
        if (falhou) localStorage.setItem(chave, String(total));
    } catch (erro) {
        tentativasSemLocalStorage += falhou ? 1 : 0;
        total = tentativasSemLocalStorage;
    }

    const dicas = painel.querySelectorAll("li");
    dicas.forEach((dica, indice) => { dica.hidden = indice >= total; });
    painel.hidden = total === 0;
}

function atualizarFeedbackCorrecao(correcao) {
    const feedback = document.getElementById("feedbackCorrecao");
    if (!feedback || !correcao) return;
    feedback.textContent = correcao.mensagem || "";
    feedback.classList.remove("success", "warning");
    feedback.classList.add(correcao.ok ? "success" : "warning");
    if (!correcao.ok) registrarTentativaCodigo(true);
}

function campoEntradaTerminal() {
    return document.getElementById("terminalInputReal") || document.getElementById("terminalInputCompilador");
}

function iniciarSocketTerminal() {
    if (socketTerminal) return socketTerminal;
    socketTerminal = io();

    socketTerminal.on("build_log", (dados) => {
        const compiladorLivre = Boolean(document.getElementById("codigoCompilador"));
        const build = document.getElementById("buildExercicio") || document.getElementById("buildCompilador");
        if (build) build.textContent = dados.texto || "";

        if (!dados.ok) {
            terminalFinalizado = true;
            definirCompilacaoEmAndamento(false);
            const input = campoEntradaTerminal();
            if (input) input.disabled = true;
            atualizarFeedbackCorrecao({ok: false, mensagem: dados.texto || "Não foi possível compilar o código."});
            if (compiladorLivre) abrirJanelaTerminal();
            else abrirBuildModal();
        } else if (compiladorLivre) {
            abrirJanelaTerminal();
            const painel = document.getElementById("entradaConsoleCompilador");
            const input = document.getElementById("terminalInputCompilador");
            if (painel) painel.hidden = false;
            if (input) {
                input.disabled = false;
                input.placeholder = "";
                setTimeout(() => input.focus(), 80);
            }
        } else {
            abrirTerminalReal();
        }
    });

    socketTerminal.on("terminal_saida", (dados) => {
        const saida = document.getElementById("terminalSaidaReal") || document.getElementById("saidaCompilador");
        if (!saida) return;
        saida.textContent += dados.texto || "";
        saida.scrollTop = saida.scrollHeight;
    });

    socketTerminal.on("terminal_finalizado", () => {
        terminalFinalizado = true;
        definirCompilacaoEmAndamento(false);
        const input = campoEntradaTerminal();
        if (input) {
            input.disabled = true;
            input.placeholder = "Processo finalizado.";
        }
    });

    socketTerminal.on("correcao_resultado", atualizarFeedbackCorrecao);

    socketTerminal.on("connect_error", () => {
        terminalFinalizado = true;
        definirCompilacaoEmAndamento(false);
        const build = document.getElementById("buildCompilador");
        if (build) build.textContent = "Não foi possível conectar ao terminal interativo agora.";
        const feedback = document.getElementById("feedbackCorrecao");
        if (feedback) {
            feedback.textContent = "Não foi possível conectar ao compilador agora.";
            feedback.classList.remove("success");
            feedback.classList.add("warning");
        }
    });

    return socketTerminal;
}

function emitirCompilacao(dados, aoFalhar) {
    try {
        iniciarSocketTerminal().emit("compilar_real", dados);
    } catch (erro) {
        terminalFinalizado = true;
        definirCompilacaoEmAndamento(false);
        aoFalhar("O terminal interativo não carregou. Recarregue a página e tente novamente.");
    }
}

// Exercício da lição e desafio diário.
function compilarReal(licaoId, tipo = "licao") {
    const codigo = document.getElementById("codigoExercicio") || document.getElementById("editorCodigo");
    const saida = document.getElementById("terminalSaidaReal");
    const input = document.getElementById("terminalInputReal");
    const build = document.getElementById("buildExercicio");
    const feedback = document.getElementById("feedbackCorrecao");

    terminalFinalizado = false;
    definirCompilacaoEmAndamento(true);
    if (saida) saida.textContent = "";
    if (input) {
        input.value = "";
        input.disabled = false;
        input.placeholder = "Digite aqui e pressione Enter";
    }
    if (build) build.textContent = "Compilando...";
    if (feedback) {
        feedback.textContent = "Executando e corrigindo automaticamente...";
        feedback.classList.remove("success", "warning");
    }

    emitirCompilacao(
        {licao_id: licaoId, tipo: tipo, codigo: obterCodigoDoEditor(codigo)},
        (mensagem) => atualizarFeedbackCorrecao({ok: false, mensagem: mensagem}),
    );
}

function restaurarCodigoInicial() {
    const inicial = document.getElementById("codigoInicial");
    const codigo = document.getElementById("codigoExercicio") || document.getElementById("editorCodigo");
    if (!inicial || !codigo) return;
    if (confirm("Trocar o código atual pelo código inicial do exercício?")) {
        definirCodigoNoEditor(codigo, inicial.value);
    }
}

function limparTerminalReal() {
    cancelarExecucao();
    const codigo = document.getElementById("codigoExercicio") || document.getElementById("editorCodigo");
    const saida = document.getElementById("terminalSaidaReal");
    const input = document.getElementById("terminalInputReal");
    const build = document.getElementById("buildExercicio");
    const feedback = document.getElementById("feedbackCorrecao");

    if (codigo) definirCodigoNoEditor(codigo, "");
    if (saida) saida.textContent = "";
    if (input) {
        input.value = "";
        input.disabled = false;
    }
    if (build) build.textContent = "Aguardando compilação.";
    if (feedback) {
        feedback.textContent = "Execute o código para receber a correção automática.";
        feedback.classList.remove("success", "warning");
    }
}

// Prática livre (página /compilador).
function compilarCompiladorInterativo() {
    const codigo = document.getElementById("codigoCompilador");
    const saida = document.getElementById("saidaCompilador");
    const build = document.getElementById("buildCompilador");
    const painelEntrada = document.getElementById("entradaConsoleCompilador");
    const input = document.getElementById("terminalInputCompilador");
    if (!codigo || !saida || !build) return;

    const codigoAtual = obterCodigoDoEditor(codigo).trim();
    if (!codigoAtual) {
        build.textContent = "Digite um programa em C antes de compilar.";
        return;
    }

    terminalFinalizado = false;
    definirCompilacaoEmAndamento(true);
    abrirJanelaTerminal();
    saida.textContent = "";
    build.textContent = "Compilando...";
    if (painelEntrada) painelEntrada.hidden = false;
    if (input) {
        input.value = "";
        input.disabled = true;
        input.placeholder = "Aguardando compilação...";
    }

    emitirCompilacao({tipo: "compilador", codigo: codigoAtual}, (mensagem) => {
        build.textContent = mensagem;
    });
}

function limparCompilador() {
    cancelarExecucao();
    const codigo = document.getElementById("codigoCompilador");
    const saida = document.getElementById("saidaCompilador");
    const build = document.getElementById("buildCompilador");
    const input = document.getElementById("terminalInputCompilador");
    const painelEntrada = document.getElementById("entradaConsoleCompilador");

    if (codigo) definirCodigoNoEditor(codigo, "");
    if (input) {
        input.value = "";
        input.disabled = true;
    }
    if (painelEntrada) painelEntrada.hidden = true;
    if (saida) saida.textContent = "Nenhum código foi executado ainda. Clique em Compilar para iniciar.";
    if (build) build.textContent = "Aguardando o usuário clicar em Compilar.";
    definirCompilacaoEmAndamento(false);
}

function carregarHistorico(codigo) {
    const editor = document.getElementById("codigoCompilador");
    if (editor) definirCodigoNoEditor(editor, codigo || "");
}

function enviarLinhaTerminal(input) {
    if (!input || input.disabled || terminalFinalizado) return;
    const texto = input.value + "\n";
    input.value = "";
    iniciarSocketTerminal().emit("terminal_entrada", {texto: texto});
}

function enviarEntradaCompilador() {
    enviarLinhaTerminal(document.getElementById("terminalInputCompilador"));
}

// Rascunho salvo automaticamente enquanto o aluno digita.
let timerSalvamentoAutomatico = null;

function mostrarStatusSalvamento(texto, tipo) {
    const status = document.getElementById("statusSalvamento");
    if (!status) return;
    status.textContent = texto;
    status.classList.remove("saving", "saved", "error");
    status.classList.add(tipo);
}

async function salvarRascunhoAtual() {
    const editorExercicio = document.getElementById("codigoExercicio");
    const editorDiario = document.getElementById("editorCodigo");
    let url = null;
    let dados = null;

    if (editorExercicio && editorExercicio.dataset.licaoId) {
        url = "/api/exercicio/salvar-rascunho";
        dados = {licao_id: Number(editorExercicio.dataset.licaoId), codigo: obterCodigoDoEditor(editorExercicio)};
    } else if (editorDiario && editorDiario.dataset.tipo === "diario") {
        url = "/api/desafio/salvar-rascunho";
        dados = {codigo: obterCodigoDoEditor(editorDiario)};
    }
    if (!url) return;

    mostrarStatusSalvamento("Salvando rascunho...", "saving");
    try {
        const retorno = await fetch(url, {
            method: "POST",
            headers: cabecalhosEnvio({"Content-Type": "application/json"}),
            body: JSON.stringify(dados),
        });
        const resposta = await retorno.json();
        mostrarStatusSalvamento(
            resposta.ok ? "Rascunho salvo." : "Erro ao salvar rascunho.",
            resposta.ok ? "saved" : "error",
        );
    } catch (erro) {
        mostrarStatusSalvamento("Erro ao salvar automaticamente.", "error");
    }
}

function agendarSalvamentoAutomatico() {
    clearTimeout(timerSalvamentoAutomatico);
    mostrarStatusSalvamento("Alterações ainda não salvas...", "saving");
    timerSalvamentoAutomatico = setTimeout(salvarRascunhoAtual, 900);
}

document.addEventListener("DOMContentLoaded", () => {
    ["terminalInputReal", "terminalInputCompilador"].forEach((id) => {
        const input = document.getElementById(id);
        if (!input) return;
        input.addEventListener("keydown", (event) => {
            if (event.key === "Enter" && !event.isComposing && !terminalFinalizado) {
                event.preventDefault();
                enviarLinhaTerminal(input);
            }
        });
    });

    const editorExercicio = document.getElementById("codigoExercicio");
    const editorDiario = document.getElementById("editorCodigo");
    if (editorExercicio) editorExercicio.addEventListener("input", agendarSalvamentoAutomatico);
    if (editorDiario && editorDiario.dataset.tipo === "diario") {
        editorDiario.addEventListener("input", agendarSalvamentoAutomatico);
    }

    registrarTentativaCodigo(false);
});
