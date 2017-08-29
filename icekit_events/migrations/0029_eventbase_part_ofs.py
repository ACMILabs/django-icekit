# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icekit_events', '0028_eventbase_price_detailed'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventbase',
            name='part_ofs',
            field=models.ManyToManyField(blank=True, to='icekit_events.EventBase', db_index=True, verbose_name=b'part of', related_name='contained_events', help_text=b'If this event is part another events, select it here.'),
        ),
    ]
