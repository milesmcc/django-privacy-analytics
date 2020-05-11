from datetime import datetime as dt

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.timezone import now, make_aware
from django.views.generic import TemplateView, RedirectView

from .models import PageView

    
class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'privacy_analytics/dashboard.html'
    permission_required = 'page_analytics.view_pageview'

    messages = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filters = {k: v for k, v in self.request.GET.items() if v}

        context['total_views'] = PageView.objects.all(**filters)
        context['unique'] = PageView.objects.all_unique_users(**filters)
        context['percent_authenticated'] = PageView.objects.percent_authenticated(**filters)
        context['referrers'] = PageView.objects.all_referrers(**filters)
        context['paths'] = PageView.objects.all_paths(**filters)
        context['average_per_visitor'] = PageView.objects.average_page_view(**filters)
        context['messages'] = self.messages
        print(len(context['paths']))
        return context


class DashboardRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'analytics:dashboard'

    def get_redirect_url(self, *args, **kwargs):
        PageView.objects.delete_by_time(**kwargs)
        return super().get_redirect_url(*args, **kwargs)
