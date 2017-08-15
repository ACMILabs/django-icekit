from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Redirect

class RedirectAdmin(admin.ModelAdmin):
    """
    A copy from django.contrib.redirects
    """
    list_display = ('old_path', 'new_path')
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path')
    radio_fields = {'site': admin.VERTICAL}

admin.site.register(Redirect, RedirectAdmin)


class RedirectInline(GenericTabularInline):
    model = Redirect
