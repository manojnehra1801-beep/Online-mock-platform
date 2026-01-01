from flask import Flask, request, session, redirect
import time
import random

app = Flask(__name__)
app.secret_key = "cbt_demo"

QUESTIONS = [
    ("भारत की राजधानी क्या है?",
     ["Delhi", "Mumbai", "Chennai", "Kolkata"], 0),
    ("सबसे बड़ा ग्रह कौन सा है?",
     ["Earth", "Mars", "Jupiter", "Venus"], 2),
    ("ताजमहल कहाँ स्थित है?",
     ["Delhi", "Agra", "Jaipur", "Lucknow"], 1)
]

TOTAL = len(QUESTIONS)
PER_MARK = 1
NEG_MARK = 0.25
PER_Q_TIME = 30          # ⏱️ 30 sec per question
TOTAL_STUDENTS = 87000   # rank calculation base


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        session["name"] = request.form["name"]
        session["ans"] = {}
        session["review"] = {}
        session["q"] = 0
        session["q_start"] = time.time()
        return redirect("/exam")

    return """
    <html><head><meta name=viewport content="width=device-width, initial-scale=1">
    <style>
    body{font-family:sans-serif;background:#020617;color:white;text-align:center}
    input,button{width:90%;padding:14px;font-size:18px;margin:10px}
    </style></head><body>
    <h2>NTPC CBT MOCK</h2>
    <form method=post>
    <input name=name placeholder="Enter Name" required>
    <button>START EXAM</button>
    </form></body></html>
    """


@app.route("/exam", methods=["GET", "POST"])
def exam():
    q = session["q"]

    # ⏱️ auto move next if 30 sec over
    if time.time() - session["q_start"] > PER_Q_TIME:
        session["q"] += 1
        session["q_start"] = time.time()
        return redirect("/exam")

    if q >= TOTAL:
        return redirect("/result")

    if request.method == "POST":
        if "ans" in request.form:
            session["ans"][str(q)] = request.form["ans"]
        if "review" in request.form:
            session["review"][str(q)] = True
        if "prev" in request.form:
            session["q"] = max(0, q - 1)
        else:
            session["q"] += 1
        session["q_start"] = time.time()
        return redirect("/exam")

    qtext, opts, _ = QUESTIONS[q]
    time_left = int(PER_Q_TIME - (time.time() - session["q_start"]))

    palette = ""
    for i in range(TOTAL):
        if i == q:
            color = "#facc15"
        elif str(i) in session["review"]:
            color = "#a855f7"
        elif str(i) in session["ans"]:
            color = "#22c55e"
        else:
            color = "#ef4444"
        palette += f"<a href='/jump/{i}' style='padding:6px;margin:3px;border-radius:50%;background:{color};color:black;text-decoration:none'>{i+1}</a>"

    return f"""
    <html><head><meta name=viewport content="width=device-width, initial-scale=1">
    <style>
    body{{font-family:sans-serif;background:#020617;color:white;font-size:16px}}
    .timer{{position:fixed;top:10px;right:10px;
            background:#dc2626;padding:10px;border-radius:8px}}
    .opt{{padding:12px;border:1px solid #64748b;border-radius:10px;margin:8px 0}}
    button{{width:100%;padding:14px;font-size:18px;margin:6px}}
    </style></head><body>

    <div class="timer">⏱ {time_left}s</div>

    <div>{palette}</div>
    <h3>Q{q+1}/{TOTAL}</h3>

    <form method=post>
    <p>{qtext}</p>
    {''.join([f"<div class='opt'><input type='radio' name='ans' value='{i}' {'checked' if session['ans'].get(str(q))==str(i) else ''}> {opts[i]}</div>" for i in range(4)])}
    <button name="prev">PREVIOUS</button>
    <button>SAVE & NEXT</button>
    <button name="review">MARK FOR REVIEW</button>
    </form>

    </body></html>
    """


@app.route("/jump/<int:i>")
def jump(i):
    session["q"] = i
    session["q_start"] = time.time()
    return redirect("/exam")


@app.route("/result")
def result():
    score = 0
    correct = wrong = unattempted = 0

    for i, (q, o, a) in enumerate(QUESTIONS):
        u = session["ans"].get(str(i))
        if u is None:
            unattempted += 1
        elif int(u) == a:
            score += PER_MARK
            correct += 1
        else:
            score -= NEG_MARK
            wrong += 1

    accuracy = round((correct / TOTAL) * 100, 2)

    # 📊 Rank estimation
    percentile = min(99.9, accuracy + random.uniform(5, 15))
    rank = int((100 - percentile) / 100 * TOTAL_STUDENTS)

    return f"""
    <html><head><meta name=viewport content="width=device-width, initial-scale=1">
    <style>
    body{{font-family:sans-serif;background:#020617;color:white;text-align:center;font-size:18px}}
    .box{{background:#020617;padding:20px;border-radius:12px}}
    </style></head><body>

    <h2>RESULT</h2>
    <div class="box">
    Name: {session.get("name")}<br><br>
    Score: {score}/{TOTAL}<br>
    Correct: {correct}<br>
    Wrong: {wrong}<br>
    Unattempted: {unattempted}<br><br>
    Accuracy: {accuracy}%<br>
    <b>Rank: {rank} / {TOTAL_STUDENTS}</b><br>
    Percentile: {round(percentile,2)}%
    </div>

    </body></html>
    """


if __name__ == "__main__":
    app.run()