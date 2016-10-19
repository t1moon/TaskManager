from __future__ import unicode_literals

from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    deadline = models.DateField(default=datetime.today())
    is_deleted = models.BooleanField(default = False)
    is_done = models.BooleanField(default = False)
    created_at = models.DateTimeField(default=datetime.now())
    category = models.ForeignKey(Category)


class Profile(models.Model):
    user = models.OneToOneField(User)