from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Lesson

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

# ========================
# INIT BANCO
# ========================
def init_db():
    db.create_all()

    if Lesson.query.count() == 0:
        lessons = [

            # 🧠 ENSINAR
            Lesson(
                title="O que é printf?",
                theory="printf é usado para mostrar texto na tela.",
                code='printf("Hello World");',
                answer="",
                type="theory",
                order=1
            ),

            # 🧪 TESTAR
            Lesson(
                title="Complete o código",
                theory="Complete o Hello World:",
                code='printf("Hello, ____!");',
                answer="world",
                type="challenge",
                order=2
            ),

            # 🧠 ENSINAR
            Lesson(
                title="Variáveis",
                theory="Variáveis guardam valores. Ex: int x = 10;",
                code='int x = 10;',
                answer="",
                type="theory",
                order=3
            ),

            # 🧪 TESTAR
            Lesson(
                title="Complete a variável",
                theory="Complete:",
                code='int x = ____;',
                answer="10",
                type="challenge",
                order=4
            ),
        ]

        db.session.add_all(lessons)
        db.session.commit()

# ========================
# PÁGINAS
# ========================
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/lesson')
def lesson_page():
    return render_template("lesson.html")

# ========================
# LISTAR
# ========================
@app.route('/lessons')
def get_lessons():
    lessons = Lesson.query.order_by(Lesson.order).all()

    return jsonify([
        {"id": l.id, "title": l.title}
        for l in lessons
    ])

# ========================
# PEGAR LIÇÃO
# ========================
@app.route('/lesson/<int:id>')
def get_lesson(id):
    l = Lesson.query.get(id)

    return jsonify({
        "id": l.id,
        "title": l.title,
        "theory": l.theory,
        "code": l.code,
        "type": l.type
    })

# ========================
# NORMALIZAR
# ========================
def normalize(text):
    return text.strip().lower().replace(" ", "")

# ========================
# VERIFICAR
# ========================
@app.route('/answer', methods=['POST'])
def check():
    data = request.get_json()

    lesson_id = data.get("lesson_id")
    answer = data.get("answer", "")

    l = Lesson.query.get(lesson_id)

    if l.type != "challenge":
        return jsonify({"error": "Não é desafio"}), 400

    if normalize(answer) == normalize(l.answer):
        return jsonify({"correct": True})

    return jsonify({"correct": False})

# ========================
# RUN
# ========================
if __name__ == "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)