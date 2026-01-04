from flask import Flask, render_template, request, redirect, session
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ===================== DATABASE =====================
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )

# ===================== CREATE TABLE (AUTO) =====================
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# ===================== LOGIN =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM students WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["name"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# ===================== SIGNUP =====================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO students (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()
        except Exception:
            conn.rollback()
            cur.close()
            conn.close()
            return render_template("signup.html", error="Username already exists")

        cur.close()
        conn.close()
        return redirect("/")

    return render_template("signup.html")

# ===================== STUDENT DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")

# ===================== SSC DASHBOARD =====================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")

# ===================== SSC CGL =====================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")

# ===================== SSC CGL FULL MOCK LIST =====================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")

# ===================== MOCK INSTRUCTIONS (1–30) =====================
@app.route("/ssc/cgl/mock/<int:mock_no>")
def ssc_cgl_mock(mock_no):
    if "name" not in session:
        return redirect("/")

    # अभी सभी mocks के लिए same instruction page
    # ताकि TemplateNotFound error न आए
    return render_template("ssc_cgl_mock_1_instructions.html", mock_no=mock_no)

# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ===================== RUN =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)