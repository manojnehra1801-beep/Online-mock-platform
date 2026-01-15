from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================= DEMO USERS (TEMP STORAGE) =================
# NOTE: अभी DB नहीं है, इसलिए server restart पर reset होगा
USERS = {
    "abc": {
        "name": "Demo Student",
        "password": "abc1"
    }
}

# ================= LOGIN =================
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
            return render_template("login.html", error="Wrong username or password")

    return render_template("login.html")


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not name or not username or not password or not confirm:
            return render_template("signup.html", error="All fields are mandatory")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        if username in USERS:
            return render_template("signup.html", error="Username already exists")

        USERS[username] = {
            "name": name,
            "password": password
        }

        return render_template("signup.html", success="Signup successful! Please login.")

    return render_template("signup.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")


# ================= SSC DASHBOARD =================
@app.route("/ssc")
def ssc_dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")


# ================= SSC CGL =================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")


# ================= SSC CGL FULL MOCK LIST =================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")


# ================= MOCK 1 INSTRUCTIONS =================
@app.route("/ssc/cgl/mock/1")
def ssc_cgl_mock_1():
    if "username" not in session:
        return redirect("/")
    return render_template("ssc_cgl_mock_1_instructions.html")


# ================= PAYMENT PAGE =================
@app.route("/payment")
def payment():
    if "username" not in session:
        return redirect("/")
    return render_template("payment.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)