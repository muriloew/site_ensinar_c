document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".quiz button[data-resposta]").forEach((botao) => {
        botao.addEventListener("click", () => {
            const quiz = botao.closest(".quiz");
            const licaoId = Number(quiz.dataset.licaoId);
            const resposta = botao.dataset.resposta;
            verificarResposta(licaoId, resposta, botao);
        });
    });
});

async function verificarResposta(licaoId, resposta, botao) {
    const resultado = document.getElementById("resultadoQuiz");

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

        resultado.textContent = dados.mensagem;

        if (dados.correta) {
            botao.classList.add("correct");
        } else {
            botao.classList.add("wrong");
        }
    } catch (erro) {
        resultado.textContent = "Erro ao verificar resposta. Recarregue a página e tente novamente.";
    }
}


async function compilarCodigo() {
    const editor = document.getElementById("editorCodigo");
    const buildLog = document.getElementById("buildLog");

    if (!buildLog) {
        return;
    }

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
