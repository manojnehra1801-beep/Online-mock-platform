from flask import Flask, request, session
import time

app = Flask(__name__)
app.secret_key="manojnehra2025"

PER_MARK=1
NEG_MARK=0.25
Q_TIME=30

QUESTIONS=[
("Which is NOT cropping season?\nनिम्न में से कौन सी फसल ऋतु नहीं है?",["Kharif","Rabi","Zaid","Barani"],3),
("Kadbanwadi grassland is in –\nकदबनवाड़ी घासभूमि किस राज्य में है?",["Tamil Nadu","Andhra Pradesh","Odisha","Maharashtra"],3),
("Which port faces silt problem in Hugli river?\nहुगली नदी में सिल्ट समस्या वाला बंदरगाह?",["Kolkata","Kochchi","Tuticorin","Chennai"],0),
("Decline in mortality (1921–51) was due to –\nमृत्यु दर में गिरावट का कारण?",["War","Improved health & sanitation","Birth control","Migration"],1),
("Approx % of plateau region in India?\nभारत में पठारी क्षेत्र का प्रतिशत?",["5%","12%","27%","59%"],2),
("Birth rate > death rate means –\nजन्म दर मृत्यु दर से अधिक है तो जनसंख्या?",["Increase","Decrease","Same","None"],0),
("Sudasari GIB breeding centre is in –\nसुदासरी ग्रेट इंडियन बस्टर्ड केन्द्र?",["Rajasthan","TN","Kerala","Karnataka"],0),
("Indian standard time is based on which longitude?\nभारतीय मानक समय?",["82.5E","85E","90E","75E"],0),
("Largest coal field of India?\nभारत का सबसे बड़ा कोयला क्षेत्र?",["Jharia","Raniganj","Bokaro","Talcher"],0),
("Black soil is also called?\nकाली मिट्टी को क्या कहते हैं?",["Regur","Laterite","Red","Alluvial"],0),
("Largest river basin in India?\nसबसे बड़ा नदी बेसिन?",["Ganga","Brahmaputra","Godavari","Krishna"],0),
("Which river is known as Dakshin Ganga?\nदक्षिण गंगा?",["Krishna","Godavari","Cauvery","Narmada"],1),
("Highest peak of India?\nभारत की सर्वोच्च चोटी?",["K2","Kanchenjunga","Nanda Devi","Everest"],1),
("Tropic of Cancer passes through how many Indian states?",["8","7","6","9"],0),
("Longest river in India?",["Yamuna","Ganga","Brahmaputra","Godavari"],1),
("Largest desert in India?",["Thar","Sahara","Kalahari","Gobi"],0),
("Pink city of India?",["Jaipur","Jodhpur","Udaipur","Bikaner"],0),
("Silicon Valley of India?",["Mumbai","Chennai","Bangalore","Pune"],2),
("Tea production highest state?",["Assam","WB","Kerala","TN"],0),
("Coffee production highest?",["TN","Karnataka","Kerala","Goa"],1),
("Which is land of rising sun?",["Japan","China","Korea","Thailand"],0),
("Which is blue planet?",["Mars","Venus","Earth","Jupiter"],2),
("Green revolution father?",["MS Swaminathan","Norman Borlaug","Mahatma Gandhi","APJ"],0),
("Highest dam in India?",["Tehri","Bhakra","Hirakud","Sardar"],0),
("Longest dam in India?",["Hirakud","Bhakra","Tehri","Sardar"],0),
("Largest delta?",["Sundarban","Nile","Mississippi","Amazon"],0),
("River of sorrow?",["Kosi","Ganga","Yamuna","Brahmaputra"],0),
("Pink lake in India?",["Lonar","Chilika","Sambhar","Pulicat"],2),
("Largest salt lake?",["Chilika","Pulicat","Sambhar","Wular"],2),
("Golden Temple city?",["Amritsar","Patna","Agra","Delhi"],0),
("City of Seven Hills?",["Rome","Jerusalem","Athens","Istanbul"],0),
("Highest waterfall?",["Jog","Dudhsagar","Nohkalikai","Kunchikal"],3),
("First Indian satellite?",["INSAT","Aryabhatta","Rohini","Bhaskara"],1),
("Largest lake India?",["Wular","Dal","Chilika","Pulicat"],2),
("Steel city?",["Jamshedpur","Bhilai","Durgapur","Rourkela"],0),
("Pink city of Rajasthan?",["Jaipur","Ajmer","Bikaner","Udaipur"],0),
("Which is longest mountain range?",["Himalaya","Andes","Alps","Ural"],1),
("Highest plateau?",["Tibet","Deccan","Iran","Mongolia"],0),
("Biggest continent?",["Asia","Africa","Europe","America"],0),
("Smallest continent?",["Europe","Australia","Antarctica","S America"],1),
("Green city India?",["Gandhinagar","Chandigarh","Shimla","Dehradun"],1),
("Largest ocean?",["Pacific","Atlantic","Indian","Arctic"],0),
("Land of Thousand lakes?",["Finland","Sweden","Norway","Denmark"],0),
("Land of midnight sun?",["Norway","Finland","Iceland","Canada"],0),
("Silk city India?",["Kanchipuram","Surat","Varanasi","Mysore"],1),
("Pearl city?",["Hyderabad","Chennai","Kolkata","Mumbai"],0),
("Scotland of East?",["Shillong","Darjeeling","Gangtok","Imphal"],0),
("Queen of Arabian Sea?",["Kochi","Goa","Mumbai","Calicut"],0),
("Manchester of India?",["Mumbai","Ahmedabad","Surat","Kanpur"],1)
]

TOTAL_Q=len(QUESTIONS)

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        session["name"]=request.form["name"]
        session["qno"]=0
        session["answers"]={}
        return instructions()
    return "<center><h2>MOCK TEST BY MANOJ NEHRA</h2><form method=post><input name=name placeholder='Enter Name' required><br><br><button>Start Test</button></form></center>"

def instructions():
    return f"<center><h3>All The Best {session['name']}</h3><p>Total Q:{TOTAL_Q}<br>1 Mark each<br>Negative:0.25<br>30 sec/Q</p><a href='/exam'>Start Exam</a></center>"

@app.route("/exam",methods=["GET","POST"])
def exam():
    qno=session["qno"]
    if request.method=="POST":
        session["answers"][qno]=int(request.form["opt"])
        session["qno"]+=1
        qno=session["qno"]
    if qno>=TOTAL_Q: return result()
    q,o,a=QUESTIONS[qno]
    p=int((qno+1)/TOTAL_Q*100)
    html=f"<h3>Q{qno+1}/{TOTAL_Q}</h3><div style='background:#ccc;height:12px'><div style='width:{p}%;background:green;height:100%'></div></div><p>{q}</p><form method=post>"
    for i,x in enumerate(o): html+=f"<input type=radio name=opt value={i} required> {x}<br>"
    return html+"<br><button>Next</button></form>"

def result():
    score=0
    for i,(q,o,a) in enumerate(QUESTIONS):
        if session["answers"].get(i)==a: score+=1
        elif i in session["answers"]: score-=0.25
    html=f"<h2>RESULT</h2><p>Marks:{score}/{TOTAL_Q}</p><h3>Answer Review</h3>"
    for i,(q,o,a) in enumerate(QUESTIONS):
        html+=f"<p>Q{i+1}. {q}<br>Correct: {o[a]}</p>"
    return html

if __name__=="__main__":
    app.run()