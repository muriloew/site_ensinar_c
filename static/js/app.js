
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
