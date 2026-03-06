import os
import django
import sys
from django.core.management import call_command

# Redirect stdout to a file because the terminal is behaving badly
sys.stdout = open('migration_debug.log', 'w')
sys.stderr = sys.stdout

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

try:
    print("Step 1: Running makemigrations core...")
    call_command('makemigrations', 'core', interactive=False)
    print("Step 2: Running migrate core...")
    call_command('migrate', 'core', interactive=False)
    print("Migration sequence completed successfully.")
except Exception as e:
    print(f"FAILED with error: {e}")
finally:
    sys.stdout.close()
