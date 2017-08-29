# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    Event = apps.get_model("icekit_events", "EventBase")
    for e in Event.objects.all():
        if e.part_of:
            e.part_ofs.add(e.part_of)



class Migration(migrations.Migration):

    dependencies = [
        ('icekit_events', '0029_eventbase_part_ofs'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
