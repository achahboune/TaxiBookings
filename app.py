from flask import Flask, render_template, session, request
from questions import QUESTIONS_ORDER
from google_sheets import append_booking
import re
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'changez_cette_clef')

def validate_input(index, value):
    key, label, required = QUESTIONS_ORDER[index]
    if required and not value:
        return False, "Ce champ est obligatoire."
    if key == "date" and value:
        if not re.match(r"\d{2}/\d{2}/\d{4}", value):
            return False, "Format attendu JJ/MM/AAAA."
    if key == "time" and value:
        if not re.match(r"\d{2}:\d{2}", value):
            return False, "Format attendu HH:MM."
    if key == "phone" and value:
        if not re.match(r"^[0-9]{10,}$", value):
            return False, "Numéro invalide."
    if key == "email" and value:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            return False, "Email invalide."
    return True, ""

@app.route("/", methods=["GET", "POST"])
def chat():
    if "answers" not in session:
        session["answers"] = []
        session["index"] = 0

    if request.method == "POST":
        user_input = request.form.get("answer", "").strip()
        index = session["index"]
        key, label, required = QUESTIONS_ORDER[index]

        if not user_input and not required:
            session["answers"].append("")
            session["index"] += 1
        else:
            valid, error_msg = validate_input(index, user_input)
            if not valid:
                return render_template("chat.html", question=label, error=error_msg, value=user_input)
            session["answers"].append(user_input)
            session["index"] += 1

        if session["index"] >= len(QUESTIONS_ORDER):
            data = session["answers"]
            append_booking(data)
            recap = dict(zip([q[0] for q in QUESTIONS_ORDER], data))
            session.clear()
            return render_template("chat.html", recap=recap)

    index = session.get("index", 0)
    if index >= len(QUESTIONS_ORDER):
        session.clear()
        return render_template("chat.html", recap=None)

    key, label, required = QUESTIONS_ORDER[index]
    return render_template("chat.html", question=label, error="", value="")

if __name__ == "__main__":
    app.run(debug=True)
