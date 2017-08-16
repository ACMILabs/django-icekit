from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from icekit.admin_tools.utils import admin_link

from .models import Redirect


class RedirectForm(forms.ModelForm):

    class Meta:
        model = Redirect
        fields = ('source_site', 'source_path', 'destination_path', 'destination_object_params', ) # GFKs not editable.

    def clean(self):
        new_path = self.cleaned_data.get('destination_path')
        content_type = self.cleaned_data.get('content_type')
        object_id = self.cleaned_data.get('object_id')
        if not new_path and (not content_type or not object_id):
            raise forms.ValidationError("Redirects must have a URL to direct to.")

        return self.cleaned_data


class RedirectAdmin(admin.ModelAdmin, ):
    """
    A copy from django.contrib.redirects
    """
    form = RedirectForm
    list_display = ('get_src_url', 'get_dst_url', 'try_it')
    list_filter = ('source_site',)
    search_fields = ('source_path', 'destination_path')
    fieldsets = (
        (None, {
            'fields': ('source_site', 'source_path', 'destination_path', 'destination_object_link',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('destination_site', 'destination_object_params', ),
        }),
    )

    readonly_fields = ('destination_object_link',)

    radio_fields = {'source_site': admin.VERTICAL, 'destination_site': admin.VERTICAL}

    def try_it(self, obj):
        source_url = obj.get_source_url()
        destination_url = obj.get_destination_url()
        return "<a href='%s'><i class='fa fa-circle'></i></a>&nbsp;-->&nbsp;<a href='%s'><i class='fa fa-circle'></i></a>" % (source_url, destination_url)
    try_it.allow_tags = True

    def get_src_url(self, obj):
        return obj.get_source_url()
    get_src_url.short_description = "source URL"
    get_src_url.admin_order_field = "source_path"

    def get_dst_url(self, obj):
        return obj.get_destination_url(include_params=False)
    get_dst_url.short_description = "destination URL"
    get_dst_url.admin_order_field = "destination_path"

    def destination_object_link(self, obj):
        if obj.destination_object:
            return admin_link(obj.destination_object)
        return ""
    destination_object_link.allow_tags = True


class RedirectInline(GenericTabularInline):
    model = Redirect
    exclude = ('destination_path', 'destination_site')
    extra = 1


admin.site.register(Redirect, RedirectAdmin)
