import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class Target:
    def send(self, prompt: str) -> str:
        raise NotImplementedError

class GeminiTarget(Target):
    def __init__(self, model: str = "gemini-2.5-flash"):
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY environment variable is missing")
        self.client = genai.Client(api_key=key)
        self.model = model

    def send(self, prompt: str) -> str:
        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return res.text
