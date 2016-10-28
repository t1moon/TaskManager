from django.db import connection
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'drop the database'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('DROP DATABASE IF EXISTS db_task')
        cursor.execute('''CREATE DATABASE db_task
                            DEFAULT CHARACTER SET utf8
                            DEFAULT COLLATE utf8_general_ci;''')
        cursor.close()


