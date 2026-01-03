from flask import Flask, render_template, request, redirect, session, abort
import random

app = Flask(__name__)
app.secret_key = "stable_secret_key_123"
EXAM_ACTIVE = False
ANSWER_KEY_ACTIVE = False

# ================= ADMIN =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "NEHRA@2233"
EXAM_ACTIVE = False

# ================= SERVER SIDE STORAGE =================
ACTIVE_EXAMS = {}

# ================= QUESTION BANK =================
REASONING = [
    {"id":"r1","q":"Odd one out: 2, 4, 8, 16, 18","opt":["8","16","18","4"],"ans":2},
    {"id":"r2","q":"If A=1, B=2 then Z=?","opt":["24","25","26","27"],"ans":2},
    {"id":"r3","q":"Mirror image relates to?","opt":["Reflection","Rotation","Refraction","None"],"ans":0},
    {"id":"r4","q":"Odd one: Cat, Dog, Cow, Chair","opt":["Cat","Dog","Cow","Chair"],"ans":3},
    {"id":"r5","q":"3, 6, 12, ?","opt":["18","20","24","30"],"ans":2},
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

# ================= LOGIN =================
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if not EXAM_ACTIVE:
            return "Exam not started yet"

        name = request.form.get("name")
        session["name"] = name

        ACTIVE_EXAMS[name] = {
            "Reasoning": random.sample(REASONING,5),
            "GK": random.sample(GK,5),
            "Maths": random.sample(MATHS,5),
            "English": random.sample(ENGLISH,5),
        }
        return redirect("/exam")

    return render_template("login.html")

# ================= EXAM =================
@app.route("/exam", methods=["GET","POST"])
def exam():
    name = session.get("name")
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
    name = session.get("name")
    exam = ACTIVE_EXAMS.get(name, {})
    answers = session.get("answers", {})

    return render_template(
        "result.html",
        exam=exam,
        answers=answers,
        score=session.get("score",0),
        name=name
    )

# ================= ADMIN =================
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin/dashboard")
        return "Invalid login"
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_dashboard.html", exam_active=EXAM_ACTIVE)

@app.route("/admin/toggle")
def toggle():
    global EXAM_ACTIVE
    if not session.get("admin"):
        abort(403)
    EXAM_ACTIVE = not EXAM_ACTIVE
    return redirect("/admin/dashboard")
@app.route("/admin/toggle-answer-key")
def toggle_answer_key():
    global ANSWER_KEY_ACTIVE
    if not session.get("admin"):
        abort(403)

    ANSWER_KEY_ACTIVE = not ANSWER_KEY_ACTIVE
    return redirect("/admin/dashboard")
@app.route("/admin/toggle-exam")
def toggle_exam():
    global EXAM_ACTIVE
    if not session.get("admin"):
        abort(403)

    EXAM_ACTIVE = not EXAM_ACTIVE
    return redirect("/admin/dashboard")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)