async function carregarLicoes() {
    const div = document.querySelector(".lesson-list");
    if (!div) return;

    const res = await fetch("/lessons");
    const data = await res.json();

    div.innerHTML = "";

    data.forEach(l => {
        const btn = document.createElement("button");
        btn.innerText = l.title;

        btn.onclick = () => {
            window.location.href = "/lesson?id=" + l.id;
        };

        div.appendChild(btn);
    });
}

if (document.querySelector(".lesson-list")) {
    carregarLicoes();
}

const params = new URLSearchParams(window.location.search);
const lessonId = params.get("id");

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

function proxima() {
    window.location.href = "/lesson?id=" + (parseInt(lessonId) + 1);
}

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
        document.getElementById("nextBtn").style.display = "block";
    } else {
        feedback.innerText = "❌ Tente novamente";
        feedback.style.color = "red";
    }
}