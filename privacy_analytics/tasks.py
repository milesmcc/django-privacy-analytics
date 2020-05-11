from celery import shared_task

from .models import PageView

@shared_task
def pageview_add_task(**request):
    return PageView.create_for_request(**request)