from flask import Flask, render_template, request, redirect, session, url_for
import os
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================= DATABASE =================
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM students WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["name"] = user["username"]
            session["student_id"] = user["id"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()
            cur.close()
            conn.close()

            return redirect("/")

        except Exception as e:
            return render_template("signup.html", error="Username already exists")

    return render_template("signup.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")

# ================= SSC DASHBOARD =================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")

# ================= SSC CGL =================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")

# ================= SSC CGL FULL MOCK LIST =================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")

# ================= MOCK INSTRUCTIONS (1–30) =================
@app.route("/ssc/cgl/mock/<int:mock_no>")
def ssc_cgl_mock_instructions(mock_no):
    if "name" not in session:
        return redirect("/")

    # अभी सभी mock same instructions page use करेंगे
    return render_template(
        "ssc_cgl_mock_1_instructions.html",
        mock_no=mock_no
    )

# ================= EXAM PAGE =================
@app.route("/exam/<int:mock_no>")
def exam(mock_no):
    if "name" not in session:
        return redirect("/")
    return render_template("exam.html", mock_no=mock_no)

# ================= SUBMIT RESULT =================
@app.route("/submit", methods=["POST"])
def submit():
    if "name" not in session:
        return redirect("/")

    score = request.form.get("score", 0)
    total = request.form.get("total", 0)
    exam_name = request.form.get("exam_name", "SSC CGL Mock")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attempts (student_id, exam_name, score, total) VALUES (%s,%s,%s,%s)",
        (session["student_id"], exam_name, score, total)
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/result")

# ================= RESULT =================
@app.route("/result")
def result():
    if "name" not in session:
        return redirect("/")
    return render_template("result.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)