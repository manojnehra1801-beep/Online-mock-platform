from flask import Flask, render_template, request, redirect, session, url_for
import json
import random
import os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================= TEMP USERS =================
USERS = {
    "abc": {
        "name": "Demo Student",
        "password": "abc1"
    }
}

# ================= CONFIG =================
TOTAL_QUESTIONS = 10

# ================= LOAD QUESTIONS.JSON =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_PATH = os.path.join(BASE_DIR, "question.json")

try:
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        QUESTION_BANK = json.load(f)
except Exception as e:
    QUESTION_BANK = []
    print("ERROR loading question.json:", e)

print("TOTAL QUESTIONS LOADED:", len(QUESTION_BANK))


# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username]["password"] == password:
            session.clear()
            session["username"] = username
            session["name"] = USERS[username]["name"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("dashboard.html", name=session["name"])


# ================= START MOCK =================
@app.route("/start-mock", methods=["POST"])
def start_mock():
    if "username" not in session:
        return redirect("/")

    if not QUESTION_BANK:
        return "No questions available", 500

    session["questions"] = random.sample(
        QUESTION_BANK,
        min(TOTAL_QUESTIONS, len(QUESTION_BANK))
    )
    session["q"] = 0
    session["answers"] = {}
    session["review"] = []   # LIST (not set)

    return redirect("/exam")


# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "username" not in session or "questions" not in session:
        return redirect("/")

    questions = session["questions"]
    q = session.get("q", 0)

    if q >= len(questions):
        q = 0
        session["q"] = 0

    # ---------- POST ----------
    if request.method == "POST":

        if "ans" in request.form:
            session["answers"][str(q)] = request.form["ans"]

        if "mark_review" in request.form:
            if str(q) not in session["review"]:
                session["review"].append(str(q))

        if q == len(questions) - 1:
            return redirect("/result")
        else:
            session["q"] = q + 1
            return redirect("/exam")

    # ---------- PALETTE ----------
    palette = []
    for i in range(len(questions)):
        if str(i) in session["review"]:
            status = "review"
        elif str(i) in session["answers"]:
            status = "attempted"
        else:
            status = "unattempted"

        palette.append({
            "qno": i + 1,
            "status": status
        })

    current = questions[q]

    return render_template(
        "ssc_cgl_exam_1.html",
        question=current.get("q"),
        options=current.get("options"),
        qno=q + 1,
        total=len(questions),
        palette=palette
    )


# ================= RESULT =================
@app.route("/result")
def result():
    if "username" not in session:
        return redirect("/")

    total = len(session.get("questions", []))
    attempted = len(session.get("answers", {}))
    reviewed = len(session.get("review", []))
    unattempted = total - attempted

    return f"""
    <h2>Result</h2>
    <p>Total Questions: {total}</p>
    <p>Attempted: {attempted}</p>
    <p>Marked for Review: {reviewed}</p>
    <p>Unattempted: {unattempted}</p>
    <br>
    <a href="/dashboard">Back to Dashboard</a>
    """


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)