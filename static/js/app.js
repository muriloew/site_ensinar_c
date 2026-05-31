async function verificarResposta(licaoId, resposta, botao) {
    const resultado = document.getElementById("resultadoQuiz");

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
    } else {
        botao.classList.add("wrong");
    }
}

async function executarCodigo(licaoId, tipo) {
    const editor = document.getElementById("editorCodigo");
    const saida = document.getElementById("saidaCodigo");

    saida.textContent = "Compilando e executando...";

    const retorno = await fetch("/executar-codigo", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            licao_id: licaoId,
            tipo: tipo,
            codigo: editor.value
        })
    });

    const dados = await retorno.json();
    saida.textContent = dados.saida;
}

async function concluirLicao(licaoId) {
    const retorno = await fetch(`/concluir/${licaoId}`, {method: "POST"});
    const dados = await retorno.json();

    alert(dados.mensagem || "Lição concluída!");

    if (dados.ok) {
        window.location.reload();
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
