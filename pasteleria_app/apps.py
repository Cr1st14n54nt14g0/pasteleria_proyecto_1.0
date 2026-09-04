from django.apps import AppConfig

class PasteleriaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pasteleria_app'

    def ready(self):
        import pasteleria_app.signals