import requests
import context
import definition
import speech
import translation
import os

def add_flashcard(word):
    try:
        # Verificar si la nota ya existe en Anki
        find_note_payload = {
            "action": "findNotes",
            "version": 6,
            "params": {"query": f'Front:"{word}"'}
        }
        response = requests.post("http://localhost:8765", json=find_note_payload).json()
        note_ids = response.get("result", [])

        # Si la nota existe, eliminarla antes de crear una nueva
        if note_ids:
            delete_note_payload = {
                "action": "deleteNotes",
                "version": 6,
                "params": {"notes": note_ids}
            }
            requests.post("http://localhost:8765", json=delete_note_payload)

        # Obtener valores para la flashcard
        palabra = word
        audio_de_palabra = definition.get_audio(word)  # URL o archivo
        definicion = translation.translate(word)["translation"]
        oracion_dict = context.get_first_result_dict(word)
        oracion_de_ejemplo = oracion_dict["en"]
        hint_traduccion = oracion_dict["es"]
        audio_de_oracion = speech.speech(word)  # Archivo MP3 generado

        # Guardar el archivo de audio en ./audios/
        audio_filename = f"./audios/{word}.mp3"
        audio_path = os.path.join("audios", audio_filename)  # Carpeta relativa ./audios/

        if audio_de_oracion:
            # Asegurar que la carpeta ./audios/ existe
            os.makedirs("audios", exist_ok=True)

            # Guardar el audio generado en la carpeta correcta
            with open(audio_path, "wb") as f:
                f.write(audio_de_oracion)

            # Leer el archivo desde ./audios/ para enviarlo a Anki
            with open(audio_path, "rb") as f:
                audio_data = f.read()

            # Subir el archivo de audio a Anki
            response = requests.post("http://localhost:8765", json={
                "action": "storeMediaFile",
                "version": 6,
                "params": {"filename": audio_filename, "data": audio_data}
            }).json()
            print("Respuesta al subir audio:", response)  # Para depuración

        # HTML para la tarjeta
        front_html = f"""
        <style>
            .flashcard {{ text-align: center; font-size: 20px; }}
            .replay-button {{ border: none; background: none; cursor: pointer; }}
        </style>
        <div class="flashcard">
            <div class="front">
                <p class="card-target">{palabra}</p>
                <div class="target-audio">
                    <button class="replay-button" onclick="document.getElementById('audio-word').play()">
                        ▶
                        <audio id="audio-word" src="{audio_de_palabra}"></audio>
                    </button>
                </div>
            </div>
        </div>
        """.strip()

        back_html = f"""
        <style>
            .flashcard {{ text-align: center; font-size: 20px; }}
            .replay-button {{ border: none; background: none; cursor: pointer; }}
        </style>
        <div class="flashcard">
            <div class="front">
                <p class="card-target">{palabra}</p>
            </div>
            <hr id="answer" />
            <div class="back">
                <div class="definition">{definicion}</div>
                <div class="sentence-wrapper">
                     <div class="flex">
                        <div class="example-sentence">
                            "{oracion_de_ejemplo}"
                            <div class="sentence-translation">
                                {hint_traduccion}
                            </div>
                        </div>
                        <div>
                            <button class="replay-button" onclick="document.getElementById('audio-sentence').play()">
                                ▶
                                <audio id="audio-sentence" src="[sound:{audio_filename}]" controls></audio>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """.strip()

        # Crear la nota en Anki
        note_payload = {
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
                    "tags": ["generated"]
                }
            }
        }

        # Enviar la petición a AnkiConnect
        response = requests.post("http://localhost:8765", json=note_payload).json()
        print("Respuesta al agregar la nota:", response)

    except Exception as e:
        print("Error al agregar la tarjeta:", e)

# Prueba con "heart"
add_flashcard("heart")
