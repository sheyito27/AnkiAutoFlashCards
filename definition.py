import requests


def fetch_definitions(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        return []
    except Exception as e:
        print(f"Error general: {e}")
        return []


def _get_phonetic_data(definitions, target_key):
    if not definitions:
        return None

    for phonetic in definitions[0].get("phonetics", []):
        audio = phonetic.get("audio", "")
        if audio and phonetic.get(target_key):
            return phonetic[target_key]
    return None


def get_phonetic(definitions):
    return _get_phonetic_data(definitions, "text")


def get_audio(definitions):
    return _get_phonetic_data(definitions, "audio")


def store_data(word):
    definitions = fetch_definitions(word)
    return {
        "word": word,
        "phonetic": get_phonetic(definitions),
        "audio": get_audio(definitions)
    }