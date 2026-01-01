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
        session.clear()
        session["name"] = request.form["name"]
        session["student_id"] = str(uuid.uuid4())
        return redirect("/exam")

    # GET request → hamesha login page dikhao
    return render_template("login.html")
# ================== EXAM ==================
# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():

    if "student_id" not in session:
        return redirect("/")

    # ================= SUBMIT EXAM =================
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

        if attempted > 0:
            accuracy = round((correct / attempted) * 100, 2)
        else:
            accuracy = 0

        return render_template(
            "result.html",
            questions=QUESTIONS,
            score=score,
            total=total_marks,
            correct=correct,
            incorrect=incorrect,
            attempted=attempted,
            unattempted=unattempted,
            accuracy=accuracy
        )

    # ================= LOAD EXAM PAGE =================
    return render_template("exam.html", questions=QUESTIONS)
 

    


 
# ================== REATTEMPT ==================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/exam")
# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)