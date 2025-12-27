from django.apps import AppConfig


class DonationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.donations"
    verbose_name = "Donations"
    
    def ready(self):
        # Import signals to register them
        from . import signals  # noqa

