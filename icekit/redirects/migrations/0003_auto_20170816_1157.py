# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('redirects', '0002_auto_20170815_1519'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='redirect',
            options={'verbose_name': 'redirect or short URL', 'verbose_name_plural': 'redirects and short URLs', 'ordering': ('source_path',)},
        ),
        migrations.AddField(
            model_name='redirect',
            name='destination_object_params',
            field=models.CharField(blank=True, help_text="Example: 'utm_source=fb&utm_medium=email&utm_campaign=spring_sale'. Don't include '?'", max_length=255, verbose_name='Additional URL parameters'),
        ),
        migrations.AddField(
            model_name='redirect',
            name='destination_site',
            field=models.ForeignKey(default=1, to='sites.Site', related_name='redirect_destinations', help_text=b"Used only if the destination URL doesn't include a domain name."),
        ),
        migrations.RenameField(
            model_name='redirect',
            old_name='new_path',
            new_name='destination_path',
        ),
        migrations.RenameField(
            model_name='redirect',
            old_name='old_path',
            new_name='source_path',
        ),
        migrations.RenameField(
            model_name='redirect',
            old_name='site',
            new_name='source_site',
        ),
        migrations.AlterUniqueTogether(
            name='redirect',
            unique_together=set([('source_site', 'source_path')]),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='destination_path',
            field=models.CharField(verbose_name='destination URL', max_length=255,
                                   help_text="This can be either an absolute path (as above) or a full URL. Example: '/events/search/?q=kids' or 'https://example.com/kids'.",
                                   blank=True),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='source_path',
            field=models.CharField(verbose_name='redirect from', max_length=255,
                                   help_text="This can be any unused path, excluding the domain name. Example: '/kids'. A short URL will be generated if this is left blank.",
                                   blank=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='redirect',
            name='source_site',
            field=models.ForeignKey(to='sites.Site', default=2),
        ),

    ]
