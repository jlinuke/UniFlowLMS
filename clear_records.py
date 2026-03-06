import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import Module, ModuleMaterial, Group, Announcement, Notification

def clear_data():
    print("Starting data clearance...")
    
    # Order matters for foreign keys, though CASCADE handles most
    print(f"Deleting {ModuleMaterial.objects.count()} ModuleMaterials...")
    ModuleMaterial.objects.all().delete()
    
    print(f"Deleting {Module.objects.count()} Modules...")
    Module.objects.all().delete()
    
    print(f"Deleting {Group.objects.count()} Groups...")
    Group.objects.all().delete()

    print(f"Deleting {Announcement.objects.count()} Announcements...")
    Announcement.objects.all().delete()

    print(f"Deleting {Notification.objects.count()} Notifications...")
    Notification.objects.all().delete()
    
    print("Data clearance completed successfully.")

if __name__ == "__main__":
    clear_data()
