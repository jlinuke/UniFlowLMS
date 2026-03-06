import os
import django
import sys
from django.core.management import call_command

# Redirect output to file
with open('health_check.log', 'w') as f:
    sys.stdout = f
    sys.stderr = f

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
    django.setup()

    try:
        print("Running system check...")
        call_command('check')
        print("Check completed with no errors.")
    except Exception as e:
        print(f"Check failed with error: {e}")
