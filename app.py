from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "testkey"

def get_db():
    return sqlite3.connect("database.db")

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
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Wrong username or password")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        mobile = request.form.get("mobile")
        email = request.form.get("email")

        if not name or not username or not password or not confirm:
            return render_template("signup.html", error="All fields are mandatory")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    username TEXT UNIQUE,
                    password TEXT,
                    mobile TEXT,
                    email TEXT
                )
            """)
            cur.execute(
                "INSERT INTO students (name, username, password, mobile, email) VALUES (?,?,?,?,?)",
                (name, username, password, mobile, email)
            )
            conn.commit()
            conn.close()

            return render_template("signup.html", success="Signup successful!")

        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username already exists")

    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return "Dashboard opened successfully"

if __name__ == "__main__":
    app.run(debug=True)