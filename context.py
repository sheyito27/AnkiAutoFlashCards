from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_first_result_dict(word):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0...")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"https://tatoeba.org/en/sentences/search?query={word}&from=eng&to=spa")

        wait = WebDriverWait(driver, 15)
        example_block = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sentence-and-translations")))

        english_sentence = example_block.find_element(By.CSS_SELECTOR, "div.sentence div.text").text.split('\n')[0]
        spanish_translation = example_block.find_element(By.CSS_SELECTOR, "div.translation div.text").text.split('\n')[
            0]

        return {
            "en": english_sentence,
            "es": spanish_translation
        }

    except Exception as e:
        print(f"Error obteniendo ejemplo: {e}")
        return {"en": "", "es": ""}
    finally:
        driver.quit()