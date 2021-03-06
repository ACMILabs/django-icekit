"""
URLconf for ``icekit_events`` app.
"""

# Prefix URL names with the app name. Avoid URL namespaces unless it is likely
# this app will be installed multiple times in a single project.

from django.conf.urls import url

from icekit_events.views import event, event_type

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$',
        event, name='icekit_events_eventbase_detail'),
    url(r'^types/(?P<slug>[\w-]+)/$',
        event_type, name='icekit_events_eventtype_detail'),
]
