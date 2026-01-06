from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ---------------- TEMP USER STORE ----------------
# Server restart पर reset होगा (demo phase)
USERS = {
    "abc": "abc1",
    "demo": "demo1"
}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        confirm  = request.form.get("confirm", "").strip()

        # Field validation
        if not username or not password or not confirm:
            return render_template(
                "signup.html",
                error="All fields are required"
            )

        if password != confirm:
            return render_template(
                "signup.html",
                error="Passwords do not match"
            )

        if username in USERS:
            return render_template(
                "signup.html",
                error="Username already exists"
            )

        # Store user (memory)
        USERS[username] = password

        return render_template(
            "signup.html",
            success="Successfully signed up! You can login now."
        )

    return render_template("signup.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template(
        "student_dashboard.html",
        user=session["user"]
    )

#----------------sscexam---------------
@app.route("/ssc-exam")
def ssc_exam():
    # login protection (optional but recommended)
    if "user" not in session:
        return redirect("/")
    return render_template("ssc_exam.html")


# ---------------- @app.route--------
def ssc_exam():
    # login protection (optional but recommended)
    if "user" not in session:
        return redirect("/")
    return render_template("ssc_exam.html") ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)