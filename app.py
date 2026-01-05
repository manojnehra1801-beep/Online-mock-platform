from flask import Flask, render_template, request, redirect, session
import sqlite3
import traceback
import os

app = Flask(__name__)
app.secret_key = "debug_secret_key"

# ----------------------
# DATABASE (SQLite)
# ----------------------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Table create
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

# ----------------------
# LOGIN
# ----------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
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

        except Exception as e:
            traceback.print_exc()
            return f"LOGIN ERROR: {e}"

    return render_template("login.html")


# ----------------------
# SIGNUP
# ----------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            conn = get_db()
            conn.execute(
                "INSERT INTO students (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()

            return redirect("/")

        except Exception as e:
            traceback.print_exc()
            return f"SIGNUP ERROR: {e}"

    return render_template("signup.html")


# ----------------------
# DASHBOARD
# ----------------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")


# ----------------------
# RUN
# ----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)