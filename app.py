from flask import Flask, render_template, request, redirect, session
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key"

# ================= SUPABASE CONFIG =================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        res = supabase.table("students") \
            .select("*") \
            .eq("username", username) \
            .eq("password", password) \
            .execute()

        if res.data:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        mobile = request.form.get("mobile")

        # Check username exists
        check = supabase.table("students") \
            .select("id") \
            .eq("username", username) \
            .execute()

        if check.data:
            return render_template("signup.html", error="Username already exists")

        supabase.table("students").insert({
            "name": name,
            "username": username,
            "password": password,
            "email": email,
            "mobile": mobile
        }).execute()

        return render_template("login.html", success="Account created successfully. Login now.")

    return render_template("signup.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("student_dashboard.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)