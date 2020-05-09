from datetime import datetime as dt

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.timezone import make_aware
from django.views.generic import TemplateView

from .models import PageView


class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'privacy_analytics/new.html'
    permission_required = 'page_analytics.view_pageview'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['views_per_visitor'] = PageView.objects.views_per_visitor(**kwargs)
        context['unique_visitors'] = PageView.objects.unique(**kwargs)
        context['total_views'] = PageView.objects.total_views(**kwargs)
        context['percent_authenticated'] = PageView.objects.percent_authenticated(**kwargs)
        context['referrers'] = PageView.objects.referrers(**kwargs)
        context['pages'] = PageView.objects.pages(**kwargs)

        context['messages'] = []

        return context
    



