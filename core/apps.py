from django.apps import AppConfig
import sys

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # We only import signals if we aren't running a management command (like migrate)
        # This prevents crashes during the very first deployment on Railway
        if 'manage.py' not in sys.argv:
            try:
                import core.signals
            except ImportError:
                pass