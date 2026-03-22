import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniflow_lms.settings')
django.setup()

from core.models import Module, ModuleWeek, ModuleMaterial, User

mod = Module.objects.first()

if mod:
    print(f"Module: {mod.title}")
    # Create week
    week, _ = ModuleWeek.objects.get_or_create(module=mod, week_number=1, defaults={'title': 'Week 1 - Test'})
    # Create material
    ModuleMaterial.objects.get_or_create(week=week, module=mod, title="Test Mat", defaults={'file_path': "test.pdf"})

    # Now verify the API Output
    from core.serializers import ModuleSerializer, ModuleWeekSerializer
    print("ModuleWeekSerializer Output:")
    print(ModuleWeekSerializer(week).data)
    print("ModuleSerializer Output:")
    import json
    print(json.dumps(ModuleSerializer(mod).data, indent=2))
else:
    print("No module found.")
