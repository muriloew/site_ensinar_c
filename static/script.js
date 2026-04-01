// =====================
// 📦 PROGRESSO
// =====================
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

// =====================
// 📚 LISTAR LIÇÕES
// =====================
async function carregarLicoes() {
    const div = document.querySelector(".lesson-list");
    if (!div) return;

    const res = await fetch("/lessons");
    const data = await res.json();

    const progresso = getProgresso();

    div.innerHTML = "";

    data.forEach(l => {
        const btn = document.createElement("button");

        // ✅ marca concluído
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

// =====================
// 📘 CARREGAR LIÇÃO
// =====================
const params = new URLSearchParams(window.location.search);
const lessonId = parseInt(params.get("id"));

let currentLesson = null;

if (lessonId) {
    fetch("/lesson/" + lessonId)
        .then(res => res.json())
        .then(data => {
            currentLesson = data;

            document.getElementById("title").innerText = data.title;
            document.getElementById("theory").innerText = data.theory;
            document.getElementById("code").innerText = data.code;

            if (data.type === "challenge") {
                document.getElementById("challenge-area").style.display = "block";
                document.getElementById("nextBtn").style.display = "none";
            }
        });
}

// =====================
// ⬅ VOLTAR
// =====================
function voltar() {
    window.location.href = "/";
}

// =====================
// ▶️ PRÓXIMA LIÇÃO
// =====================
async function proxima() {

    // 💾 salva progresso mesmo se for teoria
    salvarProgresso(lessonId);

    const res = await fetch("/lessons");
    const lessons = await res.json();

    const next = lessonId + 1;

    // 🚫 acabou as lições
    if (next > lessons.length) {
        alert("🎉 Você terminou tudo!");
        window.location.href = "/";
        return;
    }

    window.location.href = "/lesson?id=" + next;
}

// =====================
// ✅ VERIFICAR
// =====================
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
        feedback.innerText = "✅ Boa! Continue";
        feedback.style.color = "green";

        // 💾 salva progresso
        salvarProgresso(lessonId);

        document.getElementById("nextBtn").style.display = "block";
    } else {
        feedback.innerText = "❌ Tente novamente";
        feedback.style.color = "red";
    }
}