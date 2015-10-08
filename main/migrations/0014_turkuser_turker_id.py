# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_uservalidatedinstance_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='turkuser',
            name='turker_id',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]
