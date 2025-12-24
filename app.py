from flask import Flask, render_template_string, request, redirect, session, url_for
import time

app = Flask(__name__)
app.secret_key = "secret123"

QUESTIONS = [
    {
        "q": "1. Capital of India? / भारत की राजधानी क्या है?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "ans": 0
    },
    {
        "q": "2. Largest planet? / सबसे बड़ा ग्रह?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "ans": 2
    },
    {
        "q": "3. Father of Computer? / कंप्यूटर के जनक?",
        "options": ["Newton", "Einstein", "Charles Babbage", "Tesla"],
        "ans": 2
    }
]

TOTAL_TIME = len(QUESTIONS) * 30   # 30 sec per question

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        session["name"]=request.form["name"]
        session["start"]=time.time()
        session["answers"]={}
        return redirect("/instructions")
    return render_template_string("""
    <h2>MOCK TEST BY MANOJ NEHRA</h2>
    <form method="post">
        <input name="name" placeholder="Enter Name" required>
        <button>Start</button>
    </form>
    """)

@app.route("/instructions")
def instructions():
    return f"""
    <h3>All the Best {session['name']}</h3>
    <p>Total Questions: 3<br>
    Time: {TOTAL_TIME//60} Minutes<br>
    +1 for correct, -0.25 negative</p>
    <a href='/question/0'>Start Test</a>
    """

@app.route("/question/<int:qno>", methods=["GET","POST"])
def question(qno):
    if qno>=len(QUESTIONS):
        return redirect("/result")

    if request.method=="POST":
        session["answers"][str(qno)] = request.form.get("opt")
        return redirect(f"/question/{qno+1}")

    left = int(TOTAL_TIME - (time.time()-session["start"]))
    if left<=0:
        return redirect("/result")

    q = QUESTIONS[qno]
    nav = ""
    for i in range(len(QUESTIONS)):
        nav += f"<a href='/question/{i}'> {i+1} </a> | "

    return render_template_string(f"""
    <div style="float:right">{nav}</div>
    <h4>Time Left: {left} sec</h4>
    <form method="post">
        <p>{q["q"]}</p>
        {"".join([f"<input type='radio' name='opt' value='{i}' required>{o}<br>" for i,o in enumerate(q["options"])])}
        <button>Next</button>
    </form>
    """)

@app.route("/result")
def result():
    score=0
    for i,q in enumerate(QUESTIONS):
        ans = session["answers"].get(str(i))
        if ans:
            if int(ans)==q["ans"]:
                score+=1
            else:
                score-=0.25
    percent = (score/len(QUESTIONS))*100
    return f"""
    <h2>Result</h2>
    Marks: {score}/{len(QUESTIONS)}<br>
    Accuracy: {round(percent,2)}%<br>
    <hr>
    {"".join([f"<p>{q['q']}<br>Correct: {q['options'][q['ans']]}</p>" for q in QUESTIONS])}
    """

if __name__ == "__main__":
    app.run()