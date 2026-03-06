import sqlite3
import os

db_path = 'db.sqlite3'
verification_file = 'final_db_verified.txt'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_modulematerial'")
    result = cursor.fetchone()
    conn.close()
    
    with open(verification_file, 'w') as f:
        if result:
            f.write("DATABASE_READY: core_modulematerial exists.")
        else:
            f.write("DATABASE_ERROR: core_modulematerial NOT FOUND.")
except Exception as e:
    with open(verification_file, 'w') as f:
        f.write(f"SQUASHED_ERROR: {str(e)}")
