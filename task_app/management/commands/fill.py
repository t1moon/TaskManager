import datetime
from django.core.management.base import BaseCommand
import random
from faker import Factory

from task_app.models import Profile, Task, Tag


class Command(BaseCommand):
    help = 'Fill the database'

    def handle(self, *args, **options):
        fake = Factory.create('en_US')
        # Fill user
        u = Profile.objects.create_user(username="timur@mail.ru", password="12345")
        u.save()

        # Fill the tasks and tags
        for i in range(1, 10):
            task = Task(
                title=fake.name() + '?',
                deadline=datetime.datetime.now(),
                is_done=0,
                is_deleted=0,
                created_at=datetime.datetime.now(),
                user=u,
            )
            task.save()
            for j in range(1,3):
                s = fake.word()
                if Tag.objects.filter(title=s).exists():
                    tag = Tag.objects.get(title=s)
                else:
                    tag = Tag(title=s)
                tag.save()
                task.tags.add(tag)
            task.save()





