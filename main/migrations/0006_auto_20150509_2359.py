# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150509_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presurvey',
            name='rumor_known',
        ),
        migrations.RemoveField(
            model_name='presurvey',
            name='twitter_used',
        ),
    ]
