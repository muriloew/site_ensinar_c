(function () {
    "use strict";

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
