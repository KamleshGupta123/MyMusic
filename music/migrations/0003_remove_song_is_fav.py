# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-20 21:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_song_is_fav'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='is_fav',
        ),
    ]
