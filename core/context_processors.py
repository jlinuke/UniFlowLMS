from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated and request.user.role == 'student':
        return {
            'global_notifications': Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
        }
    return {'global_notifications': []}
