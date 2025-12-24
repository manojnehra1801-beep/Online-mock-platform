from flask import Flask, request, session, redirect, render_template_string
import time

app = Flask(__name__)
app.secret_key="manoj2025"

PER_MARK=1
NEG_MARK=0.25
Q_TIME=30

QUESTIONS=[
("Which cropping season is NOT in India?\nभारत में कौन सी फसल ऋतु नहीं है?",["Kharif","Rabi","Zaid","Barani"],3),
("Kadbanwadi grassland is in?\nकदबनवाड़ी घासभूमि कहाँ है?",["Tamil Nadu","Andhra Pradesh","Odisha","Maharashtra"],3),
("Which port faces silt problem in Hugli river?\nहुगली नदी में गाद समस्या वाला बंदरगाह?",["Kolkata","Kochi","Tuticorin","Chennai"],0),
("Decline in mortality (1921–51) was due to?\n1921–51 में मृत्यु दर घटने का कारण?",["War","Improved health & sanitation","Birth control","Migration"],1),
("Approx % of plateau region in India?\nभारत में पठारी क्षेत्र का प्रतिशत?",["5%","12%","27%","59%"],2),
("Birth rate > death rate means?\nजन्म दर अधिक होने पर?",["Increase","Decrease","Same","None"],0),
("Sudasari GIB centre is in?\nसुदासरी बस्टर्ड केन्द्र?",["Rajasthan","TN","Kerala","Karnataka"],0),
("Indian Standard Time based on?\nIST आधारित है?",["82.5E","75E","90E","85E"],0),
("Largest coalfield of India?\nसबसे बड़ा कोयला क्षेत्र?",["Jharia","Raniganj","Bokaro","Talcher"],0),
("Black soil is called?\nकाली मिट्टी?",["Regur","Laterite","Red","Alluvial"],0),
("Largest river basin?\nसबसे बड़ा नदी बेसिन?",["Ganga","Brahmaputra","Godavari","Krishna"],0),
("Dakshin Ganga?\nदक्षिण गंगा?",["Krishna","Godavari","Cauvery","Narmada"],1),
("Highest peak of India?\nभारत की सबसे ऊँची चोटी?",["K2","Kanchenjunga","Nanda Devi","Everest"],1),
("Tropic of Cancer passes through how many states?",["8","7","6","9"],0),
("Longest river of India?",["Ganga","Brahmaputra","Godavari","Yamuna"],0),
("Largest desert in India?",["Thar","Sahara","Gobi","Kalahari"],0),
("Pink city?",["Jaipur","Jodhpur","Udaipur","Bikaner"],0),
("Silicon Valley of India?",["Mumbai","Chennai","Bangalore","Pune"],2),
("Highest tea producer?",["Assam","WB","Kerala","TN"],0),
("Highest coffee producer?",["TN","Karnataka","Kerala","Goa"],1),
("Land of Rising Sun?",["Japan","China","Korea","Thailand"],0),
("Blue Planet?",["Earth","Mars","Venus","Jupiter"],0),
("Father of Green Revolution?",["MS Swaminathan","Norman Borlaug","APJ","Gandhi"],0),
("Highest dam?",["Tehri","Bhakra","Hirakud","Sardar"],0),
("Longest dam?",["Hirakud","Bhakra","Tehri","Sardar"],0),
("Largest delta?",["Sundarban","Nile","Amazon","Mississippi"],0),
("River of Sorrow?",["Kosi","Ganga","Yamuna","Brahmaputra"],0),
("Pink lake?",["Lonar","Chilika","Sambhar","Pulicat"],2),
("Largest salt lake?",["Sambhar","Chilika","Pulicat","Wular"],0),
("Golden Temple city?",["Amritsar","Patna","Agra","Delhi"],0),
("City of Seven Hills?",["Rome","Jerusalem","Athens","Istanbul"],0),
("Highest waterfall?",["Jog","Dudhsagar","Nohkalikai","Kunchikal"],3),
("First Indian satellite?",["Aryabhatta","INSAT","Rohini","Bhaskara"],0),
("Largest lake of India?",["Chilika","Wular","Pulicat","Dal"],0),
("Steel City?",["Jamshedpur","Bhilai","Rourkela","Durgapur"],0),
("Which is longest mountain range?",["Himalaya","Andes","Alps","Ural"],1),
("Highest plateau?",["Tibet","Deccan","Iran","Mongolia"],0),
("Largest continent?",["Asia","Africa","Europe","America"],0),
("Smallest continent?",["Australia","Europe","Antarctica","SA"],0),
("Green City?",["Chandigarh","Dehradun","Gandhinagar","Shimla"],0),
("Largest ocean?",["Pacific","Atlantic","Indian","Arctic"],0),
("Land of thousand lakes?",["Finland","Norway","Sweden","Denmark"],0),
("Land of midnight sun?",["Norway","Finland","Iceland","Canada"],0),
("Silk City of India?",["Surat","Kanchipuram","Varanasi","Mysore"],0),
("Pearl City?",["Hyderabad","Chennai","Mumbai","Kolkata"],0),
("Manchester of India?",["Ahmedabad","Kanpur","Mumbai","Surat"],0),
("Queen of Arabian Sea?",["Kochi","Goa","Calicut","Mumbai"],0)
]

