import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Create database and table
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# Route to store data (POST request)
@app.route("/send", methods=["POST"])
def store_data():
    user_input = request.json.get("input", "")

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (text) VALUES (?)", (user_input,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data stored successfully!"})


# Route to retrieve all stored data (GET request)
@app.route("/get", methods=["GET"])
def get_data():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM messages")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()

    return jsonify({"messages": messages})


if __name__ == "__main__":
    app.run(debug=True)