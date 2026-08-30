import sqlite3

rows = sqlite3.connect('reports/results.db').execute(
    "select attack_id, model, verdict, error from results"
).fetchall()
for r in rows:
    print(r[0], '|', r[1], '|', r[2], '|', str(r[3])[:300])
print('total:', len(rows))