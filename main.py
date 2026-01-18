from flask import Flask, request, jsonify
from brain import generate_response  # hakikisha hii function ipo kwenye brain.py
import os

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    answer = generate_response(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway hutuma port kupitia env
    app.run(host='0.0.0.0', port=port)
