from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
import csv
import io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import User, Module, ModuleMaterial, Announcement, Notification, Group, LoginLog
from django.contrib.auth.forms import PasswordChangeForm
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import secrets
from django.conf import settings

def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_lecturer:
        return redirect('lecturer_dashboard')
    return redirect('student_dashboard')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    
    def form_valid(self, form):
        role_select = self.request.POST.get('role_select')
        user = form.get_user()
        
        # Validation: Check if the selected role matches the user's role
        if role_select == 'lecturer' and not (user.role == 'lecturer' or user.is_staff):
            messages.error(self.request, "This account is a student account. Please login as a student.")
            return self.form_invalid(form)
        if role_select == 'student' and (user.role == 'lecturer' or user.is_staff):
            messages.error(self.request, "This account is a staff account. Please login as staff.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        # Create a login log
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        LoginLog.objects.create(user=self.request.user, ip_address=ip)
        return response

    def get_success_url(self):
        user = self.request.user
        if user.must_change_password:
            return reverse('change_password')
        if user.is_lecturer:
            return reverse('lecturer_dashboard')
        return reverse('student_dashboard')

def logout_view(request):
    logout(request)
    return redirect('login')


class TokenLoginView(View):
    def get(self, request, token):
        signer = TimestampSigner(salt=settings.UNIFLOW_SSO_SECRET)
        try:
            # Token valid for 10 minutes for easier cross-system sync
            email = signer.unsign(token, max_age=600)
            user = get_object_or_404(User, email=email)
            
            # Log the user in
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            
            # Redirect to home_redirect logic
            return home_redirect(request)
            
        except SignatureExpired:
            messages.error(request, "The login link has expired. Please try again from UniFlow Hub.")
        except BadSignature:
            messages.error(request, "Invalid login link.")
            
        return redirect('login')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'core/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            user.must_change_password = False
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        return render(request, 'core/change_password.html', {'form': form})

class LecturerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'lecturer' and not request.user.is_staff:
            return redirect('student_dashboard')
        
        students = User.objects.filter(role='student')
        modules = Module.objects.all()
        announcements = Announcement.objects.all()
        
        groups = Group.objects.all()
        
        context = {
            'students': students,
            'modules': modules,
            'announcements': announcements,
            'groups': groups,
        }
        return render(request, 'core/lecturer_dashboard.html', context)

    def post(self, request):
        if not request.user.is_lecturer:
            return redirect('student_dashboard')
            
        action = request.POST.get('action')
        if action == 'add_student':
            full_name = request.POST.get('full_name')
            student_id = request.POST.get('student_id')
            email = request.POST.get('email')
            password = request.POST.get('password')
            group_id = request.POST.get('group')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "A student with this email already exists.")
            else:
                user = User.objects.create_user(
                    username=student_id,
                    email=email,
                    password=password,
                    first_name=full_name.split(' ')[0],
                    last_name=' '.join(full_name.split(' ')[1:]) if ' ' in full_name else '',
                    role='student',
                    must_change_password=True
                )
                if group_id:
                    group = get_object_or_404(Group, id=group_id)
                    group.students.add(user)
                    
                messages.success(request, f"Student {full_name} added successfully.")
        
        elif action == 'simplified_upload':
            title = request.POST.get('title')
            existing_module_id = request.POST.get('existing_module_id')
            pdf_file = request.FILES.get('pdf_file')
            group_ids = request.POST.getlist('target_groups')
            
            if not pdf_file:
                messages.error(request, "Please select a PDF file.")
            elif not group_ids and not existing_module_id:
                messages.error(request, "Please select at least one group or an existing topic.")
            else:
                if existing_module_id:
                    module = get_object_or_404(Module, id=existing_module_id)
                    # Optionally update groups if provided
                    if group_ids:
                        groups = Group.objects.filter(id__in=group_ids)
                        module.target_groups.add(*groups)
                else:
                    # Create new Module
                    module = Module.objects.create(
                        title=title,
                        uploaded_by=request.user
                    )
                    if group_ids:
                        groups = Group.objects.filter(id__in=group_ids)
                        module.target_groups.set(groups)
                
                # Create the Material inside the module
                material_title = request.POST.get('material_title') or (f"{title} (PDF)" if title else pdf_file.name)
                ModuleMaterial.objects.create(
                    module=module,
                    title=material_title,
                    file_path=pdf_file
                )
                messages.success(request, f"Successfully added '{material_title}' to Topic: {module.title}.")

        elif action == 'send_notification':
            message_text = request.POST.get('message')
            group_ids = request.POST.getlist('target_groups')
            
            if not message_text:
                messages.error(request, "Please enter a message.")
            elif not group_ids:
                messages.error(request, "Please select at least one group.")
            else:
                students = User.objects.filter(student_groups__id__in=group_ids, role='student').distinct()
                notifications = [
                    Notification(
                        recipient=student,
                        message=message_text,
                        type='announcement'
                    ) for student in students
                ]
                Notification.objects.bulk_create(notifications)
                messages.success(request, f"Notification sent to {students.count()} students across {len(group_ids)} groups.")

        return redirect('lecturer_dashboard')

