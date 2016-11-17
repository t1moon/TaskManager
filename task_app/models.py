# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.
from django.utils import timezone


class TaskManager(models.Manager):
    def not_done(self, tag_name, author, sorting_by):
        if tag_name == u"Все теги":
            return self.filter(is_done=False, user=author, is_deleted=False).order_by(sorting_by)
        elif tag_name == u"Без тега":
            return self.filter(tags__isnull=True, is_done=False, user=author, is_deleted=False).order_by(sorting_by)
        else:
            return self.filter(tags__title__exact=tag_name, is_done=False, user=author, is_deleted=False).order_by(sorting_by)

    def done(self, tag_name, author, sorting_by):
        if tag_name == u"Все теги":
            return self.filter(is_done=True, user=author, is_deleted=False).order_by(sorting_by)
        elif tag_name == u"Без тега":
            return self.filter(tags__isnull=True, is_done=True, user=author, is_deleted=False).order_by(sorting_by)
        else:
            return self.filter(tags__title__exact=tag_name, is_done=True, user=author, is_deleted=False).order_by(sorting_by)

    def all_tasks(self, tag_name, author, sorting_by):
        if tag_name == u"Все теги":
            return self.filter(user=author, is_deleted=False).order_by(sorting_by)
        elif tag_name == u"Без тега":
            return self.filter(tags__isnull=True, user=author, is_deleted=False).order_by(sorting_by)
        else:
            return self.filter(tags__title__exact=tag_name, user=author, is_deleted=False).order_by(sorting_by)


    # def deadline_sort(self, author):
    #     return self.filter(is_deleted=False).filter(is_done=False).filter(user=author).order_by('deadline')

    def tag(self, tag_name, author, sorting_by):
        return self.filter(tags__title__exact=tag_name).filter(is_deleted=False).filter(is_done=False). \
            filter(user=author).order_by(sorting_by)

    def no_tag(self, author, sorting_by):
        return self.filter(tags__isnull=True).filter(is_deleted=False).filter(is_done=False). \
            filter(user=author).order_by(sorting_by)



class Tag(models.Model):
    title = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=255)
    deadline = models.DateField(default=datetime.date.today())
    is_deleted = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey('Profile')
    objects = TaskManager()


class Profile(User):
    activation_key = models.CharField(max_length=40, default='')
    key_expires = models.DateTimeField(default=timezone.localtime(timezone.now()))
    objects = UserManager()
