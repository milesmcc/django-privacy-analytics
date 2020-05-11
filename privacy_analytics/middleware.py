from django.conf import settings

from . import tasks


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.META.get('HTTP_DNT'):
            page = {
                'agent': request.META.get('HTTP_USER_AGENT', ''),
                'path': request.path,
                'referrer': request.META.get('HTTP_REFERRER', ''),
                'session_key': request.session.session_key,
                'is_authenticated': request.user.is_authenticated
            }

            if hasattr(settings, 'ANALYTICS_IGNORE_PATHS'):
                if not any(request.path.startswith(path) for path in settings.ANALYTICS_IGNORE_PATHS):
                    if not request.session.session_key:
                        request.session.create()
                    tasks.pageview_add_task(**page)
            else:
                tasks.pageview_add_task(**page)
        return response
