# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 08:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20170830_0720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='ischallenge',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='challenge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge', to='accounts.Challenge'),
        ),
    ]
