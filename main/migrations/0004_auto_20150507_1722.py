# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20150507_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_difficulty', models.IntegerField(null=True, blank=True)),
                ('task_clarity', models.IntegerField(null=True, blank=True)),
                ('task_value', models.IntegerField(null=True, blank=True)),
                ('suggestions', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('country', models.IntegerField(null=True, blank=True)),
                ('zip_code', models.IntegerField(null=True, blank=True)),
                ('twitter_familiarity', models.IntegerField(null=True, blank=True)),
                ('english_reading_comfort', models.IntegerField(null=True, blank=True)),
                ('english_speaking_comfort', models.IntegerField(null=True, blank=True)),
                ('overall_english_comfort', models.IntegerField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='code',
            name='key',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='condition',
            name='code_schemes',
            field=models.ManyToManyField(to='main.CodeScheme', blank=True),
        ),
        migrations.AlterField(
            model_name='condition',
            name='dataset',
            field=models.ManyToManyField(to='main.Dataset', blank=True),
        ),
    ]
