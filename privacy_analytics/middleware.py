from django.conf import settings

from .models import PageView


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.META.get('HTTP_DNT'):
            if hasattr(settings, 'ANALYTICS_IGNORE_PATHS'):
                if not any(request.path.startswith(path) for path in settings.ANALYTICS_IGNORE_PATHS):
                    if not request.session.session_key:
                        request.session.create()
                    PageView.create_for_request(request)
            else:
                PageView.create_for_request(request)

        return response
