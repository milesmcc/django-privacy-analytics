from django.contrib import admin
from .models import PageView

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "time", "referrer", "user_hash", "is_authenticated")