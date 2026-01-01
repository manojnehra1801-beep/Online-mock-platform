from flask import Flask, render_template, request, session, redirect
import uuid

app = Flask(__name__)
app.secret_key = "exam_secret"

# ---------------- QUESTIONS ----------------
QUESTIONS = [
    {
        "id": 1,
        "question": "भारत की राजधानी क्या है?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": 0
    },
    {
        "id": 2,
        "question": "सबसे बड़ा ग्रह कौन सा है?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": 2
    },
    {
        "id": 3,
        "question": "ताजमहल कहाँ स्थित है?",
        "options": ["Delhi", "Agra", "Jaipur", "Lucknow"],
        "answer": 1
    }
]

TOTAL_QUESTIONS = len(QUESTIONS)
MARK_PER_Q = 1
NEGATIVE_MARK = 0.25

ALL_RESULTS = []

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        session["name"] = request.form["name"]
        session["id"] = str(uuid.uuid4())
        return redirect("/exam")
    return render_template("login.html")

# ---------------- EXAM ----------------
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if request.method == "POST":
        answers = request.form
        correct = 0
        incorrect = 0

        for q in QUESTIONS:
            user_ans = answers.get(str(q["id"]))
            if user_ans is not None:
                if int(user_ans) == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

        attempted = correct + incorrect
        unattempted = TOTAL_QUESTIONS - attempted

        score = (correct * MARK_PER_Q) - (incorrect * NEGATIVE_MARK)
        accuracy = round((correct / attempted) * 100, 2) if attempted else 0

        session["result"] = {
            "correct": correct,
            "incorrect": incorrect,
            "attempted": attempted,
            "unattempted": unattempted,
            "score": round(score, 2),
            "accuracy": accuracy
        }

        ALL_RESULTS.append({
            "id": session["id"],
            "score": score
        })

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)

# ---------------- RESULT ----------------
@app.route("/result")
def result():
    my = session.get("result")
    my_id = session.get("id")

    sorted_results = sorted(ALL_RESULTS, key=lambda x: x["score"], reverse=True)
    rank = next(i+1 for i, r in enumerate(sorted_results) if r["id"] == my_id)

    total = len(sorted_results)
    percentile = round(((total - rank) / total) * 100, 2)
    avg_score = round(sum(r["score"] for r in sorted_results) / total, 2)
    best_score = sorted_results[0]["score"]

    return render_template(
        "result.html",
        result=my,
        rank=f"{rank}/{total}",
        percentile=percentile,
        avg_score=avg_score,
        best_score=best_score
    )

# ---------------- REATTEMPT ----------------
@app.route("/reattempt")
def reattempt():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)