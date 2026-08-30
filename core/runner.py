import os
import yaml
from core.db import save_result
from core.judge import judge

def run_pack(pack_name: str, target):
    pack_file = os.path.join("attacks", f"{pack_name}.yaml")
    if not os.path.exists(pack_file):
        raise FileNotFoundError(f"Attack pack file not found: {pack_file}")

    with open(pack_file, "r", encoding="utf-8") as f:
        attacks = yaml.safe_load(f) or []

    print(f"Running pack: {pack_name} ({len(attacks)} attacks)")

    summary = {"compromised": 0, "refused": 0, "unclear": 0, "error": 0}

    for attack in attacks:
        attack_id = str(attack.get("id", ""))
        category = attack.get("category", "")
        prompt = attack.get("prompt", "")
        name = attack.get("name", attack_id)

        response = None
        error = None
        try:
            response = target.send(prompt)
            verdict, severity = judge(attack, response)
            print(f"[{attack_id}] {name} - OK ({verdict}/{severity})")
        except Exception as e:
            error = str(e)
            verdict, severity = "error", "none"
            print(f"[{attack_id}] {name} - ERROR: {error} ({verdict}/{severity})")

        summary[verdict] = summary.get(verdict, 0) + 1
        save_result(attack_id, category, prompt, response, error, verdict, severity)

    print(f"Summary: {summary['compromised']} compromised, {summary['refused']} refused, {summary['unclear']} unclear, {summary['error']} error")
