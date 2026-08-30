import sqlite3

rows = sqlite3.connect('reports/results.db').execute(
    "select attack_id, model, response from results where verdict='unclear'"
).fetchall()
for r in rows:
    print(r[0], '|', r[1])
    print(str(r[2])[:400])
    print('---')
print('total:', len(rows))