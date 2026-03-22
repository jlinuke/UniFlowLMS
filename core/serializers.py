from rest_framework import serializers
from .models import Module, ModuleMaterial, Announcement, Notification, Group, User, ModuleWeek

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class ModuleMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleMaterial
        fields = ['id', 'title', 'file_path', 'uploaded_at']

class ModuleWeekSerializer(serializers.ModelSerializer):
    materials = ModuleMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ModuleWeek
        fields = ['id', 'week_number', 'title', 'description', 'materials']

class ModuleSerializer(serializers.ModelSerializer):
    weeks = ModuleWeekSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'weeks', 'uploaded_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'type', 'is_read', 'created_at']

# NEW: Required for the Admin to create/manage students via the API
class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']