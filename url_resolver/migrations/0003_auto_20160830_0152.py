# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-30 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_resolver', '0002_auto_20160828_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlmapper',
            name='redirect_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='urlmapper',
            name='desktop_url',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
