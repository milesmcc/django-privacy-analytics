from datetime import datetime as dt

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.timezone import now, make_aware
from django.views.generic import TemplateView

from .models import PageView

    
class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'privacy_analytics/dashboard.html'
    permission_required = 'page_analytics.view_pageview'

    messages = []

    def get(self, request, *args, **kwargs):
        if request.GET.get('action') == 'clear':
            before = make_aware(dt.strptime(request.POST.get('start'), '%Y-%m-%dT%H:%M'))
            PageView.objects.clear_by_time(**{'time__lt': before})

            self.messages.append({'content': f'Deletion of all page views before {before} has started in the background.',
            "classes": "is-success"})

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start = now().replace(hour=0, minute=0, second=0)
        end = now().replace(hour=23, minute=59, second=59)

        object_filter = {'time__gte': self.request.GET.get('time__gte', start), 'time__lte': self.request.GET.get('time__lte', end)}
        
        context['object_filter'] = object_filter
        context['views_per_visitor'] = PageView.objects.views_per_visitor(**object_filter)
        context['unique_visitors'] = PageView.objects.unique(**object_filter)
        context['total_views'] = PageView.objects.total_views(**object_filter)
        context['percent_authenticated'] = PageView.objects.percent_authenticated(**object_filter)
        context['referrers'] = PageView.objects.referrers(**object_filter)
        context['pages'] = PageView.objects.pages(**object_filter)

        context['messages'] = self.messages

        return context



