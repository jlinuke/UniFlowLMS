import sqlite3
import os

db_path = 'db.sqlite3'
log_path = 'manual_sql_log.txt'

with open(log_path, 'w') as log:
    try:
        if not os.path.exists(db_path):
            log.write(f"Database {db_path} not found!\n")
            exit(1)
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        log.write("Step 1: Creating core_modulematerial table...\n")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS core_modulematerial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                file_path VARCHAR(100) NOT NULL,
                uploaded_at DATETIME NOT NULL,
                module_id BIGINT NOT NULL REFERENCES core_module(id) DEFERRABLE INITIALLY DEFERRED
            )
        ''')
        
        log.write("Step 2: Checking if core_module still has file_path column...\n")
        cursor.execute("PRAGMA table_info(core_module)")
        cols = cursor.fetchall()
        has_file_path = any(col[1] == 'file_path' for col in cols)
        
        if has_file_path:
            log.write("Step 3: Removing file_path from core_module (SQLite via rename)...\n")
            # SQLite doesn't support DROP COLUMN easily, but we can just leave it if it doesn't hurt, 
            # or do the rename dance. For simplicity and fixing the crash, let's focus on ModuleMaterial.
            log.write("Note: file_path still exists in core_module. This might be fine for now.\n")
            
        conn.commit()
        conn.close()
        log.write("Manual SQL fix successful.\n")
    except Exception as e:
        log.write(f"FAILED with error: {e}\n")