TOTAL=len(QUESTIONS)

LOGIN_HTML="""
<h2 align=center>MOCK TEST BY MANOJ NEHRA</h2>
<form method=post align=center>
<input name=name placeholder="Enter Name" required><br><br>
<button>Start</button></form>
"""

INSTR_HTML="""
<h3 align=center>ALL THE BEST {{n}}</h3>
<p align=center>Total Questions: {{t}}<br>1 Mark Each<br>Negative:0.25<br>30 sec per Question</p>
<center><a href="/exam">Start Test</a></center>
"""

EXAM_HTML="""
<h3>Question {{no}}/{{t}}</h3>
<div>
{% for i in range(t) %}
<a href="/jump/{{i}}" style="padding:4px;">•</a>
{% endfor %}
</div><hr>
<form method=post>
<p>{{q}}</p>
{% for o in opt %}
<input type=radio name=ans value="{{loop.index0}}" required> {{o}}<br>
{% endfor %}
<br><button>Next</button></form>
<p>Time Left: <span id=t>30</span>s</p>
<script>
let s=30;setInterval(()=>{s--;t.innerText=s;if(s==0)document.forms[0].submit()},1000)
</script>
"""

RESULT_HTML="""
<h2>RESULT</h2>
<p>Marks: {{m}} / {{t}}</p>
<p>Accuracy: {{acc}} %</p>
<hr>
{% for i in range(t) %}
<p><b>Q{{i+1}}.</b> {{qs[i][0]}}<br>Correct: {{qs[i][1][qs[i][2]]}}</p>
{% endfor %}
"""

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        session["name"]=request.form["name"]
        session["i"]=0
        session["ans"]={}
        return redirect("/start")
    return LOGIN_HTML

@app.route("/start")
def start():
    return render_template_string(INSTR_HTML,n=session["name"],t=TOTAL)

@app.route("/exam",methods=["GET","POST"])
def exam():
    i=session["i"]
    if request.method=="POST":
        session["ans"][i]=int(request.form["ans"])
        session["i"]+=1
        i=session["i"]
    if i>=TOTAL:
        return redirect("/result")
    q,op,_=QUESTIONS[i]
    return render_template_string(EXAM_HTML,no=i+1,t=TOTAL,q=q,opt=op)

@app.route("/jump/<int:i>")
def jump(i):
    session["i"]=i
    return redirect("/exam")

@app.route("/result")
def result():
    score=0
    for i,(q,o,a) in enumerate(QUESTIONS):
        if i in session["ans"]:
            if session["ans"][i]==a: score+=PER_MARK
            else: score-=NEG_MARK
    acc=round((score/TOTAL)*100,2)
    return render_template_string(RESULT_HTML,m=round(score,2),t=TOTAL,acc=acc,qs=QUESTIONS)

if __name__=="__main__":
    app.run()