from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from backend.models import db, Lesson
import subprocess
import os
import uuid

app = Flask(__name__, template_folder="../templates", static_folder="../static")

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
            Lesson(title="O que é printf?", theory="printf mostra texto.", code='#include <stdio.h>\n\nint main(){\nprintf("Hello World");\nreturn 0;\n}', answer="", type="theory", order=1),

            Lesson(title="Complete o código", theory="Complete:", code='#include <stdio.h>\n\nint main(){\nprintf("Hello, ____!");\nreturn 0;\n}', answer="world", type="challenge", order=2),
        ]

        db.session.add_all(lessons)
        db.session.commit()

# ========================
# ROTAS
# ========================
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/lesson')
def lesson_page():
    return render_template("lesson.html")

@app.route('/lessons')
def get_lessons():
    lessons = Lesson.query.order_by(Lesson.order).all()
    return jsonify([{"id": l.id, "title": l.title} for l in lessons])

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
# VERIFICAR RESPOSTA
# ========================
def normalize(text):
    return text.strip().lower().replace(" ", "")

@app.route('/answer', methods=['POST'])
def check():
    data = request.get_json()
    l = Lesson.query.get(data["lesson_id"])

    if l.type != "challenge":
        return jsonify({"error": "Não é desafio"}), 400

    if normalize(data["answer"]) == normalize(l.answer):
        return jsonify({"correct": True})

    return jsonify({"correct": False})

# ========================
# COMPILADOR REAL
# ========================
@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    filename = f"temp_{uuid.uuid4().hex}"
    c_file = f"{filename}.c"
    exe_file = f"{filename}.out"

    try:
        with open(c_file, "w") as f:
            f.write(code)

        # compilar
        compile_process = subprocess.run(
            ["gcc", c_file, "-o", exe_file],
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:
            return jsonify({"output": compile_process.stderr})

        # dar permissão
        subprocess.run(["chmod", "+x", exe_file])

        # executar
        run_process = subprocess.run(
            [f"./{exe_file}"],
            capture_output=True,
            text=True,
            timeout=5
        )

        return jsonify({"output": run_process.stdout})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "⏱️ Tempo limite excedido"})

    finally:
        if os.path.exists(c_file):
            os.remove(c_file)
        if os.path.exists(exe_file):
            os.remove(exe_file)

# ========================
# START
# ========================
with app.app_context():
    init_db()