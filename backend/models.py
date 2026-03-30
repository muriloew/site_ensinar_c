from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))
    theory = db.Column(db.Text)
    code = db.Column(db.Text)
    answer = db.Column(db.String(100))

    type = db.Column(db.String(20))  # "theory" ou "challenge"
    order = db.Column(db.Integer)