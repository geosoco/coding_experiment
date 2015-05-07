# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150507_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='code_schemes',
            field=models.ManyToManyField(to='main.CodeScheme', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='condition',
            name='dataset',
            field=models.ManyToManyField(to='main.Dataset', null=True, blank=True),
        ),
    ]
