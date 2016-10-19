from django.core.management.base import BaseCommand, CommandError
from ask_app.models import Question, Tag, Answer, Profile, Like
from django.contrib.auth.models import User
from django.db import connection


class Command(BaseCommand):
    help = 'Reset the database'

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        Answer.objects.all().delete()
        User.objects.all().delete()
        Like.objects.all().delete()

        cursor = connection.cursor()
        cursor.execute('ALTER TABLE  ask_app_tag AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  ask_app_answer AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  ask_app_profile AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  ask_app_question AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  ask_app_like AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  ask_app_question_tags AUTO_INCREMENT=0')
        cursor.execute('ALTER TABLE  auth_user AUTO_INCREMENT=0')

