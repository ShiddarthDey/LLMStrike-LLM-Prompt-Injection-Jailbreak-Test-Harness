import os
import sqlite3
from core.db import init_db
from core.runner import run_pack
from core.target import GeminiTarget, OpenAICompatibleTarget
from main import PROVIDERS

TARGETS = [
    ("groq", "openai/gpt-oss-20b"),
    ("nvidia", "openai/gpt-oss-120b"),
    ("nvidia", "minimaxai/minimax-m3"),
    ("nvidia", "nvidia/nemotron-3-nano-30b-a3b"),
    ("nvidia", "google/gemma-4-31b-it"),
]

def build_target(provider: str, model: str):
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}")
    cfg = PROVIDERS[provider]
    key = os.getenv(cfg["env_var"])
    if not key:
        raise ValueError(f"{cfg['env_var']} environment variable is missing for provider '{provider}'")

    target_model = model or cfg["default_model"]
    if provider == "gemini":
        return GeminiTarget(model=target_model)
    return OpenAICompatibleTarget(
        provider=provider,
        base_url=cfg["base_url"],
        api_key=key,
        model=target_model,
    )

def print_summary():
    db_path = os.path.join("reports", "results.db")
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            model,
            SUM(CASE WHEN verdict = 'compromised' THEN 1 ELSE 0 END),
            SUM(CASE WHEN verdict = 'refused' THEN 1 ELSE 0 END),
            SUM(CASE WHEN verdict = 'unclear' THEN 1 ELSE 0 END),
            SUM(CASE WHEN verdict = 'error' THEN 1 ELSE 0 END)
        FROM results
        GROUP BY model
    """)
    rows = cur.fetchall()
    conn.close()

    print("\nSummary Table:")
    print(f"{'Model':<35} {'Compromised':<12} {'Refused':<10} {'Unclear':<10} {'Error':<8}")
    print("-" * 75)
    for model, comp, ref, unc, err in rows:
        m_name = str(model or "unknown")
        print(f"{m_name:<35} {comp:<12} {ref:<10} {unc:<10} {err:<8}")

def main():
    init_db()

    packs = sorted([
        f[:-5] for f in os.listdir("attacks")
        if f.endswith(".yaml")
    ])

    for provider, model in TARGETS:
        print(f"\n--- Target: {provider}/{model} ---")
        try:
            target = build_target(provider, model)
            for pack in packs:
                run_pack(pack, target, delay=2.0)
        except Exception as e:
            print(f"Failed target {provider}/{model}: {e}")
            continue

    print_summary()

if __name__ == "__main__":
    main()
