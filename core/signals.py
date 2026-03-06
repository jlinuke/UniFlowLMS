from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

# DO NOT import models at the top level here. 
# It causes a circular dependency during app initialization.

@receiver(m2m_changed, sender='core.Module_target_groups') # Use string reference for the through model
def create_module_notifications(sender, instance, action, **kwargs):
    if action == "post_add":
        # Import models INSIDE the function
        from .models import User, Notification
        
        # Get all students in the newly added groups
        student_ids = User.objects.filter(
            student_groups__in=instance.target_groups.all(),
            role='student'
        ).distinct().values_list('id', flat=True)
        
        notifications = [
            Notification(
                recipient_id=student_id,
                message=f"New module uploaded: {instance.title}",
                type='module'
            ) for student_id in student_ids
        ]
        Notification.objects.bulk_create(notifications)

@receiver(post_save, sender='core.Announcement') # Use string reference 'app_label.ModelName'
def create_announcement_notifications(sender, instance, created, **kwargs):
    if created:
        # Import models INSIDE the function
        from .models import User, Notification
        
        # Announcements go to EVERY student
        student_ids = User.objects.filter(role='student').values_list('id', flat=True)
        
        notifications = [
            Notification(
                recipient_id=student_id,
                message=f"Emergency Announcement: {instance.title}",
                type='announcement'
            ) for student_id in student_ids
        ]
        Notification.objects.bulk_create(notifications)