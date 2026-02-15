from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import threading
import webview
from flask_cors import CORS
from ai import ask_ai

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
CORS(app)

tasks = []

@app.route("/")
def index():
    return render_template("interface.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify(success=False, error="Missing 'title'"), 400
    tasks.append({
        "title": data["title"],
        "done": False
    })
    return jsonify(success=True), 201

@app.route("/update-task/<int:index>", methods=["PUT"])
def update_task(index):
    if index < 0 or index >= len(tasks):
        return jsonify(success=False, error="Task not found"), 404
    data = request.get_json(silent=True)
    if "done" in data:
        tasks[index]["done"] = data["done"]
    return jsonify(success=True), 200

@app.route("/stats", methods=["GET"])
def get_stats():
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["done"])
    return jsonify({
        "total": total_tasks,
        "completed": completed_tasks,
        "remaining": total_tasks - completed_tasks
    }), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]

    reply = ask_ai(message)

    return jsonify({"reply": reply})


def start_flask():
    app.run(debug=False, use_reloader=False)


if __name__ == "__main__":
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()
    webview.create_window("To_Do app", "http://Localhost:5000", width=375, height=700)
    webview.start()
