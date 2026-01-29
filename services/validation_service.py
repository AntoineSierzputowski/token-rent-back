import requests
import json
import re
import os

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2-vl") # User should have this pulled

class ValidationService:
    def _call_ollama(self, prompt: str, base64_image: str) -> str:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "images": [base64_image],
            "stream": False,
            "format": "json"
        }
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.RequestException as e:
            print(f"Ollama API Error: {e}")
            raise Exception(f"Failed to communicate with OCR service: {e}")

    def analyze_id_card(self, base64_image: str) -> dict:
        prompt = """
        Analyze this ID card image. Extract the following information and return it in a pure JSON format with keys:
        - last_name
        - first_name
        - date_of_birth (YYYY-MM-DD format)
        
        If a field is not visible, use null. do not output markdown code blocks.
        """
        
        response_text = self._call_ollama(prompt, base64_image)
        clean_text = re.sub(r'```json\n|```', '', response_text).strip()
        
        try:
            data = json.loads(clean_text)
            return data
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {response_text}")
            return {}

    def analyze_salary_slip(self, base64_image: str) -> float:
        prompt = """
        Analyze this salary slip. Extract the 'Net Salary' or 'Net Pay' amount. 
        Return ONLY a JSON object with a single key "net_salary" containing the numeric value (float).
        Example: {"net_salary": 2500.50}
        """
        
        response_text = self._call_ollama(prompt, base64_image)
        clean_text = re.sub(r'```json\n|```', '', response_text).strip()

        try:
            data = json.loads(clean_text)
            val = data.get("net_salary")
            if val:
                if isinstance(val, str):
                     val = float(re.sub(r'[^\d.]', '', val))
                return float(val)
            return 0.0
        except Exception as e:
            print(f"Failed to parse Salary: {clean_text}, error: {e}")
            return 0.0

validation_service = ValidationService()
