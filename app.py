from flask import Flask, request , jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        payload = {
            "model": "llama3:8b",
            "messages": [
                {'role':'system','content': "Kamu adalah asisten AI yang cerdas dan selalu membantu dalam Bahasa Indonesia."},
                {'role':'user','content': user_message}
            ],
            'stream':False
        }

        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        assistant_response = response.json()['message']['content']
        return jsonify({'reply': assistant_response})

    except requests.exceptions.RequestException as e:
        error_message = f"Error connecting to Ollama: {e}. Pastikan aplikasi ollama berjalan!"
        print(error_message)
        return jsonify({"error": error_message}), 503

    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return jsonify({"error": "An unexpected errorr occured"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
