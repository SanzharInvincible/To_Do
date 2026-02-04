from flask import Flask, request, jsonify


app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
