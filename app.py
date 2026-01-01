from flask import Flask, render_template, request, session, redirect, url_for
import uuid

app = Flask(__name__, static_folder=None)
@app.route("/health")
def health():
    return "FLASK IS RUNNING"
app.secret_key = "super_secret_exam_key_123"

# ================== QUESTIONS ==================
QUESTIONS = [
    {
        "id": "1",
        "question": "भारत की राजधानी क्या है?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": "0"
    },
    {
        "id": "2",
        "question": "सबसे बड़ा ग्रह कौन सा है?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "2"
    },
    {
        "id": "3",
        "question": "ताजमहल कहाँ स्थित है?",
        "options": ["Delhi", "Agra", "Jaipur", "Lucknow"],
        "answer": "1"
    }
]

TOTAL_QUESTIONS = len(QUESTIONS)
MARK_PER_Q = 1
NEGATIVE_MARK = 0.25

# runtime memory (Render-safe basic)
ALL_RESULTS = []

# ================== LOGIN ==================
@app.route("/", methods=["GET", "POST"])
def login():
    # 🔹 Agar already logged in hai (reattempt)
    if "name" in session and request.method == "GET":
        return redirect("/exam")

    if request.method == "POST":
        session.clear()
        session["name"] = request.form["name"]
        session["student_id"] = str(uuid.uuid4())
        return redirect("/exam")

    return render_template("login.html")
# ================== EXAM ==================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "student_id" not in session:
        return redirect("/")

    if request.method == "POST":
        correct = 0
        incorrect = 0

        for q in QUESTIONS:
            user_ans = request.form.get(q["id"])
            if user_ans is not None:
                if user_ans == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

        attempted = correct + incorrect
        unattempted = len(QUESTIONS) - attempted

        score = correct
        total_marks = len(QUESTIONS)

        accuracy = round((correct / attempted) * 100, 2) if attempted else 0

        return render_template(
            "result.html",
            score=score,
            total=total_marks,
            correct=correct,
            incorrect=incorrect,
            attempted=attempted,
            unattempted=unattempted,
            accuracy=accuracy
        )

    # 👇 GET request (page load)
    return render_template("exam.html", questions=QUESTIONS)

# ================== RESULT ==================


    if "student_id" not in session:
        return redirect("/")

    if request.method == "POST":
        correct = 0
        incorrect = 0

        for q in QUESTIONS:
            user_ans = request.form.get(q["id"])
            if user_ans is not None:
                if user_ans == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

        attempted = correct + incorrect
        unattempted = len(QUESTIONS) - attempted

        # 👉 1 mark per question
        score = correct
        total_marks = len(QUESTIONS)

        accuracy = round((correct / attempted) * 100, 2) if attempted else 0

        return render_template(
            "result.html",
            score=score,
            total=total_marks,
            correct=correct,
            incorrect=incorrect,
            attempted=attempted,
            unattempted=unattempted,
            accuracy=accuracy
        )

    return render_template("exam.html", questions=QUESTIONS)
# ================== REATTEMPT ==================
@app.route("/reattempt")
def reattempt():
    session.clear()
    return redirect("/")

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)