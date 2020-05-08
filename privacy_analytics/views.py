from datetime import datetime as dt

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.timezone import make_aware
from django.views.generic import TemplateView

from .models import PageView


class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'privacy_analytics/dashboard.html'
    permission_required = ('analytics.can_view',)

    def get_context_data(self, **kwargs):
        params = { k: v for k, v in self.request.GET.items() if v }

        context = super().get_context_data(**kwargs)
        
        context['views_per_visitor'] = PageView.objects.views_per_visitor(**params)
        context['unique_visitors'] = PageView.objects.unique(**params)
        context['total_views'] = PageView.objects.total_views(**params)
        context['percent_authenticated'] = PageView.objects.percent_authenticated(**params)
        context['referrers'] = PageView.objects.referrers(**params)
        context['pages'] = PageView.objects.pages(**params)

        context['messages'] = []
        context['start'], context['end'], context['path'] = params.values() if params else [None, None, '']

        return context
    



