from flask import Flask, render_template, request, redirect, session
import json, random, os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================= USERS =================
USERS = {
    "abc": {"name": "Demo Student", "password": "abc1"}
}

# ================= CONFIG =================
TOTAL_QUESTIONS = 10

# ================= LOAD QUESTIONS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_PATH = os.path.join(BASE_DIR, "questions.json")

try:
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        QUESTION_BANK = json.load(f)
    print(f"✅ QUESTIONS LOADED: {len(QUESTION_BANK)}")
except Exception as e:
    QUESTION_BANK = []
    print("❌ ERROR loading questions.json:", e)

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

# ================= SSC CGL FULL MOCK LIST =================
@app.route("/ssc/cgl")
def ssc_cgl_full_mocks():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")

# ================= SSC CGL MOCK 1 INSTRUCTIONS =================
@app.route("/ssc/cgl/mock/1")
def ssc_cgl_mock_1_instructions():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_mock_1_instructions.html")

# ================= START MOCK 1 (POST) =================
@app.route("/ssc/cgl/mock/1/start", methods=["POST"])
def start_mock_1():
    if "username" not in session:
        return redirect("/")

    print("🚀 START MOCK 1 TRIGGERED")
    print("QUESTION BANK SIZE:", len(QUESTION_BANK))

    if not QUESTION_BANK:
        return "❌ No questions found in questions.json", 500

    # Randomly pick questions
    session["questions"] = random.sample(
        QUESTION_BANK,
        min(TOTAL_QUESTIONS, len(QUESTION_BANK))
    )
    session["q"] = 0
    session["answers"] = {}
    session["review"] = []

    print("✅ Questions loaded in session.")
    return redirect("/exam")

# ================= EXAM PAGE =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "username" not in session or "questions" not in session:
        print("⚠️ Session missing questions, redirecting to dashboard.")
        return redirect("/student_dashboard")

    questions = session["questions"]
    q = session.get("q", 0)

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

    # Build palette
    palette = []
    for i in range(len(questions)):
        if str(i) in session["review"]:
            status = "review"
        elif str(i) in session["answers"]:
            status = "attempted"
        else:
            status = "unattempted"
        palette.append({"qno": i + 1, "status": status})

    current = questions[q]
    print(f"🧠 Showing Question {q+1}: {current.get('q')}")

    return render_template(
        "ssc_cgl_exam_1.html",
        question=current.get("q"),
        options=current.get("options"),
        qno=q + 1,
        total=len(questions),
        palette=palette
    )

# ================= RESULT =================
@a@app.route("/result")
def result():
    if "username" not in session:
        return redirect("/")

    questions = session.get("questions", [])
    answers = session.get("answers", {})
    total = len(questions)

    correct = 0
    wrong = 0

    # (for now assume option 0 is correct – later you’ll add correct key)
    for qno, ans in answers.items():
        if int(ans) == 0:
            correct += 1
        else:
            wrong += 1

    attempted = len(answers)
    unattempted = total - attempted

    score = (correct * PER_QUESTION_MARKS) - (wrong * NEGATIVE_MARKS)
    accuracy = round((correct / attempted) * 100, 2) if attempted else 0

    # Time
    start_time = session.get("start_time", time.time())
    time_taken_sec = int(time.time() - start_time)
    minutes = time_taken_sec // 60
    seconds = time_taken_sec % 60

    # Mock percentile & rank (safe fake logic)
    percentile = min(99, 50 + correct * 5)
    rank = max(1, 500 - correct * 10)

    return render_template(
        "result.html",
        total=total,
        attempted=attempted,
        unattempted=unattempted,
        correct=correct,
        wrong=wrong,
        score=score,
        accuracy=accuracy,
        minutes=minutes,
        seconds=seconds,
        percentile=percentile,
        rank=rank
    )

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)