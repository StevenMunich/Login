import sqlite3
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create database and table
def init_db():
    conn = sqlite3.connect("../data.db")
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

@app.route("/" , methods=['GET'])
def hello():
        return render_template('crud.html')

# Store data (POST)
@app.route("/send", methods=["POST"])
def store_data():
    user_input = request.json.get("input", "")
    conn = sqlite3.connect("../data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (text) VALUES (?)", (user_input,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data stored successfully!"})

# Retrieve data (GET)
@app.route("/get", methods=["GET"])
def get_data():
    conn = sqlite3.connect("../data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM messages")
    messages = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({"messages": messages})

# Update data (PUT)
@app.route("/update/<int:id>", methods=["PUT"])
def update_data(id):
    new_text = request.json.get("text", "")
    conn = sqlite3.connect("../data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE messages SET text = ? WHERE id = ?", (new_text, id))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Updated entry ID {id}!"})

# Delete data (DELETE)
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = sqlite3.connect("../data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Deleted entry ID {id}!"})

if __name__ == "__main__":
    app.run(debug=True)