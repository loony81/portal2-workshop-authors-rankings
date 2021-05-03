from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'

    def ready(self):
        print("Scheduler started...")
        from .authorsUpdater import scheduler
        scheduler.start()
