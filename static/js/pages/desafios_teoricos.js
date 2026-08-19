document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".module-theory-question").forEach((question) => {
        const expectedAnswer = question.dataset.answer;
        const feedback = question.querySelector(".module-theory-feedback");
        const buttons = question.querySelectorAll("button[data-answer]");

        buttons.forEach((button) => {
            button.addEventListener("click", () => {
                const selectedAnswer = button.dataset.answer;
                const isCorrect = selectedAnswer === expectedAnswer;

                buttons.forEach((item) => {
                    item.classList.remove("correct", "wrong");
                });

                button.classList.add(isCorrect ? "correct" : "wrong");

                if (feedback) {
                    feedback.classList.remove("success", "warning");
                    feedback.classList.add(isCorrect ? "success" : "warning");
                    feedback.textContent = isCorrect
                        ? "Correto. " + feedback.dataset.explanation
                        : "Revise: " + feedback.dataset.explanation;
                }
            });
        });
    });
});
