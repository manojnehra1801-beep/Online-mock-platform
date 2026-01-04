from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "abhyas_secret_key_123"

# =========================
# INSTRUCTIONS PAGE
# =========================
@app.route("/")
def instructions():
    return render_template("instructions.html")


# =========================
# EXAM PAGE
# =========================
@app.route("/exam")
def exam():
    return render_template("exam.html")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)