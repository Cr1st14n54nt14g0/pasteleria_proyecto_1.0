from django.apps import AppConfig


class PasteleriaAppConfig(AppConfig):
    name = 'pasteleria_app'

def ready(self):
    import pasteleria_app.signals
