import sqlite3
import os

db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(core_user);")
    columns = cursor.fetchall()
    with open('schema_check.txt', 'w') as f:
        for col in columns:
            f.write(col[1] + '\n')
    conn.close()
    print("Schema checked.")
else:
    with open('schema_check.txt', 'w') as f:
        f.write("DB NOT FOUND")
