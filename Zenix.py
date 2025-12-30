from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import io
import re
from gtts import gTTS
import base64
import os
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
CORS(app)
genai.configure(api_key="AIzaSyAbE3MDl4rj0PVC0LRcNoF18owF2_5-dWg")

from gtts import gTTS
import io
from pydub import AudioSegment

def speak(text, speed_factor=1.3):
    #speed_factor=1.0 is normal. 1.3 is roughly 174 WPM.

    try:
        # 1. Generate standard TTS
        tts = gTTS(text=text, lang='en')

        # 2. Write to in-memory file
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)

        # 3. If speed is 1.0, return immediately (saves processing)
        if speed_factor == 1.0:
            return audio_fp.read()

        # 4. Load into pydub to change speed
        sound = AudioSegment.from_file(audio_fp, format="mp3")

        # speedup() handles pitch correction so you don't sound like a chipmunk
        # Note: chunk_size and crossfade parameters help prevent clicking artifacts
        faster_sound = sound.speedup(playback_speed=speed_factor, chunk_size=150, crossfade=25)

        # 5. Export back to bytes
        processed_fp = io.BytesIO()
        faster_sound.export(processed_fp, format="mp3")
        processed_fp.seek(0)

        return processed_fp.read()

    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None

def get_response_from_gemini(text):

    models = ["gemini-pro", "gemini-2.5-flash"]
    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = (
                'Your answer should no longer than 2 lines.'
                'You are Zenix, a personal helpful assistant.'
                'You can understand many languages but reply only in English.'
                'You will not tell user that you can understand many languages and only answer in english unless he asks specially'
                'you can open and search websites for the user.'
                'You can provide information and help with various tasks.'
                'You are trained by Syed Masahir Abbas'
                'Be concise and clear in your responses.\n'
                f"User: {text}"
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            continue
    return "Sorry, I'm having trouble connecting to the AI service right now."
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400

        user_message = data['message']

        # Check if the user wants to open a website
        open_website_match = re.search(r'(?:open|kholo)\s*(\S+)|(\S+)\s*(?:open|kholo)', user_message.lower())
        search_google_match = re.search(r'(?:search|search kro)\s*(\S+)|(\S+)\s*(?:search|search kro)', user_message.lower())

        if open_website_match:
            website_name = (open_website_match.group(1) or open_website_match.group(2)).strip()
            if '.' not in website_name:
                website_name += '.com'
            if not website_name.startswith(('http://', 'https://')):
                website_url = f'https://{website_name}'
            else:
                website_url = website_name

            response_text = f'Opening {website_name}'
            return jsonify({
                'response': response_text,
                'action': 'open_url',
                'url': website_url
            })

        elif search_google_match:
            query = search_google_match.group(1).strip()
            search_url = f'https://www.google.com/search?q={query}'
            response_text = f'Searching for "{query}" on Google...'
            return jsonify({
                'response': response_text,
                'action': 'open_url',
                'url': search_url
            })

        else:
            # Get AI response for general queries
            ai_response = get_response_from_gemini(user_message)
            audio_data = speak(ai_response)

            if audio_data:
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                return jsonify({'response': ai_response, 'audio': audio_base64})
            else:
                return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    # Check if the API is working
    return jsonify({
        'status': 'online',
        'message': 'Zenix AI Assistant is ready to help!'
    })

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """Handle feedback submission"""
    try:
        data = request.get_json()
        if not data or 'feedback' not in data:
            return jsonify({'error': 'No feedback provided'}), 400

        feedback_text = data['feedback']

        # Send emails for Feedback
        sender_email = "masahirshah@gmail.com"
        receiver_email = "cfile7552@gmail.com"
        password = "lqnv fdun escp zbac"

        message = MIMEText(f"New feedback from a user:\n\n{feedback_text}")
        message["Subject"] = "New Feedback for Zenix AI"
        message["From"] = sender_email
        message["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return jsonify({'message': 'Feedback submitted successfully'}), 200

    except Exception as e:
        print(f"Error sending feedback: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
    
