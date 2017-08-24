#!/usr/bin/python
#  -*- coding: UTF-8 -*-
import re

import itertools


def ensure_unique(qs, field_name, value, exclude_id=None):
    """
    Makes sure that `value` is unique on model.fieldname. And nonempty.
    """
    orig = value
    if not value:
        value = "None"
    for x in itertools.count(1):
        if not qs.exclude(id=exclude_id).filter(**{field_name: value}).exists():
            break
        if orig:
            value = '%s-%d' % (orig, x)
        else:
            value = '%d' % x

    return value


def strip_parens(s):
    result = re.sub(r'^\(', '', s)
    result = re.sub(r'\)$', '', result)
    return result


def ndashify(s):
    """replace ' - ' with an n-dash character"""
    return re.sub(r' - ', u'–', unicode(s))


def fix_line_breaks(s):
    """
    Convert \r\n and \r to \n chars. Strip any leading or trailing whitespace
    on each line. Remove blank lines.
    """
    l = s.splitlines()
    x = [i.strip() for i in l]
    x = [i for i in x if i]  # remove blank lines
    return "\n".join(x)


def strip_line_breaks(s):
    """
    Remove \r and \n chars, replacing with a space. Strip leading/trailing
    whitespace on each line. Remove blank lines.
    """
    return re.sub(r'[\r\n ]+', ' ', s).strip()


def remove_url_breaking_chars(s):
    r = re.sub(r'[\?#&/]', '', s)
    return r.strip()

