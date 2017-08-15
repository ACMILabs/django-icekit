# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('redirects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='redirect',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='new_path',
            field=models.CharField(blank=True, verbose_name='URL override', max_length=200, help_text="This can be either an absolute path (as above) or a full URL. Example: '/events/search/?q=kids'."),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='old_path',
            field=models.CharField(db_index=True, blank=True, verbose_name='redirect from', max_length=200, help_text="This can be any unused path, excluding the domain name. Example: '/kids'. A short URL will be generated if this is left blank."),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='site',
            field=models.ForeignKey(to='sites.Site', default=1),
        ),
    ]
