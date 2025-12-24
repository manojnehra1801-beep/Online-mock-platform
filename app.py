from flask import Flask, request, session, redirect
import time

app = Flask(__name__)
app.secret_key="cbt_demo"

QUESTIONS=[
("भारत की राजधानी क्या है?",
["Delhi","Mumbai","Chennai","Kolkata"],0),
("सबसे बड़ा ग्रह कौन सा है?",
["Earth","Mars","Jupiter","Venus"],2),
("ताजमहल कहाँ स्थित है?",
["Delhi","Agra","Jaipur","Lucknow"],1)
]

TOTAL=len(QUESTIONS)
PER_MARK=1
NEG_MARK=0.25
TOTAL_TIME=90

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        session.clear()
        session["name"]=request.form["name"]
        session["ans"]={}
        session["q"]=0
        session["start"]=time.time()
        return redirect("/exam")
    return """<html><head><style>
    body{font-family:sans-serif;text-align:center;background:#0f172a;color:white}
    input,button{padding:12px;font-size:20px;width:80%}
    </style></head><body>
    <h2>NTPC CBT MOCK</h2>
    <form method=post>
    <input name=name placeholder="Enter Name" required><br><br>
    <button>START EXAM</button></form></body></html>"""

@app.route("/exam",methods=["GET","POST"])
def exam():
    if time.time()-session["start"]>TOTAL_TIME:
        return redirect("/result")

    q=session["q"]
    if request.method=="POST":
        if "ans" in request.form:
            session["ans"][str(q)]=request.form["ans"]
        session["q"]+=1
        return redirect("/exam")

    if q>=TOTAL: return redirect("/result")

    qtext,opts,_=QUESTIONS[q]

    palette=""
    for i in range(TOTAL):
        color="#facc15" if i==q else ("#22c55e" if str(i) in session["ans"] else "#ef4444")
        palette+=f"<a href='/jump/{i}' style='padding:8px;margin:3px;border-radius:50%;background:{color};color:black;text-decoration:none'>{i+1}</a>"

    return f"""<html><head><style>
    body{{font-family:sans-serif;background:#020617;color:white}}
    .opt{{padding:12px;border:1px solid #64748b;border-radius:10px;margin:8px 0}}
    button{{width:100%;padding:14px;font-size:20px;background:#22c55e;color:black;border-radius:12px;border:0}}
    </style></head><body>
    <div style='float:right'>{palette}</div>
    <h3>Q{q+1}/{TOTAL}</h3>
    <form method=post>
    <p>{qtext}</p>
    {''.join([f"<div class='opt'><input type='radio' name='ans' value='{i}'> {opts[i]}</div>" for i in range(4)])}
    <button>NEXT</button></form>
    <div>Time Left: {int(TOTAL_TIME-(time.time()-session["start"]))} sec</div>
    </body></html>"""

@app.route("/jump/<int:i>")
def jump(i):
    session["q"]=i
    return redirect("/exam")

@app.route("/result")
def result():
    score=0
    for i,(q,o,a) in enumerate(QUESTIONS):
        u=session["ans"].get(str(i))
        if u:
            if int(u)==a: score+=PER_MARK
            else: score-=NEG_MARK
    acc=round((score/TOTAL)*100,2)
    per=min(99,acc+10)
    return f"<h2>RESULT</h2>Score:{score}/{TOTAL}<br>Accuracy:{acc}%<br>Percentile:{per}%"

if __name__=="__main__":
    app.run()