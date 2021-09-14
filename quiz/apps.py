from django.apps import AppConfig
from django.core.signals import request_finished

class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'

    #[KIV]
    def ready(self):
        from .views import check_url
        #from .tasks import check_url
        from urllib import request
        request_finished.connect(check_url, request)
