from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_hub_link_code_user_hub_linked_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='hub_link_code',
        ),
        migrations.AddField(
            model_name='user',
            name='hub_integration_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
