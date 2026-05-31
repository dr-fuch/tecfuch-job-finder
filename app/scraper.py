import time
import math
from app.settings import Settings
from app.aihandler import AIHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OCCScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, Settings.WAIT_TIMEOUT)
        self.ai = AIHandler() if Settings.PROCESS_WITH_GOOGLE_AI else None

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
        total_results = self.get_total_results()
        total_pages = math.ceil(total_results / 20)
        
        for actual_page in range(1, total_pages + 1):
            print(f"\n📄 --- PROCESANDO PÁGINA {actual_page} DE {total_pages} ---")
            cards = self.get_cards()
            for index, card in enumerate(cards):
                global_index = ((actual_page - 1) * 20) + index
                self.process_card(card, global_index)
            
            if actual_page < total_pages:
                try:
                    print("➡️ Saltando a la siguiente página...")
                    btn_next = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-next-offer")))
                    self.driver.execute_script("arguments[0].click();", btn_next)
                    
                    time.sleep(Settings.PAGE_LOAD_SLEEP * 2) 
                except Exception as e:
                    print(f"🛑 No se pudo hacer clic en el botón siguiente: {e}")
                    break

    def process_card(self, card, index):
        JOB_DETAIL_FOOTER_SEPARATOR="Recuerda que ningún reclutador"
        start_time = time.time()

        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            time.sleep(Settings.PAGE_LOAD_SLEEP)
            card.click()
            
            print(f"\n🔍 Leyendo vacante {index + 1}...")
            time.sleep(Settings.PAGE_LOAD_SLEEP) 
            job_details = self.driver.find_element(By.ID, "job-detail-container").text
            job_details = job_details.split(JOB_DETAIL_FOOTER_SEPARATOR)[0].strip()

            print(f"Vacante: \n{job_details}")
            
            if Settings.PROCESS_WITH_GOOGLE_AI:
                print("🤖 Analizando habilidades con Gemini...")
                response = self.ai.extract_skills(job_details)
                print(f"\nSkills: {response}")

            end_time = time.time()
            duration = end_time - start_time

            print(f"\n⏱️ Tiempo total de procesamiento: {duration:.2f} segundos")
            

        except Exception as e:
            print(f"⚠️ Error en tarjeta {index + 1}: {e}")

    def get_total_results(self):
        element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[data-total-offers]")))
        total_str = element.get_attribute("data-total-offers")
        total = int(total_str)
        print(f"📊 Total de vacantes detectadas en OCC: {total}")
        return total

    def get_cards(self):
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(Settings.PAGE_LOAD_SLEEP)
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".card-job-offer")
        print(f"📋 Se encontraron {len(cards)} tarjetas.")
        return cards