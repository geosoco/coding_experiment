# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150507_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presurvey',
            old_name='english_speaking_comfort',
            new_name='english_sarcasm_comfort',
        ),
        migrations.RemoveField(
            model_name='presurvey',
            name='overall_english_comfort',
        ),
        migrations.AddField(
            model_name='presurvey',
            name='rumor_familiarity',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='presurvey',
            name='rumor_known',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='presurvey',
            name='twitter_usage',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='presurvey',
            name='twitter_used',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='answer',
            name='code',
            field=models.ForeignKey(blank=True, to='main.Code', null=True),
        ),
    ]
