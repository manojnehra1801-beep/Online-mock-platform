from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_app_secret_key_2026"

# ================= TEST LOGIN CREDENTIAL =================
TEST_USERNAME = "abc"
TEST_PASSWORD = "abc1"

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == TEST_USERNAME and password == TEST_PASSWORD:
            session["name"] = username
            return redirect("/dashboard")
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")


# ================= SIGN UP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # demo signup – baad me database aayega
        return redirect("/")

    return render_template("signup.html")


# ================= STUDENT DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")

    return render_template("student_dashboard.html")


# ================= SSC EXAMS FOLDER =================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")

    return render_template("ssc_dashboard.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)