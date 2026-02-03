print("🔥 THIS app.py IS RUNNING 🔥")
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash

# ================= APP CONFIG =================

app = Flask(__name__)
app.secret_key = "signsense_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

EMAIL_ADDRESS = "veduajipkate@gmail.com"     # ✅ correct email
EMAIL_PASSWORD = "clzvfpkbvlnrkexy"           # Gmail App Password

print("DB PATH USED BY FLASK:", DB_PATH)

# ================= DATABASE =================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()
def create_feedback_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            rating TEXT,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

create_feedback_table()

# ================= EMAIL =================

def send_reset_email(to_email):
    msg = EmailMessage()
    msg['Subject'] = 'SignSense – Password Assistance'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    msg.set_content("""
Hello,

We received a password assistance request for your SignSense account.

For security reasons, automatic password reset is disabled.
Please contact the administrator to reset your password.

Admin Email: veduajipkate@gmail.com

– SignSense Team
""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


# ================= ROUTES =================

@app.route("/")
def welcome():
    return render_template("welcome.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username = ? OR email = ?
        """, (username_or_email, username_or_email))

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return render_template("register.html",
                                   error="Username or email already exists")

    return render_template("register.html")

@app.route("/forgot", methods=["POST"])
def forgot_password():
    email = request.form["email"].strip().lower()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return redirect("/login?forgot_error=1")

    send_reset_email(email)
    return redirect("/login?forgot_success=1")



# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["username"])

# -------- LEARN --------
@app.route("/learn")
def learn():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("learn.html")

# -------- GAME --------
@app.route("/game")
def game():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("game.html")

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        rating = request.form['rating']
        comment = request.form['comment'].strip()

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO feedback (name, email, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (name, email, rating, comment))

        conn.commit()
        conn.close()

        return render_template(
            'feedback.html',
            message="✅ Thank you! Your feedback has been saved."
        )

    return render_template('feedback.html')


@app.route("/support")
def support():
    session.clear()
    return redirect("/support")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/test")
def test():
    return "TEST PAGE WORKING"

# ================= RUN =================
print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)
