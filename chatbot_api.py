from flask import Flask, request, jsonify, send_from_directory
from bot import Bot  # Import the Bot class (handles translation and voice input)
import os

app = Flask(__name__)
translator_bot = Bot()  # Create a single instance of the bot

@app.route('/')
def serve_index():
    # Serves the main chatbot HTML page when users visit the root URL
    return send_from_directory('.', 'index.html')

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    # Serves audio files from the audio_datasets folder
    audio_dir = os.path.join(os.path.dirname(__file__), 'audio_datasets')
    return send_from_directory(audio_dir, filename)

@app.route('/chat', methods=['POST'])
def chat():
    # Main API endpoint for chatbot interaction
    # Receives user message and mode (text or mic), returns translation and audio

    data = request.json
    if not data:
        # If no data is sent, return an error
        return jsonify({'response': "Invalid request.", 'recognized_text': None}), 400

    user_message = data.get('message')
    mode = data.get('mode', 'text')  # Default to 'text' mode if not provided

    recognized_text = None  # To store the recognized text for mic mode

    if mode == 'mic':
        # If mic mode, use speech recognition to get the user's spoken input
        user_message = translator_bot.voice_input()
        recognized_text = user_message
        if not user_message:
            # If nothing was recognized, inform the user
            return jsonify({'response': "Sorry, I couldn't understand your voice input.", 'recognized_text': None})

    if not user_message:
        # If no message is provided, prompt the user
        return jsonify({'response': "Please send a message.", 'recognized_text': recognized_text})

    # Translate the user's message and get the matched phrase
    translation_result, matched_phrase = translator_bot.translate(user_message)

    # Try to find an audio file for the matched phrase
    audio_url = None
    if matched_phrase:
        # Build candidate filenames: prefer space-separated (matches repo), fallback to underscores
        space_name = matched_phrase.strip().lower() + ".wav"
        underscore_name = matched_phrase.strip().lower().replace(" ", "_") + ".wav"
        candidate_filenames = [space_name]
        if underscore_name != space_name:
            candidate_filenames.append(underscore_name)

        # Search in all relevant folders
        for folder in ["Family_Members", "Greetings", "Animals", "Words"]:
            for filename in candidate_filenames:
                audio_path = os.path.join(os.path.dirname(__file__), "audio_datasets", folder, filename)
                print("Checking for audio file:", audio_path)  # Debug print for troubleshooting
                if os.path.exists(audio_path):
                    # If found, set the audio URL for the frontend to play
                    audio_url = f"/audio/{folder}/{filename}"
                    print("Audio found! URL:", audio_url)  # Debug print
                    break
            if audio_url:
                break

    # Return the translation, recognized text (if any), and audio URL (if found)
    return jsonify({'response': translation_result, 'recognized_text': recognized_text, 'audio_url': audio_url})

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)  # Disable debug mode in production