# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icekit_events', '0030_auto_20170829_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventbase',
            name='part_of',
        ),
    ]
