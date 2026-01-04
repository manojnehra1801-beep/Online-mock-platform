from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "abhyas_app_secret_key_2026"

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Demo login (no validation yet)
        username = request.form.get("username")

        if username:
            session["name"] = username
            return redirect("/dashboard")

    return render_template("login.html")


# ================= SIGN UP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Abhi signup ke baad direct login page
        return redirect("/")

    return render_template("signup.html")


# ================= STUDENT DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    # Agar user login nahi hai to login page par bhej do
    if "name" not in session:
        return redirect("/")

    return render_template("student_dashboard.html")


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)