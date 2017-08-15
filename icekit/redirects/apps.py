from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class AppConfig(AppConfig):
    name = '.'.join(__name__.split('.')[:-1])
    label = 'redirects'
    verbose_name = _("Redirects")
