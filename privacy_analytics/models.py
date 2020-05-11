from django.db import models

from .managers import PageViewManager


class PageView(models.Model):
    agent = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    path = models.TextField()
    referrer = models.TextField(blank=True)
    session_key = models.TextField()
    is_authenticated = models.BooleanField()

    objects = PageViewManager()

    @staticmethod
    def create_for_request(**page):
        PageView.objects.create(**page)

    def __str__(self):
        return self.path