class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role == 'lecturer' or request.user.is_staff:
            return redirect('lecturer_dashboard')
            
        student_groups = request.user.student_groups.all().prefetch_related('modules', 'modules__materials')
        
        # Prepare data for JSON script
        group_modules_data = {}
        for group in student_groups:
            module_list = []
            for module in group.modules.all():
                module_list.append({
                    "id": str(module.id),
                    "title": module.title,
                    "desc": (module.description or "")[:250],
                    "materials": [
                        {
                            "title": mat.title,
                            "url": mat.file_path.url
                        } for mat in module.materials.all()
                    ]
                })
            group_modules_data[str(group.id)] = {
                "name": group.name,
                "modules": module_list
            }

        announcements = Announcement.objects.all().order_by('-created_at')
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        
        context = {
            'student_groups': student_groups,
            'group_modules_data': group_modules_data,
            'announcements': announcements,
            'notifications': notifications,
        }
        return render(request, 'core/student_dashboard.html', context)

class ModuleDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        module = get_object_or_404(Module.objects.prefetch_related('materials'), pk=pk)
        
        # Check permission: student must be in a target group
        if request.user.role == 'student':
            user_groups = request.user.student_groups.all()
            if not module.target_groups.filter(id__in=user_groups).exists():
                messages.error(request, "You do not have permission to view this module.")
                return redirect('student_dashboard')
        
        return render(request, 'core/module_detail.html', {'module': module})

class ActivityLogView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'lecturer' and not request.user.is_staff:
            return redirect('student_dashboard')
        
        logs = LoginLog.objects.all().order_by('-login_at')
        return render(request, 'core/activity_log.html', {'logs': logs})

class BatchUserUploadView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'lecturer' and not request.user.is_staff:
            return redirect('student_dashboard')
        groups = Group.objects.all()
        return render(request, 'core/batch_upload.html', {'groups': groups})

    def post(self, request):
        if request.user.role != 'lecturer' and not request.user.is_staff:
            return redirect('student_dashboard')
            
        csv_file = request.FILES.get('csv_file')
        group_id = request.POST.get('group')
        
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('batch_user_upload')

        try:
            group = Group.objects.get(id=group_id)
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) # Skip header
            
            created_count = 0
            for row in csv.reader(io_string, delimiter=',', quotechar='|'):
                # Expected CSV: username,email,full_name,temp_password
                if len(row) < 4: continue
                username, email, full_name, temp_password = row
                
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=temp_password,
                        first_name=full_name.split(' ')[0],
                        last_name=' '.join(full_name.split(' ')[1:]) if ' ' in full_name else '',
                        role='student',
                        must_change_password=True
                    )
                    group.students.add(user)
                    created_count += 1
            
            messages.success(request, f'Successfully created {created_count} students.')
        except Exception as e:
            messages.error(request, f'Error processing CSV: {str(e)}')
            
        return redirect('lecturer_dashboard')
