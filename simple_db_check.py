import sqlite3

db_path = 'db.sqlite3'
log_path = 'simple_db_check.txt'

with open(log_path, 'w') as f:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        f.write("--- Groups ---\n")
        cursor.execute("SELECT id, name FROM core_group")
        groups = cursor.fetchall()
        for g in groups:
            f.write(f"Group ID {g[0]}: {g[1]}\n")
            
        f.write("\n--- Modules ---\n")
        cursor.execute("SELECT id, title FROM core_module")
        modules = cursor.fetchall()
        for m in modules:
            f.write(f"Module ID {m[0]}: {m[1]}\n")
            # Check target groups
            cursor.execute("SELECT group_id FROM core_module_target_groups WHERE module_id=?", (m[0],))
            tg = cursor.fetchall()
            f.write(f"  Target Groups: {[t[0] for t in tg]}\n")
            
        f.write("\n--- Module Materials ---\n")
        cursor.execute("SELECT id, title, module_id FROM core_modulematerial")
        mats = cursor.fetchall()
        for mat in mats:
            f.write(f"Material: {mat[1]} (Module ID {mat[2]})\n")
            
        conn.close()
    except Exception as e:
        f.write(f"ERROR: {e}\n")
