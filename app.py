import os
import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================= DATABASE =================
DB_NAME = "users.db"

def get_db():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=10,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn

# Create table once
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
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
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return "LOGIN ERROR: Invalid username or password"

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
                "INSERT INTO students (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect("/")

        except sqlite3.IntegrityError:
            return "Username already exists. Try another one."

        except Exception as e:
            return f"SIGNUP ERROR: {e}"

    return render_template("signup.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
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