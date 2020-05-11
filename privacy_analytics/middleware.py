from django.conf import settings

import tasks


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
                    tasks.create_pageview(request)
            else:
                tasks.create_pageview.delay(request)
        return response
