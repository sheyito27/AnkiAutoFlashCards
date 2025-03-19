import requests
from urllib.parse import quote

API_KEY = "7209c6607a7336cc5ce99ad5af5f9813"  # Tu clave de API
BASE_URL = "https://mt.qcri.org/api/v1"

def translate(text):
    # Parámetros para la solicitud
    params = {
        "key": API_KEY,
        "langpair": "en-es",  # Traducir de inglés a español
        "domain": "general",   # Dominio general
        "text": quote(text)    # Codificar el texto para la URL
    }

    try:
        # Hacer la solicitud a la API
        response = requests.get(f"{BASE_URL}/translate", params=params, timeout=10)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        data = response.json()

        # Devolver la traducción si la solicitud fue exitosa
        if data.get("success", False):
            return data.get("translatedText", "Error: No se pudo obtener la traducción.")
        else:
            return f"Error: {data.get('error', 'Desconocido')}"
    except Exception as e:
        return f"Error en la solicitud: {str(e)}"
