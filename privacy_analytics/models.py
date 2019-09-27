from django.db import models
from .util import get_user_hash

class PageView(models.Model):
    agent = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    referrer = models.TextField(blank=True)
    user_hash = models.TextField()
    is_authenticated = models.BooleanField()

    @staticmethod
    def create_for_request(request):
        if request.META.get('HTTP_DNT', '0') == '1':
            return

        agent = request.META.get('HTTP_USER_AGENT', "")
        path = request.path
        referrer = request.META.get('HTTP_REFERER', "")
        user_hash = get_user_hash(request)
        is_authenticated = request.user.is_authenticated

        PageView.objects.create(
            agent=agent,
            path=path,
            referrer=referrer,
            user_hash=user_hash,
            is_authenticated=is_authenticated
        )

    def __str__(self):
        return self.path