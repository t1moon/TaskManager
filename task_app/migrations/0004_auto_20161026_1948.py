# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-26 19:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0003_auto_20161026_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
