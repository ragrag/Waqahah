# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='current_impression',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='post',
            name='dislike',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='post',
            name='first_impression',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
