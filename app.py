from flask import Flask, render_template, request, redirect, session, url_for
from supabase import create_client
import os

# ================= FLASK CONFIG =================
app = Flask(__name__)
app.secret_key = "abhyas_secret_key_change_later"

# ================= SUPABASE CONFIG =================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase ENV vars missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            res = (
                supabase
                .table("students")
                .select("*")
                .eq("username", username)
                .eq("password", password)
                .execute()
            )

            if res.data:
                session["user"] = username
                return redirect("/dashboard")
            else:
                return render_template(
                    "login.html",
                    error="Invalid username or password"
                )

        except Exception as e:
            return f"LOGIN ERROR: {e}"

    return render_template("login.html")


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        email = request.form.get("email")
        mobile = request.form.get("mobile")

        if password != confirm:
            return render_template(
                "signup.html",
                error="Passwords do not match"
            )

        try:
            # username already exists check
            check = (
                supabase
                .table("students")
                .select("id")
                .eq("username", username)
                .execute()
            )

            if check.data:
                return render_template(
                    "signup.html",
                    error="Username already exists"
                )

            # insert new student
            supabase.table("students").insert({
                "name": name,
                "username": username,
                "password": password,
                "email": email,
                "mobile": mobile
            }).execute()

            return render_template(
                "signup.html",
                success=True
            )

        except Exception as e:
            return f"SIGNUP ERROR: {e}"

    return render_template("signup.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html", user=session["user"])


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)