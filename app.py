from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "mock_test_secret"

# ================= QUESTIONS =================
QUESTIONS = [
    {
        "id": "q1",
        "question": "भारत की राजधानी क्या है?",
        "options": ["मुंबई", "दिल्ली", "कोलकाता", "चेन्नई"],
        "answer": 1
    },
    {
        "id": "q2",
        "question": "सबसे बड़ा ग्रह कौन सा है?",
        "options": ["पृथ्वी", "मंगल", "बृहस्पति", "शुक्र"],
        "answer": 2
    },
    {
        "id": "q3",
        "question": "ताजमहल कहाँ स्थित है?",
        "options": ["जयपुर", "आगरा", "दिल्ली", "लखनऊ"],
        "answer": 1
    }
]

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        session["name"] = request.form["name"]
        return redirect("/exam")
    return render_template("login.html")

# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "name" not in session:
        return redirect("/")

    if request.method == "POST":
        result_data = []
        correct = incorrect = 0

        for q in QUESTIONS:
            user_ans = request.form.get(q["id"])

            if user_ans is None:
                status = "unattempted"
            elif int(user_ans) == q["answer"]:
                status = "correct"
                correct += 1
            else:
                status = "incorrect"
                incorrect += 1

            result_data.append({
                "question": q["question"],
                "options": q["options"],
                "correct": q["answer"],
                "user": user_ans,
                "status": status
            })

        attempted = correct + incorrect
        unattempted = len(QUESTIONS) - attempted
        accuracy = round((correct / attempted) * 100, 2) if attempted > 0 else 0

        # save in session
        session["result_data"] = result_data
        session["score"] = correct
        session["total"] = len(QUESTIONS)
        session["correct"] = correct
        session["incorrect"] = incorrect
        session["attempted"] = attempted
        session["unattempted"] = unattempted
        session["accuracy"] = accuracy

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)

# ================= RESULT (ONLY RESULT) =================
@app.route("/result")
def result():
    if "score" not in session:
        return redirect("/")

    return render_template(
        "result.html",
        score=session["score"],
        total=session["total"],
        correct=session["correct"],
        incorrect=session["incorrect"],
        attempted=session["attempted"],
        unattempted=session["unattempted"],
        accuracy=session["accuracy"]
    )

# ================= ANSWER KEY =================
@app.route("/answer-key")
def answer_key():
    if "result_data" not in session:
        return redirect("/")

    return render_template(
        "review.html",
        result_data=session["result_data"]
    )

# ================= LOGOUT / REATTEMPT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)