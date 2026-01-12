from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ---------------- DEMO USER STORE ----------------
users = {
    "abc": {
        "name": "Demo Student",
        "password": "abc1"
    }
}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            session["username"] = username
            session["name"] = users[username]["name"]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not name or not username or not password or not confirm:
            return render_template("signup.html", error="All fields are required")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        if username in users:
            return render_template("signup.html", error="Username already exists")

        users[username] = {
            "name": name,
            "password": password
        }

        return render_template(
            "signup.html",
            success="Account created successfully! You can login now."
        )

    return render_template("signup.html")


# ---------------- STUDENT DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template(
        "student_dashboard.html",
        name=session.get("name")
    )


# ---------------- SSC DASHBOARD ----------------
@app.route("/ssc")
def ssc_dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")


# ---------------- SSC CGL PAPERS LIST ----------------
@app.route("/ssc/cgl")
def ssc_cgl_list():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_list.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)