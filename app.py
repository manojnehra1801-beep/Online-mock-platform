from flask import Flask, render_template, request, redirect, session, url_for
import os
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
app.secret_key = "abhyas_super_secret_key"

# ================================
# DATABASE (Supabase)
# ================================
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


# ================================
# LOGIN
# ================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM students WHERE username=%s AND password=%s",
                    (username, password)
                )
                user = cur.fetchone()

        if user:
            session["student_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ================================
# SIGNUP
# ================================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with get_db() as conn:
            with conn.cursor() as cur:
                # check existing user
                cur.execute(
                    "SELECT id FROM students WHERE username=%s",
                    (username,)
                )
                existing = cur.fetchone()

                if existing:
                    return render_template(
                        "signup.html",
                        error="Username already exists"
                    )

                # insert new student
                cur.execute(
                    "INSERT INTO students (username, password) VALUES (%s, %s)",
                    (username, password)
                )

        return redirect("/")

    return render_template("signup.html")


# ================================
# DASHBOARD
# ================================
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")


# ================================
# LOGOUT
# ================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================================
# HEALTH CHECK (OPTIONAL)
# ================================
@app.route("/health")
def health():
    return "OK"


# ================================
# RUN
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)