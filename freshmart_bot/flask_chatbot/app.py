from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import openai
import json
import requests
from dotenv import load_dotenv
from summarize import generate_summary
from send_summary import send_email_summary

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
conversation_log = []

DJANGO_SAVE_URL = os.getenv("DJANGO_SAVE_URL")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Save user message
    conversation_log.append({"role": "user", "content": user_message})

    # Send to OpenAI GPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are FreshBot, a friendly chatbot for FreshMart. You help users with questions about fresh farm products like fruits, vegetables, dairy, delivery, and prices."}
            ] + conversation_log
        )
        bot_reply = response['choices'][0]['message']['content']
        conversation_log.append({"role": "assistant", "content": bot_reply})
        return jsonify({'reply': bot_reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/end-chat', methods=['POST'])
def end_chat():
    if not conversation_log:
        return jsonify({'error': 'No conversation to summarize'}), 400

    summary = generate_summary(conversation_log)

    # Send to Django
    try:
        res = requests.post(DJANGO_SAVE_URL, json={
            'conversation': json.dumps(conversation_log),
            'summary': summary
        })
        if res.status_code != 200:
            print("Error saving to Django:", res.text)
    except Exception as e:
        print("Failed to connect to Django:", e)

    # Send email to admin
    send_email_summary(summary, conversation_log)

    # Clear chat log after ending
    conversation_log.clear()

    return jsonify({'message': 'Summary sent and stored.', 'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
