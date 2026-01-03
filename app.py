from flask import Flask, render_template, request, redirect, session, abort, jsonify
import json
import os
import random

app = Flask(__name__)
app.secret_key = "stable_secret_key_123"

# ================= ADMIN CONFIG =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "NEHRA@2233"

STATUS_FILE = "exam_status.json"

# ================= UTILS =================
def read_status():
    if not os.path.exists(STATUS_FILE):
        return {"exam_active": False, "answer_key_active": False}
    with open(STATUS_FILE, "r") as f:
        return json.load(f)

def write_status(data):
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

# ================= QUESTION BANK =================
REASONING = [
    {"id":"r1","q":"Odd one out: 2, 4, 8, 16, 18","opt":["8","16","18","4"],"ans":2},
    {"id":"r2","q":"If A=1, B=2 then Z=?","opt":["24","25","26","27"],"ans":2},
    {"id":"r3","q":"3, 6, 12, ?","opt":["18","20","24","30"],"ans":2},
    {"id":"r4","q":"Mirror image is related to?","opt":["Reflection","Rotation","Refraction","None"],"ans":0},
    {"id":"r5","q":"Odd one: Cat, Dog, Cow, Chair","opt":["Cat","Dog","Cow","Chair"],"ans":3},
]

GK = [
    {"id":"g1","q":"Capital of India?","opt":["Delhi","Mumbai","Kolkata","Chennai"],"ans":0},
    {"id":"g2","q":"National animal of India?","opt":["Lion","Tiger","Elephant","Horse"],"ans":1},
    {"id":"g3","q":"Red Planet?","opt":["Mars","Earth","Jupiter","Venus"],"ans":0},
    {"id":"g4","q":"Taj Mahal is in?","opt":["Delhi","Agra","Jaipur","Lucknow"],"ans":1},
    {"id":"g5","q":"First PM of India?","opt":["Nehru","Gandhi","Patel","Bose"],"ans":0},
]

MATHS = [
    {"id":"m1","q":"5 + 7 = ?","opt":["10","11","12","13"],"ans":2},
    {"id":"m2","q":"Square of 8?","opt":["64","56","72","49"],"ans":0},
    {"id":"m3","q":"20% of 100?","opt":["10","20","25","30"],"ans":1},
    {"id":"m4","q":"15 ÷ 3 = ?","opt":["3","4","5","6"],"ans":2},
    {"id":"m5","q":"10 × 2 = ?","opt":["10","15","20","25"],"ans":2},
]

ENGLISH = [
    {"id":"e1","q":"Synonym of Fast","opt":["Quick","Slow","Late","Lazy"],"ans":0},
    {"id":"e2","q":"Antonym of Hot","opt":["Warm","Cold","Heat","Fire"],"ans":1},
    {"id":"e3","q":"Plural of Child","opt":["Childs","Children","Childes","Childrens"],"ans":1},
    {"id":"e4","q":"Correct spelling","opt":["Beautifull","Beautyful","Beautiful","Beutiful"],"ans":2},
    {"id":"e5","q":"Fill blank: I ___ a book","opt":["read","reads","reading","have"],"ans":0},
]

ACTIVE_EXAMS = {}

# ================= STUDENT LOGIN =================
@app.route("/", methods=["GET","POST"])
def login():
    status = read_status()
    if request.method == "POST":
        if not status["exam_active"]:
            return "Exam not started yet"

        name = request.form.get("name")
        session["student_name"] = name

        ACTIVE_EXAMS[name] = {
            "Reasoning": random.sample(REASONING, 5),
            "GK": random.sample(GK, 5),
            "Maths": random.sample(MATHS, 5),
            "English": random.sample(ENGLISH, 5),
        }
        return redirect("/exam")

    return render_template("login.html")

# ================= EXAM STATUS (POLLING) =================
@app.route("/exam-status")
def exam_status():
    status = read_status()
    return jsonify({"active": status["exam_active"]})

# ================= EXAM =================
@app.route("/exam", methods=["GET","POST"])
def exam():
if request.method == "POST":
    score = 0
    answers = {}
    name = session.get("student_name")
    if not name or name not in ACTIVE_EXAMS:
        return redirect("/")

    exam = ACTIVE_EXAMS[name]

    if request.method == "POST":
        score = 0
        answers = {}

        for sec in exam:
            for q in exam[sec]:
                a = request.form.get(q["id"])
                answers[q["id"]] = int(a) if a else None
                if a and int(a) == q["ans"]:
                    score += 1

        session["score"] = score
        session["answers"] = answers
        return redirect("/result")

    return render_template("exam.html", exam=exam)

# ================= RESULT =================
@app.route("/result")
def result():
    name = session.get("student_name")
    exam = ACTIVE_EXAMS.get(name, {})
    answers = session.get("answers", {})

    total = 20
    correct = session.get("score", 0)
    attempted = len([v for v in answers.values() if v is not None])
    incorrect = attempted - correct
    accuracy = round((correct / attempted) * 100, 2) if attempted else 0

    status = read_status()
    if not status["answer_key_active"]:
        return "Thank you for attempting the test. Result will be updated soon."

    return render_template(
        "result.html",
        name=name,
        correct=correct,
        incorrect=incorrect,
        attempted=attempted,
        total=total,
        accuracy=accuracy
    )

# ================= ADMIN LOGIN =================
@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
            session["admin_user"] = ADMIN_USER
            return redirect("/admin/dashboard")
        return "Invalid admin login"

    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    status = read_status()
    return render_template(
        "admin_dashboard.html",
        exam_active=status["exam_active"],
        answer_key_active=status["answer_key_active"]
    )

# ================= TOGGLES =================
@app.route("/admin/toggle-exam")
def toggle_exam():
    if not session.get("admin"):
        abort(403)

    status = read_status()
    status["exam_active"] = not status["exam_active"]
    write_status(status)
    return redirect("/admin/dashboard")

@app.route("/admin/toggle-answer-key")
def toggle_answer_key():
    if not session.get("admin"):
        abort(403)

    status = read_status()
    status["answer_key_active"] = not status["answer_key_active"]
    write_status(status)
    return redirect("/admin/dashboard")

# ================= ADMIN LOGOUT =================
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    session.pop("admin_user", None)
    return redirect("/admin")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)