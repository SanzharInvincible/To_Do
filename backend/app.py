from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import ask_ai

app = Flask(__name__)
CORS(app)

tasks = []

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    tasks.append({
        "title": data["title"],
        "done": False
    })
    return jsonify(success=True)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]

    reply = ask_ai(message)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
