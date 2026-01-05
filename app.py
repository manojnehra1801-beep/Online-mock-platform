from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

DB_NAME = "users.db"

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            username TEXT UNIQUE,
            password TEXT,
            mobile TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= LOGIN (LOCKED) =================
@app.route("/", methods=["GET", "POST"])
def login():
    # already logged in → dashboard
    if "username" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM students WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        student_name = request.form.get("student_name")
        username = request.form.get("username")
        password = request.form.get("password")
        mobile = request.form.get("mobile")
        email = request.form.get("email")

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO students
                (student_name, username, password, mobile, email)
                VALUES (?, ?, ?, ?, ?)
                """,
                (student_name, username, password, mobile, email)
            )
            conn.commit()
            conn.close()

            # popup trigger
            return redirect("/signup?success=1")

        except sqlite3.IntegrityError:
            return render_template(
                "signup.html",
                error="Account could not be created. Please try again."
            )
        except Exception as e:
            return f"SIGNUP ERROR: {e}"

    return render_template("signup.html")

# ================= DASHBOARD (PROTECTED) =================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")   # 🔒 login required
    return render_template(
        "student_dashboard.html",
        username=session["username"]
    )

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)