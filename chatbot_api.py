from flask import Flask, request, jsonify, send_from_directory
from bot import Bot
import os

app = Flask(__name__)
translator_bot = Bot()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    audio_dir = os.path.join(os.path.dirname(__file__), 'audio_datasets')
    return send_from_directory(audio_dir, filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid request'}), 400

    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'response': 'Please send a message.'})

    translation_result, matched_phrase = translator_bot.translate(user_message)
    
    # Try to find audio file
    audio_url = None
    if matched_phrase:
        space_name = matched_phrase.strip().lower() + ".wav"
        underscore_name = matched_phrase.strip().lower().replace(" ", "_") + ".wav"
        
        for folder in ["Family_Members", "Greetings", "Animals", "Words"]:
            for filename in [space_name, underscore_name]:
                audio_path = os.path.join(os.path.dirname(__file__), "audio_datasets", folder, filename)
                if os.path.exists(audio_path):
                    audio_url = f"/audio/{folder}/{filename}"
                    break
            if audio_url:
                break

    return jsonify({
        'response': translation_result,
        'audio_url': audio_url
    })

if __name__ == '__main__':
    app.run(debug=True)