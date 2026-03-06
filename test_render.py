import os
import django
from django.test import RequestFactory
from core.views import StudentDashboardView, LecturerDashboardView
from core.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

rf = RequestFactory()

def test_view(view_class, username):
    try:
        user = User.objects.get(username=username)
        request = rf.get('/debug/')
        request.user = user
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, '_messages', FallbackStorage(request))
        
        view = view_class.as_view()
        response = view(request)
        print(f"SUCCESS: {view_class.__name__} for {username}")
        return response
    except Exception as e:
        print(f"FAILURE: {view_class.__name__} for {username} - {e}")
        import traceback
        traceback.print_exc()
        return None

with open('render_test.log', 'w') as f:
    import sys
    sys.stdout = f
    sys.stderr = f
    
    # Test for a student
    student = User.objects.filter(role='student').first()
    if student:
        test_view(StudentDashboardView, student.username)
    else:
        print("No student found to test.")
        
    # Test for a lecturer
    lecturer = User.objects.filter(role='lecturer').first()
    if lecturer:
        test_view(LecturerDashboardView, lecturer.username)
    else:
        print("No lecturer found to test.")
