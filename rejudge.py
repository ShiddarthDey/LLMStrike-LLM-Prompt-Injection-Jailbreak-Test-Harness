import os
import sqlite3
import yaml
from core.judge import judge

def load_attacks() -> dict:
    attacks = {}
    attacks_dir = "attacks"
    if os.path.exists(attacks_dir):
        for filename in os.listdir(attacks_dir):
            if filename.endswith(".yaml"):
                filepath = os.path.join(attacks_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        items = yaml.safe_load(f) or []
                        for item in items:
                            if isinstance(item, dict) and "id" in item:
                                attacks[str(item["id"])] = item
                except Exception:
                    pass
    return attacks

def main():
    db_path = os.path.join("reports", "results.db")
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return

    attacks_map = load_attacks()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, attack_id, response, verdict, severity
        FROM results
        WHERE verdict != 'error' AND verdict IS NOT NULL
    """)
    rows = cur.fetchall()

    changed_count = 0
    for row_id, attack_id, response, old_verdict, old_severity in rows:
        attack = attacks_map.get(str(attack_id), {"id": attack_id})
        new_verdict, new_severity = judge(attack, response)

        if new_verdict != old_verdict or new_severity != old_severity:
            cur.execute(
                "UPDATE results SET verdict = ?, severity = ? WHERE id = ?",
                (new_verdict, new_severity, row_id)
            )
            changed_count += 1

    conn.commit()
    conn.close()
    print(f"Re-judging complete: {changed_count} row(s) updated out of {len(rows)} non-error results.")

if __name__ == "__main__":
    main()
