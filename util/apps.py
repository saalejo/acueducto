from django.apps import AppConfig


class UtilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'util'

    def ready(self):
            import util.signals
