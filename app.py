from flask import Flask, request, session, redirect, render_template_string
import time

app = Flask(__name__)
app.secret_key = "manoj_exam_2025"

PER_MARK = 1
NEG_MARK = 0.25
Q_TIME = 30

QUESTIONS = [
 ("Which cropping season is NOT in India? / भारत में कौन सा फसल मौसम नहीं है?",
  ["Kharif","Rabi","Zaid","Barani"],3),
 ("Kadbanwadi grassland is in? / कडबनवाड़ी घासभूमि कहाँ है?",
  ["Tamil Nadu","Andhra Pradesh","Odisha","Maharashtra"],3),
 ("Port with silt problem on Hugli river? / हुगली नदी पर गाद समस्या वाला बंदरगाह?",
  ["Kolkata","Kochi","Chennai","Tuticorin"],0),
 ("Sudarsari GIB breeding centre is in? / सुदरसरी ग्रेट इंडियन बस्टर्ड केंद्र?",
  ["Rajasthan","TN","Kerala","Karnataka"],0),
 ("Birth rate > Death rate means? / जन्म दर > मृत्यु दर मतलब?",
  ["Increase","Decrease","Same","None"],0),
]

while len(QUESTIONS)<50:
    QUESTIONS.append(QUESTIONS[len(QUESTIONS)%5])

HTML_LOGIN = '''
<html><head><title>MOCK TEST</title></head>
<body style="font-family:arial;text-align:center">
<h2>MOCK TEST BY MANOJ NEHRA</h2>
<form method=post>
<input name=name placeholder="Enter your name" required>
<br><br><button>Start Test</button>
</form></body></html>
'''

HTML_Q = '''
<h3>Question {{no}} / 50</h3>
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
'''

HTML_RES = '''
<h2>Result</h2>
<p>Marks: {{m}} / 50</p>
<p>Accuracy: {{acc}}%</p>
<p>Percentile: {{per}}%</p>
'''

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        session["name"]=request.form["name"]
        session["i"]=0
        session["score"]=0
        session["attempt"]=0
        return redirect("/q")
    return HTML_LOGIN

@app.route("/q", methods=["GET","POST"])
def q():
    i=session["i"]
    if request.method=="POST":
        session["attempt"]+=1
        if int(request.form["ans"])==QUESTIONS[i][2]:
            session["score"]+=PER_MARK
        else:
            session["score"]-=NEG_MARK
        session["i"]+=1
    if session["i"]>=50:
        return redirect("/result")
    q,op,_=QUESTIONS[session["i"]]
    return render_template_string(HTML_Q,no=session["i"]+1,q=q,opt=op)

@app.route("/result")
def res():
    m=round(session["score"],2)
    acc=round((session["score"]/50)*100,2)
    per=min(99,acc+10)
    return render_template_string(HTML_RES,m=m,acc=acc,per=per)

if __name__=="__main__":
    app.run()