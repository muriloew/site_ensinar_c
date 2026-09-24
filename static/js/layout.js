// Token que acompanha cada envio ao servidor (proteção CSRF).
window.cabecalhosEnvio = function (extras = {}) {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return {...extras, "X-CSRFToken": meta ? meta.content : ""};
};

(function () {
    "use strict";

    function lerPreferencia(chave) {
        try { return localStorage.getItem(chave) || ""; } catch (erro) { return ""; }
    }

    function salvarPreferencia(chave, valor) {
        try {
            if (valor) localStorage.setItem(chave, valor);
            else localStorage.removeItem(chave);
            return true;
        } catch (erro) {
            return false;
        }
    }

    const botaoTema = document.querySelector("[data-alternar-tema]");
    function aplicarTema(escolha) {
        const tema = escolha || (matchMedia("(prefers-color-scheme: light)").matches ? "claro" : "escuro");
        document.documentElement.dataset.theme = tema;
        if (botaoTema) {
            botaoTema.textContent = tema === "claro" ? "◐ Tema escuro" : "◐ Tema claro";
            botaoTema.setAttribute("aria-pressed", String(tema === "claro"));
        }
    }
    aplicarTema(lerPreferencia("tema"));
    botaoTema?.addEventListener("click", () => {
        const novo = document.documentElement.dataset.theme === "claro" ? "escuro" : "claro";
        salvarPreferencia("tema", novo);
        aplicarTema(novo);
        const seletor = document.querySelector('[data-preferencia="tema"]');
        if (seletor) seletor.value = novo;
    });

    // Página de configurações: preferências guardadas no navegador.
    const statusPreferencia = document.querySelector("[data-preferencia-status]");
    document.querySelectorAll("[data-preferencia]").forEach((seletor) => {
        const chave = seletor.dataset.preferencia;
        seletor.value = lerPreferencia(chave) || (chave === "tema" ? "sistema" : "");
        seletor.addEventListener("change", () => {
            const valor = seletor.value === "sistema" ? "" : seletor.value;
            const salvo = salvarPreferencia(chave, valor);
            if (chave === "tema") aplicarTema(valor);
            if (statusPreferencia) {
                statusPreferencia.textContent = salvo
                    ? "Preferência salva."
                    : "O navegador bloqueou o armazenamento; a escolha vale só nesta página.";
            }
        });
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
