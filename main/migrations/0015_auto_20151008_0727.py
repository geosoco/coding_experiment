# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_turkuser_turker_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='turkuser',
            name='exclude',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='turkuser',
            name='exclusion_reason',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
