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


# ===================== MOCK INSTRUCTIONS (1–30) =====================
@app.route("/ssc/cgl/mock/<int:mock_no>")
def ssc_cgl_mock(mock_no):
    if "name" not in session:
        return redirect("/")

    # only mock 1 is open now
    if mock_no == 1:
        return render_template("ssc_cgl_mock_1_instructions.html")

    return "<h2 style='text-align:center;margin-top:50px;'>🔒 This mock is locked. Please unlock to continue.</h2>"


# ===================== MOCK 1 EXAM =====================
@app.route("/ssc/cgl/exam/1", methods=["GET", "POST"])
def ssc_cgl_exam_1():
    if "name" not in session:
        return redirect("/")

    questions = [
        {
            "q": "What is the capital of India?",
            "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"]
        },
        {
            "q": "Who wrote the Indian National Anthem?",
            "options": [
                "Bankim Chandra Chattopadhyay",
                "Rabindranath Tagore",
                "Jawaharlal Nehru",
                "Mahatma Gandhi"
            ]
        },
        {
            "q": "2 + 2 × 2 = ?",
            "options": ["6", "8", "4", "10"]
        }
    ]

    if request.method == "POST":
        return redirect("/thank-you")

    return render_template("ssc_cgl_exam_1.html", questions=questions)


# ===================== THANK YOU =====================
@app.route("/thank-you")
def thank_you():
    return """
    <h2 style='text-align:center;margin-top:60px;'>
        Thank you for attempting the test
    </h2>
    """


# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===================== RUN =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)