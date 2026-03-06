from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Group, Module, ModuleMaterial, Announcement, Notification, LoginLog

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'must_change_password', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('LMS Profile', {'fields': ('role', 'must_change_password')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('LMS Profile', {'fields': ('role', 'must_change_password')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group)
admin.site.register(Module)
admin.site.register(ModuleMaterial)
admin.site.register(Announcement)
admin.site.register(Notification)
admin.site.register(LoginLog)
