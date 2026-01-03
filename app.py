# ===== BLANK SCREEN FIX : MINIMAL & SAFE app.py =====
# Is file ko POORA copy–paste karo. Extra kuch nahi.

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "mock_exam_secret_key_123"

# ===== FLAG =====
EXAM_ACTIVE = True   # test ke liye True rakho

# ===== QUESTIONS =====
QUESTIONS = [
    {
        "id": "q1",
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": 1
    }
]

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not EXAM_ACTIVE:
            return render_template("login.html", exam_active=EXAM_ACTIVE)

        session.clear()
        session["name"] = request.form.get("name")
        return redirect("/exam")

    return render_template("login.html", exam_active=EXAM_ACTIVE)

# ===== EXAM =====
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if request.method == "POST":
        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)

# ===== RESULT =====
@app.route("/result")
def result():
    return "Result Page Working"

# ===== RUN =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)