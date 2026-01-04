from flask import Flask, render_template, request, redirect, session, abort

app = Flask(__name__)
app.secret_key = "exam_secret_123"
@app.route("/test")
def test():
    return "TEST OK"

# ================= ADMIN =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "NEHRA@2233"
EXAM_ACTIVE = False

# ================= QUESTIONS =================
QUESTIONS = [
    {
        "id": "q1",
        "question": "Industrial Policy Resolution 1956 classified industries into?",
        "options": [
            "Two categories",
            "Three categories",
            "Four categories",
            "Only private sector"
        ],
        "answer": 1
    },
    {
        "id": "q2",
        "question": "Baisakhi is related to which Sikh institution?",
        "options": [
            "Akal Takht",
            "Khalsa Panth",
            "Guru Granth Sahib",
            "Harmandir Sahib"
        ],
        "answer": 1
    },
    {
        "id": "q3",
        "question": "Who wrote Mrichchhakatika?",
        "options": [
            "Kalidasa",
            "Shudraka",
            "Bhasa",
            "Valmiki"
        ],
        "answer": 1
    }
]

# ================= STUDENT LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not EXAM_ACTIVE:
            return render_template("login.html", error="Exam not started yet")
        session["student"] = request.form.get("name")
        return redirect("/exam")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Abhi sirf signup page dikhayenge (demo)
    return render_template("signup.html")

# ================= EXAM =================
@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "student" not in session:
        return redirect("/")

    if request.method == "POST":
        score = 0
        for q in QUESTIONS:
            ans = request.form.get(q["id"])
            if ans and int(ans) == q["answer"]:
                score += 1

        session["score"] = score
        session["total"] = len(QUESTIONS)
        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)

# ================= RESULT =================
@app.route("/result")
def result():
    if "score" not in session:
        return redirect("/")
    return render_template(
        "result.html",
        score=session["score"],
        total=session["total"]
    )

# ================= ADMIN LOGIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin/dashboard")
        return render_template("admin_login.html", error="Invalid login")
    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_dashboard.html", exam_active=EXAM_ACTIVE)

# ================= TOGGLE EXAM =================
@app.route("/admin/toggle")
def toggle_exam():
    global EXAM_ACTIVE
    if not session.get("admin"):
        abort(403)
    EXAM_ACTIVE = not EXAM_ACTIVE
    return redirect("/admin/dashboard")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)