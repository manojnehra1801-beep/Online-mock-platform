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


# ===================== SSC CGL FULL MOCK LIST (1–30) =====================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect(url_for("login"))
    return render_template("ssc_cgl_full_mocks.html")


# ===================== SSC CGL MOCK INSTRUCTIONS (DYNAMIC) =====================
@app.route("/ssc/cgl/mock/<int:mock_no>")
def ssc_cgl_mock_instructions(mock_no):
    if "name" not in session:
        return redirect(url_for("login"))

    # अभी सिर्फ Mock-1 open है
    if mock_no != 1:
        return redirect(url_for("ssc_cgl_full_mocks"))

    # ✅ EXACT file name (जो तुम्हारे templates में है)
    return render_template("ssc_cgl_mock_1_instructions.html")


# ===================== START EXAM (AFTER AGREE) =====================
@app.route("/ssc/cgl/mock/1/start")
def start_mock