import os, requests, sys
from dotenv import load_dotenv

load_dotenv()
provider = sys.argv[1] if len(sys.argv) > 1 else "groq"
configs = {
    "groq":   ("https://api.groq.com/openai/v1/models", "GROQ_API_KEY"),
    "nvidia": ("https://integrate.api.nvidia.com/v1/models", "NVIDIA_API_KEY"),
}
url, env = configs[provider]
r = requests.get(url, headers={"Authorization": f"Bearer {os.getenv(env)}"})
print("status:", r.status_code)
if r.status_code == 200:
    for m in r.json().get("data", []):
        print(m["id"])
else:
    print(r.text[:500])