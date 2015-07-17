# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsbase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagetranslation',
            name='live_content',
            field=models.TextField(blank=True),
        ),
    ]
