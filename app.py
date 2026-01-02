from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "ssc_mock_test_secret"

# ================= QUESTIONS (20) =================
QUESTIONS = [
    {
        "id": "q1",
        "question": "Which statement is TRUE about the Industrial Policy Resolution of 1956?\n1956 की औद्योगिक नीति संकल्प के बारे में कौन सा कथन सत्य है?",
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
        "question": "Shudraka wrote which play where Charudatta is a Brahmin and merchant?\nशूद्रक द्वारा रचित वह नाटक कौन सा है?",
        "options": ["Ditta Mangalika", "Mrichchhakatika", "Jataka Kathayen", "Manusmriti"],
        "answer": 1
    },
    {
        "id": "q3",
        "question": "The festival of Baisakhi is associated with which Sikh institution?\nबैसाखी किस सिख संस्था से जुड़ा है?",
        "options": ["Akal Takht", "Khalsa Panth", "Harmandir Sahib", "Guru Granth Sahib"],
        "answer": 1
    },
    {
        "id": "q4",
        "question": "Which Indian state is considered the birthplace of Kho-Kho?\nखो-खो का जन्मस्थान कौन सा राज्य है?",
        "options": ["Tamil Nadu", "Maharashtra", "Punjab", "Haryana"],
        "answer": 1
    },
    {
        "id": "q5",
        "question": "Where was the final match of the first IPL held in 2008?\n2008 IPL का फाइनल कहाँ खेला गया?",
        "options": ["Kolkata", "Mumbai", "Chennai", "Bangalore"],
        "answer": 0
    },
    {
        "id": "q6",
        "question": "Where was the final match of the first Men's Kabaddi World Cup held?\nपहला पुरुष कबड्डी विश्व कप फाइनल कहाँ हुआ?",
        "options": ["New Delhi", "Mumbai", "Ahmedabad", "Patna"],
        "answer": 1
    },
    {
        "id": "q7",
        "question": "National Education Day is celebrated on whose birth anniversary?\nराष्ट्रीय शिक्षा दिवस किसकी जयंती पर मनाया जाता है?",
        "options": ["Jyotirao Phule", "Dr. B. R. Ambedkar", "Maulana Abul Kalam Azad", "C. R. Das"],
        "answer": 2
    },
    {
        "id": "q8",
        "question": "Who is India's first full-time woman Finance Minister?\nभारत की पहली पूर्णकालिक महिला वित्त मंत्री कौन हैं?",
        "options": ["Indira Gandhi", "Hemvati Nandan Bahuguna", "Sushma Swaraj", "Nirmala Sitharaman"],
        "answer": 3
    },
    {
        "id": "q9",
        "question": "What is the main objective of PM Jan Dhan Yojana?\nप्रधानमंत्री जन धन योजना का मुख्य उद्देश्य क्या है?",
        "options": ["Housing for all", "Financial inclusion", "Free education", "Rural electrification"],
        "answer": 1
    },
    {
        "id": "q10",
        "question": "Gabriel Garcia Marquez won the Nobel Prize for which novel?\nगैब्रियल गार्सिया मार्केज़ को किस उपन्यास के लिए नोबेल मिला?",
        "options": [
            "The Autumn of the Patriarch",
            "Love in the Time of Cholera",
            "One Hundred Years of Solitude",
            "Chronicle of a Death Foretold"
        ],
        "answer": 2
    },
    {
        "id": "q11",
        "question": "‘Raag Darbari’ novel was written by?\n‘राग दरबारी’ किसने लिखा?",
        "options": ["Sri Lal Shukla", "Kamleshwar", "Yashpal", "Premchand"],
        "answer": 0
    },
    {
        "id": "q12",
        "question": "Global Innovation Index is released by?\nग्लोबल इनोवेशन इंडेक्स कौन जारी करता है?",
        "options": ["IMF", "UNCTAD", "WIPO", "World Bank"],
        "answer": 2
    },
    {
        "id": "q13",
        "question": "Natural increase of population is measured by?\nजनसंख्या की प्राकृतिक वृद्धि किससे मापी जाती है?",
        "options": [
            "Birth rate & migration",
            "Death rate & life expectancy",
            "Birth rate & death rate",
            "Fertility rate & sex ratio"
        ],
        "answer": 2
    },
    {
        "id": "q14",
        "question": "Shifting cultivation ‘Jhum’ is practiced in which region?\nझूम कृषि कहाँ प्रचलित है?",
        "options": ["Rajasthan", "Punjab", "North-East India", "Western Ghats"],
        "answer": 2
    },
    {
        "id": "q15",
        "question": "In Kho-Kho, how many defenders start the defense?\nखो-खो में रक्षा की शुरुआत में कितने खिलाड़ी होते हैं?",
        "options": ["2", "3", "4", "5"],
        "answer": 1
    },
    {
        "id": "q16",
        "question": "Judicial Review concept is borrowed from which country?\nन्यायिक पुनरावलोकन की अवधारणा किस देश से ली गई?",
        "options": ["USA", "Canada", "Australia", "UK"],
        "answer": 0
    },
    {
        "id": "q17",
        "question": "Effect of devaluation of currency?\nमुद्रा अवमूल्यन का प्रभाव क्या होता है?",
        "options": [
            "Deflation",
            "Improve trade balance",
            "Reduce exports",
            "Increase imports"
        ],
        "answer": 1
    },
    {
        "id": "q18",
        "question": "Reducing corporate tax leads to?\nकॉर्पोरेट टैक्स घटाने से क्या होता है?",
        "options": [
            "Imports rise",
            "Fiscal deficit reduces",
            "Disposable income decreases",
            "Supply-side investment increases"
        ],
        "answer": 3
    },
    {
        "id": "q19",
        "question": "Who wrote Malayalam novel ‘Chemmeen’?\nमलयालम उपन्यास ‘चेम्मीन’ किसने लिखा?",
        "options": [
            "O. V. Vijayan",
            "Thakazhi Sivasankara Pillai",
            "S. K. Pottekkatt",
            "M. T. Vasudevan Nair"
        ],
        "answer": 1
    },
    {
        "id": "q20",
        "question": "Which ministry launched NYPS 2.0 in March 2025?\nमार्च 2025 में NYPS 2.0 किस मंत्रालय ने लॉन्च किया?",
        "options": [
            "Ministry of Education",
            "Ministry of Parliamentary Affairs",
            "Ministry of Youth Affairs & Sports",
            "Ministry of Information & Broadcasting"
        ],
        "answer": 1
    }
]

# ================= ROUTES =================
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
        result_data = []

        for q in QUESTIONS:
            ans = request.form.get(q["id"])
            if ans is not None:
                ans = int(ans)
                if ans == q["answer"]:
                    correct += 1
                else:
                    incorrect += 1

                result_data.append({
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["answer"],
                    "selected": ans
                })

        attempted = correct + incorrect
        unattempted = len(QUESTIONS) - attempted
        accuracy = round((correct / attempted) * 100, 2) if attempted > 0 else 0

        session.update({
            "score": correct,
            "total": len(QUESTIONS),
            "correct": correct,
            "incorrect": incorrect,
            "attempted": attempted,
            "unattempted": unattempted,
            "accuracy": accuracy,
            "result_data": result_data
        })

        return redirect("/result")

    return render_template("exam.html", questions=QUESTIONS)


@app.route("/result")
def result():
    if "score" not in session:
        return redirect("/")
    return render_template("result.html", **session)


@app.route("/answer-key")
def answer_key():
    if "result_data" not in session:
        return redirect("/")
    return render_template("review.html", result_data=session["result_data"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)