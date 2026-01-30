from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

tasks = []

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

# новый маршрут для фронтенда
@app.route("/")
def serve_frontend():
    print("Frontend запрошен!")  # добавили лог
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
    return send_from_directory(frontend_dir, "Interface.html")

@app.route("/<path:path>")
def serve_static(path):
    # Serve files from the frontend folder using an absolute path
    frontend_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
    print(f"Static file requested: {path} -> {frontend_dir}")
    return send_from_directory(frontend_dir, path)

if __name__ == "__main__":
    app.run(debug=True)


