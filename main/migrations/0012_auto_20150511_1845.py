# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150511_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presurvey',
            name='age',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='presurvey',
            name='country',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='presurvey',
            name='zip_code',
            field=models.TextField(null=True, blank=True),
        ),
    ]
