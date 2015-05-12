# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_instructioncheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='last_condition',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
