from django.db.models import Manager, Count, Q, FloatField, Sum, F#, Subquery
from django.db.models.functions import Cast

class PageViewManager(Manager):
    def all(self, **kwargs):
        return self.filter(**kwargs)

    def all_unique_users(self, **kwargs):
        return self.filter(**kwargs).values('session_key').distinct()

    def average_page_view(self, **kwargs):
        return self.filter(**kwargs).values('session_key').aggregate(views=Cast(Count('pk'), FloatField()) / Cast(Count('session_key', distinct=True), FloatField()))

    def percent_authenticated(self, **kwargs):
        return self.filter(**kwargs) \
            .annotate(users=Cast(Count('pk', distinct=True), FloatField()), authenticated=Cast(Count('pk', filter=Q(is_authenticated=True)), FloatField())) \
            .aggregate(percent=Sum('authenticated') / Sum('users'))

    def all_referrers(self, **kwargs):
        return self.filter(**kwargs).values('referrer').annotate(total=Count('referrer')).order_by('-total')

    def all_paths(self, **kwargs):
        # Waiting for https://code.djangoproject.com/ticket/28296 to be fixed for subquery method with aggregates
        # GitHub pull request https://github.com/django/django/pull/11841
        # return self.filter(**kwargs).values('path').annotate(total=Subquery(self.filter(**kwargs).aggregate(Count('path')),percent=Count('path')/F('total'))

        total = Cast(self.filter(**kwargs).count(), FloatField())
        return self.filter(**kwargs).values('path').annotate(total=Count('path'), percent=Cast(F('total'), FloatField()) / total).order_by('-total')

    def delete_by_time(self, **kwargs):
        return self.filter(**kwargs).delete()

