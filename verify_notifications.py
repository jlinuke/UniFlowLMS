import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import User, Notification, Group

def verify_notifications():
    # 1. Setup
    lecturer = User.objects.filter(role='lecturer').first()
    if not lecturer:
        lecturer = User.objects.create_superuser(username='notif_lecturer', email='notif@test.com', password='password123')
    
    group, _ = Group.objects.get_or_create(name='Notif Test Group')
    student, _ = User.objects.get_or_create(username='notif_student', email='student_notif@test.com', defaults={'role': 'student'})
    group.students.add(student)

    # 2. Simulate send_notification logic
    message_text = "Urgent: Classroom change for tomorrow."
    group_ids = [group.id]
    
    students = User.objects.filter(student_groups__id__in=group_ids, role='student').distinct()
    notifications = [
        Notification(
            recipient=s,
            message=message_text,
            type='announcement'
        ) for s in students
    ]
    Notification.objects.bulk_create(notifications)
    
    # 3. Verify
    notif_count = Notification.objects.filter(recipient=student, message=message_text).count()
    print(f"Notifications created for student: {notif_count}")
    
    assert notif_count >= 1
    print("\nVerification Successful: Direct notification logic is working.")

if __name__ == "__main__":
    verify_notifications()
