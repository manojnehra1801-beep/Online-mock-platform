from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ===================== DEMO LOGIN =====================
DEMO_USERNAME = "abc"
DEMO_PASSWORD = "abc1"


# ===================== LOGIN =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["name"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")


# ===================== DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")


# ===================== SSC DASHBOARD =====================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")


# ===================== SSC CGL =====================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")


# ===================== SSC CGL FULL MOCK LIST =====================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")


# ===================== MOCK 1 INSTRUCTIONS =====================
@app.route("/ssc/cgl/mock/1")
def ssc_cgl_mock_1():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_mock_1_instructions.html")


# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===================== RUN =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)