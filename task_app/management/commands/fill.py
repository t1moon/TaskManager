from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from task_app.models import Task, Category, Profile
import random
from faker import Factory


class Command(BaseCommand):
    help = 'Fill the database'

    def handle(self, *args, **options):
        fake = Factory.create('en_US')
        # Fill users
        for i in range(0, 10):
            u = Profile.objects.create_user(username=str(i), email=fake.email(), password=fake.word())
            u.save()

        # Fill the questions and tags
        for i in range(1, 50):
            user = Profile.objects.get(username=str(random.randint(1, 9)))
            q = Question(
                text=fake.text(),
                title=fake.name() + '?',
                author=user,
                rating=random.randint(1, 220)
            )
            q.save()


