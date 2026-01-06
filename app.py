from flask import Flask, render_template, request, redirect, session
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# ================== SUPABASE CONFIG ==================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

# DEBUG (temporary – logs me dikhega)
print("SUPABASE_URL =", SUPABASE_URL)
print("SUPABASE_KEY =", SUPABASE_KEY)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase ENV vars missing")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================== ROUTES ==================

@app.route("/")
def home():
    return redirect("/login")


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        mobile = request.form.get("mobile")
        email = request.form.get("email")

        try:
            supabase.table("students").insert({
                "name": name,
                "username": username,
                "password": password,
                "mobile": mobile,
                "email": email
            }).execute()

            return redirect("/login")

        except Exception as e:
            return f"SIGNUP ERROR: {e}"

    return render_template("signup.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            res = supabase.table("students") \
                .select("*") \
                .eq("username", username) \
                .eq("password", password) \
                .execute()

            if res.data:
                session["user"] = username
                return redirect("/dashboard")
            else:
                return "Invalid username or password"

        except Exception as e:
            return f"LOGIN ERROR: {e}"

    return render_template("login.html")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return f"Welcome {session['user']} – Dashboard working"


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)