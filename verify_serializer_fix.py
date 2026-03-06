import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

try:
    from core.serializers import ModuleSerializer
    print("SUCCESS: ModuleSerializer imported successfully.")
except NameError as e:
    print(f"FAILURE: NameError during import: {e}")
except Exception as e:
    print(f"FAILURE: Unexpected error: {e}")
