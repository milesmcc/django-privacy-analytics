from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import timedelta, make_aware
from django.db import models
from .models import PageView
from .util import mean
import threading

# @user_passes_test(lambda user: user.is_superuser)
# def dashboard(request):
#     messages = []
#     if request.method == "POST":
#         if request.POST.get("action") == "clear":
#             before = make_aware(datetime.strptime(request.POST.get("before"), "%Y-%m-%dT%H:%M"))
#             def delete():
#                 PageView.objects.filter(time__lt=before).delete()
#             threading.Thread(target=delete).start()
#             messages.append({"content": "Deletion of all page views before %s has started in the background." % request.POST.get("before"),
#             "classes": "is-success"})

#     from_str = request.GET.get("from", "")
#     if from_str == "":
#         from_time = timezone.now() - timedelta(weeks=4)
#     else:
#         from_time = make_aware(datetime.strptime(from_str, "%Y-%m-%dT%H:%M"))
#     until_str = request.GET.get("until", "")
#     if until_str == "":
#         until_time = timezone.now()
#     else:
#         until_time = make_aware(datetime.strptime(until_str, "%Y-%m-%dT%H:%M"))

#     views = PageView.objects.filter(time__lt=until_time, time__gt=from_time)

#     path = request.GET.get("path", "")
#     if path != "":
#         views = views.filter(path=path)

#     views_per_visitor = mean([item["n"] for item in views.values("session_key").annotate(n=models.Count("pk"))])
#     unique_visitors = views.values("session_key").distinct().count()
#     total_views = views.count()
#     percent_authenticated = views.filter(is_authenticated=True).count() * 100 / views.count()
#     pages = sorted(views.values("path").annotate(n=models.Count("pk")), key=lambda k: k["n"], reverse=True)[:20]
#     referrers = sorted(views.values("referrer").annotate(n=models.Count("pk")), key=lambda k: k["n"], reverse=True)[:20]
    
#     for page in pages:
#         page["percent"] = page["n"] * 100 / total_views

#     return render(request, "privacy_analytics/dashboard.html", context={
#         "from": from_time.strftime("%Y-%m-%dT%H:%M"),
#         "until": until_time.strftime("%Y-%m-%dT%H:%M"),
#         "views_per_visitor": views_per_visitor,
#         "unique_visitors": unique_visitors,
#         "total_views": total_views,
#         "percent_authenticated": percent_authenticated,
#         "path": path,
#         "pages": pages,
#         "referrers": referrers,
#         "messages": messages
#     })

from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.utils.timezone import now, timedelta as td
from django.views.generic import TemplateView

from .models import PageView
from .util import mean

class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = 'privacy_analytics/dashboard.html'
    permission_required = ('analytics.can_view',)
    analytics_filter = {}

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context['analytics_filter'] = self.analytics_filter
        context['views_per_visitor'] = PageView.objects.views_per_visitor(**kwargs)
        context['unique_visitors'] = PageView.objects.unique(**kwargs)
        context['total_views'] = PageView.objects.total_views(**kwargs)
        context['percent_authenticated'] = PageView.objects.percent_authenticated(**kwargs)
        context['referrers'] = PageView.objects.referrers(**kwargs)
        context['pages'] = PageView.objects.pages(**kwargs)

        return context
    



