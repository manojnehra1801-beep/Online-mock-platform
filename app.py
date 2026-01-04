from flask import Flask, render_template, request, redirect, session, url_for

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
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# ===================== STUDENT DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("student_dashboard.html")


# ===================== SSC DASHBOARD =====================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("ssc_dashboard.html")


# ===================== SSC CGL MAIN =====================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("ssc_cgl_tests.html")


# ===================== SSC CGL FULL MOCK LIST =====================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("ssc_cgl_full_mocks.html")


# ===================== MOCK INSTRUCTIONS =====================
@app.route("/ssc/cgl/mock/<int:mock_no>")
def ssc_cgl_mock_instructions(mock_no):
    if "name" not in session:
        return redirect(url_for("login"))

    # अभी सिर्फ Mock-1 open
    if mock_no != 1:
        return redirect(url_for("ssc_cgl_full_mocks"))

    return render_template("ssc_cgl_mock_1_instructions.html", mock_no=mock_no)


# ===================== STEP-1: START EXAM ROUTE (FIX) =====================
@app.route("/ssc/cgl/mock/<int:mock_no>/start")
def start_exam(mock_no):
    if "name" not in session:
        return redirect(url_for("login"))

    # Exam page (same for now)
    return render_template("exam.html", mock_no=mock_no)


# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ===================== RUN APP =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)