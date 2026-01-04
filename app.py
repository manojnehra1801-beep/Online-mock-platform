from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "abhyas_secret_key"


# ===================== LOGIN =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # DEMO LOGIN
        if username == "abc" and password == "abc1":
            session["name"] = username
            return redirect("/dashboard")
        else:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")


# ===================== SIGN UP =====================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Future DB logic
        return redirect("/")
    return render_template("signup.html")


# ===================== STUDENT DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template(
        "student_dashboard.html",
        name=session["name"]
    )


# ===================== SSC DASHBOARD =====================
@app.route("/ssc")
def ssc_dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_dashboard.html")


# ===================== SSC → CGL =====================
@app.route("/ssc/cgl")
def ssc_cgl():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_tests.html")


# ===================== SSC → CGL → FULL MOCK LIST =====================
@app.route("/ssc/cgl/full-mocks")
def ssc_cgl_full_mocks():
    if "name" not in session:
        return redirect("/")
    return render_template("ssc_cgl_full_mocks.html")


# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===================== RUN APP =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)