import os
import django
import sys
from django.core.management import call_command

# Redirect stdout to a file because the terminal is behaving badly
sys.stdout = open('db_fix_log.txt', 'w')
sys.stderr = sys.stdout

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

try:
    print("Attempting to apply migrations for 'core'...")
    call_command('migrate', 'core', interactive=False)
    print("Migration command completed successfully.")
except Exception as e:
    print(f"Migration failed with error: {e}")
finally:
    sys.stdout.close()
