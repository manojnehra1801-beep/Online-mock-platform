from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_app_secret_key"

# ---------------- DEMO USER ----------------
DEMO_USERNAME = "abc"
DEMO_PASSWORD = "abc1"

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
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
        # future me database add hoga
        return redirect("/")

    return render_template("signup.html")


# ================= STUDENT DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")

    return render_template(
        "student_dashboard.html",
        username=session["name"]
    )


# ================= SSC FOLDER =================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")

    return render_template("ssc_dashboard.html")


# ================= SSC CGL TESTS =================
@app.route("/ssc/cgl/tests")
def ssc_cgl_tests():
    if "name" not in session:
        return redirect("/")

    return render_template("ssc_cgl_tests.html")


# ================= RAILWAY FOLDER =================
@app.route("/railway")
def railway_dashboard():
    if "name" not in session:
        return redirect("/")

    return render_template("railway_dashboard.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)