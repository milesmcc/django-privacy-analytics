from .models import PageView
import threading
import queue
from django.conf import settings

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