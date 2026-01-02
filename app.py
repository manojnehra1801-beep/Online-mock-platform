from flask import Flask, render_template, request, redirect, session, abort

app = Flask(__name__)
app.secret_key = "ssc_mock_test_secret"
STUDENT_ATTEMPTS = []
# ================= ADMIN CONFIG =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "Nehra@2233"
ANSWER_KEY_OPEN = False   # admin control

# ================= QUESTIONS (20) =================
QUESTIONS = [
    {
        "id": "q1",
        "question": "Which statement is TRUE about the Industrial Policy Resolution of 1956?\n1956 की औद्योगिक नीति संकल्प के बारे में कौन सा कथन सही है?",
        "options": [
            "It aimed to promote only private industries",
            "It classified industries into three categories",
            "It discouraged public sector investment",
            "It focused only on agriculture"
        ],
        "answer": 1
    },
    {
        "id": "q2",
        "question": "Shudraka wrote which play?\nशूद्रक द्वारा लिखा गया नाटक कौन सा है?",
        "options": ["Ditta Mangalika", "Mrichchhakatika", "Jataka Kathayen", "Manusmriti"],
        "answer": 1
    },
    {
        "id": "q3",
        "question": "Baisakhi is associated with which Sikh institution?\nबैसाखी किस सिख संस्था से जुड़ी है?",
        "options": ["Akal Takht", "Khalsa Panth", "Harmandir Sahib", "Guru Granth Sahib"],
        "answer": 1
    },
    {
        "id": "q4",
        "question": "Birthplace of Kho-Kho?\nखो-खो का जन्मस्थान?",
        "options": ["Tamil Nadu", "Maharashtra", "Punjab", "Haryana"],
        "answer": 1
    },
    {
        "id": "q5",
        "question": "First IPL final (2008) was held at?\nपहला IPL फाइनल कहाँ हुआ?",
        "options": ["Kolkata", "Mumbai", "Chennai", "Bangalore"],
        "answer": 1
    },
    {
        "id": "q6",
        "question": "First Men's Kabaddi World Cup final venue?\nपहला पुरुष कबड्डी विश्व कप फाइनल कहाँ हुआ?",
        "options": ["New Delhi", "Mumbai", "Ahmedabad", "Patna"],
        "answer": 1
    },
    {
        "id": "q7",
        "question": "National Education Day is celebrated on whose birthday?\nराष्ट्रीय शिक्षा दिवस किसकी जयंती पर?",
        "options": ["Jyotirao Phule", "Dr. B. R. Ambedkar", "Maulana Abul Kalam Azad", "C. R. Das"],
        "answer": 2
    },
    {
        "id": "q8",
        "question": "India’s first full-time woman Finance Minister?\nभारत की पहली पूर्णकालिक महिला वित्त मंत्री?",
        "options": ["Indira Gandhi", "Hemvati Bahuguna", "Sushma Swaraj", "Nirmala Sitharaman"],
        "answer": 3
    },
    {
        "id": "q9",
        "question": "Main objective of PM Jan Dhan Yojana?\nप्रधानमंत्री जन धन योजना का उद्देश्य?",
        "options": ["Housing", "Financial inclusion", "Education", "Electrification"],
        "answer": 1
    },
    {
        "id": "q10",
        "question": "Nobel Prize novel of Gabriel Garcia Marquez?\nमार्केज़ को किस उपन्यास के लिए नोबेल मिला?",
        "options": ["Autumn of Patriarch", "Love in Cholera", "One Hundred Years of Solitude", "Chronicle"],
        "answer": 2
    }
]

# ================= STUDENT ROUTES =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        session["name"] = request.form["name"]
        return redirect("/exam")
    return render_template("login.html")


@app.route("/exam", methods=["GET", "POST"])
def exam():
    if request.method == "POST":
        correct = 0
        incorrect = 0

        for q in QUESTIONS:
            ans = request.form.get(q["id"])
            if ans is not None:
                if int(ans) == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

        attempted = correct + incorrect
        unattempted = len(QUESTIONS) - attempted
        accuracy = round((correct / attempted) * 100, 2) if attempted else 0
STUDENT_ATTEMPTS.append({
            "name": session.get("name"),
            "score": correct,
            "attempted": attempted,
            "total": len(QUESTIONS),
            "accuracy": accuracy
        })
        session.update({
            "score": correct,
            "total": len(QUESTIONS),
            "correct": correct,
            "incorrect": incorrect,
            "attempted": attempted,
            "unattempted": unattempted,
            "accuracy": accuracy
        })

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)


@app.route("/result")
def result():
    return render_template("result.html", **session)


# ================= ANSWER KEY =================
@app.route("/answer-key")
def answer_key():
    if not ANSWER_KEY_OPEN:
        return "Answer key not released by admin yet."
    return render_template("review.html", questions=QUESTIONS)


# ================= ADMIN ROUTES =================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin/dashboard")
        return "Invalid admin credentials"
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_dashboard.html", status=ANSWER_KEY_OPEN)


@app.route("/admin/toggle")
def toggle_answer_key():
    if not session.get("admin"):
        abort(403)
    global ANSWER_KEY_OPEN
    ANSWER_KEY_OPEN = not ANSWER_KEY_OPEN
    return redirect("/admin/dashboard")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)