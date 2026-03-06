import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.api_views import MyNotificationsView, ModuleContentView
from core.models import Module, Notification, Group

User = get_user_model()

def verify():
    # 1. Setup Test Data
    student, _ = User.objects.get_or_create(email='test_student@example.com', defaults={'username': 'test_student', 'role': 'student'})
    student.set_password('password123')
    student.save()

    lecturer, _ = User.objects.get_or_create(email='test_lecturer@example.com', defaults={'username': 'test_lecturer', 'role': 'lecturer'})
    
    group, _ = Group.objects.get_or_create(name='Test Group')
    group.students.add(student)

    module, _ = Module.objects.get_or_create(
        title='Test API Module', 
        uploaded_by=lecturer,
        defaults={'description': 'API Test'}
    )
    module.target_groups.add(group)

    Notification.objects.get_or_create(
        recipient=student,
        message='Test API Notification',
        type='module'
    )

    factory = RequestFactory()

    # 2. Test MyNotificationsView
    print("Testing MyNotificationsView...")
    request = factory.get('/api/v1/my-notifications/')
    request.user = student
    view = MyNotificationsView.as_view()
    response = view(request)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 200
    assert len(response.data) >= 1

    # 3. Test ModuleContentView
    print("\nTesting ModuleContentView...")
    request = factory.get(f'/api/v1/module-content/{module.id}/')
    request.user = student
    view = ModuleContentView.as_view()
    response = view(request, pk=module.id)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    assert response.status_code == 200
    assert response.data['module_id'] == module.id

    print("\nAPI Verification Successful!")

if __name__ == "__main__":
    verify()
