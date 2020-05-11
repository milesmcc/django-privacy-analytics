from celery import shared_task

from .models import PageView


@shared_task
def create_pageview(request):
    return PageView.create_for_request(request)
