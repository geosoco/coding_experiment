# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_auto_20150511_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserValidatedInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('kind', models.IntegerField(default=1, choices=[(1, b'Attention Check'), (2, b'Duplicate Check')])),
                ('tweet_1_codes', models.TextField(null=True, blank=True)),
                ('tweet_2_codes', models.TextField(null=True, blank=True)),
                ('tweet_1', models.ForeignKey(related_name='uservalidatedinstance_tweet_1', to='main.Tweet')),
                ('tweet_2', models.ForeignKey(related_name='uservalidatedinstance_tweet_2', blank=True, to='main.Tweet', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='instructioncheck',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 11, 18, 37, 34, 993543, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postsurvey',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 11, 18, 37, 41, 252307, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presurvey',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 11, 18, 37, 44, 964275, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
