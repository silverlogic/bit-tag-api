# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-14 19:39
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('center_point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('radius', models.FloatField()),
                ('buy_in', models.DecimalField(decimal_places=8, max_digits=12)),
                ('status', django_fsm.FSMField(choices=[('pending', 'Pending'), ('started', 'Started')], default='pending', max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_fsm.FSMField(choices=[('invited', 'Invited'), ('joined', 'Joined')], default='invited', max_length=50)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='games.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]