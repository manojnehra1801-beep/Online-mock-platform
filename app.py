from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_demo_secret_key"

# ======================
# TEMP USER STORE (MEMORY)
# ======================
# NOTE: Server restart → data reset (demo phase)
USERS = {
    "abc": "abc1"   # demo user
}

# ======================
# LOGIN
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ======================
# SIGNUP
# ======================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # DEBUG SAFETY (temporary)
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

        # demo in-memory store
        USERS[username] = password

        return render_template(
            "signup.html",
            success="Account created successfully. Login now."
        )

    return render_template("signup.html")


# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("student_dashboard.html", user=session["user"])


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