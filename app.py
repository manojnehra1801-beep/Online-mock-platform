from flask import Flask, render_template, request, redirect, session, abort
import time

app = Flask(__name__)
app.secret_key = "mock_exam_secret_key"

# ================= ADMIN CONFIG =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "NEHRA@2233"

EXAM_ACTIVE = False
ANSWER_KEY_OPEN = True   # ab result page se answer key dikhegi
STUDENT_ATTEMPTS = []

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

# ================= STUDENT LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not EXAM_ACTIVE:
            return {"status": "blocked"}

        session.clear()
        session["name"] = request.form["name"]
        return {"status": "ok"}

    return render_template("login.html")

# ================= EXAM STATUS (POLLING) =================
@app.route("/exam-status")
def exam_status():
    return {"active": EXAM_ACTIVE}

# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if not EXAM_ACTIVE:
        return "Exam not started yet."

    if request.method == "POST":
        correct = 0
        incorrect = 0
        user_answers = {}

        for q in QUESTIONS:
            ans = request.form.get(q["id"])
            user_answers[q["id"]] = int(ans) if ans is not None else None

            if ans is not None:
                if int(ans) == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

        attempted = correct + incorrect
        accuracy = round((correct / attempted) * 100, 2) if attempted else 0

        STUDENT_ATTEMPTS.append({
            "name": session.get("name"),
            "score": correct
        })

     session.update({
    "score": correct,
    "total": len(QUESTIONS),
    "correct": correct,
    "incorrect": incorrect,
    "attempted": attempted,
    "unattempted": len(QUESTIONS) - attempted,
    "accuracy": accuracy
})

# 🔑 answers ko memory me rakho (not session)
session["answers_key"] = str(user_answers)

    return render_template("exam.html", questions=QUESTIONS)

# ================= RESULT =================
@app.route("/result")
def result():
    return render_template(
        "result.html",
        questions=QUESTIONS,
        user_answers=session.get("user_answers", {}),
        **session
    )

# ================= ADMIN LOGIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin/dashboard")
        return "Invalid admin login"
    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template(
        "admin_dashboard.html",
        exam_active=EXAM_ACTIVE,
        answer_key=ANSWER_KEY_OPEN
    )

# ================= TOGGLE EXAM =================
@app.route("/admin/toggle-exam")
def toggle_exam():
    global EXAM_ACTIVE
    if not session.get("admin"):
        abort(403)
    EXAM_ACTIVE = not EXAM_ACTIVE
    return redirect("/admin/dashboard")

# ================= STUDENT LIST =================
@app.route("/admin/students")
def admin_students():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_students.html", students=STUDENT_ATTEMPTS)

# ================= ADMIN LOGOUT =================
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)