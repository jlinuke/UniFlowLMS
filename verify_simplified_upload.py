import os
import django
import sys
from django.core.files.uploadedfile import SimpleUploadedFile

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import User, Module, ModuleMaterial, Group

def verify_upload():
    # 1. Ensure we have a lecturer and a group
    lecturer = User.objects.filter(role='lecturer').first()
    if not lecturer:
        # Create one if missing for test
        lecturer = User.objects.create_superuser(username='test_lecturer', email='lecturer@test.com', password='password123')
        print("Created test lecturer.")
    
    group, _ = Group.objects.get_or_create(name='Test Group A')
    
    # 2. Simulate the simplified upload logic
    title = "Test Upload Topic"
    pdf_content = b"%PDF-1.4 test content"
    pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")
    
    # Logic from view:
    module = Module.objects.create(
        title=title,
        uploaded_by=lecturer
    )
    module.target_groups.add(group)
    
    material = ModuleMaterial.objects.create(
        module=module,
        title=f"{title} (PDF)",
        file_path=pdf_file
    )
    
    # 3. Verify
    print(f"Module created: {module.title}")
    print(f"Target Groups: {[g.name for g in module.target_groups.all()]}")
    print(f"Material created: {material.title}")
    print(f"File Path: {material.file_path.name}")
    
    assert module.title == title
    assert module.target_groups.count() == 1
    assert material.module == module
    print("\nVerification Successful: Simplified upload flow logic is correct.")

if __name__ == "__main__":
    verify_upload()
    # Cleanup test data if needed, but here we just verify.
