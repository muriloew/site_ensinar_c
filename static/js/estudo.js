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
            headers: cabecalhosEnvio({"Content-Type": "application/json"}),
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
        const retorno = await fetch(url, {method: "POST", headers: cabecalhosEnvio()});
        const dados = await retorno.json();
        alert(dados.mensagem || falha);
        return dados.ok ? dados : null;
    } catch (erro) {
        alert(`${falha} Verifique sua conexão e tente novamente.`);
        return null;
    }
}

async function concluirLicao(licaoId) {
    const dados = await enviarConclusao(`/concluir/${licaoId}`, "Não foi possível concluir a lição.");
    if (dados) window.location.href = dados.proxima || "/dashboard";
}

async function concluirDesafioDiario() {
    if (await enviarConclusao("/concluir-desafio-diario", "Não foi possível concluir o desafio.")) {
        window.location.reload();
    }
}

async function copiarCodigo(botao) {
    const codigo = botao.closest(".card, section, main").querySelector(".code-window code");
    if (!codigo) return;
    const original = botao.textContent;
    try {
        await navigator.clipboard.writeText(codigo.textContent);
        botao.textContent = "Copiado!";
    } catch (erro) {
        botao.textContent = "Selecione e copie com Ctrl+C";
    }
    setTimeout(() => { botao.textContent = original; }, 2000);
}

let timerAnotacao = null;

async function salvarAnotacao(campo) {
    const status = document.getElementById("statusAnotacao");
    try {
        const retorno = await fetch(`/api/anotacoes/${campo.dataset.licaoId}`, {
            method: "POST",
            headers: cabecalhosEnvio({"Content-Type": "application/json"}),
            body: JSON.stringify({texto: campo.value}),
        });
        const dados = await retorno.json();
        if (status) status.textContent = dados.ok ? "Anotação salva." : (dados.mensagem || "Não foi possível salvar.");
    } catch (erro) {
        if (status) status.textContent = "Sem conexão: a anotação ainda não foi salva.";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".quiz button[data-resposta]").forEach((botao) => {
        botao.addEventListener("click", () => {
            const quiz = botao.closest(".quiz");
            verificarResposta(Number(quiz.dataset.licaoId), botao.dataset.resposta, botao);
        });
    });

    document.querySelectorAll("[data-copiar-codigo]").forEach((botao) => {
        botao.addEventListener("click", () => copiarCodigo(botao));
    });

    const anotacao = document.getElementById("anotacaoLicao");
    if (anotacao) {
        anotacao.addEventListener("input", () => {
            const status = document.getElementById("statusAnotacao");
            if (status) status.textContent = "Salvando...";
            clearTimeout(timerAnotacao);
            timerAnotacao = setTimeout(() => salvarAnotacao(anotacao), 800);
        });
    }

    const buscaReferencia = document.getElementById("buscaReferencia");
    if (buscaReferencia) {
        const itens = Array.from(document.querySelectorAll("[data-busca]"));
        const resultado = document.getElementById("resultadoReferencia");
        const normalizarTexto = (texto) => texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
        itens.forEach((item) => { item.dataset.texto = normalizarTexto(item.textContent); });
        buscaReferencia.addEventListener("input", () => {
            const termo = normalizarTexto(buscaReferencia.value.trim());
            let visiveis = 0;
            itens.forEach((item) => {
                const combina = !termo || item.dataset.texto.includes(termo);
                item.hidden = !combina;
                if (combina) visiveis += 1;
            });
            document.querySelectorAll(".reference-section").forEach((secao) => {
                secao.hidden = Boolean(termo) && !secao.querySelector("[data-busca]:not([hidden])");
            });
            if (resultado) resultado.textContent = termo ? `${visiveis} resultado(s).` : "";
        });
    }

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
