import json
from google import genai
from .settings import Settings

class AIHandler:
    def __init__(self):
        self.client = genai.Client(api_key=Settings.GOOGLE_AI_API_KEY)
        self.model_id = Settings.GOOGLE_AI_MODEL

    def extract_skills(self, job_text):
        job_text_clean = job_text.replace("\n", " ").strip()
        full_prompt = Settings.GOOGLE_AI_PROMPT_TEMPLATE.format(job_text=job_text_clean)
        
        try:
            response = self.client.models.generate_content(model=self.model_id, contents=full_prompt)
            response = str(response.text)
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            return json.loads(response.strip())
        except Exception as e:
            print(f"Error al analizar con IA: {e}")
            return None