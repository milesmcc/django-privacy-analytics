from django.db.models import Manager, Avg, Count, Q, FloatField
from django.db.models.functions import Cast


class PageViewManager(Manager):
    def unique(self, **kwargs):
        return self.filter(**kwargs).values('session_key').distinct().count()

    def views_per_visitor(self, **kwargs):
        return self.filter(**kwargs).values('session_key').annotate(total=Count('pk')).aggregate(Avg('total'))

    def total_views(self, **kwargs):
        return self.filter(**kwargs).values('session_key').count()

    def percent_authenticated(self, **kwargs):
        return self.filter(**kwargs).aggregate(total=(Cast(Count('is_authenticated', filter=Q(is_authenticated=True)), FloatField()) / Cast(Count('pk'), FloatField())) * 100.00)
    
    def referrers(self, **kwargs):
        return self.filter(**kwargs).values('referrer').annotate(total=Count('pk')).all()[:10]
    
    def pages(self, **kwargs):
        return self.filter(**kwargs).values('path').annotate(total=Count('pk'), percent=(Count('pk') * 100) / self.filter(**kwargs).all().count()).order_by('-total')
    
    def clear_by_time(self, **kwargs):
        return self.filter(**kwargs).all().remove()