from gtts import gTTS
import os
import requests
import base64


def generate_audio(text, filename):
    try:
        tts = gTTS(text=text, lang="en", tld="com", slow=False)
        temp_path = f"temp_{filename}.mp3"
        tts.save(temp_path)

        with open(temp_path, "rb") as f:
            audio_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": filename,
                "data": audio_data
            }
        }

        response = requests.post("http://localhost:8765", json=payload)
        os.remove(temp_path)

        return response.json().get("result", None)

    except Exception as e:
        print(f"Error generando audio: {e}")
        return None