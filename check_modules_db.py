import os
import django
import sys

# Redirect output to file
sys.stdout = open('db_diagnostic.log', 'w')
sys.stderr = sys.stdout

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import User, Group, Module, ModuleMaterial

try:
    print("--- Users ---")
    users = User.objects.all()
    if not users.exists():
        print("No users found.")
    for u in users:
        print(f"User: {u.username}, Role: {u.role}, Groups: {[g.name for g in u.student_groups.all()]}")

    print("\n--- Groups ---")
    groups = Group.objects.all()
    if not groups.exists():
        print("No groups found.")
    for g in groups:
        print(f"Group: {g.name}, Modules: {[m.title for m in g.modules.all()]}")

    print("\n--- Modules ---")
    modules = Module.objects.all()
    if not modules.exists():
        print("No modules found.")
    for m in modules:
        print(f"Module (ID {m.id}): {m.title}, Target Groups: {[g.name for g in m.target_groups.all()]}, Materials: {[mat.title for mat in m.materials.all()]}")

    print("\n--- Module Materials ---")
    materials = ModuleMaterial.objects.all()
    if not materials.exists():
        print("No materials found.")
    for mat in materials:
        print(f"Material: {mat.title}, Module: {mat.module.title}, Path: {mat.file_path}")

except Exception as e:
    print(f"ERROR: {e}")

finally:
    sys.stdout.close()
