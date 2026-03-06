import os
import django
import sys

# Ensure the working directory is in sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import Module, ModuleMaterial, Group, Announcement, Notification

def verify_and_clear():
    models = [ModuleMaterial, Module, Group, Announcement, Notification]
    
    print("--- Current Database State ---")
    for model in models:
        print(f"{model.__name__}: {model.objects.count()} records")
    
    print("\n--- Starting Clearance ---")
    for model in models:
        count = model.objects.count()
        if count > 0:
            print(f"Deleting {count} {model.__name__} records...")
            model.objects.all().delete()
    
    print("\n--- Final Database State ---")
    for model in models:
        print(f"{model.__name__}: {model.objects.count()} records")
    
    print("\nClearance process finished.")

if __name__ == "__main__":
    verify_and_clear()
