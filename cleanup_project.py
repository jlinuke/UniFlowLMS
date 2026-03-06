import os
import shutil

files_to_delete = [
    "FIX_DATABASE.bat", "check_db.py", "check_modules_db.py", "clear_records.py", 
    "db_fix.py", "debug_users.py", "env_diag.py", "final_verify.py", 
    "manual_db_fix.py", "migration_debug_forced.py", "orchestrate_migrate.py", 
    "robust_clear_records.py", "run_health_check.py", "simple_db_check.py", 
    "student_view_debug.log", "test.py", "test_render.py", "verify_api.py", 
    "verify_notifications.py", "verify_serializer_fix.py", "verify_simplified_upload.py"
]

for file in files_to_delete:
    if os.path.exists(file):
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    else:
        print(f"Not found: {file}")

# Clear media/modules
media_dir = os.path.join("media", "modules")
if os.path.exists(media_dir):
    for f in os.listdir(media_dir):
        file_path = os.path.join(media_dir, f)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted media: {f}")
        except Exception as e:
            print(f"Error deleting media {f}: {e}")
