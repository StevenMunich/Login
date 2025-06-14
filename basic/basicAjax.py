from flask import Flask, jsonify, request
from flask_cors import CORS  # Allows frontend requests

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify({"message": "Hello from Flask!", "status": "success"})

@app.route("/send", methods=["POST"])
def receive_data():
    user_data = request.json.get("input", "")
    return jsonify({"response": f"Received: {user_data}"})

if __name__ == "__main__":
    app.run(debug=True)