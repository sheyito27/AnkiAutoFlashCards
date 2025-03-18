import requests
import urllib.parse

API_KEY = "7209c6607a7336cc5ce99ad5af5f9813"
BASE_URL = "https://mt.qcri.org/api/v1"

def get_language_pairs():
    """Obtiene los pares de idiomas disponibles en la API."""
    url = f"{BASE_URL}/getLanguagePairs?key={API_KEY}"
    try:
        response = requests.get(url).json()
        return response.get("langpairs", [])
    except requests.exceptions.RequestException as e:
        return {}

def get_domains():
    """Obtiene los dominios de traducción disponibles en la API."""
    url = f"{BASE_URL}/getDomains?key={API_KEY}"
    try:
        response = requests.get(url).json()
        return response.get("domains", [])
    except requests.exceptions.RequestException as e:
        return {}

def detect_language(word):
    """
    Función simple para detectar el idioma de la palabra.
    Si la palabra es toda ASCII, se asume que es inglés;
    de lo contrario, se asume español.
    """
    if word.isascii():
        return "en"
    else:
        return "es"

def translate(text, langpair=None):
    """
    Traduce un texto usando la API de traducción.
    Si no se especifica langpair, se determina dinámicamente:
      - Si el texto está en inglés se traduce a español (en-es).
      - Si el texto está en español se traduce a inglés (es-en).
    """
    # Determinar automáticamente el par de idiomas si no se proporciona
    if langpair is None:
        source_lang = detect_language(text)
        langpair = "en-es" if source_lang == "en" else "es-en"

    domains = get_domains()
    valid_domains = ["general", "general-fast", "general-neural", "dialectal"]
    # Filtrar dominios válidos
    valid_domains_available = [domain for domain in valid_domains if domain in domains]

    if not valid_domains_available:
        return {"error": "No se encontraron dominios válidos para la traducción"}

    for domain in valid_domains_available:
        encoded_text = urllib.parse.quote(text)
        url = f"{BASE_URL}/translate?key={API_KEY}&langpair={langpair}&domain={domain}&text={encoded_text}"
        try:
            response = requests.get(url).json()
            if response.get("success"):
                return {"original": text, "translation": response.get("translatedText", "Error en la traducción")}
            else:
                return {"error": f"Error con dominio {domain}: {response.get('error', 'Error desconocido')}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error al traducir: {e}"}

if __name__ == "__main__":
    # Diccionario donde se almacenarán las traducciones
    translations = {}

    # Palabra a traducir
    text = "cow"  # O cualquier palabra que necesites traducir

    # Traducir y almacenar en el diccionario
    result = translate(text)
    translations[text] = result

    # Ahora 'translations' contiene la traducción de la palabra