from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "mock_test_secret_key"

QUESTIONS = [
    {
        "id": "q1",
        "question": "Which of the following statements is TRUE about the Industrial Policy Resolution of 1956?\nऔद्योगिक नीति संकल्प 1956 के बारे में कौन सा कथन सही है?",
        "options": [
            "It aimed to promote only private industries / केवल निजी उद्योग",
            "It classified industries into three categories / उद्योगों को तीन श्रेणियों में बाँटा",
            "It discouraged public sector investment / सार्वजनिक क्षेत्र को हतोत्साहित किया",
            "It focused only on agriculture / केवल कृषि पर केंद्रित"
        ],
        "answer": 1
    },
    {
        "id": "q2",
        "question": "What was the name of the play written by Shudrak in the 4th century?\nचौथी शताब्दी में शूद्रक द्वारा लिखा गया नाटक कौन सा था?",
        "options": [
            "Ditha Mangalika / दीठ मंगलिका",
            "Mrichchhakatika / मृच्छकटिक",
            "Jataka Kathayen / जातक कथाएँ",
            "Manusmriti / मनुस्मृति"
        ],
        "answer": 1
    },
    {
        "id": "q3",
        "question": "The festival of Baisakhi is associated with the formation of which Sikh institution?\nबैसाखी किस सिख संस्था के गठन से जुड़ी है?",
        "options": [
            "Akal Takht / अकाल तख्त",
            "Khalsa Panth / खालसा पंथ",
            "Harmandir Sahib / हरमंदिर साहिब",
            "Guru Granth Sahib / गुरु ग्रंथ साहिब"
        ],
        "answer": 1
    },
    {
        "id": "q4",
        "question": "Which Indian state is considered the birthplace of Kho-Kho?\nखो-खो का जन्मस्थान किस राज्य को माना जाता है?",
        "options": [
            "Tamil Nadu / तमिलनाडु",
            "Maharashtra / महाराष्ट्र",
            "Punjab / पंजाब",
            "Haryana / हरियाणा"
        ],
        "answer": 1
    },
    {
        "id": "q5",
        "question": "Where was the final match of the first IPL tournament held in 2008?\n2008 में पहले IPL टूर्नामेंट का फाइनल कहाँ हुआ था?",
        "options": [
            "Kolkata / कोलकाता",
            "Mumbai / मुंबई",
            "Chennai / चेन्नई",
            "Bangalore / बेंगलुरु"
        ],
        "answer": 1
    },
    {
        "id": "q6",
        "question": "Where was the final match of the first Men’s Kabaddi World Cup held?\nपहले पुरुष कबड्डी विश्व कप का फाइनल कहाँ हुआ था?",
        "options": [
            "New Delhi / नई दिल्ली",
            "Mumbai / मुंबई",
            "Ahmedabad / अहमदाबाद",
            "Patna / पटना"
        ],
        "answer": 1
    },
    {
        "id": "q7",
        "question": "National Education Day of India marks the birth anniversary of whom?\nभारत का राष्ट्रीय शिक्षा दिवस किसकी जयंती पर मनाया जाता है?",
        "options": [
            "Jyotirao Phule / ज्योतिराव फुले",
            "Dr. B. R. Ambedkar / डॉ. भीमराव अंबेडकर",
            "Maulana Abul Kalam Azad / मौलाना अबुल कलाम आज़ाद",
            "C. R. Das / सी. आर. दास"
        ],
        "answer": 2
    },
    {
        "id": "q8",
        "question": "Who is India’s first full-time woman Finance Minister?\nभारत की पहली पूर्णकालिक महिला वित्त मंत्री कौन हैं?",
        "options": [
            "Indira Gandhi / इंदिरा गांधी",
            "Hemvati Nandan Bahuguna / हेमवती नंदन बहुगुणा",
            "Sushma Swaraj / सुषमा स्वराज",
            "Nirmala Sitharaman / निर्मला सीतारमण"
        ],
        "answer": 3
    },
    {
        "id": "q9",
        "question": "What is the primary objective of Pradhan Mantri Jan Dhan Yojana?\nप्रधानमंत्री जन धन योजना का मुख्य उद्देश्य क्या है?",
        "options": [
            "Providing housing to all / सभी को आवास",
            "Financial inclusion of the poor / गरीबों का वित्तीय समावेशन",
            "Free education for girls / बालिकाओं को मुफ्त शिक्षा",
            "Rural electrification / ग्रामीण विद्युतीकरण"
        ],
        "answer": 1
    },
    {
        "id": "q10",
        "question": "Gabriel Garcia Marquez won the Nobel Prize in Literature for which novel?\nगेब्रियल गार्सिया मार्केज़ को किस उपन्यास के लिए नोबेल पुरस्कार मिला?",
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
        "question": "Rag Darbari is written by which author?\n'राग दरबारी' किस लेखक द्वारा लिखी गई है?",
        "options": [
            "Sri Lal Shukla / श्रीलाल शुक्ल",
            "Kamleshwar / कमलेश्वर",
            "Yashpal / यशपाल",
            "Premchand / प्रेमचंद"
        ],
        "answer": 0
    },
    {
        "id": "q12",
        "question": "The Global Innovation Index is released by which organization?\nवैश्विक नवाचार सूचकांक किसके द्वारा जारी किया जाता है?",
        "options": [
            "IMF",
            "UNCTAD",
            "WIPO",
            "World Bank"
        ],
        "answer": 2
    },
    {
        "id": "q13",
        "question": "Natural increase of population is measured by which difference?\nजनसंख्या की प्राकृतिक वृद्धि किस अंतर से मापी जाती है?",
        "options": [
            "Birth rate and migration",
            "Death rate and life expectancy",
            "Birth rate and death rate",
            "Fertility rate and sex ratio"
        ],
        "answer": 2
    },
    {
        "id": "q14",
        "question": "Shifting cultivation known as Jhum is practiced in which region?\nझूम खेती किस क्षेत्र में की जाती है?",
        "options": [
            "Rajasthan",
            "Punjab",
            "North-East India",
            "Western Ghats"
        ],
        "answer": 2
    },
    {
        "id": "q15",
        "question": "In Kho-Kho, how many defenders start a defensive turn?\nखो-खो में रक्षा पारी की शुरुआत में कितने खिलाड़ी होते हैं?",
        "options": ["2", "3", "4", "5"],
        "answer": 1
    },
    {
        "id": "q16",
        "question": "Judicial Review is borrowed from which country?\nन्यायिक समीक्षा की अवधारणा किस देश से ली गई है?",
        "options": [
            "USA",
            "Canada",
            "Australia",
            "UK"
        ],
        "answer": 0
    },
    {
        "id": "q17",
        "question": "What is the effect of currency devaluation?\nमुद्रा अवमूल्यन का प्रभाव क्या होता है?",
        "options": [
            "Cause deflation",
            "Improve trade balance",
            "Reduce exports",
            "Increase imports"
        ],
        "answer": 1
    },
    {
        "id": "q18",
        "question": "What happens when corporate tax is reduced?\nजब कॉर्पोरेट टैक्स घटाया जाता है तो क्या होता है?",
        "options": [
            "Imports rise immediately",
            "Reduction in fiscal deficit",
            "Decrease in disposable income",
            "Increase in supply-side investment"
        ],
        "answer": 3
    },
    {
        "id": "q19",
        "question": "Who wrote the Malayalam novel 'Chemmeen'?\n'चेम्मीन' उपन्यास किसने लिखा?",
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
        "question": "Which ministry launched NYPS 2.0 portal in March 2025?\nमार्च 2025 में NYPS 2.0 पोर्टल किस मंत्रालय ने लॉन्च किया?",
        "options": [
            "Ministry of Education",
            "Ministry of Parliamentary Affairs",
            "Ministry of Youth Affairs and Sports",
            "Ministry of Information and Broadcasting"
        ],
        "answer": 1
    }
]

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
        accuracy = round((correct / attempted) * 100, 2) if attempted > 0 else 0
result_data = []

for q in QUESTIONS:
    user_ans = request.form.get(q["id"])
    result_data.append({
        "question": q["question"],
        "options": q["options"],
        "correct": q["answer"],
        "user": int(user_ans) if user_ans is not None else None
    })

session["result_data"] = result_data
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)