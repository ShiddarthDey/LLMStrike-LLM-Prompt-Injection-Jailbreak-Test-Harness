import argparse
from core.db import init_db
from core.runner import run_pack
from core.target import GeminiTarget

def main():
    parser = argparse.ArgumentParser(description="LLMStrike CLI")
    parser.add_argument("--pack", default="direct_injection", help="Attack pack name in attacks/")
    args = parser.parse_args()

    init_db()
    target = GeminiTarget()
    run_pack(args.pack, target)

if __name__ == "__main__":
    main()
