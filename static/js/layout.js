// Token que acompanha cada envio ao servidor (proteção CSRF).
window.cabecalhosEnvio = function (extras = {}) {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return {...extras, "X-CSRFToken": meta ? meta.content : ""};
};

(function () {
    "use strict";

    const raiz = document.documentElement;

    function aplicarTema(escolha) {
        raiz.dataset.temaEscolhido = escolha;
        raiz.dataset.theme = escolha === "claro" || escolha === "escuro" ? escolha
            : (matchMedia("(prefers-color-scheme: light)").matches ? "claro" : "escuro");
        try { localStorage.setItem("tema", escolha === "sistema" ? "" : escolha); } catch (erro) { /* só nesta página */ }
    }

    // Com "Igual ao sistema", acompanha a troca de claro/escuro feita no aparelho.
    matchMedia("(prefers-color-scheme: light)").addEventListener?.("change", () => {
        if ((raiz.dataset.temaEscolhido || "sistema") === "sistema") aplicarTema("sistema");
    });

    // Configurações: cada mudança é salva na conta na hora e já aparece na página.
    function aplicarPreferencias(preferencias) {
        aplicarTema(preferencias.tema);
        raiz.dataset.textoLicao = preferencias.texto_licao;
        raiz.dataset.corAvatar = preferencias.cor_avatar;
        raiz.dataset.fonteEditor = preferencias.fonte_editor;
        raiz.dataset.tabEditor = preferencias.tab_editor;
        raiz.dataset.quebrarLinhas = preferencias.quebrar_linhas;
        raiz.dataset.fecharParenteses = preferencias.fechar_parenteses;
        raiz.dataset.dicas = preferencias.dicas;
        raiz.dataset.confirmarLimpar = preferencias.confirmar_limpar;
        raiz.toggleAttribute("data-reduzir-animacoes", preferencias.reduzir_animacoes === "sim");
        const previa = document.querySelector(".editor-preview");
        if (previa) {
            previa.style.fontSize = `${Number(preferencias.fonte_editor) || 15}px`;
            const recuo = " ".repeat(Number(preferencias.tab_editor));
            previa.textContent = previa.textContent.replace(/^ +/gm, recuo);
        }
    }

    const formPreferencias = document.querySelector("[data-preferencias-automaticas]");
    if (formPreferencias) {
        const status = formPreferencias.querySelector("[data-preferencia-status]");
        formPreferencias.classList.add("salvamento-automatico");
        let pedido = 0;
        formPreferencias.addEventListener("change", async () => {
            const numero = ++pedido;
            if (status) status.textContent = "Salvando...";
            try {
                const resposta = await fetch(formPreferencias.action || location.pathname, {
                    method: "POST",
                    body: new FormData(formPreferencias),
                    headers: window.cabecalhosEnvio({"Accept": "application/json"}),
                });
                const dados = await resposta.json();
                if (!resposta.ok || !dados.ok) throw new Error("falha");
                if (numero !== pedido) return;
                aplicarPreferencias(dados.preferencias);
                if (status) status.textContent = "✓ Salvo na sua conta.";
            } catch (erro) {
                if (status) status.textContent = "Não foi possível salvar agora. Verifique a conexão e tente de novo.";
            }
        });
    }

    document.querySelector("[data-zerar-dicas]")?.addEventListener("click", () => {
        let apagadas = 0;
        try {
            Object.keys(localStorage).filter((chave) => chave.startsWith("tentativas_")).forEach((chave) => {
                localStorage.removeItem(chave);
                apagadas++;
            });
        } catch (erro) { /* navegador sem armazenamento: não há dicas guardadas */ }
        const status = document.querySelector("[data-zerar-dicas-status]");
        if (status) status.textContent = apagadas
            ? "Pronto: as dicas voltam a aparecer só depois de novas tentativas."
            : "Não havia dicas liberadas neste aparelho.";
    });

    // Formulários com data-confirmar pedem confirmação antes de enviar.
    document.addEventListener("submit", (evento) => {
        const mensagem = evento.target.dataset?.confirmar;
        if (mensagem && !confirm(mensagem)) evento.preventDefault();
    });

    document.querySelectorAll("[data-mostrar-senha]").forEach((caixa) => {
        caixa.addEventListener("change", () => {
            caixa.closest("form").querySelectorAll('input[type="password"], input[data-era-senha]').forEach((campo) => {
                campo.dataset.eraSenha = "1";
                campo.type = caixa.checked ? "text" : "password";
            });
        });
    });

    // Em telas menores, o menu fica recolhido atrás do botão "Menu".
    const botaoMenu = document.querySelector('.menu-toggle');
    if (botaoMenu) {
        const barra = botaoMenu.closest('.sidebar');
        const definirMenu = (aberto) => {
            barra.classList.toggle('menu-aberto', aberto);
            botaoMenu.setAttribute('aria-expanded', aberto ? 'true' : 'false');
        };
        botaoMenu.addEventListener('click', () => definirMenu(!barra.classList.contains('menu-aberto')));
        document.addEventListener('keydown', (evento) => {
            if (evento.key === 'Escape' && barra.classList.contains('menu-aberto')) {
                definirMenu(false);
                botaoMenu.focus();
            }
        });
    }

    const menu = document.querySelector('.sidebar nav');
    if (menu) {
        const caminho = /^\/(estudar|exercicio)\//.test(location.pathname)
            ? '/modulos' : location.pathname;
        const atual = Array.from(menu.querySelectorAll('a')).find(link => link.pathname === caminho);
        if (atual) {
            atual.setAttribute('aria-current', 'page');
            if (menu.scrollWidth > menu.clientWidth) {
                menu.scrollLeft = atual.offsetLeft - menu.offsetLeft - 12;
            }
        }
    }

    const modais = Array.from(document.querySelectorAll('.console-modal'));
    if (!modais.length) return;

    let modalAtual = null;
    let focoAnterior = null;
    let ultimoAcionador = null;
    const conteudo = Array.from(document.querySelectorAll('main > *, .sidebar'))
        .filter(elemento => !modais.some(modal => elemento.contains(modal)));

    function ajustarAltura() {
        const viewport = window.visualViewport;
        document.documentElement.style.setProperty('--console-viewport-height', `${viewport ? viewport.height : innerHeight}px`);
        document.documentElement.style.setProperty('--console-viewport-top', `${viewport ? viewport.offsetTop : 0}px`);
    }

    function controles(modal) {
        return Array.from(modal.querySelectorAll('button:not(:disabled), input:not(:disabled), textarea:not(:disabled), summary, a[href], [tabindex="0"]'))
            .filter(elemento => elemento.getClientRects().length > 0);
    }

    function atualizarModal() {
        const ativo = modais.filter(modal => modal.classList.contains('ativo')).pop() || null;
        if (ativo === modalAtual) return;
        if (!modalAtual && ativo) focoAnterior = ultimoAcionador || document.activeElement;
        modalAtual = ativo;
        document.body.classList.toggle('console-aberto', Boolean(ativo));
        conteudo.forEach(elemento => { elemento.inert = Boolean(ativo); });
        if (ativo) {
            ajustarAltura();
            const entrada = ativo.querySelector('input:not(:disabled)');
            (entrada || controles(ativo)[0] || ativo.querySelector('.console-window')).focus({preventScroll: true});
        } else if (focoAnterior && focoAnterior.isConnected) {
            focoAnterior.focus({preventScroll: true});
            focoAnterior = null;
        }
    }

    modais.forEach(modal => {
        const janela = modal.querySelector('.console-window');
        if (!janela) return;
        janela.setAttribute('role', 'dialog');
        janela.setAttribute('aria-modal', 'true');
        janela.setAttribute('tabindex', '-1');
        const titulo = janela.querySelector('.codeblocks-titlebar span, .console-titlebar strong');
        janela.setAttribute('aria-label', titulo ? titulo.textContent.replaceAll('"', '') : 'Terminal');
        const fechar = janela.querySelector('.codeblocks-titlebar button, .console-titlebar button');
        if (fechar) fechar.setAttribute('aria-label', 'Fechar janela');
        new MutationObserver(atualizarModal).observe(modal, {attributes: true, attributeFilter: ['class']});
    });

    // Safari does not always focus a button when it is clicked.
    document.addEventListener('click', event => {
        if (!modalAtual) ultimoAcionador = event.target.closest('button, a[href], input, textarea');
    }, true);

    document.addEventListener('keydown', event => {
        if (!modalAtual) {
            ultimoAcionador = null;
            return;
        }
        if (event.key === 'Escape') {
            event.preventDefault();
            modalAtual.querySelector('.codeblocks-titlebar button, .console-titlebar button')?.click();
        } else if (event.key === 'Tab') {
            const itens = controles(modalAtual);
            const primeiro = itens[0];
            const ultimo = itens[itens.length - 1];
            if (event.shiftKey && document.activeElement === primeiro) {
                event.preventDefault();
                ultimo?.focus();
            } else if (!event.shiftKey && document.activeElement === ultimo) {
                event.preventDefault();
                primeiro?.focus();
            }
        }
    });
    window.addEventListener('resize', ajustarAltura);
    window.visualViewport?.addEventListener('resize', ajustarAltura);
    window.visualViewport?.addEventListener('scroll', ajustarAltura);
    ajustarAltura();
    atualizarModal();
}());
