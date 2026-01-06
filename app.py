from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# The secret key is required for 'flash' messages (pop-up alerts)
app.secret_key = 'abhyas_secret_key_123'

# This is a 'Mock' database. In a real app, you'd use a database like PostgreSQL.
# Format: "Username": "Password"
STUDENT_DB = {
    "admin": "password123",
    "student01": "studyhard",
    "nehratech": "abhyas2026"
}

@app.route('/')
def login_page():
    # This renders your HTML file from the /templates folder
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Getting the data from the HTML form 'name' attributes
    username = request.form.get('username')
    password = request.form.get('password')

    # Logic to check if user exists and password matches
    if username in STUDENT_DB and STUDENT_DB[username] == password:
        # If successful, redirect to a dashboard (you can create this next)
        return f"<h2>Welcome to Abhyas App, {username}!</h2><p>Login Successful.</p>"
    else:
        # If it fails, send an error message and go back to login
        flash("Invalid Username or Password. Please try again.")
        return redirect(url_for('login_page'))

if __name__ == '__main__':
    # Run the app locally for testing
    app.run(debug=True)
