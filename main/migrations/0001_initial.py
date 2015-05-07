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
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(null=True, blank=True)),
                ('css_class', models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CodeInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='main.Assignment')),
                ('code', models.ForeignKey(to='main.Code')),
            ],
        ),
        migrations.CreateModel(
            name='CodeScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('mutually_exclusive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(null=True, blank=True)),
                ('code_schemes', models.ManyToManyField(to='main.CodeScheme')),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TurkUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initial_browser_details', models.TextField(null=True, blank=True)),
                ('final_browser_details', models.TextField(null=True, blank=True)),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('completion_code', models.CharField(max_length=64, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('tweet_id', models.BigIntegerField(default=None)),
                ('text', models.CharField(max_length=1024)),
                ('screen_name', models.CharField(max_length=64)),
                ('embed_code', models.TextField(default=None, null=True, blank=True)),
                ('attention_check', models.BooleanField(default=False)),
                ('dataset', models.ForeignKey(to='main.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='ValidatedCodeInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.ForeignKey(to='main.Code')),
                ('condition', models.ForeignKey(to='main.Condition')),
                ('tweet', models.ForeignKey(to='main.Tweet')),
            ],
        ),
        migrations.AddField(
            model_name='condition',
            name='dataset',
            field=models.ManyToManyField(to='main.Dataset'),
        ),
        migrations.AddField(
            model_name='condition',
            name='study',
            field=models.ForeignKey(to='main.Study'),
        ),
        migrations.AddField(
            model_name='codeinstance',
            name='tweet',
            field=models.ForeignKey(to='main.Tweet'),
        ),
        migrations.AddField(
            model_name='code',
            name='scheme',
            field=models.ForeignKey(to='main.CodeScheme'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='condition',
            field=models.ForeignKey(to='main.Condition'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='codes',
            field=models.ForeignKey(to='main.Code'),
        ),
        migrations.AddField(
            model_name='answer',
            name='condition',
            field=models.ForeignKey(to='main.Condition'),
        ),
        migrations.AddField(
            model_name='answer',
            name='tweet',
            field=models.ForeignKey(to='main.Tweet'),
        ),
    ]
