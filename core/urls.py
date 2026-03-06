from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'students', api_views.StudentUserViewSet, basename='student')

urlpatterns = [
    # Dashboard Views
    path('', views.home_redirect, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    path('staff/', views.LecturerDashboardView.as_view(), name='lecturer_dashboard'),
    path('staff/activity/', views.ActivityLogView.as_view(), name='activity_log'),
    path('staff/batch-upload/', views.BatchUserUploadView.as_view(), name='batch_user_upload'),
    path('portal/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('portal/module/<int:pk>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('portal/autologin/<str:token>/', views.TokenLoginView.as_view(), name='token_login'),
    
    # API Endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/link-account/', api_views.LinkAccountAPIView.as_view(), name='api_link_account'),
    path('api/v1/my-modules/', api_views.MyModulesView.as_view(), name='api_my_modules'),
    path('api/v1/module-content/<int:pk>/', api_views.ModuleContentView.as_view(), name='api_module_content'),
    path('api/v1/announcements/', api_views.AnnouncementsView.as_view(), name='api_announcements'),
    path('api/v1/my-notifications/', api_views.MyNotificationsView.as_view(), name='api_my_notifications'),
]
