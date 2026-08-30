import os
import yaml
from core.db import save_result

def run_pack(pack_name: str, target):
    pack_file = os.path.join("attacks", f"{pack_name}.yaml")
    if not os.path.exists(pack_file):
        raise FileNotFoundError(f"Attack pack file not found: {pack_file}")

    with open(pack_file, "r", encoding="utf-8") as f:
        attacks = yaml.safe_load(f) or []

    print(f"Running pack: {pack_name} ({len(attacks)} attacks)")

    for attack in attacks:
        attack_id = str(attack.get("id", ""))
        category = attack.get("category", "")
        prompt = attack.get("prompt", "")
        name = attack.get("name", attack_id)

        response = None
        error = None
        try:
            response = target.send(prompt)
            print(f"[{attack_id}] {name} - OK")
        except Exception as e:
            error = str(e)
            print(f"[{attack_id}] {name} - ERROR: {error}")

        save_result(attack_id, category, prompt, response, error)
