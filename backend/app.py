from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import threading
import webview

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

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
def start_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()
    webview.create_window("To_Do app", "http://Localhost:5000", width=375, height=700)
    webview.start()


