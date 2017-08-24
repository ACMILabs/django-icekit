#!/usr/bin/python
#  -*- coding: UTF-8 -*-

import itertools
from django.utils.functional import allow_lazy
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import re
import six
from unidecode import unidecode


def wikipedia_slugify(value, do_unidecode=False):
    """
    Converts to ASCII via unidecode.
    Converts spaces to underscore.

    Removes characters that
    aren't alphanumerics, underscores, or hyphens.

    Preserve case.

    Also strips leading and trailing whitespace.
    """
    if do_unidecode:
        value = unidecode(value)
    value = value.strip()
    return mark_safe(re.sub('[\s/#\?:@]+', '_', value))
wikipedia_slugify = allow_lazy(wikipedia_slugify, six.text_type)


def alt_slugify(value):
    """
    More extreme version of slugify, unidecoding, and removing hyphens.

    Useful for fallback slug values.
    """
    if value and value.strip():
        return re.sub('[-_]', '', slugify(unicode(unidecode(value))))
    else:
        return ""
alt_slugify = allow_lazy(alt_slugify, six.text_type)
