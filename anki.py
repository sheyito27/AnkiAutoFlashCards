import requests
from html import escape
import context
import speech


def add_flashcard(word):
    try:
        # Obtener datos
        context_data = context.get_first_result_dict(word)
        example_sentence = context_data["en"]
        translation = context_data["es"]

        # Generar audios
        speech.generate_audio(word, f"{word}.mp3")  # Audio de la palabra
        speech.generate_audio(example_sentence, f"{word}_example.mp3")  # Audio del ejemplo

        # Construir HTML
        front_html = f'''
        <div style="text-align: center;">
            <h1>{escape(word)}</h1>
            <audio controls>
                <source src="{word}.mp3" type="audio/mpeg">
            </audio>
        </div>
        '''

        back_html = f'''
        <div style="text-align: center;">
            <div class="example">
                <p>{escape(example_sentence)}</p>
                <audio controls style="margin: 10px 0;">
                    <source src="{word}_example.mp3" type="audio/mpeg">
                </audio>
                <button onclick="this.nextElementSibling.style.display='block';this.style.display='none'">
                    Mostrar traducción
                </button>
                <p style="display: none; color: #666;">{escape(translation)}</p>
            </div>
        </div>
        '''

        # Crear nota en Anki (CORRECCIÓN CLAVE AQUÍ)
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
                    "audio": [  # Lista de diccionarios CORRECTAMENTE formateada
                        {
                            "filename": f"{word}.mp3",
                            "fields": ["Front"]
                        },
                        {
                            "filename": f"{word}_example.mp3",
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
    add_flashcard("heart")