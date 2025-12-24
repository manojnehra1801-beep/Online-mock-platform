from flask import Flask, render_template_string, request, redirect, session
import random, time

app = Flask(__name__)
app.secret_key = "mock2025"

QUESTIONS = [
    ("Which gas is used by plants in photosynthesis?",
     ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], 1),

    ("Who is known as the Father of Indian Constitution?",
     ["Nehru", "Gandhi", "Dr. B.R. Ambedkar", "Rajendra Prasad"], 2),

    ("What is the capital of Rajasthan?",
     ["Jodhpur", "Jaipur", "Udaipur", "Ajmer"], 1)
]

PER_MARK = 1
NEG_MARK = 0.25

@app.route("/", methods=["GET","POST"])
def start():
    if request.method=="POST":
        session["name"] = request.form["name"]
        session["qs"] = random.sample(QUESTIONS, 3)
        session["ans"] = {}
        return redirect("/exam")
    return '''
    <center>
    <h1>ONLINE MOCK TEST</h1>
    <form method=post>
    <input name=name placeholder="Enter your name" required><br><br>
    <button>Start Exam</button>
    </form>
    </center>
    '''

@app.route("/exam", methods=["GET","POST"])
def exam():
    qs = session["qs"]
    if request.method=="POST":
        session["ans"][request.form["qid"]] = int(request.form["opt"])
    qid = int(request.args.get("q",0))
    q = qs[qid]
    done = len(session["ans"])
    left = 3-done
    return render_template_string("""
    <style>
    body{font-family:arial;background:#f0f8ff}
    .nav{position:fixed;right:10px;top:10px}
    button{padding:10px;margin:5px}
    </style>
    <div class=nav>
    Attempted: {{done}} | Left: {{left}}<br>
    {% for i in range(3) %}
    <a href="/exam?q={{i}}">•</a>
    {% endfor %}
    </div>
    <h2>Q{{qid+1}}. {{q[0]}}</h2>
    <form method=post>
    <input type=hidden name=qid value="{{qid}}">
    {% for o in q[1] %}
    <input type=radio name=opt value="{{loop.index0}}" required>{{o}}<br>
    {% endfor %}
    <button>Save</button>
    </form>
    <br>
    {% if qid<2 %}<a href="/exam?q={{qid+1}}">Next</a>{% endif %}
    {% if done==3 %}<a href="/result">Submit Exam</a>{% endif %}
    """,q=q,qid=qid,done=done,left=left)

@app.route("/result")
def result():
    score=0
    review=[]
    for i,q in enumerate(session["qs"]):
        if str(i) in session["ans"]:
            if session["ans"][str(i)]==q[2]:
                score+=PER_MARK
            else:
                score-=NEG_MARK
        review.append((q[0],q[1],q[2],session["ans"].get(str(i),None)))
    return render_template_string("""
    <h1>RESULT</h1>
    Name: {{session['name']}}<br>
    Score: {{score}} / 3<br><hr>
    {% for r in review %}
    <b>{{r[0]}}</b><br>
    Correct: {{r[1][r[2]]}}<br>
    Your: {{r[1][r[3]] if r[3]!=None else "Not Attempted"}}<br><hr>
    {% endfor %}
    """,score=score,review=review)

app.run()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)