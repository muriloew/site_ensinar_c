(function () {
    "use strict";

    const editores = new Map();
    const sugestoesC = [
        "auto", "break", "case", "char", "const", "continue", "default", "do",
        "double", "else", "enum", "extern", "float", "for", "free", "fgets",
        "fopen", "fclose", "fprintf", "fscanf", "if", "int", "long", "malloc",
        "printf", "realloc", "register", "return", "scanf", "short", "signed",
        "sizeof", "static", "strcat", "strcmp", "strcpy", "strlen", "struct",
        "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
        "#include <stdio.h>", "#include <stdlib.h>", "#include <string.h>",
        "#include <math.h>", "printf(\"\\n\");", "scanf(\"%d\", &valor);",
        "int main(void) {\n    \n    return 0;\n}",
        "if (condicao) {\n    \n}",
        "for (int i = 0; i < limite; i++) {\n    \n}",
        "while (condicao) {\n    \n}",
    ];

    function elementoEditor(alvo) {
        if (typeof alvo === "string") return document.getElementById(alvo);
        return alvo || null;
    }

    function obterEditor(alvo) {
        const elemento = elementoEditor(alvo);
        return elemento ? editores.get(elemento.id) || null : null;
    }

    window.obterValorEditor = function (alvo) {
        const elemento = elementoEditor(alvo);
        const editor = obterEditor(elemento);
        return editor ? editor.getValue() : elemento ? elemento.value : "";
    };

    window.definirValorEditor = function (alvo, valor) {
        const elemento = elementoEditor(alvo);
        const editor = obterEditor(elemento);
        const texto = valor || "";
        if (editor) {
            editor.setValue(texto);
            editor.focus();
        } else if (elemento) {
            elemento.value = texto;
            elemento.dispatchEvent(new Event("input", {bubbles: true}));
        }
    };

    function executarAtalho(editor) {
        const id = editor.getTextArea().id;
        if (id === "codigoCompilador" && typeof window.executarCompiladorOnline === "function") {
            window.executarCompiladorOnline();
        } else if (id === "codigoExercicio" && typeof window.compilarReal === "function") {
            const licaoId = Number(editor.getTextArea().dataset.licaoId);
            window.compilarReal(licaoId, "licao");
        } else if (id === "editorCodigo" && typeof window.compilarReal === "function") {
            window.compilarReal(null, "diario");
        }
    }

    function salvarAtalho(editor) {
        editor.save();
        const textarea = editor.getTextArea();
        if (textarea.id === "codigoCompilador") {
            localStorage.setItem("ensinar-c-pratica-livre", editor.getValue());
        } else if (typeof window.salvarRascunhoAtual === "function") {
            window.salvarRascunhoAtual();
        }
    }

    function moverLinha(editor, direcao) {
        const inicio = editor.getCursor("from").line;
        const fim = editor.getCursor("to").line;
        const destino = direcao < 0 ? inicio - 1 : fim + 1;
        if (destino < 0 || destino >= editor.lineCount()) return;

        editor.operation(() => {
            const linhas = [];
            for (let linha = inicio; linha <= fim; linha += 1) linhas.push(editor.getLine(linha));
            const textoDestino = editor.getLine(destino);
            if (direcao < 0) {
                editor.replaceRange(linhas.join("\n") + "\n" + textoDestino, {line: destino, ch: 0}, {line: fim, ch: editor.getLine(fim).length});
                editor.setSelection({line: inicio - 1, ch: 0}, {line: fim - 1, ch: linhas[linhas.length - 1].length});
            } else {
                editor.replaceRange(textoDestino + "\n" + linhas.join("\n"), {line: inicio, ch: 0}, {line: destino, ch: textoDestino.length});
                editor.setSelection({line: inicio + 1, ch: 0}, {line: fim + 1, ch: linhas[linhas.length - 1].length});
            }
        });
    }

    function duplicarLinha(editor) {
        const inicio = editor.getCursor("from").line;
        const fim = editor.getCursor("to").line;
        const linhas = [];
        for (let linha = inicio; linha <= fim; linha += 1) linhas.push(editor.getLine(linha));
        editor.replaceRange("\n" + linhas.join("\n"), {line: fim, ch: editor.getLine(fim).length});
        editor.setSelection({line: inicio + linhas.length, ch: 0}, {line: fim + linhas.length, ch: linhas[linhas.length - 1].length});
    }

    function completar(editor) {
        const cursor = editor.getCursor();
        const linha = editor.getLine(cursor.line);
        const trecho = linha.slice(0, cursor.ch);
        const encontrado = trecho.match(/[#\w.<>]+$/);
        const termo = encontrado ? encontrado[0] : "";
        const inicio = CodeMirror.Pos(cursor.line, cursor.ch - termo.length);
        const filtro = termo.toLowerCase();
        const lista = sugestoesC
            .filter((item) => !filtro || item.toLowerCase().startsWith(filtro))
            .map((item) => ({text: item, displayText: item.split("\n")[0]}));
        return {list: lista, from: inicio, to: cursor};
    }

    function formatar(editor) {
        editor.operation(() => {
            for (let linha = 0; linha < editor.lineCount(); linha += 1) {
                editor.indentLine(linha, "smart");
            }
        });
    }

    function criarBotao(rotulo, titulo, acao) {
        const botao = document.createElement("button");
        botao.type = "button";
        botao.className = "ide-tool-button";
        botao.textContent = rotulo;
        botao.title = titulo;
        botao.setAttribute("aria-label", titulo);
        botao.addEventListener("click", acao);
        return botao;
    }

    function montarInterface(textarea, editor) {
        const frame = editor.getWrapperElement().closest(".ide-editor-frame");
        const toolbar = document.createElement("div");
        toolbar.className = "ide-editor-toolbar";
        toolbar.append(
            criarBotao("↶", "Desfazer", () => editor.undo()),
            criarBotao("↷", "Refazer", () => editor.redo()),
            criarBotao("{ }", "Organizar indentação", () => formatar(editor)),
            criarBotao("⌕", "Sugerir comando C", () => editor.showHint({hint: completar, completeSingle: false})),
        );

        const status = document.createElement("div");
        status.className = "ide-editor-status";
        const posicao = document.createElement("span");
        const linguagem = document.createElement("span");
        linguagem.textContent = "C11";
        status.append(posicao, linguagem);

        function atualizarPosicao() {
            const cursor = editor.getCursor();
            posicao.textContent = `Ln ${cursor.line + 1}, Col ${cursor.ch + 1}`;
        }

        frame.insertBefore(toolbar, editor.getWrapperElement());
        frame.appendChild(status);
        editor.on("cursorActivity", atualizarPosicao);
        atualizarPosicao();
    }

    function iniciarEditor(textarea) {
        const frame = document.createElement("div");
        frame.className = `ide-editor-frame ide-editor-${textarea.id}`;
        textarea.parentNode.insertBefore(frame, textarea);
        frame.appendChild(textarea);

        const editor = CodeMirror.fromTextArea(textarea, {
            mode: "text/x-csrc",
            theme: "material-darker",
            lineNumbers: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: false,
            extraKeys: {
                "Ctrl-Enter": executarAtalho,
                "Cmd-Enter": executarAtalho,
                "Ctrl-S": salvarAtalho,
                "Cmd-S": salvarAtalho,
                "Ctrl-Space": (cm) => cm.showHint({hint: completar, completeSingle: false}),
                "Ctrl-/": (cm) => cm.execCommand("toggleComment"),
                "Cmd-/": (cm) => cm.execCommand("toggleComment"),
                "Alt-Up": (cm) => moverLinha(cm, -1),
                "Alt-Down": (cm) => moverLinha(cm, 1),
                "Shift-Alt-Down": duplicarLinha,
                "Tab": (cm) => cm.somethingSelected() ? cm.indentSelection("add") : cm.execCommand("insertSoftTab"),
                "Shift-Tab": (cm) => cm.indentSelection("subtract"),
            },
        });

        const campoEntrada = editor.getInputField();
        campoEntrada.setAttribute("aria-label", "Editor de código C");
        campoEntrada.setAttribute("autocomplete", "off");
        campoEntrada.setAttribute("autocapitalize", "off");
        campoEntrada.setAttribute("spellcheck", "false");

        editores.set(textarea.id, editor);
        textarea._codeMirror = editor;
        editor.on("change", () => {
            editor.save();
            textarea.dispatchEvent(new Event("input", {bubbles: true}));
            if (textarea.id === "codigoCompilador" && !new URLSearchParams(location.search).has("licao_id")) {
                clearTimeout(editor._timerPraticaLivre);
                editor._timerPraticaLivre = setTimeout(() => {
                    localStorage.setItem("ensinar-c-pratica-livre", editor.getValue());
                }, 500);
            }
        });

        if (textarea.id === "codigoCompilador" && !new URLSearchParams(location.search).has("licao_id")) {
            const salvo = localStorage.getItem("ensinar-c-pratica-livre");
            if (salvo && salvo.trim()) editor.setValue(salvo);
        }

        montarInterface(textarea, editor);
        setTimeout(() => editor.refresh(), 0);
    }

    document.addEventListener("DOMContentLoaded", () => {
        if (typeof window.CodeMirror === "undefined") return;
        document.querySelectorAll("textarea.code-editor").forEach(iniciarEditor);
        window.editoresCodigo = editores;
    });
}());
