import sqlite3

db = sqlite3.connect('reports/results.db')
db.execute("delete from results where verdict='error'")
db.commit()
print("deleted", db.total_changes, "error rows")