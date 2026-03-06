from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Group, Module, Announcement, Notification

class LMSLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a lecturer
        self.lecturer = User.objects.create_user(
            username='lecturer1',
            password='password123',
            role='lecturer'
        )
        # Create a group
        self.group = Group.objects.create(name='CS-Year1')
        # Create a student
        self.student = User.objects.create_user(
            username='student1',
            password='password123',
            role='student',
            must_change_password=True
        )
        self.group.students.add(self.student)

    def test_first_login_redirection(self):
        """Verify student is redirected to change password on first login."""
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertRedirects(response, reverse('change_password'))

    def test_module_notification_signal(self):
        """Verify notification is created when a module is assigned to a group."""
        module = Module.objects.create(
            title='Test Module',
            uploaded_by=self.lecturer
        )
        # Trigger many-to-many signal
        module.target_groups.add(self.group)
        
        notification = Notification.objects.filter(recipient=self.student).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.type, 'module')
        self.assertIn('Test Module', notification.message)

    def test_announcement_notification_signal(self):
        """Verify notification is created for all students on announcement save."""
        Announcement.objects.create(
            title='Emergency',
            content='Test Content',
            uploaded_by=self.lecturer
        )
        notification = Notification.objects.filter(recipient=self.student, type='announcement').first()
        self.assertIsNotNone(notification)

    def test_staff_restriction_middleware(self):
        """Verify students cannot access staff views."""
        self.client.login(username='student1', password='password123')
        # Bypass first login for this test
        self.student.must_change_password = False
        self.student.save()
        
        response = self.client.get(reverse('lecturer_dashboard'))
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_api_access(self):
        """Verify API returns correct data for student."""
        self.client.login(username='student1', password='password123')
        self.student.must_change_password = False
        self.student.save()
        
        # Create a module for the student
        module = Module.objects.create(title='API Module', uploaded_by=self.lecturer)
        module.target_groups.add(self.group)
        
        response = self.client.get(reverse('api_my_modules'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], 'API Module')
