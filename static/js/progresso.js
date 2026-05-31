function buscarLicoesConcluidas() {
    const dados = localStorage.getItem("licoesConcluidas");

    if (!dados) {
        return [];
    }

    try {
        return JSON.parse(dados);
    } catch (erro) {
        return [];
    }
}

function salvarLicoesConcluidas(licoes) {
    localStorage.setItem("licoesConcluidas", JSON.stringify(licoes));
}

function marcarConcluida(idLicao) {
    const licoes = buscarLicoesConcluidas();

    if (!licoes.includes(idLicao)) {
        licoes.push(idLicao);
    }

    salvarLicoesConcluidas(licoes);
    atualizarVisualLicoes();
    atualizarBarraProgresso();
}

function atualizarVisualLicoes() {
    const licoes = buscarLicoesConcluidas();

    document.querySelectorAll("[data-licao-id]").forEach((elemento) => {
        const idLicao = elemento.getAttribute("data-licao-id");

        if (licoes.includes(idLicao)) {
            elemento.classList.add("concluida");
        }
    });
}

function atualizarBarraProgresso() {
    const barra = document.getElementById("barraProgresso");
    const texto = document.getElementById("textoProgresso");

    if (!barra || !texto) {
        return;
    }

    const concluidas = buscarLicoesConcluidas().length;
    const total = typeof TOTAL_LICOES !== "undefined" ? TOTAL_LICOES : 1;
    const porcentagem = Math.round((concluidas / total) * 100);

    barra.style.width = `${porcentagem}%`;
    texto.textContent = `${concluidas} de ${total} lições concluídas (${porcentagem}%).`;
}

document.addEventListener("DOMContentLoaded", () => {
    atualizarVisualLicoes();
    atualizarBarraProgresso();
});
