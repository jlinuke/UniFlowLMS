import os
import django
import json
from django.test import RequestFactory
from core.api_views import MyModulesView
from core.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

rf = RequestFactory()

def test_api():
    try:
        student = User.objects.filter(role='student').first()
        if not student:
            print("No student found.")
            return

        request = rf.get('/api/v1/my-modules/')
        request.user = student
        
        view = MyModulesView.as_view()
        response = view(request)
        
        print(f"API STATUS: {response.status_code}")
        if response.status_code == 200:
            print("API DATA PREVIEW:")
            print(json.dumps(response.data[:2], indent=2))
        else:
            print(f"API ERROR: {response.data}")
            
    except Exception as e:
        print(f"API CRASH: {e}")
        import traceback
        traceback.print_exc()

with open('api_verify.log', 'w') as f:
    import sys
    sys.stdout = f
    sys.stderr = f
    test_api()
