# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-26 16:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0002_auto_20161026_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 26, 16, 48, 24, 784245)),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=datetime.date(2016, 10, 26)),
        ),
    ]
