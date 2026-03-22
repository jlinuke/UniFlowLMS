from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    must_change_password = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Hub Integration Fields
    hub_integration_enabled = models.BooleanField(default=False)
    hub_linked_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_lecturer(self):
        return self.role == 'lecturer' or self.is_superuser

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'lecturer'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    login_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_at}"

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField(User, related_name='student_groups', limit_choices_to={'role': 'student'})

    def __str__(self):
        return self.name

class Module(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_groups = models.ManyToManyField(Group, related_name='modules')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_modules', limit_choices_to={'role': 'lecturer'})
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ModuleWeek(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200, default='New Week')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('module', 'week_number')
        ordering = ['week_number']

    def __str__(self):
        return f"Week {self.week_number} - {self.title} ({self.module.title})"

class ModuleMaterial(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='materials_old', null=True, blank=True)
    week = models.ForeignKey(ModuleWeek, on_delete=models.CASCADE, related_name='materials', null=True, blank=True)
    title = models.CharField(max_length=200)
    file_path = models.FileField(upload_to='modules/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        module_title = self.week.module.title if self.week else (self.module.title if self.module else "Unknown")
        return f"{self.title} ({module_title})"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements', limit_choices_to={'role': 'lecturer'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    TYPE_CHOICES = (
        ('module', 'New Module'),
        ('announcement', 'New Announcement'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:20]}..."
