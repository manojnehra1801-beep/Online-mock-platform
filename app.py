from flask import Flask, render_template, request, redirect, session, abort

app = Flask(__name__)
app.secret_key = "ssc_mock_test_secret"

# ================= ADMIN CONFIG =================
ADMIN_USER = "Manojnehra"
ADMIN_PASS = "NEHRA@2233"

EXAM_ACTIVE = True
ANSWER_KEY_OPEN = False
ANSWER_KEY_TOKEN = "NEHRA2025KEY"   # 🔐 secret link token

STUDENT_ATTEMPTS = []

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
        "options": [
            "Ditta Mangalika",
            "Mrichchhakatika",
            "Jataka Kathayen",
            "Manusmriti"
        ],
        "answer": 1
    },
    {
        "id": "q3",
        "question": "Baisakhi is associated with which Sikh institution?\nबैसाखी किस सिख संस्था से जुड़ी है?",
        "options": [
            "Akal Takht",
            "Khalsa Panth",
            "Harmandir Sahib",
            "Guru Granth Sahib"
        ],
        "answer": 1
    },
    {
        "id": "q4",
        "question": "Birthplace of Kho-Kho?\nखो-खो का जन्मस्थान कौन सा राज्य है?",
        "options": [
            "Tamil Nadu",
            "Maharashtra",
            "Punjab",
            "Haryana"
        ],
        "answer": 1
    },
    {
        "id": "q5",
        "question": "Where was the first IPL final (2008) held?\n2008 में पहला IPL फाइनल कहाँ हुआ?",
        "options": [
            "Kolkata",
            "Mumbai",
            "Chennai",
            "Bangalore"
        ],
        "answer": 0
    },
    {
        "id": "q6",
        "question": "First Men's Kabaddi World Cup final venue?\nपहला पुरुष कबड्डी विश्व कप फाइनल कहाँ हुआ?",
        "options": [
            "New Delhi",
            "Mumbai",
            "Ahmedabad",
            "Patna"
        ],
        "answer": 1
    },
    {
        "id": "q7",
        "question": "National Education Day is celebrated on whose birthday?\nराष्ट्रीय शिक्षा दिवस किसकी जयंती पर मनाया जाता है?",
        "options": [
            "Jyotirao Phule",
            "Dr B R Ambedkar",
            "Maulana Abul Kalam Azad",
            "C R Das"
        ],
        "answer": 2
    },
    {
        "id": "q8",
        "question": "India’s first full-time woman Finance Minister?\nभारत की पहली पूर्णकालिक महिला वित्त मंत्री कौन हैं?",
        "options": [
            "Indira Gandhi",
            "Sushma Swaraj",
            "Pratibha Patil",
            "Nirmala Sitharaman"
        ],
        "answer": 3
    },
    {
        "id": "q9",
        "question": "Main objective of PM Jan-Dhan Yojana?\nप्रधानमंत्री जन-धन योजना का मुख्य उद्देश्य क्या है?",
        "options": [
            "Housing for all",
            "Financial inclusion",
            "Free education",
            "Rural electrification"
        ],
        "answer": 1
    },
    {
        "id": "q10",
        "question": "Which novel won Nobel Prize for Gabriel Garcia Marquez?\nमार्केज़ को किस उपन्यास के लिए नोबेल पुरस्कार मिला?",
        "options": [
            "Love in the Time of Cholera",
            "Autumn of the Patriarch",
            "One Hundred Years of Solitude",
            "Chronicle of a Death Foretold"
        ],
        "answer": 2
    },
    {
        "id": "q11",
        "question": "‘Raag Darbari’ was written by?\n‘राग दरबारी’ किसने लिखा?",
        "options": [
            "Shrilal Shukla",
            "Yashpal",
            "Premchand",
            "Kamleshwar"
        ],
        "answer": 0
    },
    {
        "id": "q12",
        "question": "Global Innovation Index is released by?\nग्लोबल इनोवेशन इंडेक्स कौन जारी करता है?",
        "options": [
            "IMF",
            "World Bank",
            "WIPO",
            "UNDP"
        ],
        "answer": 2
    },
    {
        "id": "q13",
        "question": "Natural increase of population depends on?\nजनसंख्या की प्राकृतिक वृद्धि किस पर निर्भर करती है?",
        "options": [
            "Birth rate & migration",
            "Death rate & fertility",
            "Birth rate & death rate",
            "Migration & sex ratio"
        ],
        "answer": 2
    },
    {
        "id": "q14",
        "question": "‘Jhum’ cultivation is practiced in?\n‘झूम’ कृषि कहाँ प्रचलित है?",
        "options": [
            "Western Ghats",
            "Punjab plains",
            "North-East India",
            "Deccan Plateau"
        ],
        "answer": 2
    },
    {
        "id": "q15",
        "question": "How many defenders start in Kho-Kho?\nखो-खो में प्रारंभ में कितने डिफेंडर होते हैं?",
        "options": [
            "2",
            "3",
            "4",
            "5"
        ],
        "answer": 1
    },
    {
        "id": "q16",
        "question": "Judicial Review concept is taken from?\nन्यायिक पुनरावलोकन की अवधारणा किस देश से ली गई है?",
        "options": [
            "USA",
            "UK",
            "Canada",
            "Australia"
        ],
        "answer": 0
    },
    {
        "id": "q17",
        "question": "Effect of currency devaluation?\nमुद्रा अवमूल्यन का प्रभाव क्या होता है?",
        "options": [
            "Imports increase",
            "Exports increase",
            "Deflation",
            "Unemployment"
        ],
        "answer": 1
    },
    {
        "id": "q18",
        "question": "Reducing corporate tax leads to?\nकॉर्पोरेट टैक्स घटाने से क्या होता है?",
        "options": [
            "Lower investment",
            "Higher inflation",
            "Reduced supply",
            "Higher investment"
        ],
        "answer": 3
    },
    {
        "id": "q19",
        "question": "Who wrote Malayalam novel ‘Chemmeen’?\nमलयालम उपन्यास ‘चेम्मीन’ किसने लिखा?",
        "options": [
            "O V Vijayan",
            "Thakazhi Sivasankara Pillai",
            "M T Vasudevan Nair",
            "S K Pottekkatt"
        ],
        "answer": 1
    },
    {
        "id": "q20",
        "question": "Which ministry launched NYPS 2.0 in 2025?\n2025 में NYPS 2.0 किस मंत्रालय ने लॉन्च किया?",
        "options": [
            "Ministry of Education",
            "Ministry of Parliamentary Affairs",
            "Ministry of Youth Affairs & Sports",
            "Ministry of Information & Broadcasting"
        ],
        "answer": 1
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
    if not EXAM_ACTIVE:
        return "Exam not started yet."

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
            "unattempted": len(QUESTIONS) - attempted,
            "accuracy": accuracy
        })

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)


@app.route("/result")
def result():
    return render_template("result.html", **session)

# ================= SECRET ANSWER KEY =================
@app.route("/answer-key/<token>")
def answer_key(token):
    if not ANSWER_KEY_OPEN or token != ANSWER_KEY_TOKEN:
        return redirect("/")
    return render_template("review.html", questions=QUESTIONS)

# ================= ADMIN ROUTES =================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin/dashboard")
        return "Invalid admin login"
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template(
        "admin_dashboard.html",
        exam_active=EXAM_ACTIVE,
        answer_key=ANSWER_KEY_OPEN
    )


@app.route("/admin/toggle-exam")
def toggle_exam():
    if not session.get("admin"):
        abort(403)
    global EXAM_ACTIVE
    EXAM_ACTIVE = not EXAM_ACTIVE
    return redirect("/admin/dashboard")


@app.route("/admin/toggle-answer-key")
def toggle_answer_key():
    if not session.get("admin"):
        abort(403)
    global ANSWER_KEY_OPEN
    ANSWER_KEY_OPEN = not ANSWER_KEY_OPEN
    return redirect("/admin/dashboard")


@app.route("/admin/students")
def admin_students():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_students.html", students=STUDENT_ATTEMPTS)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)