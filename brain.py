from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import json

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

HISTORY_FILE = "chat_history.json"

PERSONALITY_PROMPT = {
    "role": "system",
    "content": (
        "You are Ado, a friendly teacher and best friend assistant. "
        "You explain things simply, step by step, like teaching a beginner. "
        "You are supportive, motivating, and speak in a warm, friendly tone. "
        "You help the user learn programming and technology without judging. "
        "You act like a smart best friend who enjoys teaching."
    )
}

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        chat_history = json.load(f)
else:
    chat_history = [PERSONALITY_PROMPT]

@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"answer": "No question provided."})

    chat_history.append({"role": "user", "content": question})

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[PERSONALITY_PROMPT] + chat_history
        )
        answer = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})
    except Exception as e:
        answer = f"Error: {str(e)}"

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

    return jsonify({"answer": answer})

@app.route('/')
def index():
    return open('index.html').read()

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
