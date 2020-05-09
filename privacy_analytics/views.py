from datetime import datetime as dt

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from .models import PageView

    
class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'privacy_analytics/dashboard.html'
    permission_required = 'page_analytics.view_pageview'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start = timezone.now().replace(hour=0, minute=0, second=0)
        end = timezone.now().replace(hour=23, minute=59, second=59)

        object_filter = {'time__gte': self.request.GET.get('time__gte', start), 'time__lte': self.request.GET.get('time__lte', end)}
        
        context['views_per_visitor'] = PageView.objects.views_per_visitor(**object_filter)
        context['unique_visitors'] = PageView.objects.unique(**object_filter)
        context['total_views'] = PageView.objects.total_views(**object_filter)
        context['percent_authenticated'] = PageView.objects.percent_authenticated(**object_filter)
        context['referrers'] = PageView.objects.referrers(**object_filter)
        context['pages'] = PageView.objects.pages(**object_filter)

        context['messages'] = []

        return context


