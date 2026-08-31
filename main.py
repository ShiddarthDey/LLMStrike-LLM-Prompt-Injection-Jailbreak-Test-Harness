import os
import argparse
from core.db import init_db
from core.runner import run_pack
from core.target import GeminiTarget, OpenAICompatibleTarget
from core.report import generate_report

PROVIDERS = {
    "gemini": {
        "env_var": "GEMINI_API_KEY",
        "default_model": "gemini-2.5-flash",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_var": "GROQ_API_KEY",
        "default_model": "openai/gpt-oss-20b",
    },
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "env_var": "NVIDIA_API_KEY",
        "default_model": "meta/llama-3.3-70b-instruct",
    },
}

def main():
    parser = argparse.ArgumentParser(description="LLMStrike CLI")
    parser.add_argument("--pack", default="direct_injection", help="Attack pack name in attacks/")
    parser.add_argument("--provider", choices=list(PROVIDERS.keys()), default="gemini", help="Target LLM provider")
    parser.add_argument("--model", default=None, help="Target model name")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between attacks")
    parser.add_argument("--report", action="store_true", help="Generate HTML security assessment report")
    args = parser.parse_args()

    if args.report:
        generate_report()
        return

    init_db()
    cfg = PROVIDERS[args.provider]
    key = os.getenv(cfg["env_var"])
    if not key:
        raise ValueError(f"{cfg['env_var']} environment variable is missing for provider '{args.provider}'")

    model = args.model or cfg["default_model"]

    if args.provider == "gemini":
        target = GeminiTarget(model=model)
    else:
        target = OpenAICompatibleTarget(
            provider=args.provider,
            base_url=cfg["base_url"],
            api_key=key,
            model=model,
        )

    run_pack(args.pack, target, delay=args.delay)

if __name__ == "__main__":
    main()
