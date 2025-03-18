from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_first_result_dict(word):
    url = ("https://tatoeba.org/en/sentences/search?from=eng&has_audio=&list=907&native=&original="
           f"orphans=no&query={word}&sort=relevance&sort_reverse=&tags=&to=spa&trans_filter=limit"
           "&trans_has_audio=&trans_link=&trans_orphan=&trans_to=spa&trans_unapproved=&trans_user="
           "&unapproved=no&user=&word_count_max=&word_count_min=6")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    try:
        # Esperamos a que se cargue el bloque de la oración y sus traducciones.
        result_block = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sentence-and-translations")))

        # Obtenemos la oración en inglés
        english_elem = result_block.find_element(By.CSS_SELECTOR, "div.sentence")
        english_text = english_elem.text.strip()

        # Obtenemos la traducción en español
        translation_container = result_block.find_element(By.CSS_SELECTOR, "div.translations")
        spanish_elem = translation_container.find_element(By.CSS_SELECTOR, "div.translation")
        spanish_text = spanish_elem.text.strip()

        # Función para filtrar líneas no deseadas
        def clean_text(text):
            lines = text.splitlines()
            unwanted = {"content_copy", "volume_up", "volume_off", "info", "chevron_right"}
            cleaned_lines = [line for line in lines if line.strip() not in unwanted]
            return "\n".join(cleaned_lines)

        english_clean = clean_text(english_text)
        spanish_clean = clean_text(spanish_text)

        # Almacenamos el resultado en un diccionario
        result = {"en": english_clean, "es": spanish_clean}
        return result

    except Exception as e:
        print("Error al extraer la información:", e)
    finally:
        driver.quit()
print(get_first_result_dict("heart"))