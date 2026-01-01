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
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return redirect("/")

        session.clear()
        session["name"] = name
        session["student_id"] = str(uuid.uuid4())
        return redirect("/exam")

    return render_template("login.html")

# ================== EXAM ==================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "student_id" not in session:
        return redirect("/")

    if request.method == "POST":
        form_data = request.form

        correct = 0
        incorrect = 0

        for q in QUESTIONS:
            user_ans = form_data.get(q["id"])
            if user_ans is not None:
                if user_ans == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

        attempted = correct + incorrect
        unattempted = TOTAL_QUESTIONS - attempted

        score = (correct * MARK_PER_Q) - (incorrect * NEGATIVE_MARK)
        score = round(score, 2)

        accuracy = round((correct / attempted) * 100, 2) if attempted > 0 else 0

        session["result"] = {
            "correct": correct,
            "incorrect": incorrect,
            "attempted": attempted,
            "unattempted": unattempted,
            "score": score,
            "accuracy": accuracy
        }

        ALL_RESULTS.append({
            "id": session["student_id"],
            "score": score
        })

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)

# ================== RESULT ==================
@app.route("/result")
def result():
    if "result" not in session or "student_id" not in session:
        return redirect("/")

    my_result = session["result"]
    my_id = session["student_id"]

    if not ALL_RESULTS:
        return redirect("/")

    sorted_results = sorted(ALL_RESULTS, key=lambda x: x["score"], reverse=True)

    rank = None
    for i, r in enumerate(sorted_results):
        if r["id"] == my_id:
            rank = i + 1
            break

    if rank is None:
        return redirect("/")

    total_students = len(sorted_results)

    percentile = round(((total_students - rank) / total_students) * 100, 2)
    avg_score = round(sum(r["score"] for r in sorted_results) / total_students, 2)
    best_score = sorted_results[0]["score"]

    return render_template(
        "result.html",
        result=my_result,
        rank=f"{rank}/{total_students}",
        percentile=percentile,
        avg_score=avg_score,
        best_score=best_score
    )

# ================== REATTEMPT ==================
@app.route("/reattempt")
def reattempt():
    session.clear()
    return redirect("/")

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)