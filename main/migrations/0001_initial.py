# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('schema', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CodeInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TurkUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('worker_id', models.CharField(max_length=256, null=True, blank=True)),
                ('condition', models.IntegerField(default=0, null=True, blank=True)),
                ('initial_browser_details', models.TextField(null=True, blank=True)),
                ('final_browser_details', models.TextField(null=True, blank=True)),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('tweet_id', models.BigIntegerField(default=None)),
                ('text', models.CharField(max_length=1024)),
                ('screen_name', models.CharField(max_length=64)),
                ('embed_code', models.TextField(default=None, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='codeinstance',
            name='assignment',
            field=models.ForeignKey(to='main.TurkUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='codeinstance',
            name='code',
            field=models.ForeignKey(to='main.Code'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='codeinstance',
            name='tweet',
            field=models.ForeignKey(to='main.Tweet'),
            preserve_default=True,
        ),
    ]
