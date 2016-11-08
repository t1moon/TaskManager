from django.db import connection
from django.core.management import BaseCommand
import MySQLdb



class Command(BaseCommand):
    help = 'drop the database'

    def handle(self, *args, **options):
        task_db = MySQLdb.connect(host="task_db", user="dbuser", password="secret", port=3306)
        cursor = task_db.cursor()
        cursor.execute('DROP DATABASE IF EXISTS db_task')
        cursor.execute('''CREATE DATABASE db_task
                            DEFAULT CHARACTER SET utf8
                            DEFAULT COLLATE utf8_general_ci;''')
        cursor.close()


