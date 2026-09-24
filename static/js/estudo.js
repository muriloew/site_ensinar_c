// Desafios teóricos da lição, conclusão de lições e desafios, e busca na jornada de módulos.

async function verificarResposta(licaoId, resposta, botao) {
    const quiz = botao.closest(".quiz");
    const item = quiz.closest(".theory-challenge-item");
    const resultado = item ? item.querySelector(".resultadoQuiz") : null;
    if (!resultado) return;

    const botoes = Array.from(quiz.querySelectorAll("button"));
    botoes.forEach((btn) => {
        btn.classList.remove("correct", "wrong");
        btn.setAttribute("aria-pressed", "false");
        btn.disabled = true;
    });
    botao.setAttribute("aria-pressed", "true");
    resultado.textContent = "Verificando resposta...";

    try {
        const retorno = await fetch("/verificar", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                licao_id: licaoId,
                desafio_id: quiz.dataset.desafioId || "conceito",
                resposta: resposta,
            }),
        });
        const dados = await retorno.json();

        if (!retorno.ok) {
            resultado.textContent = dados.mensagem || "Erro no servidor ao verificar resposta.";
            return;
        }

        const explicacao = dados.explicacao ? ` ${dados.explicacao}` : "";
        botao.classList.add(dados.correta ? "correct" : "wrong");
        item.classList.toggle("completed", Boolean(dados.correta));
        resultado.textContent = `Resposta salva: ${dados.correta ? "correta" : "incorreta"}.${explicacao}`;
        quiz.dataset.respostaSalva = resposta;
        quiz.dataset.correta = dados.correta ? "1" : "0";

        const progresso = document.querySelector(".theory-challenge-progress");
        if (progresso && typeof dados.corretos !== "undefined") {
            progresso.dataset.corretos = dados.corretos;
            progresso.dataset.total = dados.total;
            progresso.textContent = `${dados.corretos}/${dados.total}`;
            progresso.setAttribute("aria-label", `${dados.corretos} de ${dados.total} desafios corretos`);
        }
    } catch (erro) {
        resultado.textContent = "Erro ao verificar resposta. Recarregue a página e tente novamente.";
    } finally {
        botoes.forEach((btn) => { btn.disabled = false; });
    }
}

async function enviarConclusao(url, falha) {
    try {
        const retorno = await fetch(url, {method: "POST"});
        const dados = await retorno.json();
        alert(dados.mensagem || falha);
        return Boolean(dados.ok);
    } catch (erro) {
        alert(`${falha} Verifique sua conexão e tente novamente.`);
        return false;
    }
}

async function concluirLicao(licaoId) {
    if (await enviarConclusao(`/concluir/${licaoId}`, "Não foi possível concluir a lição.")) {
        window.location.href = "/dashboard";
    }
}

async function concluirDesafioDiario() {
    if (await enviarConclusao("/concluir-desafio-diario", "Não foi possível concluir o desafio.")) {
        window.location.reload();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".quiz button[data-resposta]").forEach((botao) => {
        botao.addEventListener("click", () => {
            const quiz = botao.closest(".quiz");
            verificarResposta(Number(quiz.dataset.licaoId), botao.dataset.resposta, botao);
        });
    });

    const busca = document.getElementById("buscaModulos");
    const resultadoBusca = document.getElementById("resultadoBusca");
    const cards = Array.from(document.querySelectorAll("[data-search]"));
    if (!busca || !cards.length) return;

    const normalizar = (texto) => texto.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
    busca.addEventListener("input", () => {
        const termo = normalizar(busca.value.trim());
        let visiveis = 0;
        cards.forEach((card) => {
            const combina = !termo || card.dataset.search.includes(termo);
            card.hidden = !combina;
            if (combina) visiveis += 1;
        });
        if (resultadoBusca) {
            resultadoBusca.textContent = termo ? `${visiveis} módulo(s) encontrado(s).` : "";
        }
    });
});
