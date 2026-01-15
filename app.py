from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_safe"

# ---------------- TEMP USER STORE ----------------
USERS = {
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

        if username in USERS and USERS[username]["password"] == password:
            session["username"] = username
            session["name"] = USERS[username]["name"]
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

        if username in USERS:
            return render_template("signup.html", error="Username already exists")

        USERS[username] = {
            "name": name,
            "password": password
        }

        return render_template(
            "signup.html",
            success="Signup successful! You can login now."
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

# ---------------- CGL TEST LIST ----------------
@app.route("/ssc/cgl")
def ssc_cgl_tests():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")

# ---------------- MOCK 1 INSTRUCTIONS ----------------
@app.route("/ssc/cgl/mock/1")
def mock_1_instructions():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_mock_1_instructions.html")

# ---------------- MOCK 1 START (PLACEHOLDER) ----------------
@app.route("/ssc/cgl/mock/1/start")
def mock_1_start():
    if "username" not in session:
        return redirect("/")
    return "Mock Test 1 Exam Page (Coming Next)"

# ---------------- PAYMENT PAGE ----------------
@app.route("/payment")
def payment_page():
    if "username" not in session:
        return redirect("/")
    return render_template("payment.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)