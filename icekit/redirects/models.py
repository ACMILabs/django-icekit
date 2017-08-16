from random import randint
from urlparse import urlparse, urljoin

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .utils import short_code_from_id

"""
The default Django `redirect` implementation has the following limitations:

    - source site and destination Site must be the same. We want to be able to specify different Sites, in order to
      be able to use a short URL domain name that redirects to the (or any) main site domain name.
    - the destination can only be a hand-typed URL. We'd like to reference content.
    
This app modifies the `redirect` implementation to add these features, and to make them available through an InlineAdmin
on ListableMixin content.
"""

# use the last site as the redirect
try:
    REDIRECT_SOURCE_SITE_ID = settings.REDIRECT_SOURCE_SITE_ID
except AttributeError:
    REDIRECT_SOURCE_SITE_ID = Site.objects.last().id

# At the moment we assume domains are served via https.
SOURCE_SCHEME = "https://"
DESTINATION_SCHEME = "https://"

@python_2_unicode_compatible
class Redirect(models.Model):
    """
    A simple model, based on django.contrib.redirect, for sending one URL to another.

    We customise this model to:
     - generate short URLs if old_path isn't given
     - ensure slashes
     -
    """

    # redirect fields
    source_site = models.ForeignKey(Site, default=REDIRECT_SOURCE_SITE_ID)
    source_path = models.CharField(_('redirect from'), max_length=255, db_index=True, blank=True,
        help_text=_("This can be any unused path, excluding the domain name. Example: '/kids'. "
                    "A short URL will be generated if this is left blank."))

    # adding the option to specify a site other than the default for destination URL
    destination_path = models.CharField(
        _('destination URL'), max_length=255, blank=True,
        help_text=_("This can be either an absolute path (as above) or a full URL. "
                    "Example: '/events/search/?q=kids' or 'https://example.com/kids'.")
    )
    destination_site = models.ForeignKey(
        Site, default=settings.SITE_ID, related_name='redirect_destinations',
        help_text="Used only if the destination URL doesn't include a domain name."
    )


    # GFK to a piece of content, plus GET string to use if necessary.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    destination_object = GenericForeignKey('content_type', 'object_id')
    destination_object_params = models.CharField(_('Additional URL parameters'), help_text=_("Example: 'utm_source=fb&utm_medium=email&utm_campaign=spring_sale'. Don't include '?'"), max_length=255, blank=True)

    class Meta:
        verbose_name = _('redirect or short URL')
        verbose_name_plural = _('redirects and short URLs')
        db_table = 'django_redirect'
        unique_together = (('source_site', 'source_path'),)
        ordering = ('source_path',)

    def __str__(self):
        return "%s ---> %s" % (self.get_source_url(), self.get_destination_url(include_params=False))

    def get_source_url(self):
        return urljoin(SOURCE_SCHEME + self.source_site.domain, self.source_path)

    def get_destination_url(self, include_params=True):
        """
        :return: the fully-qualified destination URL of the redirect, including scheme and domain name.
        """
        try:
            url = self.destination_path or self.destination_object.get_absolute_url()
        except AttributeError: # no content with URL
            return None
        else:
            parsed = urlparse(url)

            if self.destination_object_params and include_params:
                if parsed.params: # url already has GET params. Append ours.
                    url = url + self.destination_object_params
                else:
                    url = url + "?" + self.destination_object_params

            if not parsed.scheme:
                url = urljoin(DESTINATION_SCHEME + self.destination_site.domain, url)

            return url
    get_destination_url.short_description = "redirect to"

    get_absolute_url = get_source_url

    def save(self, *args, **kwargs):
        if not self.source_path:
            # we'll need to generate a short code. We want to use the DB ID. If we don't already have one, we
            # fake a value, save, and use that ID to generate the code.
            if not self.id:
                self.source_path = "__TEMPPATH_%s__" % randint(0,32000)
                super(Redirect, self).save(*args, **kwargs)
            self.source_path = short_code_from_id(self.id)

        if not self.source_path.startswith('/'):
            self.source_path = "/%s" % self.source_path

        if self.destination_object_params.startswith('?'):
            self.destination_object_params = self.destination_object_params[1:]

        super(Redirect, self).save(*args, **kwargs)
