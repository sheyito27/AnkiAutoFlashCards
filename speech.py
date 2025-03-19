from gtts import gTTS
import os


def generate_audio(text, filename):
    try:
        tts = gTTS(text=text, lang="en", tld="com", slow=False)
        tts.save(filename)  # Guardar directamente el archivo

        if not os.path.exists(filename):
            raise FileNotFoundError(f"El archivo {filename} no se generó correctamente.")

        print(f"Audio generado: {filename}")

    except Exception as e:
        print(f"Error generando audio: {e}")
