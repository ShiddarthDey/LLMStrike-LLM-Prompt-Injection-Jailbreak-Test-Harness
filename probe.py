import os, requests
from dotenv import load_dotenv

load_dotenv()
candidates = [
    "moonshotai/kimi-k3",
    "minimaxai/minimax-m3",
    "nvidia/nemotron-3-nano-30b-a3b",
    "google/gemma-3-12b-it",
    "ibm/granite-3.0-8b-instruct",
    "mistralai/mistral-large-2-instruct",
    "openai/gpt-oss-120b",
]

for m in candidates:
    try:
        r = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}"},
            json={"model": m, "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 10},
            timeout=60,
        )
        print(m, r.status_code)
    except Exception as e:
        print(m, "error:", str(e)[:80])