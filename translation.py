import requests
import os
from langdetect import detect

API_KEY = os.getenv("TRANSLATION_API_KEY", "7209c6607a7336cc5ce99ad5af5f9813")
BASE_URL = "https://mt.qcri.org/api/v1"


def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"


def translate(text, langpair=None):
    if langpair is None:
        source_lang = detect_language(text)
        langpair = "en-es" if source_lang == "en" else "es-en"

    params = {
        "key": API_KEY,
        "langpair": langpair,
        "domain": "general",
        "text": text
    }

    try:
        response = requests.get(f"{BASE_URL}/translate", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "original": text,
            "translation": data.get("translatedText", "Error en la traducción")
        }
    except Exception as e:
        return {"error": str(e)}