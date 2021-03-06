# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 12:59
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('activation_key', models.CharField(default='', max_length=40)),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2016, 11, 13, 12, 59, 24, 604425, tzinfo=utc))),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('deadline', models.DateField(default=datetime.date(2016, 11, 13))),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('tags', models.ManyToManyField(to='task_app.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_app.Profile')),
            ],
        ),
    ]
