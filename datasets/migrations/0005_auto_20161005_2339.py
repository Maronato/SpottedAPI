# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-05 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_auto_20161005_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='notspam',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='notspam',
            name='time',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='spam',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='spam',
            name='time',
            field=models.CharField(default='', max_length=50),
        ),
    ]
