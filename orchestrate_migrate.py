import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

try:
    call_command('migrate', 'core', interactive=False)
    with open('db_sync_verified.txt', 'w') as f:
        f.write('Migration Applied Successfully')
except Exception as e:
    with open('db_sync_error.txt', 'w') as f:
        f.write(str(e))
