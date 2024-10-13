from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'


class YourAppConfig(AppConfig):
    name = 'students'

    def ready(self):
        import students.signals