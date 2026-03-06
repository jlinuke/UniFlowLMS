from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_user_hub_link_code_add_hub_integration_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('file_path', models.FileField(upload_to='modules/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='core.module')),
            ],
        ),
        migrations.RemoveField(
            model_name='module',
            name='file_path',
        ),
    ]
