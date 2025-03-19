import requests
from html import escape
import os
import context
import speech
from urllib.parse import quote

import translation


def add_flashcard(word):
    try:
        # Obtener datos
        context_data = context.get_first_result_dict(word)
        example_sentence = context_data["en"]
        translated_text = context_data["es"]
        translated_word = translation.translate(word)

        # Definir nombres de archivo
        word_audio = f"{word}.mp3"
        example_audio = f"{word}_example.mp3"

        # Generar audios
        speech.generate_audio(word, word_audio)
        speech.generate_audio(example_sentence, example_audio)

        # Verificar archivos de audio
        if not (os.path.exists(word_audio) and os.path.exists(example_audio)):
            raise FileNotFoundError(f"Archivos de audio no encontrados: {word_audio}, {example_audio}")

        # Codificar nombres de archivo
        encoded_word = quote(word)
        encoded_example = quote(example_audio)

        # Leer el contenido del archivo style.css y guardarlo en una variable
        with open("style.css", "r", encoding="utf-8") as archivo_css:
            CSS = archivo_css.read()

        # Construir HTML
        front_html = f'''
         <style>
            {CSS}
        </style>
        <sytle>
        </style>
         <div class="flashcard">
        <div class="content">
            <p class="word">{escape(word)}</p>
            <div class="audio-container">
            </div>
        </div>
        <div>
        '''

        back_html = f'''
        <style>
            {CSS}
        </style>
        <div>
            <div class="content">
                <p class="translated-word">{translated_word}</p>
                <p class="sentence-text">{escape(example_sentence)}</p>
                <button class="hint" onclick="this.nextElementSibling.style.display='block';this.style.display='none'">
                    Mostrar traducción
                </button>
                <p class="translation-text" style="display: none;">{escape(translated_text)}</p>
            <div class="audio-container">
        </div>
        </div>
    </div>
        '''

        # Crear nota en Anki
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": "Default",
                    "modelName": "Basic",
                    "fields": {
                        "Front": front_html,
                        "Back": back_html
                    },
                    "tags": ["auto-generated"],
                    "audio": [
                        {
                            "filename": word_audio,
                            "path": os.path.abspath(word_audio),
                            "fields": ["Front"]
                        },
                        {
                            "filename": example_audio,
                            "path": os.path.abspath(example_audio),
                            "fields": ["Back"]
                        }
                    ]
                }
            }
        }

        response = requests.post("http://localhost:8765", json=payload, timeout=10)
        return response.json()

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    add_flashcard(input("Introduce una palabra: "))
