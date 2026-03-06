from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Module, Announcement, Notification, User, Group

@receiver(m2m_changed, sender=Module.target_groups.through)
def create_module_notifications(sender, instance, action, **kwargs):
    if action == "post_add":
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

@receiver(post_save, sender=Announcement)
def create_announcement_notifications(sender, instance, created, **kwargs):
    if created:
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
