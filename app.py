from flask import Flask, render_template, request, redirect, session
import json, random, os, time

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================= USERS =================
USERS = {
    "abc": {"name": "Demo Student", "password": "abc1"}
}

# ================= CONFIG =================
TOTAL_QUESTIONS = 100
PER_QUESTION_MARKS = 2
NEGATIVE_MARKS = 0.5

# ================= LOAD QUESTIONS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_PATH = os.path.join(BASE_DIR, "questions.json")

try:
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        DATA = json.load(f)

    # Expecting structure:
    # { "cgl_full_mock_1": { "reasoning":[], "gk":[], "maths":[], "english":[] } }

    MOCK = DATA["cgl_full_mock_1"]

    QUESTION_BANK = (
        MOCK["reasoning"] +
        MOCK["gk"] +
        MOCK["maths"] +
        MOCK["english"]
    )

    print("✅ QUESTIONS LOADED:", len(QUESTION_BANK))

except Exception as e:
    QUESTION_BANK = []
    print("❌ ERROR loading questions:", e)

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        if u in USERS and USERS[u]["password"] == p:
            session.clear()
            session["username"] = u
            session["name"] = USERS[u]["name"]
            return redirect("/student_dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ================= STUDENT DASHBOARD =================
@app.route("/student_dashboard")
def student_dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("student_dashboard.html", name=session["name"])

# ================= SSC DASHBOARD =================
@app.route("/ssc")
def ssc():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")

# ================= SSC CGL MOCK LIST =================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")

# ================= INSTRUCTIONS =================
@app.route("/ssc/cgl/mock/1")
def mock_1_instructions():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_mock_1_instructions.html")

# ================= START MOCK =================
@app.route("/ssc/cgl/mock/1/start", methods=["POST"])
def start_mock():
    if "username" not in session:
        return redirect("/")

    if not QUESTION_BANK:
        return "No questions found", 500

    session["questions"] = QUESTION_BANK
    session["q"] = 0
    session["answers"] = {}
    session["review"] = {}

    # TEMP: random correct answers (until real key added)
    session["correct_answers"] = {
        str(i): random.randint(0, 3) for i in range(len(QUESTION_BANK))
    }

    return redirect("/exam")

# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "username" not in session or "questions" not in session:
        return redirect("/student_dashboard")

    questions = session["questions"]
    q = session.get("q", 0)

    # ---------- POST ----------
    if request.method == "POST":

        # Save answer
        if "ans" in request.form:
            session["answers"][str(q)] = request.form["ans"]

        # Mark for review
        if "mark_review" in request.form:
            session["review"][str(q)] = True

        action = request.form.get("action")

        # Previous
        if action == "prev":
            session["q"] = max(0, q - 1)
            return redirect("/exam")

        # Section jump
        if action and action.startswith("jump_"):
            target = int(action.split("_")[1])
            session["q"] = min(target, len(questions) - 1)
            return redirect("/exam")

        # Next
        if q == len(questions) - 1:
            return redirect("/result")

        session["q"] = q + 1
        return redirect("/exam")

    # ---------- GET ----------
    current = questions[q]

    return render_template(
        "ssc_cgl_exam_1.html",
        question=current["question"],
        options=current["options"],
        qno=q + 1,
        total=len(questions),
        session=session
    )

# ================= RESULT =================
@app.route("/result")
def result():
    if "username" not in session:
        return redirect("/")

    answers = session.get("answers", {})
    correct_answers = session.get("correct_answers", {})

    correct = 0
    wrong = 0

    for qno, ans in answers.items():
        if qno in correct_answers and int(ans) == correct_answers[qno]:
            correct += 1
        else:
            wrong += 1

    attempted = len(answers)
    total = len(session.get("questions", []))
    unattempted = total - attempted

    score = (correct * PER_QUESTION_MARKS) - (wrong * NEGATIVE_MARKS)
    accuracy = round((correct / attempted) * 100, 2) if attempted else 0

    return render_template(
        "result.html",
        total=total,
        attempted=attempted,
        unattempted=unattempted,
        correct=correct,
        wrong=wrong,
        score=score,
        accuracy=accuracy,
        percentile=min(99, 50 + correct),
        rank=max(1, 500 - correct * 5),
        minutes=0,
        seconds=0
    )

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)