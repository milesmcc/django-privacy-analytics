from django.db import models
from .util import get_user_hash

class PageView(models.Model):
    agent = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    referrer = models.TextField(blank=True)
    session_key = models.TextField()
    is_authenticated = models.BooleanField()

    objects = models.Manager()

    @staticmethod
    def create_for_request(request):
        PageView.objects.create(
            agent=request.META.get('HTTP_USER_AGENT', ""),
            path=request.path,
            referrer=request.META.get('HTTP_REFERER', ""),
            session_key=request.session_key,
            is_authenticated=request.user.is_authenticated
        )

    def __str__(self):
        return self.path