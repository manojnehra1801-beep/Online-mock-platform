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


# ===================== SIGN UP =====================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # abhi sirf demo ke liye, store baad me
        return redirect(url_for("login"))

    return render_template("signup.html")


# ===================== DASHBOARD =====================
@app.route("/dashboard")
def dashboard():
    if "name" not in session:
        return redirect(url_for("login"))
    return "Dashboard OK (already working)"


# ===================== LOGOUT =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ===================== RUN =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)