# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 21:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20170114_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='tagged_by',
        ),
    ]
