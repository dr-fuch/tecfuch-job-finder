from app.config import FirefoxConfig
from app.scraper import OCCScraper
from app.settings import Settings

def main():
    config = FirefoxConfig()
    driver = None
    
    try:
        driver = config.get_driver()
        bot = OCCScraper(driver)
        bot.search_jobs(Settings.JOB_POSITION, Settings.JOB_LOCATION)
        bot.scrape_all_cards()

        input("\n✅ Proceso terminado. Presiona ENTER para salir...")

    except Exception as e:
        print(f"❌ Error general: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()