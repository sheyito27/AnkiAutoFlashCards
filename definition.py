import requests

def fetch_definitions(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener las definiciones: {e}")
        return {}

def get_phonetic(word):
    definitions = fetch_definitions(word)
    if not definitions:
        return None  # Si no hay definición, devuelve None
    phonetics = definitions[0].get("phonetics", [])
    for phonetic in phonetics:
        if "audio" in phonetic and "us.mp3" in phonetic["audio"]:
            return phonetic.get("text")
    return None  # Retorna None si no encuentra fonética

def get_audio(word):
    definitions = fetch_definitions(word)
    if not definitions:
        return None  # Si no hay definición, devuelve None
    phonetics = definitions[0].get("phonetics", [])
    for phonetic in phonetics:
        if "audio" in phonetic and "us.mp3" in phonetic["audio"]:
            return phonetic.get("audio")
    return None  # Retorna None si no encuentra audio

def store_data(word):
    data = {}
    data["word"] = word
    data["phonetic"] = get_phonetic(word)
    data["audio"] = get_audio(word)
    return data

