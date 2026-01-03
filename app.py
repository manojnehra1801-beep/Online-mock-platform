from flask import Flask, render_template, request, redirect, session, abort
import ast, random

app = Flask(__name__)
app.secret_key = "mock_exam_secret_key_123"

# ================= ADMIN CONFIG =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "NEHRA@2233"

EXAM_ACTIVE = False
STUDENT_ATTEMPTS = []

# ================= QUESTION BANK =================

REASONING = [
    {"id":"r1","question":"Find the odd one out: 2, 4, 8, 16, 18",
     "options":["8","16","18","4"],"answer":2},
    {"id":"r2","question":"If A=1, B=2 then Z=?",
     "options":["24","25","26","27"],"answer":2},
    {"id":"r3","question":"Mirror image is related to?",
     "options":["Reflection","Rotation","Refraction","None"],"answer":0},
    {"id":"r4","question":"Odd one out: Cat, Dog, Cow, Chair",
     "options":["Cat","Dog","Cow","Chair"],"answer":3},
    {"id":"r5","question":"3, 6, 12, ?",
     "options":["18","20","24","30"],"answer":2},
]

GK = [
    {"id":"g1","question":"Capital of India?",
     "options":["Delhi","Mumbai","Kolkata","Chennai"],"answer":0},
    {"id":"g2","question":"National animal of India?",
     "options":["Lion","Tiger","Elephant","Horse"],"answer":1},
    {"id":"g3","question":"Red Planet?",
     "options":["Mars","Earth","Jupiter","Venus"],"answer":0},
    {"id":"g4","question":"Taj Mahal is in?",
     "options":["Delhi","Agra","Jaipur","Lucknow"],"answer":1},
    {"id":"g5","question":"Who was the first PM of India?",
     "options":["Nehru","Gandhi","Patel","Bose"],"answer":0},
]

MATHS = [
    {"id":"m1","question":"5 + 7 = ?",
     "options":["10","11","12","13"],"answer":2},
    {"id":"m2","question":"Square of 8?",
     "options":["64","56","72","49"],"answer":0},
    {"id":"m3","question":"20% of 100?",
     "options":["10","20","25","30"],"answer":1},
    {"id":"m4","question":"15 ÷ 3 = ?",
     "options":["3","4","5","6"],"answer":2},
    {"id":"m5","question":"10 × 2 = ?",
     "options":["10","15","20","25"],"answer":2},
]

ENGLISH = [
    {"id":"e1","question":"Synonym of Fast",
     "options":["Quick","Slow","Late","Lazy"],"answer":0},
    {"id":"e2","question":"Antonym of Hot",
     "options":["Warm","Cold","Heat","Fire"],"answer":1},
    {"id":"e3","question":"Plural of Child",
     "options":["Childs","Children","Childes","Childrens"],"answer":1},
    {"id":"e4","question":"Correct spelling",
     "options":["Beautifull","Beautyful","Beautiful","Beutiful"],"answer":2},
    {"id":"e5","question":"Fill blank: I ___ a book",
     "options":["read","reads","reading","have"],"answer":0},
]

# ================= STUDENT LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not EXAM_ACTIVE:
            return {"status": "blocked"}

        session.clear()
        session["name"] = request.form.get("name")

        exam = {
            "Reasoning": random.sample(REASONING,5),
            "GK": random.sample(GK,5),
            "Maths": random.sample(MATHS,5),
            "English": random.sample(ENGLISH,5),
        }
        session["exam"] = str(exam)

        return {"status": "ok"}

    return render_template("login.html")

# ================= EXAM STATUS =================
@app.route("/exam-status")
def exam_status():
    return {"active": EXAM_ACTIVE}

# ================= EXAM =================
@app.route("/exam", methods=["GET","POST"])
def exam():
    if not EXAM_ACTIVE:
        return "Exam not started yet."

    exam = ast.literal_eval(session.get("exam","{}"))

    if request.method == "POST":
        correct = 0
        incorrect = 0
        user_answers = {}

        for sec in exam:
            for q in exam[sec]:
                ans = request.form.get(q["id"])
                if ans is not None:
                    ans = int(ans)
                    user_answers[q["id"]] = ans
                    if ans == q["answer"]:
                        correct += 1
                    else:
                        incorrect += 1
                else:
                    user_answers[q["id"]] = None

        attempted = correct + incorrect
        accuracy = round((correct / attempted) * 100, 2) if attempted else 0

        STUDENT_ATTEMPTS.append({
            "name": session.get("name"),
            "score": correct
        })

        session.update({
            "score": correct,
            "total": 20,
            "correct": correct,
            "incorrect": incorrect,
            "attempted": attempted,
            "unattempted": 20 - attempted,
            "accuracy": accuracy,
            "answers_key": str(user_answers)
        })

        return redirect("/result")

    return render_template("exam.html", exam=exam)

# ================= RESULT =================
@app.route("/result")
def result():
    exam = ast.literal_eval(session.get("exam","{}"))
    user_answers = ast.literal_eval(session.get("answers_key","{}"))

    return render_template(
        "result.html",
        exam=exam,
        user_answers=user_answers,
        **session
    )

# ================= ADMIN LOGIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if (
            request.form.get("username") == ADMIN_USER
            and request.form.get("password") == ADMIN_PASS
        ):
            session["admin"] = True
            return redirect("/admin/dashboard")
        return "Invalid admin login"
    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_dashboard.html", exam_active=EXAM_ACTIVE)

# ================= TOGGLE EXAM =================
@app.route("/admin/toggle-exam")
def toggle_exam():
    global EXAM_ACTIVE
    if not session.get("admin"):
        abort(403)
    EXAM_ACTIVE = not EXAM_ACTIVE
    return redirect("/admin/dashboard")

# ================= STUDENT LIST =================
@app.route("/admin/students")
def admin_students():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_students.html", students=STUDENT_ATTEMPTS)

# ================= ADMIN LOGOUT =================
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)