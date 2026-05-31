async function verificarResposta(botao, resposta, respostaCorreta) {
    const card = botao.closest(".licao");
    const resultado = card.querySelector(".resultado");
    const botoes = card.querySelectorAll(".alternativa");

    botoes.forEach((item) => {
        item.classList.remove("correta", "errada");
    });

    try {
        const retorno = await fetch("/api/verificar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resposta: resposta,
                resposta_correta: respostaCorreta
            })
        });

        const dados = await retorno.json();

        if (dados.acertou) {
            botao.classList.add("correta");
            resultado.className = "resultado correto";
        } else {
            botao.classList.add("errada");
            resultado.className = "resultado errado";
        }

        resultado.textContent = dados.mensagem;
    } catch (erro) {
        resultado.className = "resultado errado";
        resultado.textContent = "Erro ao verificar resposta.";
    }
}
