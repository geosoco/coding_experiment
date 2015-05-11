# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_study_last_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turkuser',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
