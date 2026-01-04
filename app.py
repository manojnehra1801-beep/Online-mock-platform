from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ===================== DATABASE CONNECTION =====================
def get_db_connection():
    return psycopg2.connect(
        os.environ.get("DATABASE_URL"),
        sslmode="require"
    )

# ===================== LOGIN =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM students WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session["student_id"] = user[0]
            session["username"] = username
            return redirect("/dashboard")
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

# ===================== SIGNUP =====================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        # ✅ check only username
        cur.execute(
            "SELECT id FROM students WHERE username=%s",
            (username,)
        )
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            conn.close()
            return render_template(
                "signup.html",
                error="Username already exists"
            )

        # ✅ insert new user
        cur.execute(
            "INSERT INTO students (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()

        cur.close()
        conn.close()

        return redirect("/")

    return render_template("signup.html")

# ===================== DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/")
    return render_template(
        "student_dashboard.html",
        username=session["username"]
    )

# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ===================== RUN =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)