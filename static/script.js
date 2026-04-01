function voltar() {
    window.location.href = "/";
}

// progresso
function getProgresso() {
    return JSON.parse(localStorage.getItem("progresso") || "[]");
}

function salvarProgresso(id) {
    let progresso = getProgresso();
    if (!progresso.includes(id)) {
        progresso.push(id);
        localStorage.setItem("progresso", JSON.stringify(progresso));
    }
}

// listar lições
async function carregarLicoes() {
    const div = document.querySelector(".lesson-list");
    if (!div) return;

    const res = await fetch("/lessons");
    const data = await res.json();

    const progresso = getProgresso();

    div.innerHTML = "";

    data.forEach(l => {
        const btn = document.createElement("button");

        if (progresso.includes(l.id)) {
            btn.innerText = "✅ " + l.title;
            btn.style.background = "#999";
        } else {
            btn.innerText = l.title;
        }

        btn.onclick = () => {
            window.location.href = "/lesson?id=" + l.id;
        };

        div.appendChild(btn);
    });
}

if (document.querySelector(".lesson-list")) {
    carregarLicoes();
}

// carregar lição
const params = new URLSearchParams(window.location.search);
const lessonId = parseInt(params.get("id"));

if (lessonId) {
    fetch("/lesson/" + lessonId)
        .then(res => res.json())
        .then(data => {
            document.getElementById("title").innerText = data.title;
            document.getElementById("theory").innerText = data.theory;
            document.getElementById("code").innerText = data.code;

            document.getElementById("codeInput").value = data.code;

            if (data.type === "challenge") {
                document.getElementById("challenge-area").style.display = "block";
                document.getElementById("nextBtn").style.display = "none";
            }
        });
}

// próxima
async function proxima() {
    const res = await fetch("/lessons");
    const lessons = await res.json();

    const next = lessonId + 1;

    if (next > lessons.length) {
        alert("🎉 Você terminou!");
        window.location.href = "/";
        return;
    }

    window.location.href = "/lesson?id=" + next;
}

// verificar
async function verificar() {
    const resposta = document.getElementById("answer").value;
    const feedback = document.getElementById("feedback");

    const res = await fetch("/answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            lesson_id: lessonId,
            answer: resposta
        })
    });

    const data = await res.json();

    if (data.correct) {
        feedback.innerText = "✅ Boa!";
        feedback.style.color = "green";
        salvarProgresso(lessonId);
        document.getElementById("nextBtn").style.display = "block";
    } else {
        feedback.innerText = "❌ Tente novamente";
        feedback.style.color = "red";
    }
}

// compilador REAL
async function executarCodigo() {
    const code = document.getElementById("codeInput").value;
    const output = document.getElementById("output");

    output.innerText = "⏳ Executando...";

    const res = await fetch("/run", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code })
    });

    const data = await res.json();

    output.innerText = data.output;
}