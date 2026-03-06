from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

# IMPORTANT: No model imports at the top level to avoid Circular Imports.

@receiver(m2m_changed, sender='core.Module_target_groups')
def create_module_notifications(sender, instance, action, **kwargs):
    """Sends notifications when a Module is assigned to Groups."""
    if action == "post_add":
        from .models import User, Notification
        
        # Get students in the newly assigned groups
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
        
        if notifications:
            Notification.objects.bulk_create(notifications)

@receiver(post_save, sender='core.Announcement')
def create_announcement_notifications(sender, instance, created, **kwargs):
    """Sends notifications to all students when a new Announcement is created."""
    if created:
        from .models import User, Notification
        
        # Announcements go to all users with the student role
        student_ids = User.objects.filter(role='student').values_list('id', flat=True)
        
        notifications = [
            Notification(
                recipient_id=student_id,
                message=f"Emergency Announcement: {instance.title}",
                type='announcement'
            ) for student_id in student_ids
        ]
        
        if notifications:
            Notification.objects.bulk_create(notifications)