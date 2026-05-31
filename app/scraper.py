import time
from app.settings import Settings
from app.aihandler import AIHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OCCScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, Settings.WAIT_TIMEOUT)
        self.ai = AIHandler()

    def search_jobs(self, position, location):
        self.driver.get(Settings.SITE)

        pos_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Puesto, área laboral o empresa']")))
        pos_input.send_keys(position)

        loc_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Ciudad o Estado']")
        loc_input.send_keys(location)

        ul_list = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#list-result-department ul")))
        options = ul_list.find_elements(By.TAG_NAME, "li")
        if options:
            self.driver.execute_script("arguments[0].click();", options[0])

        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Encontrar')]")))
        btn.click()
        print("🚀 Búsqueda enviada.")

    def scrape_all_cards(self):
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(Settings.PAGE_LOAD_SLEEP)
        
        cards = self.driver.find_elements(By.XPATH, "//*[starts-with(@id, 'jobcard-')]")
        print(f"📋 Se encontraron {len(cards)} tarjetas.")

        for index, card in enumerate(cards):
            self._process_card(card, index)

    def _process_card(self, card, index):
        start_time = time.time()

        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            time.sleep(Settings.PAGE_LOAD_SLEEP)
            card.click()
            
            print(f"\n🔍 Leyendo vacante {index + 1}...")
            time.sleep(Settings.PAGE_LOAD_SLEEP) 
            detail = self.driver.find_element(By.ID, "job-detail-container")
            
            print("🤖 Analizando habilidades con Gemini...")
            response = self.ai.extract_skills(detail.text)
            print(f"\nSkills: {response}")

            end_time = time.time()
            duration = end_time - start_time

            print(f"\n⏱️ Tiempo total de procesamiento: {duration:.2f} segundos")
            

        except Exception as e:
            print(f"⚠️ Error en tarjeta {index + 1}: {e}")