# ================= FULL app.py (COPY–PASTE READY) =================
# Purpose: Login (no blank screen) → Exam with questions → Submit → Result
# Notes:
# - Uses in-memory flags (simple & stable for now)
# - Templates required: login.html, exam.html, result.html
# - PWA files optional: manifest.json, service-worker.js (served below)

from flask import Flask, render_template, request, redirect, session, abort, send_from_directory
import ast

app = Flask(__name__)
app.secret_key = "mock_exam_secret_key_123"

# ================= ADMIN FLAGS =================
EXAM_ACTIVE = True        # set False to block exam
ANSWER_KEY_ACTIVE = True # set False to hide answers

# ================= QUESTIONS =================
QUESTIONS = [
    {
        "id": "q1",
        "question": "Which statement is TRUE about the Industrial Policy Resolution of 1956?",
        "options": [
            "It aimed to promote only private industries",
            "It classified industries into three categories",
            "It discouraged public sector investment",
            "It focused only on agriculture"
        ],
        "answer": 1
    },
    {
        "id": "q2",
        "question": "Shudraka wrote which play?",
        "options": [
            "Ditta Mangalika",
            "Mrichchhakatika",
            "Jataka Kathayen",
            "Manusmriti"
        ],
        "answer": 1
    },
    {
        "id": "q3",
        "question": "Baisakhi is associated with which Sikh institution?",
        "options": [
            "Akal Takht",
            "Khalsa Panth",
            "Harmandir Sahib",
            "Guru Granth Sahib"
        ],
        "answer": 1
    }
]

# ================= PWA FILES =================
@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(".", "service-worker.js")

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not EXAM_ACTIVE:
            return render_template("login.html", exam_active=EXAM_ACTIVE)

        session.clear()
        session["name"] = request.form.get("name")
        return redirect("/exam")

    return render_template("login.html", exam_active=EXAM_ACTIVE)

# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if not EXAM_ACTIVE:
        return redirect("/")

    if request.method == "POST":
        correct = 0
        incorrect = 0
        user_answers = {}

        for q in QUESTIONS:
            ans = request.form.get(q["id"])
            if ans is not None:
                ans = int(ans)
                user_answers[q["id"]] = ans
                if ans == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1
            else:
                user_answers[q["id"]] = None

        attempted = correct + incorrect
        unattempted = len(QUESTIONS) - attempted
        accuracy = round((correct / attempted) * 100, 2) if attempted else 0

        session.update({
            "name": session.get("name"),
            "total": len(QUESTIONS),
            "correct": correct,
            "incorrect": incorrect,
            "attempted": attempted,
            "unattempted": unattempted,
            "accuracy": accuracy,
            "answers_key": str(user_answers)
        })

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)

# ================= RESULT =================
@app.route("/result")
def result():
    if "correct" not in session:
        return redirect("/")

    user_answers = ast.literal_eval(session.get("answers_key", "{}"))

    return render_template(
        "result.html",
        name=session.get("name"),
        total=session.get("total"),
        correct=session.get("correct"),
        incorrect=session.get("incorrect"),
        attempted=session.get("attempted"),
        unattempted=session.get("unattempted"),
        accuracy=session.get("accuracy"),
        questions=QUESTIONS,
        user_answers=user_answers,
        show_answer_key=ANSWER_KEY_ACTIVE
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)