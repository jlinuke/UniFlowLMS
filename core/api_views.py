from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import Module, Announcement, User, Notification
from .serializers import ModuleSerializer, AnnouncementSerializer, StudentUserSerializer, NotificationSerializer, ModuleMaterialSerializer

class StudentUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='student')
    serializer_class = StudentUserSerializer
    permission_classes = [permissions.IsAdminUser]

class LinkAccountAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate using email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.role == 'student':
            user.hub_integration_enabled = True
            user.hub_linked_at = timezone.now()
            user.save()
            
            return Response({
                "status": "success",
                "message": f"Account {email} successfully linked and integration activated.",
                "linked_at": user.hub_linked_at
            })
        else:
            return Response({
                "status": "error",
                "message": "Invalid credentials or unauthorized role."
            }, status=401)

class MyModulesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can access this endpoint."}, status=403)
        
        # Get modules targeted to groups the student is in
        modules = Module.objects.filter(target_groups__students=request.user).distinct()
        serializer = ModuleSerializer(modules, many=True, context={'request': request})
        return Response(serializer.data)

class ModuleContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.role != 'student':
            return Response({"error": "Only students can access this endpoint."}, status=403)
        
        # Verify student has access to this module via their groups
        module = get_object_or_404(Module, pk=pk, target_groups__students=request.user)
        materials = module.materials.all()
        serializer = ModuleMaterialSerializer(materials, many=True, context={'request': request})
        return Response({
            "module_id": module.id,
            "module_title": module.title,
            "content": serializer.data
        })

class AnnouncementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        announcements = Announcement.objects.all().order_by('-created_at')
        serializer = AnnouncementSerializer(announcements, many=True, context={'request': request})
        return Response(serializer.data)

class MyNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'student':
            return Response({"error": "Only students can access this endpoint."}, status=403)
        
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True, context={'request': request})
        return Response(serializer.data)
