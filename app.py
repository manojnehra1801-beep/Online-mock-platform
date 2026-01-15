from flask import Flask, render_template, request, redirect, session
import json, random

app = Flask(__name__)
app.secret_key = "ssc_mock_secret"

TOTAL_QUESTIONS = 10

# ---------- LOAD QUESTIONS ----------
with open("questions.json", "r", encoding="utf-8") as f:
    QUESTION_BANK = json.load(f)

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()

        # random 10 questions
        session["questions"] = random.sample(QUESTION_BANK, TOTAL_QUESTIONS)
        session["q"] = 0
        session["answers"] = {}
        session["review"] = set()

        return redirect("/exam")

    return render_template("login.html")


# ---------- EXAM ----------
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "questions" not in session:
        return redirect("/")

    q = session["q"]
    questions = session["questions"]

    # POST → save answer / review / next
    if request.method == "POST":

        if "ans" in request.form:
            session["answers"][str(q)] = request.form["ans"]

        if "mark_review" in request.form:
            session["review"].add(str(q))

        if q == TOTAL_QUESTIONS - 1:
            return redirect("/result")
        else:
            session["q"] += 1
            return redirect("/exam")

    # ---------- PALETTE ----------
    palette = []
    for i in range(TOTAL_QUESTIONS):
        if str(i) in session["review"]:
            status = "review"
        elif str(i) in session["answers"]:
            status = "attempted"
        else:
            status = "unattempted"

        palette.append({"qno": i + 1, "status": status})

    current = questions[q]

    return render_template(
        "ssc_cgl_exam_1.html",
        question=current["q"],
        options=current["options"],
        qno=q + 1,
        total=TOTAL_QUESTIONS,
        palette=palette
    )


# ---------- RESULT ----------
@app.route("/result")
def result():
    attempted = len(session["answers"])
    reviewed = len(session["review"])
    unattempted = TOTAL_QUESTIONS - attempted

    return f"""
    <h2>Result</h2>
    <p>Attempted: {attempted}</p>
    <p>Marked for Review: {reviewed}</p>
    <p>Unattempted: {unattempted}</p>
    <a href="/">Restart</a>
    """


if __name__ == "__main__":
    app.run(debug=True)