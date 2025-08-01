import sqlite3
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import re

def validate_input(input_str: str, max_length: int = 50) -> str:
    # Remove leading/trailing whitespace
    input_str = input_str.strip()
    # Check for empty string
    if not input_str:
        raise ValueError("Input cannot be empty.")
    # Check length
    if len(input_str) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}.")
    # Optional: Only allow alphanumeric and underscores
    if not re.match(r"^\w+$", input_str):
        raise ValueError("Input contains invalid characters.")
    return input_str

app = Flask(__name__)
CORS(app)

app.secret_key = "your_secret_key"  # Set a secret key for session management

# Create database and table
def init_db():
    conn = sqlite3.connect("../data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized")

init_db()

#home page
@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)


@app.route("/about", methods=['GET'])

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        validate_input(username)
        validate_input(password)
        hashed_password = generate_password_hash(password)
        try:
            with sqlite3.connect("../data.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
            return jsonify({"message": "Sign up successfully!"})
        except sqlite3.IntegrityError:
            print("Signup failed: Username already exists")
            return jsonify({"message": "Signup failed: Username already exists!"})
        except Exception as e:
            print(f"Signup failed: {e} for username {username}")
            return jsonify({"message": "Signup failed. Error occurred!"})
    return render_template("signup.html")


@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST": #Submission of form
        username = request.form["username"]
        password = request.form["password"]
        validate_input(username)
        validate_input(password)
        try: # Check if the username and password are correct
            with sqlite3.connect("../data.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM accounts WHERE username = ?", (username,)) #get matching username
                row = cursor.fetchone() #stores row in variable row
                if row and check_password_hash(row[0], password): #check if row exists and password matches
                    cursor.execute("DELETE FROM accounts WHERE username = ?", (username,))
                    conn.commit() #This will delete the account
                    return jsonify({"message": "Account deleted successfully!"})
                else:
                    return jsonify({"message": "Invalid username or password!"})
        except Exception as e:
            print(f"Delete failed: {e}")
            print(f"Traceback: {e.with_traceback()}")
            print(f"-------------------------------------------------------")
            print(f"CAUSE: {e.__cause__}")
            return jsonify({"message": "Error occurred while deleting account!"})
    return render_template("delete_account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        validate_input(username)
        validate_input(password)
        try:
            with sqlite3.connect("../data.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM accounts WHERE username = ?", (username,))
                row = cursor.fetchone()
                if row and check_password_hash(row[0], password):
                    #return jsonify({"message": "Login successful!"})
                    session['username'] = username
                    return jsonify({"redirect": url_for('index')})
                else:
                    return jsonify({"message": "Invalid username or password!"})
        except Exception as e:
            print(f"Login failed: {e}")
            return jsonify({"message": "Error occurred during login!"})
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():
    # Implement profile update logic here
    return render_template("update_profile.html")

# Retrieve data (GET)
@app.route("/get", methods=["GET"])
def get_data():
    conn = sqlite3.connect("../data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM messages")
    messages = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({"accounts": messages})

if __name__ == "__main__":

    app.run(debug=False)

    #TO HOST LIVE ON NETWORK UNCOMMENT AND READ INSTRUCTIONS BELOW
    #app.run(host='0.0.0.0', port=5000, debug=False)
    # set to 0.0.0.0 for all network interfaces

'''
- You’ll need to use your actual IP address (e.g., 192.168.x.x) in the browser, not 0.0.0.0.
- Ensure your firewall allows traffic on port (or whatever you change it to).
- If you're on a VPN, it may block local access—try disconnecting temporarily.
- Avoid using the Flask dev server in production; it's not secure or performant.

For deployment use Gunicorn or reverse proxy with Nginx


non-issues
CSS can change the Font and Position with phone app. @media rules for landscape and portrait orientation.


Learn: App.py is the backend. templates contains front-end pages that use asynchronous calls.

'''








