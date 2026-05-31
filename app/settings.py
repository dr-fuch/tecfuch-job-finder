import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # --- Site Configs ---
    SITE = os.getenv("SITE")

    # --- Browser Configs ---
    ORIGINAL_PROFILE_PATH = str(Path(os.getenv("ORIGINAL_PROFILE_PATH")).expanduser())
    TEMP_PROFILE_PATH = str(Path(os.getenv("TEMP_PROFILE_PATH")).expanduser())
    FIREFOX_BINARY = os.getenv("FIREFOX_BINARY")

    # --- Searching Configs ---
    JOB_POSITION = os.getenv("JOB_POSITION")
    JOB_LOCATION = os.getenv("JOB_LOCATION")

    # --- Apply Configs ---
    ENABLE_AUTO_APPLY = os.getenv("ENABLE_AUTO_APPLY").lower() == "true"
    
    # --- Times Configs ---
    WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT"))
    PAGE_LOAD_SLEEP = int(os.getenv("PAGE_LOAD_SLEEP"))

    # --- Google AI Configs ---
    PROCESS_WITH_GOOGLE_AI= os.getenv("PROCESS_WITH_GOOGLE_AI").lower() == "true"
    GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
    GOOGLE_AI_MODEL = str(os.getenv("GOOGLE_AI_MODEL"))
    GOOGLE_AI_PROMPT_TEMPLATE = str(os.getenv("GOOGLE_AI_PROMPT_TEMPLATE"))