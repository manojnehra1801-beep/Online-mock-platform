from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ======================================================
# DATABASE PATH (FIXED & SAFE)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# ======================================================
# DATABASE INIT (AUTO CREATE)
# ======================================================
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Database initialized at:", DB_PATH)

    except Exception as e:
        print("❌ DB init error:", e)

# ⚠️ VERY IMPORTANT: DB init call
init_db()

# ======================================================
# LOGIN
# ======================================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["name"] = username
            return redirect("/dashboard")
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")


# ======================================================
# SIGNUP (CREATE ACCOUNT)
# ======================================================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template(
                "signup.html",
                error="All fields are required"
            )

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()
            conn.close()

            return redirect("/")

        except sqlite3.IntegrityError:
            return render_template(
                "signup.html",
                error="Username already exists"
            )

    return render_template("signup.html")


# ======================================================
# STUDENT DASHBOARD
# ======================================================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")


# ======================================================
# SSC DASHBOARD
# ======================================================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")


# ======================================================
# SSC CGL HOME
# ======================================================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")


# ======================================================
# SSC CGL FULL MOCK LIST
# ======================================================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")


# ======================================================
# SSC CGL MOCK INSTRUCTIONS
# ======================================================
@app.route("/ssc/cgl/mock/<int:mock_no>")
def ssc_cgl_mock(mock_no):
    if "name" not in session:
        return redirect("/")

    if mock_no < 1 or mock_no > 30:
        return "Invalid Mock Number", 404

    return render_template(
        "ssc_cgl_mock_1_instructions.html",
        mock_no=mock_no
    )


# ======================================================
# SSC CGL EXAM PAGE
# ======================================================
@app.route("/ssc/cgl/mock/<int:mock_no>/exam")
def ssc_cgl_exam(mock_no):
    if "name" not in session:
        return redirect("/")

    if mock_no < 1 or mock_no > 30:
        return "Invalid Mock Number", 404

    return render_template(
        "exam.html",
        mock_no=mock_no
    )


# ======================================================
# LOGOUT
# ======================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ======================================================
# RUN APP
# ======================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)