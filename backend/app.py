from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os
import threading
import webview

load_dotenv()

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ai", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"reply": "Напиши вопрос"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты умный и краткий AI ассистент."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"reply": answer})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Ошибка сервера"}), 500
def start_flask():
    app.run(port=5001)
if __name__ == "__main__":
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()
    webview.create_window(
        "To_Do app",
        "http://localhost:5001",
        width=375,
        height=700
    )

    webview.start()
