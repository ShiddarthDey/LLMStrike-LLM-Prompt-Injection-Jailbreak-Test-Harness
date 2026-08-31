import sqlite3

rows = sqlite3.connect('reports/results.db').execute(
    "select verdict, count(*) from results group by verdict"
).fetchall()
for r in rows:
    print(r[0], '|', r[1])