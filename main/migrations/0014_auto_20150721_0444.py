# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_uservalidatedinstance_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='rumor',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='original_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
