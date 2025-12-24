from flask import Flask, request, session, redirect, url_for
import time

app = Flask(__name__)
app.secret_key = "manoj2025"

PER_MARK = 1
NEG_MARK = 0.25
Q_TIME = 30

QUESTIONS = [
    ("भारत की राजधानी क्या है?\nWhat is the capital of India?",
     ["Delhi", "Mumbai", "Chennai", "Kolkata"], 0),

    ("सबसे लंबी नदी कौन सी है?\nWhich is the longest river?",
     ["Ganga", "Yamuna", "Nile", "Amazon"], 2),

    ("ताजमहल कहाँ स्थित है?\nWhere is Taj Mahal located?",
     ["Delhi", "Agra", "Jaipur", "Lucknow"], 1),
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        session["name"] = request.form["name"]
        session["i"] = 0
        session["answers"] = {}
        session["start"] = time.time()
        return redirect("/exam")
    return """
    <html><body style='text-align:center;font-family:sans-serif'>
    <h2>MOCK TEST BY MANOJ NEHRA</h2>
    <form method='post'>
    <input name='name' placeholder='Enter Name' required><br><br>
    <button>Start Test</button>
    </form></body></html>
    """

@app.route("/exam", methods=["GET", "POST"])
def exam():
    i = session["i"]
    if i >= len(QUESTIONS):
        return redirect("/result")

    if request.method == "POST":
        session["answers"][str(i)] = request.form.get("ans")
        session["i"] += 1
        return redirect("/exam")

    q, opts, _ = QUESTIONS[i]
    return f"""
    <html><body style='font-family:sans-serif'>
    <h3>Question {i+1}/{len(QUESTIONS)}</h3>
    <p>{q}</p>
    <form method='post'>
    {''.join([f"<input type='radio' name='ans' value='{j}' required> {opts[j]}<br>" for j in range(4)])}
    <br><button>Next</button>
    </form></body></html>
    """

@app.route("/result")
def result():
    score = 0
    html = "<h2>Result</h2>"
    for i,(q,opts,ans) in enumerate(QUESTIONS):
        user = session["answers"].get(str(i))
        if user is not None:
            if int(user)==ans:
                score+=PER_MARK
            else:
                score-=NEG_MARK
        html += f"<p>{q}<br>Your: {opts[int(user)] if user else 'None'} | Correct: {opts[ans]}</p>"
    html += f"<h3>Score: {score}/{len(QUESTIONS)}</h3>"
    return html

if __name__ == "__main__":
    app.run()