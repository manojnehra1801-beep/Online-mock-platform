from flask import Flask, request, session, redirect
import time

app = Flask(__name__)
app.secret_key = "ntpc2025"

PER_MARK = 1
NEG_MARK = 1/3
TOTAL_TIME = 15 * 30   # 15 questions × 30 sec

QUESTIONS = [
("कौन सा स्मृति प्रकार गैर-अस्थिर है और एम्बेडेड नियंत्रकों में फर्मवेयर भंडारण के लिए उपयोग होता है?",
["Flash ROM","DRAM","L3 Cache","SRAM"],0),

("एक वर्गाकार मैदान का क्षेत्रफल 1369 m² है। इसका परिमाप कितना है?",
["146","152","148","139"],2),

("मुहम्मद क़ासिम नानोत्वी और रशीद अहमद गंगोही ने किस आंदोलन की स्थापना की?",
["पागल पंथी आंदोलन","देवबंद आंदोलन","वहाबी आंदोलन","शरिया आंदोलन"],1),

("A और B मिलकर कार्य को 14 दिनों में करते हैं। A अकेले 42 दिनों में करता है। B अकेले एक-तिहाई कार्य कितने दिनों में करेगा?",
["14","7","21","28"],2),

("दिल्ली में 1857 के विद्रोह का नेता कौन था?",
["मंगल पांडे","बहादुर शाह द्वितीय","बेगम हजरत महल","नाना साहब"],1),

("₹9900 को A,B,C में बाँटा गया। A:C = 4:18 और B = A+C का 50%। B का हिस्सा कितना है?",
["3300","3302","3301","3298"],0),

("भारतीय संविधान का कौन-सा अनुच्छेद DPSP से संबंधित है?",
["46–51","56–51","66–51","36–51"],0),

("चुनाव परिणाम की आधिकारिक घोषणा कौन करता है?",
["Presiding Officer","Returning Officer","Chief Observer","Polling Officer"],1),

("घर की ऊँचाई 25m, घर के शीर्ष का उन्नयन कोण 45°, खंभे के शीर्ष का 60°। खंभे की ऊँचाई?",
["8.66","15","25","43.3"],1),

("ASCII का पूर्ण रूप क्या है?",
["American Standard Code for International Interchange","Advanced Standard Code for Information Interchange",
"American Standard Code for Information Interchange","American Scientific Code for Information Interchange"],2),

("भारत में न्यायाधिकरणों हेतु संवैधानिक प्रावधान किस संशोधन से आए?",
["42वां, 1976","41वां, 1975","44वां, 1978","40वां, 1974"],0),

("यदि A+B 10 दिन में और B अकेले 15 दिन में, तो A अकेले कितने दिन?",
["20","25","30","15"],0),

("श्रृंखला: 57 58 62 71 87 112 ?",
["137","148","144","76"],0),

("दंतिदुर्ग ने किस राजवंश की स्थापना की?",
["गुर्जर प्रतिहार","राष्ट्रकूट","पाल","चोल"],1),

("विजय हजारे ट्रॉफी 2024–25 विजेता?",
["विदर्भ","हरियाणा","गुजरात","कर्नाटक"],0),
]

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        session.clear()
        session["name"]=request.form["name"]
        session["i"]=0
        session["ans"]={}
        session["start"]=time.time()
        return redirect("/exam")
    return """
    <center><h2>NTPC CBT-2 MOCK</h2>
    <form method=post>
    <input name=name placeholder="Enter Name" required><br><br>
    <button>Start Test</button></form></center>"""

@app.route("/exam", methods=["GET","POST"])
def exam():
    if time.time()-session["start"]>TOTAL_TIME:
        return redirect("/result")

    i=session["i"]
    if request.method=="POST":
        session["ans"][str(i)] = request.form.get("ans")
        session["i"]+=1
        return redirect("/exam")

    if i>=len(QUESTIONS):
        return redirect("/result")

    q,opts,_=QUESTIONS[i]
    return f"""
    <h3>Q{i+1}/15</h3>
    <form method=post>
    <p>{q}</p>
    {''.join([f"<input type='radio' name='ans' value='{j}' required> {opts[j]}<br>" for j in range(4)])}
    <br><button>Next</button></form>
    """

@app.route("/result")
def result():
    score=0
    for i,(q,opts,ans) in enumerate(QUESTIONS):
        u=session["ans"].get(str(i))
        if u:
            if int(u)==ans: score+=PER_MARK
            else: score-=NEG_MARK
    return f"<h2>Result</h2>Score: {round(score,2)}/15"

if __name__=="__main__":
    app.run()