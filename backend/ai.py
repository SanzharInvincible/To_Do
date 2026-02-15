import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
def ask_ai(message):
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1-mini",
            "input": message
        }
    )
    data = response.json()
    return data["output"][0]["content"][0]["text"]
