from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.
from django.utils import timezone


class TaskManager(models.Manager):
    def not_done(self,author):
        return self.filter(is_deleted=False).filter(is_done=False).filter(user=author).order_by('-created_at')

    def done(self,author):
        return self.filter(is_done=True).filter(user=author).order_by('-created_at')

    def all_tasks(self,author):
        return self.filter(is_deleted=False).filter(user=author).order_by('-created_at')

    def deadline_sort(self, author):
        return self.filter(is_deleted=False).filter(is_done=False).filter(user=author).order_by('-deadline')

    def tag(self, tag_name, author):
        if tag_name == 'None':
            return self.filter(tags__isnull=True).filter(is_deleted=False).filter(is_done=False).\
            filter(user=author).order_by('-created_at')

        return self.filter(tags__title__exact=tag_name).filter(is_deleted=False).filter(is_done=False).\
            filter(user=author).order_by('-created_at')


class Tag(models.Model):
    title = models.CharField(max_length=255)



class Task(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.DateField(default=datetime.date.today())
    is_deleted = models.BooleanField(default = False)
    is_done = models.BooleanField(default = False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey('Profile')
    objects = TaskManager()


class Profile(User):
    activation_key = models.CharField(max_length=40, default='')
    key_expires = models.DateTimeField(default=timezone.localtime(timezone.now()))
    objects = UserManager()
