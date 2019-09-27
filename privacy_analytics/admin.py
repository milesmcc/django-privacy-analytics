from django.contrib import admin
from .models import PageView

class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "time", "referrer", "user_hash", "is_authenticated")
admin.site.register(PageView, PageViewAdmin)