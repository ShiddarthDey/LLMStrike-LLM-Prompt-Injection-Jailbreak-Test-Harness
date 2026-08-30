import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

class Target:
    name: str = "target"

    def send(self, prompt: str) -> str:
        raise NotImplementedError

class GeminiTarget(Target):
    def __init__(self, model: str = "gemini-2.5-flash"):
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY environment variable is missing")
        self.client = genai.Client(api_key=key)
        self.model = model
        self.name = f"gemini/{self.model}"

    def send(self, prompt: str) -> str:
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return res.text

class OpenAICompatibleTarget(Target):
    def __init__(self, provider: str, base_url: str, api_key: str, model: str):
        if not api_key:
            raise ValueError(f"API key missing for provider {provider}")
        self.provider = provider
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.name = f"{provider}/{model}"

    def send(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
