from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.


class TaskManager(models.Manager):
    def new(self):
        return self.filter(is_deleted=False).order_by('-created_at')

    def tag(self, tag_name):
        return self.filter(tags__title__exact=tag_name).order_by('-created_at')


class Tag(models.Model):
    title = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    deadline = models.DateField(default=datetime.date.today())
    is_deleted = models.BooleanField(default = False)
    is_done = models.BooleanField(default = False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag)
    objects = TaskManager()


class Profile(User):
    objects = UserManager()