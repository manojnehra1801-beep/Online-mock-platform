import os
from flask import Flask, render_template, request, redirect, session
import psycopg

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_change_later"

# ======================
# DATABASE CONNECTION
# ======================
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg.connect(DATABASE_URL)


# ======================
# LOGIN
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="All fields required")

        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT id FROM students WHERE username=%s AND password=%s",
                        (username, password)
                    )
                    user = cur.fetchone()

            if user:
                session["student_id"] = user[0]
                session["username"] = username
                return redirect("/dashboard")
            else:
                return render_template(
                    "login.html",
                    error="Invalid username or password"
                )

        except Exception as e:
            print("LOGIN ERROR:", e)
            return render_template(
                "login.html",
                error="Server error, try again"
            )

    return render_template("login.html")


# ======================
# SIGNUP
# ======================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template(
                "signup.html",
                error="All fields required"
            )

        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO students (username, password) VALUES (%s, %s)",
                        (username, password)
                    )

            return redirect("/")

        except psycopg.errors.UniqueViolation:
            return render_template(
                "signup.html",
                error="Username already exists"
            )

        except Exception as e:
            print("SIGNUP ERROR:", e)
            return render_template(
                "signup.html",
                error="Server error, try again"
            )

    return render_template("signup.html")


# ======================
# STUDENT DASHBOARD
# ======================
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")


# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)