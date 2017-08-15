from random import randint

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from icekit.fields import ICEkitURLField

from .utils import short_code_from_id
from django.conf import settings


@python_2_unicode_compatible
class Redirect(models.Model):
    """
    A simple model, database-superset of django.contrib.redirect, for sending one URL to another.

    We customise this model to generate short URLs if old_path isn't given, and to ensure slashes.
    """

    # redirect fields
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    old_path = models.CharField(_('redirect from'), max_length=200, db_index=True, blank=True,
        help_text=_("This can be any unused path, excluding the domain name. Example: '/kids'. "
                    "A short URL will be generated if this is left blank."))
    # this contrib.redirect field is now used as an 'override'.
    new_path = models.CharField(_('URL override'), max_length=200, blank=True,
        help_text=_("This can be either an absolute path (as above) or a full URL. Example: '/events/search/?q=kids'."))


    # GFK to a piece of content
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        db_table = 'django_redirect'
        unique_together = (('site', 'old_path'),)
        ordering = ('old_path',)

    def __str__(self):
        return "%s ---> %s" % (self.old_path, self.new_path)

    def save(self, *args, **kwargs):
        if not self.old_path:
            # we'll need to generate a short code. We want to use the DB ID. If we don't already have one, we
            # fake a value, save, and use that ID to generate the code.
            if not self.id:
                self.old_path = "__TEMPPATH_%s__" % randint(0,32000)
                super(Redirect, self).save(*args, **kwargs)
            self.old_path = short_code_from_id(self.id)

        if not self.old_path.startswith('/'):
            self.old_path = "/%s" % self.old_path

        super(Redirect, self).save(*args, **kwargs)
