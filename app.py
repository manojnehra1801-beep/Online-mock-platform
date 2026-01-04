from flask import Flask, render_template, request, redirect, session, abort

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_2026"

# ===================== DEMO USERS =====================
DEMO_USERS = {
    "abc": "abc1"
}

# ===================== HOME / LOGIN =====================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in DEMO_USERS and DEMO_USERS[username] == password:
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
        # Abhi demo signup — baad me database
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

@app.route("/ssc/cgl")
def ssc_cgl():
    return render_template("ssc_cgl.html")


# ===================== RAILWAY DASHBOARD =====================
@app.route("/railway")
def railway_dashboard():
    if "name" not in session:
        return redirect("/")
    return render_template("railway_dashboard.html")


# ===================== EXAM PAGE =====================
@app.route("/exam")
def exam():
    if "name" not in session:
        return redirect("/")
    return render_template("exam.html")


# ===================== RESULT PAGE =====================
@app.route("/result")
def result():
    if "name" not in session:
        return redirect("/")
    return render_template("result.html")


# ===================== ADMIN LOGIN =====================
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if (
            request.form.get("username") == "Manojnehra"
            and request.form.get("password") == "NEHRA@2233"
        ):
            session["admin"] = True
            return redirect("/admin/dashboard")
        else:
            return render_template(
                "admin_login.html",
                error="Invalid admin credentials"
            )

    return render_template("admin_login.html")


# ===================== ADMIN DASHBOARD =====================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_dashboard.html")


# ===================== ADMIN STUDENTS =====================
@app.route("/admin/students")
def admin_students():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin_students.html")


# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===================== RUN APP =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)