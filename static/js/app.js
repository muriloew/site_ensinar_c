async function verificarResposta(licaoId, resposta, botao) {
    const resultado = document.getElementById("resultadoQuiz");
    const concluir = document.getElementById("btnConcluir");

    document.querySelectorAll(".quiz button").forEach(btn => {
        btn.classList.remove("correct", "wrong");
    });

    const retorno = await fetch("/verificar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({licao_id: licaoId, resposta: resposta})
    });

    const dados = await retorno.json();

    resultado.textContent = dados.mensagem;

    if (dados.correta) {
        botao.classList.add("correct");
        concluir.classList.remove("hidden");
    } else {
        botao.classList.add("wrong");
        concluir.classList.add("hidden");
    }
}

async function concluirLicao(licaoId) {
    const retorno = await fetch(`/concluir/${licaoId}`, {method: "POST"});
    const dados = await retorno.json();

    alert(dados.mensagem || "Lição concluída!");
    window.location.reload();
}

function simularExecucao() {
    const saida = document.getElementById("saidaCodigo");
    saida.textContent = "Execução simulada:\nPrograma executado com sucesso.\nObservação: o compilador real pode ser implementado futuramente.";
}

function limparEditor() {
    const editor = document.querySelector(".code-editor");
    editor.value = "";
}
