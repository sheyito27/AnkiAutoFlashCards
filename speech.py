# speech.py

from gtts import gTTS
import context  # Suponiendo que esta es tu librería para obtener ejemplos y contexto


def speech(word):
    # Verificar si context.get_first_result_dict(word) no devuelve None
    result = context.get_first_result_dict(word)

    if result is None:
        print(f"Error: No se encontró contexto para la palabra '{word}'.")
        return  # Termina la ejecución si no hay contexto

    # Usar el resultado solo si es un diccionario válido
    tts = gTTS(result["en"], lang="en", tld="com")
    tts.save(f"./audios/{word}.mp3")
    print(f"Audio guardado como './audios/{word}.mp3'")

