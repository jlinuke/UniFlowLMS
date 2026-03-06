from django.shortcuts import redirect
from django.urls import reverse

class FirstLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # If student must change password and is not already on the change_password page
            if request.user.must_change_password and request.path != reverse('change_password') and not request.path.startswith('/admin/'):
                return redirect('change_password')
        
        response = self.get_response(request)
        return response

class StaffRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Prevent students from accessing /staff/
        if request.path.startswith('/staff/') and request.user.is_authenticated and not request.user.is_staff:
            return redirect('student_dashboard')
            
        response = self.get_response(request)
        return response
