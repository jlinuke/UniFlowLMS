import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import User

def check_users():
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    for user in users:
        print(f"- Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  Is Staff: {user.is_staff}")
        print(f"  Is Superuser: {user.is_superuser}")
        print(f"  Must Change Password: {user.must_change_password}")
        print("-" * 20)

if __name__ == "__main__":
    check_users()
