import os
import shutil
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from settings import Settings
from webdriver_manager.firefox import GeckoDriverManager


class FirefoxConfig:
    def __init__(self):
        load_dotenv()
        self.original_profile = Settings.ORIGINAL_PROFILE_PATH
        self.temp_profile = Settings.TEMP_PROFILE_PATH
        self.binary_path = Settings.FIREFOX_BINARY

    def sync_profile(self):
        print("🔄 Sincronizando perfil...")
        if os.path.exists(self.temp_profile):
            shutil.rmtree(self.temp_profile)
        shutil.copytree(self.original_profile, self.temp_profile, 
                        ignore=shutil.ignore_patterns("parent.lock", "lock", ".parentlock", "cache*", "startupCache*"))

    def get_driver(self):
        self.sync_profile()
        options = Options()
        options.binary_location = self.binary_path
        options.add_argument("-profile")
        options.add_argument(self.temp_profile)
        
        service = Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)