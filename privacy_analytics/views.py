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

@user_passes_test(lambda user: user.is_superuser)
def dashboard(request):
    messages = []
    if request.method == "POST":
        if request.POST.get("action") == "clear":
            before = make_aware(datetime.strptime(request.POST.get("before"), "%Y-%m-%dT%H:%M"))
            def delete():
                PageView.objects.filter(time__lt=before).delete()
            threading.Thread(target=delete).start()
            messages.append({"content": "Deletion of all page views before %s has started in the background." % request.POST.get("before"),
            "classes": "is-success"})

    from_str = request.GET.get("from", "")
    if from_str == "":
        from_time = timezone.now() - timedelta(weeks=4)
    else:
        from_time = make_aware(datetime.strptime(from_str, "%Y-%m-%dT%H:%M"))
    until_str = request.GET.get("until", "")
    if until_str == "":
        until_time = timezone.now()
    else:
        until_time = make_aware(datetime.strptime(until_str, "%Y-%m-%dT%H:%M"))

    views = PageView.objects.filter(time__lt=until_time, time__gt=from_time)

    path = request.GET.get("path", "")
    if path != "":
        views = views.filter(path=path)

    views_per_visitor = mean([item["n"] for item in views.values("user_hash").annotate(n=models.Count("pk"))])
    unique_visitors = views.values("user_hash").distinct().count()
    total_views = views.count()
    percent_authenticated = views.filter(is_authenticated=True).count() * 100 / views.count()
    pages = sorted(views.values("path").annotate(n=models.Count("pk")), key=lambda k: k["n"], reverse=True)[:20]
    referrers = sorted(views.values("referrer").annotate(n=models.Count("pk")), key=lambda k: k["n"], reverse=True)[:20]
    
    for page in pages:
        page["percent"] = page["n"] * 100 / total_views

    return render(request, "privacy_analytics/dashboard.html", context={
        "from": from_time.strftime("%Y-%m-%dT%H:%M"),
        "until": until_time.strftime("%Y-%m-%dT%H:%M"),
        "views_per_visitor": views_per_visitor,
        "unique_visitors": unique_visitors,
        "total_views": total_views,
        "percent_authenticated": percent_authenticated,
        "path": path,
        "pages": pages,
        "referrers": referrers,
        "messages": messages
    })
