import threading
import queue

from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore

from .models import PageView


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.processing_queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self._thread_run)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def _thread_run(self):
        while True:
           PageView.create_for_request(self.processing_queue.get())
           # Will lock until item is available

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(settings, "ANALYTICS_IGNORE_PATHS"):
            for path in settings.ANALYTICS_IGNORE_PATHS:
                if request.path.startswith(path):
                    return response
        self.processing_queue.put_nowait(request)
        return response

class NewAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if not request.Meta.get('HTTP_DNT'):
            if hasattr(settings, 'ANALYTICS_IGNORE_PATHS'):
                if not any(request.path.startswith(path) for path in settings.ANALYTICS_IGNORE_PATHS):
                    PageView.create_for_request(request)
        
        return response



        