from flask import Flask, request, session, redirect
import time

app = Flask(__name__)
app.secret_key = "mock2025"

PER_MARK = 1
NEG_MARK = 0.25
EXAM_TIME = 90   # seconds

QUESTIONS = [
    ("भारत की राजधानी क्या है?",
     ["Delhi","Mumbai","Chennai","Kolkata"],0),

    ("सबसे लंबी नदी कौन सी है?",
     ["Ganga","Yamuna","Nile","Amazon"],2),

    ("ताजमहल कहाँ स्थित है?",
     ["Delhi","Agra","Jaipur","Lucknow"],1)
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
    return """<html><head><style>
    body{font-family:sans-serif;text-align:center;}
    input,button{font-size:20px;padding:10px;width:80%}
    </style></head><body>
    <h2>ONLINE MOCK TEST</h2>
    <form method='post'>
    <input name='name' placeholder='Enter Name' required><br><br>
    <button>START EXAM</button></form></body></html>"""

@app.route("/exam", methods=["GET","POST"])
def exam():
    if time.time()-session["start"]>EXAM_TIME:
        return redirect("/result")
    i=session["i"]
    if request.method=="POST":
        session["ans"][str(i)] = request.form.get("ans")
        session["i"]+=1
        return redirect("/exam")
    if i>=len(QUESTIONS): return redirect("/result")

    q,opts,_=QUESTIONS[i]
    return f"""<html><head><style>
    body{{font-family:sans-serif;padding:10px}}
    .opt{{font-size:18px;padding:10px;border:1px solid #444;border-radius:10px;margin:8px 0}}
    button{{width:100%;padding:12px;font-size:20px;background:#4caf50;color:white;border:0;border-radius:12px}}
    </style></head><body>
    <b>Question {i+1}/3</b><br><br>{q}
    <form method='post'>
    {''.join([f"<div class='opt'><input type='radio' name='ans' value='{j}' required> {opts[j]}</div>" for j in range(4)])}
    <button>NEXT</button></form></body></html>"""

@app.route("/result")
def result():
    score=0
    html="<h2>RESULT</h2>"
    for i,(q,opts,ans) in enumerate(QUESTIONS):
        u=session["ans"].get(str(i))
        if u!=None:
            if int(u)==ans: score+=PER_MARK
            else: score-=NEG_MARK
        html+=f"<p>{i+1}. {q}<br>Your: {opts[int(u)] if u else 'None'} | Correct: {opts[ans]}</p>"
    html+=f"<h2>FINAL SCORE : {score}/3</h2>"
    return html

if __name__=="__main__":
    app.run()