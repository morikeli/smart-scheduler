from django.apps import AppConfig


class CampusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campus'

    def ready(self):
        import campus.signals