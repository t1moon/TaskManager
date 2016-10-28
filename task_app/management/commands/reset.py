from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import connection
from task_app.models import Tag, Task, Profile

class Command(BaseCommand):
    help = 'Reset the database'

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Task.objects.all().delete()
        Profile.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute('ALTER TABLE  task_app_task AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  task_app_tag AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  task_app_profile AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  task_app_task_tags AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  auth_user AUTO_INCREMENT=0')

